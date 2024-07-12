from ..db_services.db_service import get_from_postgres
from ..db_services.db_service import post_to_postgres

DB_NAME = 'cities'

def get_city_location(city) -> list:
    sql = '''
    select location
        from cities.cities
        where name = '%s'
    ''' % city

    try:
        return get_from_postgres(sql=sql, db_name=DB_NAME)
    except Exception as e:
        raise RuntimeError(e)

def get_cities_count(cities_list) -> int:
    for city in cities_list:
        sql = "insert into cities.cities values ('{}', '{}')".format(
            city["name"], city["location"])
        post_to_postgres(sql=sql, db_name=DB_NAME)
    new_sql = '''select count(*) from cities.cities'''
    try:
        return get_from_postgres(sql=new_sql, db_name=DB_NAME)
    except Exception as e:
        raise RuntimeError(e)

def get_joined_table_count() -> int:
    sql = "select count(*) from cities.cities join cities.weather on name=city"
    try:
        return get_from_postgres(sql=sql, db_name=DB_NAME)
    except Exception as e:
        raise RuntimeError(e)

def get_city_name() -> int:
    sql = "SELECT name from (SELECT row_number() over(order by name)\
as number, name, location from cities.cities)\
as new_one where number = (SELECT count(*) from cities.weather);"
    try:
        return get_from_postgres(sql=sql, db_name=DB_NAME)
    except Exception as e:
        raise RuntimeError(e);

def get_cities_count_after_deletion(cities_list) -> int:
    for city in cities_list:
        sql = "delete from cities.cities where name = '%s'" % city["name"]
        post_to_postgres(sql=sql, db_name=DB_NAME)
    new_sql = '''select count(*) from cities.cities'''
    try:
        return get_from_postgres(sql=new_sql, db_name=DB_NAME)
    except Exception as e:
        raise RuntimeError(e)
    
