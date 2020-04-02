#!/usr/bin/python
 
import psycopg2
from config import config
 
  # -- id serial GENERATED ALWAYS AS IDENTITY,
# https://chartio.com/resources/tutorials/how-to-define-an-auto-increment-primary-key-in-postgresql/
# http://www.postgresqltutorial.com/postgresql-unique-constraint/
# http://www.postgresqltutorial.com/postgresql-identity-column/

def create_component_production_table(cloud_connect=True):
    commands = ( 
    """
    DROP TABLE IF EXISTS public.component_production CASCADE;
    """,
    """
    CREATE TABLE public.component_production(
        id SERIAL PRIMARY KEY,
        component_id VARCHAR(100),
        date timestamp NOT NULL,
        value numeric,
        unit VARCHAR(10),
        created_on TIMESTAMP default NOW()
    );
    """)
    
    return run_query(commands,cloud_connect)

def create_communication_interval_per_site_id(cloud_connect=True):
    commands = (
        """
        -- DROP TABLE IF EXISTS public.communication_interval_per_site_id;
        """,
        """
        CREATE TABLE public.communication_interval_per_site_id
        (
        id SERIAL PRIMARY KEY,
        site_id character varying(30),
        date timestamp without time zone,
        comm_interval integer,
        comm_interval_expected integer
        );
        """
        )
    return run_query(commands,cloud_connect)

def create_component_details_table(cloud_connect=True):
    commands = ( 
    """
    DROP TABLE IF EXISTS public.component_details CASCADE;
    """,
    """
    CREATE TABLE public.component_details(
        id SERIAL PRIMARY KEY,
        component_id VARCHAR(100),
        manufacturers_component_id VARCHAR,
        type VARCHAR,
        sub_type VARCHAR,
        site_id VARCHAR,
        data_provider VARCHAR,
        manufacturer VARCHAR,
        is_energy_producing BOOLEAN, 
        created_on TIMESTAMP default NOW()
    );
    """)

    return run_query(commands,cloud_connect)

def create_expected_production_table(cloud_connect=True):
    commands = (
        """ DROP TABLE IF EXISTS public.expected_production;
        """,
        """
        CREATE TABLE expected_production
           (
               id SERIAL PRIMARY KEY,
               site_id VARCHAR(30),
               date TIMESTAMP NOT NULL,
               expected_production numeric,
               created_on TIMESTAMP default NOW()
           );
        """)
    return run_query(commands,cloud_connect)

def create_production_table(cloud_connect=True):
    commands = ( 
    """
    DROP TABLE IF EXISTS public.production CASCADE;
    """,
    """
    CREATE TABLE public.production (
            site_id VARCHAR(30), 
            measured_by VARCHAR(30),
            date TIMESTAMP NOT NULL,
            value integer, 
            unit VARCHAR(10),
            created_on TIMESTAMP default NOW()
    );

    """)

    return run_query(commands,cloud_connect)

def create_site_table(cloud_connect=True):
    commands = (
        """DROP TABLE IF EXISTS public.site CASCADE; 
        """,
        """
        CREATE TABLE public.site (
            site_id VARCHAR(20),
            name VARCHAR(100),
            account_id VARCHAR(100),
            status VARCHAR(20),
            size numeric,
            installation_date TIMESTAMP,
            pto_date TIMESTAMP,
            address VARCHAR(200),
            city VARCHAR(200),
            state CHAR(2),
            zip VARCHAR(12),
            timezone VARCHAR(50),
            latitude numeric,
            longitude numeric,
            owner_id VARCHAR(20),
            fetch_id VARCHAR(50),
            created_on TIMESTAMP default NOW()
            );
        """)
    return run_query(commands,cloud_connect)

def create_site_owner_table(cloud_connect=True):
    commands = (
        """ DROP TABLE IF EXISTS public.site_owner CASCADE; 
        """,
        """
        CREATE TABLE public.site_owner (
            owner_id VARCHAR(20),
            name VARCHAR(200),
            status VARCHAR(20),
            created_on TIMESTAMP default NOW()

            );
        """)
    return run_query(commands,cloud_connect)


def create_all_tables(cloud_connect=True,company_name=None):
    """ create tables in the PostgreSQL database"""
    print('creating production table: ', create_production_table(cloud_connect))
    print('creating site table: ', create_site_table(cloud_connect))
    print('creating site owner table: ', create_site_owner_table(cloud_connect))
    print('creating component production table: ', create_component_production_table(cloud_connect))
    print('creating component details table: ', create_component_details_table(cloud_connect))
    print('creating weather table: ', create_weather_table(cloud_connect))
    #print('creating communication table: ', create_communication_interval_per_site_id(cloud_connect))    
    return True

def connect_to_postgres(cloud_connect=True):
    
    print('testing cloud connect = ', cloud_connect)
    
    if cloud_connect:

        print('Connection type: Cloud')

        #if str(self.company_name).lower() == 'aws_sandbox':

         #   return config(filename='aws_sandbox.ini')

        #if str(self.company_name).lower() == 'barrier':
            
        #    return config(filename='barrier_cloudsql.ini')

        #return config(filename='aws_production.ini')
        return config()

    else:

        print('Connection type: Localhost')

        return config(filename='database.ini')

def run_query(commands,cloud_connect=True):
    conn = None
    try:

        # read the connection parameters
        params = connect_to_postgres(cloud_connect)
        print(params)
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        # success!
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False
    finally:
        if conn is not None:
            conn.close()
    return False
 
def test_connection(cloud_connect=True):
    #add print params to the run_query method
    print('hello world')
    print('test query')
    sql = ("""SELECT 1;""","""SELECT 2;""")
    run_query(sql, cloud_connect=True)
    

if __name__ == '__main__':
    company_name = 'aws_sandbox'
    #create_all_tables(cloud_connect=True, company_name=company_name)
    create_all_tables(cloud_connect=True, company_name=company_name)


'''
SELECT d.site_id, date_trunc('Day',p.date), sum(p.value)/1000
FROM component_production p
JOIN component_details d
ON p.component_id = d.manufacturers_component_id
WHERE d.site_id = '225542'
GROUP BY 1,2
ORDER BY 2
limit 100;

CREATE TABLE production_guarantee (
    contract_id serial,
    site_id varchar,
    contract_start_date DATE,
    contract_end_date DATE,
    production_guarantee numeric,
    unit varchar,
    term_months int
)
'''

'''
Changes to schema:
CREATE TABLE public.site (
    site_id VARCHAR(20),
    name VARCHAR(100),
    account_id VARCHAR(100),
    status VARCHAR(20),
    size numeric,
    installation_date TIMESTAMP,
    pto_date TIMESTAMP,
    address VARCHAR(200),
    city VARCHAR(200),
    state CHAR(2),
    zip VARCHAR(12),
    timezone VARCHAR(50),
    latitude numeric,
    longitude numeric,
    owner_id VARCHAR(20),
    fetch_id VARCHAR(50),
    created_on TIMESTAMP default NOW()
    );
CREATE TABLE weather
   (
       id SERIAL PRIMARY KEY,
       site_id VARCHAR(30),
       date TIMESTAMP NOT NULL,
       temperature_ambient numeric,
       temperature_module numeric,
       irradiance numeric,
       wind_direction numeric,
       wind_speed numeric
   );
'''