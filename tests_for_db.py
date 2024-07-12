import pytest
from .processing.cities import *
from .cities_examples import cities_list
from .db_test import TestBases


@pytest.fixture(scope="session", autouse=True)
def test_db():
    test_base = TestBases(db_image_name='postgres:16.3')
    test_base.base_schema_data_creation()
    yield
    test_base.db.stop()


def test_get_location_before(test_db):
    assert get_city_location(city='San Francisco') == [["(-194.0, 53.0)"]]

def test_count_of_joined_tables(test_db):
    assert get_joined_table_count() == [[2]]

def test_count_after_insert_data(test_db):
    assert get_cities_count(cities_list) == [[6]]

def test_city_name_with_inserted_cities(test_db):
    assert get_city_name() == [['Denver']]

def test_cities_count_after_deletion(test_db):
    assert get_cities_count_after_deletion(cities_list) == [[1]]

