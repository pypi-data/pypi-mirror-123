""" Utilities for working with LEMS models

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2021-04-05
:Copyright: 2021, Center for Reproducible Biomedical Modeling
:License: MIT
"""

from ...sedml.data_model import (  # noqa: F401
    SedDocument, ModelAttributeChange, Variable, Symbol,
    Simulation, UniformTimeCourseSimulation,
    Algorithm,
    Task,
    )
from ...utils.core import flatten_nested_list_of_strings
from .validation import validate_model
import os
import pint
import types  # noqa: F401

__all__ = ['get_parameters_variables_outputs_for_simulation']


def get_parameters_variables_outputs_for_simulation(model_filename, model_language, simulation_type, algorithm_kisao_id=None,
                                                    change_level=SedDocument, native_ids=False, native_data_types=False):
    """ Get the possible observables for a simulation of a model

    Args:
        model_filename (:obj:`str`): path to model file
        model_language (:obj:`str`): model language (e.g., ``urn:sedml:language:lems``)
        simulation_type (:obj:`types.Type`): subclass of :obj:`Simulation`
        algorithm_kisao_id (:obj:`str`): KiSAO id of the algorithm for simulating the model (e.g., ``KISAO_0000019``
            for CVODE)
        change_level (:obj:`types.Type`, optional): level at which model changes will be made (:obj:`SedDocument` or :obj:`Task`)
        native_ids (:obj:`bool`, optional): whether to return the raw id and name of each model component rather than the suggested name
            for the variable of an associated SED-ML data generator
        native_data_types (:obj:`bool`, optional): whether to return new_values in their native data types

    Returns:
        :obj:`list` of :obj:`ModelAttributeChange`: possible attributes of a model that can be changed and their default values
        :obj:`list` of :obj:`Simulation`: simulation of the model
        :obj:`list` of :obj:`Variable`: possible observables for a simulation of the model
        :obj:`list` of :obj:`Plot`: possible plots of the results of a simulation of the model
    """
    # check model file exists and is valid
    if not isinstance(model_filename, str):
        raise ValueError('`{}` is not a path to a model file.'.format(model_filename))

    if not os.path.isfile(model_filename):
        raise FileNotFoundError('Model file `{}` does not exist.'.format(model_filename))

    errors, _, model = validate_model(model_filename)
    if errors:
        raise ValueError('Model file `{}` is not a valid LEMS file.\n  {}'.format(
            model_filename, flatten_nested_list_of_strings(errors).replace('\n', '\n  ')))

    if simulation_type not in [UniformTimeCourseSimulation]:
        raise NotImplementedError('`simulation_type` must be `UniformTimeCourseSimulation`')

    # get simulation -- gauranteed to have 1 due to :obj:`validate_model`
    sim = next(component for component in model.components if component.type == 'Simulation')

    # get simulation target -- gauranteed to exist due to :obj:`validate_model`
    sim_target_id = sim.parameters['target']
    sim_target = next(component for component in model.components if component.id == sim_target_id)

    # get populations
    populations = filter(lambda child: child.type == 'population', sim_target.children)
    components = []
    for population in populations:
        for i_el in range(int(population.parameters['size'])):
            component = next(child for child in model.components if child.id == population.parameters['component'])
            components.append((component, '{}[{}]'.format(population.id, i_el)))

    unit_reg = pint.UnitRegistry()
    sim_end_time = unit_reg.parse_expression(sim.parameters['length'])
    sim_end_time_sec = sim_end_time.to('second').magnitude
    step = unit_reg.parse_expression(sim.parameters['step'])
    number_of_steps = int((sim_end_time / step).magnitude)

    # parameters
    params = []
    sim = UniformTimeCourseSimulation(
        id='simulation',
        initial_time=0.,
        output_start_time=0.,
        output_end_time=sim_end_time_sec,
        number_of_steps=number_of_steps,
        algorithm=Algorithm(
            kisao_id=algorithm_kisao_id or 'KISAO_0000019',
        ),
    )
    vars = []
    vars.append(Variable(
        id='time',
        name='Time',
        symbol=Symbol.time,
    ))

    while components:
        # get a component to explore
        component, component_uri = components.pop()

        # explore its children
        for child in component.children:
            components.append((child, component.id + '/' + child.id))

        # if component.type in ['Simulation', 'Display', 'OutputFile', 'notes', 'annotation']:
        #    continue

        # collect its parameters
        for parameter_id, parameter_value in component.parameters.items():
            params.append(ModelAttributeChange(
                id='value_parameter_{}_{}'.format(component_uri.replace('/', '_'), parameter_id),
                name='Value of parameter "{}" of "{}"'.format(parameter_id, component_uri),
                target=component_uri + '/' + parameter_id,
                new_value=parameter_value,
            ))

        #  todo
        # vars.append(Variable(
        #    id='amount_molecule_{}'.format(escaped_el_molecule),
        #    name='Dynamics of molecule "{}"'.format(el_molecule),
        #    target='molecules.{}.count'.format(el_molecule),
        # ))

    # TODO
    outputs = []

    # return parameters and observables
    return (params, [sim], vars, outputs)
