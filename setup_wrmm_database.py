# """
# WRMM Database Schema Setup
# ==========================
# This script creates the necessary database tables and indexes for WRMM data.

# Run this script ONCE before using the database integration.

# Usage:
#     python setup_wrmm_database.py
# """

# from sqlalchemy import create_engine, text, inspect
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# def create_wrmm_schema():
#     """Create database schema and tables for WRMM."""
    
#     # Database configuration
#     # DB_CONFIG = {
#     #     'host': 'C-GOA-APM-13250',
#     #     'port': '5432',
#     #     'database': 'sopan_wrmm_test',
#     #     'user': 'postgres',
#     #     'password': 'postgres',
#     #     'schema': 'wrmm'
#     # }

#     DB_CONFIG = {
#         'host': 'C-GOA-APM-13251',
#         'port': '5432',
#         'database': 'Main',
#         'user': 'postgres',
#         'password': 'IEMP_POSTGRES',
#         'schema': 'wrmm'
#     }
    
#     connection_string = (
#         f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
#         f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
#     )
    
#     engine = create_engine(connection_string)
    
#     try:
#         with engine.connect() as conn:
#             # Create schema
#             logger.info(f"Creating schema: {DB_CONFIG['schema']}")
#             conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {DB_CONFIG['schema']}"))
#             conn.commit()
            
#             # Main WRMM Outputs Table
#             logger.info("Creating wrmmoutputs table...")
#             conn.execute(text(f"""
#                 CREATE TABLE IF NOT EXISTS {DB_CONFIG['schema']}.wrmmoutputs (
#                     id SERIAL PRIMARY KEY,
#                     run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     data_type VARCHAR(100),
#                     model_name VARCHAR(100),
#                     component_type VARCHAR(50),
#                     component_name VARCHAR(200),
#                     component_number INTEGER,
#                     year INTEGER,
#                     interval INTEGER,
#                     date DATE,
#                     value DOUBLE PRECISION,
#                     unit VARCHAR(50),
#                     per_storage DOUBLE PRECISION,
#                     io_failed VARCHAR(10),
#                     wco_failed VARCHAR(10),
#                     total_irrigated_area_ha DOUBLE PRECISION,
#                     comments TEXT,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                 )
#             """))
#             conn.commit()
            
#             # Create indexes for better query performance
#             logger.info("Creating indexes on wrmmoutputs...")
#             conn.execute(text(f"""
#                 CREATE INDEX IF NOT EXISTS idx_wrmmoutputs_year_interval 
#                 ON {DB_CONFIG['schema']}.wrmmoutputs(year, interval)
#             """))
            
#             conn.execute(text(f"""
#                 CREATE INDEX IF NOT EXISTS idx_wrmmoutputs_component 
#                 ON {DB_CONFIG['schema']}.wrmmoutputs(component_type, component_name)
#             """))
            
#             conn.execute(text(f"""
#                 CREATE INDEX IF NOT EXISTS idx_wrmmoutputs_data_type 
#                 ON {DB_CONFIG['schema']}.wrmmoutputs(data_type)
#             """))
            
#             conn.execute(text(f"""
#                 CREATE INDEX IF NOT EXISTS idx_wrmmoutputs_run_timestamp 
#                 ON {DB_CONFIG['schema']}.wrmmoutputs(run_timestamp)
#             """))
#             conn.commit()
            
#             # Executive Summary Table
#             logger.info("Creating executive_summary table...")
#             conn.execute(text(f"""
#                 CREATE TABLE IF NOT EXISTS {DB_CONFIG['schema']}.executive_summary (
#                     id SERIAL PRIMARY KEY,
#                     run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     component_type VARCHAR(100),
#                     year INTEGER,
#                     component_name VARCHAR(200),
#                     value DOUBLE PRECISION,
#                     comments TEXT,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                 )
#             """))
#             conn.commit()
            
#             # Reservoir Summary Table
#             logger.info("Creating reservoir_summary table...")
#             conn.execute(text(f"""
#                 CREATE TABLE IF NOT EXISTS {DB_CONFIG['schema']}.reservoir_summary (
#                     id SERIAL PRIMARY KEY,
#                     run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     reservoir VARCHAR(200),
#                     owned_by_goa VARCHAR(10),
#                     percent_fsl VARCHAR(20),
#                     projected_total_inflow_dam3 VARCHAR(50),
#                     start_week INTEGER,
#                     end_week INTEGER,
#                     year INTEGER,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                 )
#             """))
#             conn.commit()
            
#             # Reservoir Inflow Table
#             logger.info("Creating reservoir_inflow table...")
#             conn.execute(text(f"""
#                 CREATE TABLE IF NOT EXISTS {DB_CONFIG['schema']}.reservoir_inflow (
#                     id SERIAL PRIMARY KEY,
#                     run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     scenario VARCHAR(100),
#                     reservoir VARCHAR(200),
#                     inflow_dam3 DOUBLE PRECISION,
#                     year INTEGER,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                 )
#             """))
#             conn.commit()
            
#             # Irrigation Diversion Table
#             logger.info("Creating irrigation_diversion table...")
#             conn.execute(text(f"""
#                 CREATE TABLE IF NOT EXISTS {DB_CONFIG['schema']}.irrigation_diversion (
#                     id SERIAL PRIMARY KEY,
#                     run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     component_name VARCHAR(200),
#                     diversion_year INTEGER,
#                     scenario VARCHAR(100),
#                     diversion_volume DOUBLE PRECISION,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                 )
#             """))
#             conn.commit()
            
#             # WISKI Combined Data Table
#             logger.info("Creating wiski_combined_data table...")
#             conn.execute(text(f"""
#                 CREATE TABLE IF NOT EXISTS {DB_CONFIG['schema']}.wiski_combined_data (
#                     id SERIAL PRIMARY KEY,
#                     run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     station VARCHAR(200),
#                     data_source VARCHAR(100),
#                     value DOUBLE PRECISION,
#                     interval INTEGER,
#                     date DATE,
#                     year INTEGER,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                 )
#             """))
#             conn.commit()
            
#             # WISKI Summary Table
#             logger.info("Creating wiski_summary table...")
#             conn.execute(text(f"""
#                 CREATE TABLE IF NOT EXISTS {DB_CONFIG['schema']}.wiski_summary (
#                     id SERIAL PRIMARY KEY,
#                     run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     station VARCHAR(200),
#                     data_source VARCHAR(100),
#                     value_count INTEGER,
#                     value_mean DOUBLE PRECISION,
#                     value_std DOUBLE PRECISION,
#                     interval_min INTEGER,
#                     interval_max INTEGER,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                 )
#             """))
#             conn.commit()
            
#             # Weather Forecast Table
#             logger.info("Creating weather_forecast table...")
#             conn.execute(text(f"""
#                 CREATE TABLE IF NOT EXISTS {DB_CONFIG['schema']}.weather_forecast (
#                     id SERIAL PRIMARY KEY,
#                     run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     station VARCHAR(200),
#                     date DATE,
#                     temperature DOUBLE PRECISION,
#                     precipitation DOUBLE PRECISION,
#                     forecast_type VARCHAR(50),
#                     interval INTEGER,
#                     year INTEGER,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                 )
#             """))
#             conn.commit()
            
#             # MAA (Mean Annual Allocation) Table
#             logger.info("Creating maa_summary table...")
#             conn.execute(text(f"""
#                 CREATE TABLE IF NOT EXISTS {DB_CONFIG['schema']}.maa_summary (
#                     id SERIAL PRIMARY KEY,
#                     run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     component_name VARCHAR(200),
#                     maa_1969 DOUBLE PRECISION,
#                     scenario VARCHAR(100),
#                     year INTEGER,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                 )
#             """))
#             conn.commit()
            
#             # Apportionment Table
#             logger.info("Creating apportionment table...")
#             conn.execute(text(f"""
#                 CREATE TABLE IF NOT EXISTS {DB_CONFIG['schema']}.apportionment (
#                     id SERIAL PRIMARY KEY,
#                     run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     station VARCHAR(200),
#                     date DATE,
#                     week INTEGER,
#                     natural_flow DOUBLE PRECISION,
#                     diversions DOUBLE PRECISION,
#                     net_flow DOUBLE PRECISION,
#                     year INTEGER,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                 )
#             """))
#             conn.commit()
            
#             # Run History Table (for tracking processing runs)
#             logger.info("Creating run_history table...")
#             conn.execute(text(f"""
#                 CREATE TABLE IF NOT EXISTS {DB_CONFIG['schema']}.run_history (
#                     id SERIAL PRIMARY KEY,
#                     run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     start_week INTEGER,
#                     end_week INTEGER,
#                     year INTEGER,
#                     status VARCHAR(50),
#                     rows_processed INTEGER,
#                     processing_time_seconds DOUBLE PRECISION,
#                     notes TEXT,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                 )
#             """))
#             conn.commit()
            
#             logger.info("✓ All tables created successfully!")
            
#             # Create a view for easy querying
#             logger.info("Creating convenience views...")
#             conn.execute(text(f"""
#                 CREATE OR REPLACE VIEW {DB_CONFIG['schema']}.latest_wrmm_output AS
#                 SELECT DISTINCT ON (component_name, component_type, year, interval)
#                     *
#                 FROM {DB_CONFIG['schema']}.wrmmoutputs
#                 ORDER BY component_name, component_type, year, interval, run_timestamp DESC
#             """))
#             conn.commit()
            
#             logger.info("✓ Database setup completed successfully!")
            
#     except Exception as e:
#         logger.error(f"Error setting up database: {e}")
#         raise
#     finally:
#         engine.dispose()


# def verify_setup():
#     """Verify that all tables were created successfully."""
    
#     DB_CONFIG = {
#         'host': 'C-GOA-APM-13251',
#         'port': '5432',
#         'database': 'Main',
#         'user': 'postgres',
#         'password': 'IEMP_POSTGRES',
#         'schema': 'wrmm'
#     }
    
#     connection_string = (
#         f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
#         f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
#     )
    
#     engine = create_engine(connection_string)
#     inspector = inspect(engine)
    
#     expected_tables = [
#         'wrmmoutputs',
#         'executive_summary',
#         'reservoir_summary',
#         'reservoir_inflow',
#         'irrigation_diversion',
#         'wiski_combined_data',
#         'wiski_summary',
#         'weather_forecast',
#         'maa_summary',
#         'apportionment',
#         'run_history'
#     ]
    
#     existing_tables = inspector.get_table_names(schema=DB_CONFIG['schema'])
    
#     logger.info("\nVerification Results:")
#     logger.info("=" * 50)
    
#     all_exist = True
#     for table in expected_tables:
#         exists = table in existing_tables
#         status = "✓" if exists else "✗"
#         logger.info(f"{status} {table}")
#         if not exists:
#             all_exist = False
    
#     if all_exist:
#         logger.info("\n✓ All tables verified successfully!")
#     else:
#         logger.warning("\n✗ Some tables are missing!")
    
#     engine.dispose()
#     return all_exist


# def add_sample_data():
#     """Add some sample data for testing."""
    
#     DB_CONFIG = {
#         'host': 'C-GOA-APM-13251',
#         'port': '5432',
#         'database': 'Main',
#         'user': 'postgres',
#         'password': 'IEMP_POSTGRES',
#         'schema': 'wrmm'
#     }
    
#     connection_string = (
#         f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
#         f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
#     )
    
#     engine = create_engine(connection_string)
    
#     try:
#         with engine.connect() as conn:
#             logger.info("Adding sample run history record...")
#             conn.execute(text(f"""
#                 INSERT INTO {DB_CONFIG['schema']}.run_history 
#                 (start_week, end_week, year, status, rows_processed, processing_time_seconds, notes)
#                 VALUES 
#                 (33, 38, 2025, 'SUCCESS', 0, 0, 'Database setup completed - ready for data')
#             """))
#             conn.commit()
#             logger.info("✓ Sample data added successfully!")
    
#     except Exception as e:
#         logger.error(f"Error adding sample data: {e}")
#     finally:
#         engine.dispose()


# def drop_all_tables():
#     """
#     DANGER: Drop all WRMM tables.
#     Use this only for cleanup/reset.
#     """
#     DB_CONFIG = {
#         'host': 'C-GOA-APM-13251',
#         'port': '5432',
#         'database': 'Main',
#         'user': 'postgres',
#         'password': 'IEMP_POSTGRES',
#         'schema': 'wrmm'
#     }
    
#     response = input(
#         f"WARNING: This will drop all tables in schema '{DB_CONFIG['schema']}'. "
#         "Type 'YES' to confirm: "
#     )
    
#     if response != 'YES':
#         logger.info("Operation cancelled")
#         return
    
#     connection_string = (
#         f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
#         f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
#     )
    
#     engine = create_engine(connection_string)
    
#     try:
#         with engine.connect() as conn:
#             logger.info(f"Dropping schema {DB_CONFIG['schema']} CASCADE...")
#             conn.execute(text(f"DROP SCHEMA IF EXISTS {DB_CONFIG['schema']} CASCADE"))
#             conn.commit()
#             logger.info("✓ Schema dropped successfully")
#     except Exception as e:
#         logger.error(f"Error dropping schema: {e}")
#     finally:
#         engine.dispose()


# if __name__ == "__main__":
#     import sys
    
#     print("=" * 60)
#     print("WRMM Database Setup")
#     print("=" * 60)
    
#     if len(sys.argv) > 1:
#         if sys.argv[1] == '--drop':
#             drop_all_tables()
#         elif sys.argv[1] == '--verify':
#             verify_setup()
#         else:
#             print(f"Unknown option: {sys.argv[1]}")
#             print("Usage:")
#             print("  python setup_wrmm_database.py          # Create tables")
#             print("  python setup_wrmm_database.py --verify # Verify setup")
#             print("  python setup_wrmm_database.py --drop   # Drop all tables")
#     else:
#         # Default: Create tables
#         create_wrmm_schema()
#         verify_setup()
#         add_sample_data()
        
#         print("\n" + "=" * 60)
#         print("Setup Complete!")
#         print("=" * 60)
#         print("\nNext steps:")
#         print("1. Update your WRMM_workflow_v2.py to use WRMMOutputManager")
#         print("2. Run your workflow - data will be automatically saved to database")
#         print("3. Query your data using SQL or pandas read_sql()")


"""
WRMM Database Setup - Clean Install
====================================
This script drops existing tables and recreates them fresh.
Use this when you need to start clean or fix column issues.

For: C-GOA-APM-13251 server setup
"""

from sqlalchemy import create_engine, text, inspect
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def drop_and_recreate_wrmm_schema():
    """Drop existing WRMM tables and recreate them fresh."""
    
    DB_CONFIG = {
        'host': 'C-GOA-APM-13251',
        'port': '5432',
        'database': 'Main',
        'user': 'postgres',
        'password': 'IEMP_POSTGRES',
        'schema': 'wrmm_sopan'
    }
    
    connection_string = (
        f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
        f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    
    engine = create_engine(connection_string)
    
    try:
        with engine.connect() as conn:
            logger.info("=" * 60)
            logger.info("WRMM Database Clean Setup")
            logger.info("=" * 60)
            
            # Create schema if it doesn't exist
            logger.info(f"Creating schema: {DB_CONFIG['schema']}")
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {DB_CONFIG['schema']}"))
            conn.commit()
            
            # Drop all existing tables in wrmm schema
            logger.info("\nDropping existing tables if any...")
            tables_to_drop = [
                'wrmmoutputs',
                'executive_summary',
                'reservoir_summary',
                'reservoir_inflow',
                'irrigation_diversion',
                'wiski_combined_data',
                'wiski_summary',
                'weather_forecast',
                'maa_summary',
                'apportionment',
                'run_history'
            ]
            
            for table in tables_to_drop:
                try:
                    conn.execute(text(f"DROP TABLE IF EXISTS {DB_CONFIG['schema']}.{table} CASCADE"))
                    logger.info(f"  ✓ Dropped {table} (if existed)")
                except Exception as e:
                    logger.warning(f"  ⚠ Could not drop {table}: {e}")
            
            conn.commit()
            logger.info("✓ Old tables cleaned up")
            
            # Now create all tables fresh
            logger.info("\nCreating fresh tables...")
            
            # 1. Main WRMM Outputs Table
            logger.info("Creating wrmmoutputs table...")
            conn.execute(text(f"""
                CREATE TABLE {DB_CONFIG['schema']}.wrmmoutputs (
                    id SERIAL PRIMARY KEY,
                    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_type VARCHAR(100),
                    model_name VARCHAR(100),
                    component_type VARCHAR(50),
                    component_name VARCHAR(200),
                    component_number INTEGER,
                    year INTEGER,
                    interval INTEGER,
                    date DATE,
                    value DOUBLE PRECISION,
                    unit VARCHAR(50),
                    per_storage DOUBLE PRECISION,
                    io_failed VARCHAR(10),
                    wco_failed VARCHAR(10),
                    total_irrigated_area_ha DOUBLE PRECISION,
                    comments TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            logger.info("✓ wrmmoutputs table created")
            
            # Create indexes
            logger.info("Creating indexes on wrmmoutputs...")
            conn.execute(text(f"""
                CREATE INDEX idx_wrmmoutputs_year_interval 
                ON {DB_CONFIG['schema']}.wrmmoutputs(year, interval)
            """))
            conn.execute(text(f"""
                CREATE INDEX idx_wrmmoutputs_component 
                ON {DB_CONFIG['schema']}.wrmmoutputs(component_type, component_name)
            """))
            conn.execute(text(f"""
                CREATE INDEX idx_wrmmoutputs_data_type 
                ON {DB_CONFIG['schema']}.wrmmoutputs(data_type)
            """))
            conn.execute(text(f"""
                CREATE INDEX idx_wrmmoutputs_run_timestamp 
                ON {DB_CONFIG['schema']}.wrmmoutputs(run_timestamp)
            """))
            conn.commit()
            logger.info("✓ Indexes created")
            
            # 2. Executive Summary Table
            logger.info("Creating executive_summary table...")
            conn.execute(text(f"""
                CREATE TABLE {DB_CONFIG['schema']}.executive_summary (
                    id SERIAL PRIMARY KEY,
                    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    component_type VARCHAR(100),
                    year INTEGER,
                    component_name VARCHAR(200),
                    value DOUBLE PRECISION,
                    comments TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            logger.info("✓ executive_summary table created")
            
            # 3. Reservoir Summary Table
            logger.info("Creating reservoir_summary table...")
            conn.execute(text(f"""
                CREATE TABLE {DB_CONFIG['schema']}.reservoir_summary (
                    id SERIAL PRIMARY KEY,
                    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    reservoir VARCHAR(200),
                    owned_by_goa VARCHAR(10),
                    percent_fsl VARCHAR(20),
                    projected_total_inflow_dam3 VARCHAR(50),
                    start_week INTEGER,
                    end_week INTEGER,
                    year INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            logger.info("✓ reservoir_summary table created")
            
            # 4. Reservoir Inflow Table
            logger.info("Creating reservoir_inflow table...")
            conn.execute(text(f"""
                CREATE TABLE {DB_CONFIG['schema']}.reservoir_inflow (
                    id SERIAL PRIMARY KEY,
                    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    scenario VARCHAR(100),
                    reservoir VARCHAR(200),
                    inflow_dam3 DOUBLE PRECISION,
                    year INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            logger.info("✓ reservoir_inflow table created")
            
            # 5. Irrigation Diversion Table
            logger.info("Creating irrigation_diversion table...")
            conn.execute(text(f"""
                CREATE TABLE {DB_CONFIG['schema']}.irrigation_diversion (
                    id SERIAL PRIMARY KEY,
                    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    component_name VARCHAR(200),
                    diversion_year INTEGER,
                    scenario VARCHAR(100),
                    diversion_volume DOUBLE PRECISION,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            logger.info("✓ irrigation_diversion table created")
            
            # 6. WISKI Combined Data Table
            logger.info("Creating wiski_combined_data table...")
            conn.execute(text(f"""
                CREATE TABLE {DB_CONFIG['schema']}.wiski_combined_data (
                    id SERIAL PRIMARY KEY,
                    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    station VARCHAR(200),
                    data_source VARCHAR(100),
                    value DOUBLE PRECISION,
                    interval INTEGER,
                    date DATE,
                    year INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            logger.info("✓ wiski_combined_data table created")
            
            # 7. WISKI Summary Table
            logger.info("Creating wiski_summary table...")
            conn.execute(text(f"""
                CREATE TABLE {DB_CONFIG['schema']}.wiski_summary (
                    id SERIAL PRIMARY KEY,
                    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    station VARCHAR(200),
                    data_source VARCHAR(100),
                    value_count INTEGER,
                    value_mean DOUBLE PRECISION,
                    value_std DOUBLE PRECISION,
                    interval_min INTEGER,
                    interval_max INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            logger.info("✓ wiski_summary table created")
            
            # 8. Weather Forecast Table
            logger.info("Creating weather_forecast table...")
            conn.execute(text(f"""
                CREATE TABLE {DB_CONFIG['schema']}.weather_forecast (
                    id SERIAL PRIMARY KEY,
                    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    station VARCHAR(200),
                    date DATE,
                    temperature DOUBLE PRECISION,
                    precipitation DOUBLE PRECISION,
                    forecast_type VARCHAR(50),
                    interval INTEGER,
                    year INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            logger.info("✓ weather_forecast table created")
            
            # 9. MAA Summary Table
            logger.info("Creating maa_summary table...")
            conn.execute(text(f"""
                CREATE TABLE {DB_CONFIG['schema']}.maa_summary (
                    id SERIAL PRIMARY KEY,
                    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    component_name VARCHAR(200),
                    maa_1969 DOUBLE PRECISION,
                    scenario VARCHAR(100),
                    year INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            logger.info("✓ maa_summary table created")
            
            # 10. Apportionment Table
            logger.info("Creating apportionment table...")
            conn.execute(text(f"""
                CREATE TABLE {DB_CONFIG['schema']}.apportionment (
                    id SERIAL PRIMARY KEY,
                    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    station VARCHAR(200),
                    date DATE,
                    week INTEGER,
                    natural_flow DOUBLE PRECISION,
                    diversions DOUBLE PRECISION,
                    net_flow DOUBLE PRECISION,
                    year INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            logger.info("✓ apportionment table created")
            
            # 11. Run History Table
            logger.info("Creating run_history table...")
            conn.execute(text(f"""
                CREATE TABLE {DB_CONFIG['schema']}.run_history (
                    id SERIAL PRIMARY KEY,
                    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    start_week INTEGER,
                    end_week INTEGER,
                    year INTEGER,
                    status VARCHAR(50),
                    rows_processed INTEGER,
                    processing_time_seconds DOUBLE PRECISION,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            logger.info("✓ run_history table created")
            
            # Create convenience view
            logger.info("\nCreating convenience views...")
            conn.execute(text(f"""
                CREATE OR REPLACE VIEW {DB_CONFIG['schema']}.latest_wrmm_output AS
                SELECT DISTINCT ON (component_name, component_type, year, interval)
                    *
                FROM {DB_CONFIG['schema']}.wrmmoutputs
                ORDER BY component_name, component_type, year, interval, run_timestamp DESC
            """))
            conn.commit()
            logger.info("✓ Views created")
            
            # Add sample run history record
            logger.info("\nAdding sample run history record...")
            conn.execute(text(f"""
                INSERT INTO {DB_CONFIG['schema']}.run_history 
                (start_week, end_week, year, status, rows_processed, processing_time_seconds, notes)
                VALUES 
                (33, 38, 2025, 'SETUP', 0, 0, 'Database setup completed - ready for data')
            """))
            conn.commit()
            logger.info("✓ Sample data added")
            
            logger.info("\n" + "=" * 60)
            logger.info("✓ DATABASE SETUP COMPLETED SUCCESSFULLY!")
            logger.info("=" * 60)
            logger.info(f"\nDatabase: {DB_CONFIG['database']}")
            logger.info(f"Schema: {DB_CONFIG['schema']}")
            logger.info(f"Tables created: 11")
            logger.info(f"Host: {DB_CONFIG['host']}")
            
    except Exception as e:
        logger.error(f"Error setting up database: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        engine.dispose()


def verify_setup():
    """Verify that all tables were created successfully."""
    
    DB_CONFIG = {
        'host': 'C-GOA-APM-13251',
        'port': '5432',
        'database': 'Main',
        'user': 'postgres',
        'password': 'IEMP_POSTGRES',
        'schema': 'wrmm'
    }
    
    connection_string = (
        f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
        f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    
    engine = create_engine(connection_string)
    inspector = inspect(engine)
    
    expected_tables = [
        'wrmmoutputs',
        'executive_summary',
        'reservoir_summary',
        'reservoir_inflow',
        'irrigation_diversion',
        'wiski_combined_data',
        'wiski_summary',
        'weather_forecast',
        'maa_summary',
        'apportionment',
        'run_history'
    ]
    
    existing_tables = inspector.get_table_names(schema=DB_CONFIG['schema'])
    
    logger.info("\n" + "=" * 60)
    logger.info("VERIFICATION RESULTS")
    logger.info("=" * 60)
    
    all_exist = True
    for table in expected_tables:
        exists = table in existing_tables
        status = "✓" if exists else "✗"
        logger.info(f"{status} {table}")
        if not exists:
            all_exist = False
    
    if all_exist:
        logger.info("\n✓ All tables verified successfully!")
        
        # Show table structure for wrmmoutputs
        logger.info("\nwrmmoutputs table structure:")
        columns = inspector.get_columns('wrmmoutputs', schema=DB_CONFIG['schema'])
        for col in columns:
            logger.info(f"  - {col['name']}: {col['type']}")
    else:
        logger.warning("\n✗ Some tables are missing!")
    
    engine.dispose()
    return all_exist


if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("WRMM Database Clean Setup")
    print("=" * 60)
    print("\n⚠️  WARNING: This will DROP all existing WRMM tables!")
    print("All data in these tables will be LOST.\n")
    
    if len(sys.argv) > 1 and sys.argv[1] == '--verify':
        verify_setup()
    else:
        response = input("Are you sure you want to proceed? (type 'YES' to confirm): ")
        
        if response == 'YES':
            try:
                drop_and_recreate_wrmm_schema()
                print("\n" + "=" * 60)
                print("Verifying setup...")
                verify_setup()
            except Exception as e:
                print(f"\nSetup failed: {e}")
                sys.exit(1)
        else:
            print("\nSetup cancelled")
            sys.exit(0)