from sqlalchemy import create_engine
from sqlalchemy import insert
from sqlalchemy import text
from testcontainers.postgres import PostgresContainer
from .db_services.engine_factory import EngineFactory
from .cities_db import Base as Cities_Base, CITY_ROWS


class TestBases():
    __test__ = False
    db = None
    main_url = None

    def __init__(self, db_image_name):
        self.engine = EngineFactory()
        self.engine.stand = 'localhost'
        self.postgres_container = PostgresContainer(image=db_image_name)

    def create_base(self, base_name):
        engine = create_engine(self.main_url)
        connection = engine.connect()
        connection.execution_options(
            isolation_level='AUTOCOMMIT').execute(
                text(f'create database {base_name}'))
        __host, __port = self.main_url.replace(
            'postgresql+psycopg2://test:test@', '').replace(
                '/test', '').split(':')
        new_base_url = f'postgresql+psycopg2://test:test@{__host}:{__port}/\
{base_name}'
        
        engine = EngineFactory()
        engine.add_db(base_name=base_name, url=new_base_url)

    def create_schema(self, url, schema_name):
        engine = create_engine(url)
        connection = engine.connect()
        connection.execution_options(
            isolation_level='AUTOCOMMIT').execute(text(
                f'create schema {schema_name}'))

    def base_schema_data_creation(self):
        self.db = self.postgres_container.start()
        self.main_url = self.db.get_connection_url()
        
        BASES = {'cities': {'class': Cities_Base, 'rows': CITY_ROWS}}
        
        for new_base_name, new_base_data in BASES.items():
            self.create_base(base_name=new_base_name)
            self.engine.user, self.engine.passw = 'test', 'test'
    
            new_url = self.engine.get_postgres_url(base_name=new_base_name)
            
            self.create_schema(schema_name=new_base_name, url=new_url)
            db_engine = self.engine.get_engine(new_base_name)
            
            new_base_data.get('class').metadata.create_all(db_engine)
            
            with db_engine.connect() as conn:
                for cls, rows in new_base_data.get('rows').items():
                    conn.execute(insert(cls).values(rows))
                    conn.commit()
