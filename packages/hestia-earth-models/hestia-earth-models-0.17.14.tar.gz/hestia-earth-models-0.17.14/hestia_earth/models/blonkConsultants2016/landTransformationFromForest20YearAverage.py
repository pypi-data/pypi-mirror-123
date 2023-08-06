from hestia_earth.schema import EmissionMethodTier, EmissionStatsDefinition

from hestia_earth.models.log import debugRequirements, logger
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.cycle import land_occupation_per_ha
from .utils import get_emission_factor
from . import MODEL

TERM_ID = 'landTransformationFromForest20YearAverage'


def _emission(value: float):
    logger.info('model=%s, term=%s, value=%s', MODEL, TERM_ID, value)
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = EmissionMethodTier.TIER_1.value
    emission['statsDefinition'] = EmissionStatsDefinition.MODELLED.value
    return emission


def _run(land_occupation_m2: float, land_transformation_factor: float):
    value = land_occupation_m2 * land_transformation_factor
    return [_emission(value)]


def _should_run(cycle: dict):
    land_occupation_m2 = land_occupation_per_ha(cycle) * 10000
    land_transformation_factor = get_emission_factor(cycle, 'landTransformation20YearsAverage')

    debugRequirements(model=MODEL, term=TERM_ID,
                      land_occupation_m2=land_occupation_m2,
                      land_transformation_factor=land_transformation_factor)

    should_run = all([land_occupation_m2, land_transformation_factor is not None])
    logger.info('model=%s, term=%s, should_run=%s', MODEL, TERM_ID, should_run)
    return should_run, land_occupation_m2, land_transformation_factor


def run(cycle: dict):
    should_run, land_occupation_m2, land_transformation_factor = _should_run(cycle)
    return _run(land_occupation_m2, land_transformation_factor) if should_run else []
