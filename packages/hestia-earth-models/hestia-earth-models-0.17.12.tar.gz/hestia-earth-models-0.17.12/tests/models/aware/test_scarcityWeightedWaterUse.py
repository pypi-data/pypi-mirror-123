from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_indicator, fake_load_impacts

from hestia_earth.models.aware.scarcityWeightedWaterUse import MODEL, TERM_ID, run, _should_run

class_path = f"hestia_earth.models.{MODEL}.{TERM_ID}"
fixtures_folder = f"{fixtures_path}/{MODEL}/{TERM_ID}"


@patch(f"{class_path}.emission_value", return_value=None)
def test_should_run(mock_emission_value):
    impact = {}

    # with emission => no run
    mock_emission_value.return_value = 100
    should_run, *args = _should_run(impact)
    assert not should_run

    cycle = {}
    impact['cycle'] = cycle

    # with a site and awareWaterBasinId => run
    cycle['site'] = {'awareWaterBasinId': '2424'}
    should_run, *args = _should_run(impact)
    assert should_run is True

    # with a site and region => run
    cycle['site'] = {'region': {'@id': 'GADM-AUS'}}
    should_run, *args = _should_run(impact)
    assert should_run is True


@patch(f"{class_path}._new_indicator", side_effect=fake_new_indicator)
def test_run(*args):
    with open(f"{fixtures_folder}/impact-assessment.jsonld", encoding='utf-8') as f:
        impact = json.load(f)

    with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(impact)
    assert value == expected


@patch(f"{class_path}._new_indicator", side_effect=fake_new_indicator)
def test_run_site_cropland(*args):
    with open(f"{fixtures_folder}/with-site-cropland/impact-assessment.jsonld", encoding='utf-8') as f:
        impact = json.load(f)

    with open(f"{fixtures_folder}/with-site-cropland/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(impact)
    assert value == expected


@patch(f"{class_path}._new_indicator", side_effect=fake_new_indicator)
def test_run_country(*args):
    with open(f"{fixtures_folder}/with-country/impact-assessment.jsonld", encoding='utf-8') as f:
        impact = json.load(f)

    with open(f"{fixtures_folder}/with-country/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(impact)
    assert value == expected


@patch('hestia_earth.models.utils.input.load_impacts', side_effect=fake_load_impacts)
@patch(f"{class_path}._new_indicator", side_effect=fake_new_indicator)
def test_run_with_inputs(*args):
    with open(f"{fixtures_folder}/with-inputs/impact-assessment.jsonld", encoding='utf-8') as f:
        impact = json.load(f)

    with open(f"{fixtures_folder}/with-inputs/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(impact)
    assert value == expected
