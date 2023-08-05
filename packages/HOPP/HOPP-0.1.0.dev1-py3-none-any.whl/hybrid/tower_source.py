from typing import Optional, Union, Sequence
import os
import datetime
from math import pi, log

import PySAM.Singleowner as Singleowner

from hybrid.dispatch.power_sources.tower_dispatch import TowerDispatch
from hybrid.dispatch.power_sources.csp_dispatch import CspDispatch


from hybrid.power_source import *
from hybrid.csp_source import CspPlant


class TowerPlant(CspPlant):
    _system_model: None
    _financial_model: Singleowner.Singleowner
    # _layout: TowerLayout
    _dispatch: TowerDispatch

    def __init__(self,
                 site: SiteInfo,
                 tower_config: dict):
        """

        :param tower_config: dict, with keys ('cycle_capacity_kw', 'solar_multiple', 'tes_hours',
        'optimize_field_before_sim')
        """
        financial_model = Singleowner.default('MSPTSingleOwner')

        # set-up param file paths
        # TODO: Site should have dispatch factors consistent across all models
        self.param_files = {'tech_model_params_path': 'tech_model_defaults.json',
                            'cf_params_path': 'construction_financing_defaults.json',
                            'dispatch_factors_ts_path': 'dispatch_factors_ts.csv',
                            'ud_ind_od_path': 'ud_ind_od.csv',
                            'wlim_series_path': 'wlim_series.csv',
                            'helio_positions_path': 'helio_positions.csv'}
        rel_path_to_param_files = os.path.join('pySSC_daotk', 'tower_data')
        self.param_file_paths(rel_path_to_param_files)

        super().__init__("TowerPlant", 'tcsmolten_salt', site, financial_model, tower_config)

        # Set full annual weather data before field layout
        self.set_weather(self.year_weather_df)  

        self.optimize_field_before_sim = True
        if 'optimize_field_before_sim' in tower_config:
            self.optimize_field_before_sim = tower_config['optimize_field_before_sim']

        self._dispatch: TowerDispatch = None

    def initialize_params(self, keep_eta_flux_maps=False):
        if keep_eta_flux_maps:
            flux_eta_maps = {k:self.ssc.get(k) for k in ['eta_map', 'flux_maps', 'A_sf_in', 'helio_positions', 'N_hel', 'D_rec', 'rec_height', 'h_tower', 'land_area_base']}

        super().initialize_params()

        if keep_eta_flux_maps:
            self.set_flux_eta_maps(flux_eta_maps)

    def set_params_from_files(self):
        super().set_params_from_files()

        # load heliostat field  # TODO: Can we get rid of this if always creating a new field layout?
        heliostat_layout = np.genfromtxt(self.param_files['helio_positions_path'], delimiter=',')
        N_hel = heliostat_layout.shape[0]
        helio_positions = [heliostat_layout[j, 0:2].tolist() for j in range(N_hel)]
        self.ssc.set({'helio_positions': helio_positions})

    def create_field_layout_and_simulate_flux_eta_maps(self, optimize_tower_field: bool = False):
        self.ssc.set({'time_start': 0})
        self.ssc.set({'time_stop': 0})

        if optimize_tower_field:
            # Run field, tower height, and receiver diameter and height optimization
            self.ssc.set({'field_model_type': 0})
            print('Optimizing field layout, tower height, receiver diameter, and receiver height'
                  ' and simulating flux and eta maps ...')
        else:
            # Create field layout and generate flux and eta maps, but don't optimize field or tower
            self.ssc.set({'field_model_type': 1})
            print('Generating field layout and simulating flux and eta maps ...')

        original_values = {k: self.ssc.get(k) for k in['is_dispatch_targets', 'rec_clearsky_model', 'time_steps_per_hour', 'sf_adjust:hourly']}
        # set so unneeded dispatch targets and clearsky DNI are not required
        # TODO: probably don't need hourly sf adjustment factors
        self.ssc.set({'is_dispatch_targets': False, 'rec_clearsky_model': 1, 'time_steps_per_hour': 1,
                      'sf_adjust:hourly': [0.0 for j in range(8760)]})
        tech_outputs = self.ssc.execute()
        print('Finished creating field layout and simulating flux and eta maps ...')
        self.ssc.set(original_values)
        eta_map = tech_outputs["eta_map_out"]
        flux_maps = [r[2:] for r in tech_outputs['flux_maps_for_import']]  # don't include first two columns
        A_sf_in = tech_outputs["A_sf"]
        field_and_flux_maps = {'eta_map': eta_map, 'flux_maps': flux_maps, 'A_sf_in': A_sf_in}
        for k in ['helio_positions', 'N_hel', 'D_rec', 'rec_height', 'h_tower', 'land_area_base']:
            field_and_flux_maps[k] = tech_outputs[k]

        # Check if specified receiver dimensions make sense relative to heliostat dimensions
        if min(field_and_flux_maps['rec_height'], field_and_flux_maps['D_rec']) < max(self.ssc.get('helio_width'), self.ssc.get('helio_height')):
            print('Warning: Receiver height or diameter is smaller than the heliostat dimension. Design will likely have high spillage loss')

        return field_and_flux_maps

    def set_field_layout_and_flux_eta_maps(self, field_and_flux_maps):
        self.ssc.set(field_and_flux_maps)  # set flux maps etc. so they don't have to be recalculated
        self.ssc.set({'field_model_type': 3})  # use the provided flux and eta map inputs
        self.ssc.set({'eta_map_aod_format': False})

    def optimize_field_and_tower(self):
        self.set_field_layout_and_flux_eta_maps(
            self.create_field_layout_and_simulate_flux_eta_maps(optimize_tower_field=True))

    def generate_field(self):
        self.set_field_layout_and_flux_eta_maps(self.create_field_layout_and_simulate_flux_eta_maps())

    def calculate_total_installed_cost(self) -> float:
        # Note this must be called after heliostat field layout is created
        # Tower total installed cost is also a direct output from the ssc compute module
        site_improvement_cost = self.ssc.get('site_spec_cost') * self.ssc.get('A_sf_in')
        heliostat_cost = self.ssc.get('cost_sf_fixed') + self.ssc.get('heliostat_spec_cost') * self.ssc.get('A_sf_in')
        height = self.ssc.get('h_tower')-0.5*self.ssc.get('rec_height') + 0.5*self.ssc.get('helio_height')
        tower_cost = self.ssc.get('tower_fixed_cost') * np.exp(self.ssc.get('tower_exp') * height)
        Arec = 3.1415926 * self.ssc.get('rec_height') * self.ssc.get('D_rec')
        receiver_cost = self.ssc.get('rec_ref_cost') * (Arec / self.ssc.get('rec_ref_area'))**self.ssc.get('rec_cost_exp')
        tes_capacity = self.ssc.get('P_ref') / self.ssc.get('design_eff')*self.ssc.get('tshours')
        tes_cost = tes_capacity * 1000 * self.ssc.get('tes_spec_cost')
        cycle_cost = self.ssc.get('P_ref') * 1000 * self.ssc.get('plant_spec_cost')
        bop_cost = self.ssc.get('P_ref') * 1000 * self.ssc.get('bop_spec_cost')
        fossil_backup_cost = self.ssc.get('P_ref') * 1000 * self.ssc.get('fossil_spec_cost')
        direct_cost = site_improvement_cost + heliostat_cost + tower_cost + receiver_cost + tes_cost + cycle_cost + bop_cost + fossil_backup_cost
        contingency_cost = self.ssc.get('contingency_rate')/100 * direct_cost
        total_direct_cost = direct_cost + contingency_cost
        total_land_area = self.ssc.get('land_area_base') * self.ssc.get('csp.pt.sf.land_overhead_factor') + self.ssc.get('csp.pt.sf.fixed_land_area')
        plant_net_capacity = self.ssc.get('P_ref') * self.ssc.get('gross_net_conversion_factor')
        
        land_cost = total_land_area * self.ssc.get('land_spec_cost') + \
                    total_direct_cost * self.ssc.get('csp.pt.cost.plm.percent')/100 + \
                    plant_net_capacity * 1e6 * self.ssc.get('csp.pt.cost.plm.per_watt') + \
                    self.ssc.get('csp.pt.cost.plm.fixed')

        epc_cost = total_land_area * self.ssc.get('csp.pt.cost.epc.per_acre') + \
                   total_direct_cost * self.ssc.get('csp.pt.cost.epc.percent')/100 + \
                   plant_net_capacity * 1e6 * self.ssc.get('csp.pt.cost.epc.per_watt') + \
                   self.ssc.get('csp.pt.cost.epc.fixed')
        
        sales_tax_cost = total_direct_cost * self.ssc.get('sales_tax_frac')/100 * self.ssc.get('sales_tax_rate')/100
        total_indirect_cost = land_cost + epc_cost + sales_tax_cost
        total_installed_cost = total_direct_cost + total_indirect_cost
        return total_installed_cost

    def estimate_receiver_pumping_parasitic(self, nonheated_length=0.2):
        m_rec_design = self.get_receiver_design_mass_flow()  # kg/s
        Tavg = 0.5 * (self.value('T_htf_cold_des') + self.value('T_htf_hot_des'))
        rho = self.get_density_htf(Tavg)
        visc = self.get_visc_htf(Tavg)

        npath = 1
        nperpath = self.value('N_panels')
        if self.value('Flow_type') == 1 or self.value('Flow_type') == 2:
            npath = 2
            nperpath = int(nperpath / 2)
        elif self.value('Flow_type') == 9:
            npath = int(nperpath / 2)
            nperpath = 2

        ntube = int(pi * self.value('D_rec') / self.value('N_panels') / (
                self.value('d_tube_out') * 1.e-3))  # Number of tubes per panel
        m_per_tube = m_rec_design / npath / ntube  # kg/s per tube
        tube_id = (self.value('d_tube_out') - 2 * self.value('th_tube')) / 1000.  # Tube ID in m
        Ac = 0.25 * pi * (tube_id ** 2)
        vel = m_per_tube / rho / Ac  # HTF velocity
        Re = rho * vel * tube_id / visc
        if Re < 2300:
            print("Warning: Poor Receiver Design! Receiver will experience laminar flow. Consider revising.")
        eD = 4.6e-5 / tube_id
        ff = (-1.737 * log(0.269 * eD - 2.185 / Re * log(0.269 * eD + 14.5 / Re))) ** -2
        fd = 4 * ff
        Htot = self.value('rec_height') * (1 + nonheated_length)
        dp = 0.5 * fd * rho * (vel ** 2) * (
                Htot / tube_id + 4 * 30 + 2 * 16) * nperpath  # Frictional pressure drop (Pa) (straight tube, 90deg bends, 45def bends)
        dp += rho * 9.8 * self.value('h_tower')  # Add pressure drop from pumping up the tower
        if nperpath % 2 == 1:
            dp += rho * 9.8 * Htot

        wdot = dp * m_rec_design / rho / self.value('eta_pump') / 1.e6  # Pumping parasitic at design point reciever mass flow rate (MWe)
        return wdot / self.field_thermal_rating  # MWe / MWt

    def get_receiver_design_mass_flow(self):
        cp_des = self.get_cp_htf(0.5*(self.value('T_htf_cold_des') + self.value('T_htf_hot_des')))  # J/kg/K
        m_des = self.field_thermal_rating*1.e6 / (cp_des * (self.value('T_htf_hot_des')
                                                            - self.value('T_htf_cold_des')))  # kg/s
        return m_des

    def get_density_htf(self, TC):
        if self.value('rec_htf') != 17:
            print('HTF %d not recognized' % self.value('rec_htf'))
            return 0.0
        TK = TC+273.15
        return -1.0e-7*(TK**3) + 2.0e-4*(TK**2) - 0.7875*TK + 2299.4  # kg/m3

    def get_visc_htf(self, TC):
        if self.value('rec_htf') != 17:
            print('HTF %d not recognized' % self.value('rec_htf'))
            return 0.0
        return max(1e-4, 0.02270616 - 1.199514e-4*TC + 2.279989e-7*TC*TC - 1.473302e-10*TC*TC*TC)

    @staticmethod
    def get_plant_state_io_map() -> dict:
        io_map = {  # State:
                  # Number Inputs                         # Arrays Outputs (end of timestep)
                  'is_field_tracking_init':               'is_field_tracking_final',
                  'rec_op_mode_initial':                  'rec_op_mode_final',
                  'rec_startup_time_remain_init':         'rec_startup_time_remain_final',
                  'rec_startup_energy_remain_init':       'rec_startup_energy_remain_final',

                  'T_tank_cold_init':                     'T_tes_cold',
                  'T_tank_hot_init':                      'T_tes_hot',
                  'csp.pt.tes.init_hot_htf_percent':      'hot_tank_htf_percent_final',

                  'pc_op_mode_initial':                   'pc_op_mode_final',
                  'pc_startup_time_remain_init':          'pc_startup_time_remain_final',
                  'pc_startup_energy_remain_initial':     'pc_startup_energy_remain_final',
                  # For dispatch ramping penalty
                  'heat_into_cycle':                      'q_pb'
                  }
        return io_map        

    def set_initial_plant_state(self) -> dict:
        plant_state = super().set_initial_plant_state()
        # Use initial storage charge state that came from tech_model_defaults.json file
        plant_state['csp.pt.tes.init_hot_htf_percent'] = self.value('csp.pt.tes.init_hot_htf_percent')

        plant_state['rec_startup_time_remain_init'] = self.value('rec_su_delay')
        plant_state['rec_startup_energy_remain_init'] = (self.value('rec_qf_delay') * self.field_thermal_rating
                                                         * 1e6)  # MWh -> Wh
        return plant_state

    @property
    def solar_multiple(self) -> float:
        return self.ssc.get('solarm')

    @solar_multiple.setter
    def solar_multiple(self, solar_multiple: float):
        """
        Set the solar multiple and updates the system model. Solar multiple is defined as the the ratio of receiver
        design thermal power over power cycle design thermal power.
        :param solar_multiple:
        :return:
        """
        self.ssc.set({'solarm': solar_multiple})

    @property
    def cycle_thermal_rating(self) -> float:
        return self.value('P_ref') / self.value('design_eff')

    @property
    def field_thermal_rating(self) -> float:
        return self.value('solarm') * self.cycle_thermal_rating

    @property
    def cycle_nominal_efficiency(self) -> float:
        return self.value('design_eff')

    @property
    def number_of_reflector_units(self) -> float:
        """Returns number of heliostats within the field"""
        return self.value('N_hel')

    @property
    def minimum_receiver_power_fraction(self) -> float:
        """Returns minimum receiver mass flow rate turn down fraction."""
        return self.value('f_rec_min')

    @property
    def field_tracking_power(self) -> float:
        """Returns power load for field to track sun position in MWe"""
        return self.value('p_track') * self.number_of_reflector_units / 1e3

    @property
    def htf_cold_design_temperature(self) -> float:
        """Returns cold design temperature for HTF [C]"""
        return self.value('T_htf_cold_des')

    @property
    def htf_hot_design_temperature(self) -> float:
        """Returns hot design temperature for HTF [C]"""
        return self.value('T_htf_hot_des')

    @property
    def initial_tes_hot_mass_fraction(self) -> float:
        """Returns initial thermal energy storage fraction of mass in hot tank [-]"""
        return self.plant_state['csp.pt.tes.init_hot_htf_percent'] / 100.


