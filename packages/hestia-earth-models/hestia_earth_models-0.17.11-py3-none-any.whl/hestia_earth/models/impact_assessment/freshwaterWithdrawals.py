from hestia_earth.schema import IndicatorStatsDefinition, TermTermType
from hestia_earth.utils.tools import list_sum, safe_parse_float
from hestia_earth.utils.model import filter_list_term_type
from hestia_earth.utils.lookup import column_name, download_lookup, get_table_value

from hestia_earth.models.log import debugRequirements, logger
from hestia_earth.models.utils.indicator import _new_indicator
from hestia_earth.models.utils.impact_assessment import get_product, convert_value_from_cycle, get_site
from hestia_earth.models.utils.blank_node import get_total_value
from hestia_earth.models.utils.dataCompleteness import _is_term_type_complete
from hestia_earth.models.utils.input import sum_input_impacts
from hestia_earth.models.utils.crop import get_crop_grouping_fao
from . import MODEL

TERM_ID = 'freshwaterWithdrawals'


def _indicator(value: float):
    logger.info('model=%s, term=%s, value=%s', MODEL, TERM_ID, value)
    indicator = _new_indicator(TERM_ID)
    indicator['value'] = value
    indicator['statsDefinition'] = IndicatorStatsDefinition.MODELLED.value
    return indicator


def _get_conveyancing_efficiency(impact_assessment: dict, product: dict):
    site = get_site(impact_assessment)
    country = impact_assessment.get('country', {}).get('@id') or site.get('country', {}).get('@id')
    grouping = get_crop_grouping_fao(product.get('term', {}).get('@id'))
    lookup = download_lookup('region.csv')
    value = get_table_value(lookup, 'termid', country, column_name(f"Conveyancing_Efficiency_{grouping}"))
    logger.debug('model=%s, term=%s, conveyancing efficiency=%s', MODEL, TERM_ID, value)
    return safe_parse_float(value, 1)


def _run(impact_assessment: dict, product: dict, irrigation: float):
    cycle = impact_assessment.get('cycle', {})
    conveyancing = _get_conveyancing_efficiency(impact_assessment, product)
    cycle_value = convert_value_from_cycle(product, irrigation / conveyancing) if irrigation > 0 else 0
    inputs_value = convert_value_from_cycle(product, sum_input_impacts(cycle.get('inputs', []), TERM_ID))
    logger.debug('model=%s, term=%s, cycle value=%s, inputs value=%s', MODEL, TERM_ID, cycle_value, inputs_value)
    # convert from m3 to litre
    value = (cycle_value * 1000) + inputs_value
    return _indicator(value)


def _get_irrigation(impact_assessment: dict):
    cycle = impact_assessment.get('cycle', {})
    data_complete = _is_term_type_complete(cycle, {'termType': TermTermType.WATER.value})
    inputs = filter_list_term_type(cycle.get('inputs', []), TermTermType.WATER)
    value = list_sum(get_total_value(inputs))
    return None if len(inputs) == 0 and not data_complete else value


def _should_run(impact_assessment: dict):
    product = get_product(impact_assessment) or {}
    product_id = product.get('term', {}).get('@id')
    irrigation = _get_irrigation(impact_assessment)

    debugRequirements(model=MODEL, term=TERM_ID,
                      product=product_id,
                      irrigation=irrigation)

    should_run = all([product_id, irrigation is not None])
    logger.info('model=%s, term=%s, should_run=%s', MODEL, TERM_ID, should_run)
    return should_run, product, irrigation


def run(impact_assessment: dict):
    should_run, product, irrigation = _should_run(impact_assessment)
    return _run(impact_assessment, product, irrigation) if should_run else None
