
import logging
import numpy as np
import traceback
from typing import Callable


SIMULATION_ATTRIBUTES = ['annual_energies', 'generation_profile', 'internal_rate_of_returns',
                         'lcoe_nom', 'lcoe_real', 'net_present_values', 'cost_installed',
                         'total_revenues', 'capacity_payments', 'energy_purchases_values',
                         'energy_sales_values', 'energy_values', 'benefit_cost_ratios']

TOWER_ATTRIBUTES = ['dispatch', 'ssc_time_series']

class HybridSizingProblem():  # OptimizationProblem (unwritten base)
    """
    Problem class holding the design variable definitions and executing the HOPP simulation
    """
    sep = '::'

    def __init__(self,
                 init_simulation: Callable,
                 design_variables: dict,
                 fixed_variables: dict = {}) -> None:
        """
        Create the problem instance, the simulation is not created until the objective is evauated

        :param design_variables: Nested dictionary defining the design variables of the problem
            Example:
                design_variables = dict(
                    pv=      {'system_capacity_kw':  {'bounds':(25*1e3,  75*1e3),  'precision': 3},
                              'tilt':                {'bounds':(30,      60),      'precision': 0},
                              },
                    battery= {'system_capacity_kwh': {'bounds':(150*1e3, 250*1e3), 'precision': 3},
                              'system_capacity_kw':  {'bounds':(25*1e3,  75*1e3),  'precision': 3},
                              'system_voltage_volts':{'bounds':(400,     600),     'precision': 1},
                              },
                )

            Each design variable needs an upper and lower bound, precision defaults to -6 if not given
        :param fixed_variables: Nested dictionary defining the fixed variables of the problem
            Example:
                    fixed_variables = dict(
                        pv=      {'system_capacity_kw': 75*1e3
                                 },
                    )
        :return: None
        """

        logging.info("Problem init")
        self.simulation = None
        self.init_simulation = init_simulation
        self._parse_design_variables(design_variables, fixed_variables)

    def _parse_design_variables(self,
                                design_variables: dict,
                                fixed_variables: dict) -> None:
        """
        Parse the nested dictionary structure into separate attributes

        :param design_variables: Nested dictionary defining the design variables of the problem
        :param fixed_variables: Nested dictionary defining the fixed variables of the problem
        :return: None
        """
        self.design_variables = design_variables
        self.fixed_variables = fixed_variables

        try:
            bounds = list()
            fields = list()
            field_set = set()
            fixed_values = list()

            for key, val in self.design_variables.items():
                for subkey, subval in val.items():

                    # Candidate field name, e.g., pv::tilt
                    field_name = self.sep.join([key, subkey])

                    # Check if field name has been repeated
                    if field_name in field_set:
                        raise Exception(f"{field_name} repeated in design variables")

                    # Assert that 'bounds' value is of length 2
                    field_bounds = subval['bounds']

                    num_bounds = len(field_bounds)
                    assert num_bounds == 2, f"{key}:{subkey} 'bounds' of length {num_bounds} not understood"

                    # Assert that 'bounds' first value (lower) is less than or equal to the second value (upper)
                    assert field_bounds[0] <= field_bounds[1], \
                        f"{key}:{subkey} invalid 'bounds': {field_bounds[0]}(lower) > {field_bounds[1]}(upper)"

                    field_set.add(field_name)
                    fields.append(field_name)
                    bounds.append(field_bounds)

            for key, val in self.fixed_variables.items():
                for subkey, subval in val.items():

                    # Candidate field name, e.g., pv::tilt
                    field_name = self.sep.join([key, subkey])

                    # # Check if field name has been repeated   (allow repeated in fixed variables)
                    # if field_name in field_set:
                    #     raise Exception(f"{field_name} repeated in design variables")

                    fields.append(field_name)
                    fixed_values.append(subval)

            self.candidate_fields = fields
            self.n_dim = len(fields)
            self.lower_bounds = np.array([bnd[0] for bnd in bounds])
            self.upper_bounds = np.array([bnd[1] for bnd in bounds])
            self.fixed_values = fixed_values

        except KeyError as error:
            raise KeyError(f"{key}:{subkey} needs simple bounds defined as 'bounds':(lower,upper)") from error

    def _check_candidate(self,
                         candidate: tuple) -> None:
        """
        Check if candidate tuple is valid for this problem.

        :param candidate: tuple containing field, value pairs in the order of self.fields and having values between the
            specified upper and lower bounds
        :return: None
        """
        # Assert that the correct number of field value pairs is present
        actual_length = len(candidate)
        assert actual_length == self.n_dim, \
            f"Expected candidate with {self.n_dim} (field,value) pairs, got candidate of length {actual_length}"

        # For each field value pair assert that the field name is correct and that the value is between the upper
        # and lower bounds
        for i, (field, value) in enumerate(candidate):
            if i == len(self.lower_bounds):
                break

            assert field == self.candidate_fields[i], \
                f"Expected field named {self.candidate_fields[i]} in position {i} of candidate, but found {field}"
            assert (value >= self.lower_bounds[i]) and (value <= self.upper_bounds[i]), \
                f"{field} invalid value ({value}), outside 'bounds':({self.lower_bounds[i]},{self.upper_bounds[i]})"

    def _set_simulation_to_candidate(self,
                                     candidate: tuple) -> None:
        """
        Set the simulation according to the provided design candidate

        :param candidate: Tuple containing field value pairs
        :return: None
        """
        for field,value in candidate:
            tech_key, key = field.split(self.sep)
            tech_model = getattr(self.simulation, tech_key)

            if hasattr(tech_model, key):
                setattr(tech_model, key, value)
            else:
                tech_model.value(key, value)

    def candidate_from_array(self, values: np.array) -> tuple:
        """
        Create a tuple of field value pairs according to the problem's design variables given an array of values

        :param values: An array of values in the problem's native units representing a design candidate
        :return: A candidate tuple of field value pairs, where values have been rounded to the variable's precision
        """
        # Round the values according to the provided precision value
        # rounded_values = [np.round(x, decimals=-self.precision[i]) for i,x in enumerate(values)] + self.fixed_values
        candidate = tuple([(field, val)
                           for field, val in zip(self.candidate_fields, np.append(values, self.fixed_values))])
        return candidate

    def candidate_from_unit_array(self, values: np.array) -> tuple:
        """
        Create a tuple of field value pairs according to the problem's design variables given an array of values

        :param values: An array of unit values representing a design candidate
        :return: A candidate tuple of field value pairs, where values have been rounded to the variable's precision
        """
        # Scale the unit input array to the problem's units
        scaled_values = values * (self.upper_bounds - self.lower_bounds) + self.lower_bounds

        # Round the values according to the provided precision value
        # rounded_values = [np.round(x, decimals=-self.precision[i]) for i, x in enumerate(scaled_values)] + self.fixed_values
        candidate = tuple([(field, val)
                           for field,val in zip(self.candidate_fields, np.append(scaled_values, self.fixed_values))])
        return candidate

    def evaluate_objective(self, candidate: tuple) -> (tuple, dict):
        """
        Set the simulation to the design candidate provided, evaluate the objective, build out a nested dictionary of
        results from that simulation. One or more of these results can then represent the objective of the problem.
        TODO: the objective is currently a driver convention, should this be a problem convention?

        :param candidate: A tuple of field value pairs representing a design candidate for this problem
        :return:
        """

        try:
            result = dict()

            if self.simulation is not None:
                del self.simulation

            self.simulation = self.init_simulation()

            # Check if valid candidate, update simulation, execute simulation
            self._check_candidate(candidate)
            self._set_simulation_to_candidate(candidate)
            self.simulation.simulate(1)

            # Create the result dictionary according to SIMULATION_ATTRIBUTES and simulation.power_sources.keys()
            tech_list = list(self.simulation.power_sources.keys()) + ['hybrid']
            _ = tech_list.pop(tech_list.index('grid'))

            for sim_output in SIMULATION_ATTRIBUTES:
                try:
                    for key in tech_list:
                        value = getattr(getattr(self.simulation, sim_output), key)

                        if not callable(value):
                            temp = {key: value}

                        else:
                            temp = {key: value()}

                        if sim_output in result.keys():
                            result[sim_output].update(temp)

                        else:
                            result[sim_output] = temp

                except Exception:
                    err_str = traceback.format_exc()
                    result['exception'] = err_str

            result['tower_outputs'] = dict()
            for tower_output in TOWER_ATTRIBUTES:
                try:
                    value = getattr(self.simulation.tower.outputs, tower_output)

                    result['tower_outputs'][tower_output] = value

                except Exception:
                    err_str = traceback.format_exc()
                    result['tower_output_exception'] = err_str

            result['dispatch_factors'] = self.simulation.dispatch_factors

        except Exception:
            # Some exception occured while evaluating the objective
            err_str = traceback.format_exc()
            logging.info(f"Error when evaluating objective: {err_str}")

            result['exception'] = err_str

        logging.info(f"Objective evaluation complete: {candidate}")
        return candidate, result