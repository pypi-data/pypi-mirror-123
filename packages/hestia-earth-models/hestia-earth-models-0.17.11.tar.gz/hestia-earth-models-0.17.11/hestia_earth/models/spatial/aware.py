from hestia_earth.models.log import logger
from .utils import download, has_geospatial_data, _site_gadm_id
from . import MODEL

EE_PARAMS = {
    'collection': 'AWARE',
    'type': 'vector',
    'field': 'Name'
}


def _download(site: dict):
    return download(
        collection=EE_PARAMS['collection'],
        ee_type=EE_PARAMS['type'],
        fields=EE_PARAMS['field'],
        latitude=site.get('latitude'),
        longitude=site.get('longitude'),
        gadm_id=_site_gadm_id(site),
        boundary=site.get('boundary')
    ).get(EE_PARAMS['field'], None)


def _run(site: dict):
    value = _download(site)
    logger.info('model=%s, term=aware, value=%s', MODEL, value)
    return value


def _should_run(site: dict):
    should_run = has_geospatial_data(site)
    logger.info('model=%s, term=aware, should_run=%s', MODEL, should_run)
    return should_run


def run(site: dict): return _run(site) if _should_run(site) else None
