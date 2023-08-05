from functools import reduce
from hestia_earth.schema import InputStatsDefinition, TermTermType
from hestia_earth.utils.model import filter_list_term_type
from hestia_earth.utils.tools import flatten, list_sum, non_empty_list
from hestia_earth.utils.lookup import get_table_value, download_lookup, column_name

from hestia_earth.models.log import logger
from hestia_earth.models.utils.input import _new_input
from . import MODEL


def _input(term_id: str, value: float):
    logger.info('model=%s, term=%s, value=%s', MODEL, term_id, value)
    input = _new_input(term_id, MODEL)
    input['value'] = [value]
    input['statsDefinition'] = InputStatsDefinition.MODELLED.value
    return input


def _run_operation(practice: dict):
    term_id = practice.get('term', {}).get('@id')
    value = list_sum(practice.get('value'))
    lookup = download_lookup('operation.csv')
    coeffs = get_table_value(lookup, 'termid', term_id, column_name('fuelUse'))
    values = non_empty_list(coeffs.split(';')) if coeffs else []
    return [(c.split(':')[0], float(c.split(':')[1]) * value) for c in values]


def _group_inputs(values: list):
    def group_by(prev: dict, curr: tuple):
        id, value = curr
        prev[id] = prev.get(id, 0) + value
        return prev

    return reduce(group_by, values, {})


def _run(operations: list):
    inputs = flatten(map(_run_operation, operations))
    inputs = _group_inputs(inputs)
    return [_input(key, value) for key, value in inputs.items()]


def _should_run(cycle: dict):
    operations = filter_list_term_type(cycle.get('practices', []), TermTermType.OPERATION)
    operations = [p for p in operations if list_sum(p.get('value', [])) > 0]

    should_run = len(operations) > 0
    logger.info('model=%s, term=fuelElectricity, should_run=%s', MODEL, should_run)
    return should_run, operations


def run(cycle: dict):
    should_run, operations = _should_run(cycle)
    return _run(operations) if should_run else []
