"""
WRMM Database Utilities
=======================
Module for handling database operations for WRMM outputs.
Can be integrated into existing WRMM workflow with minimal changes.

Features:
- Direct PostgreSQL push using SQLAlchemy
- Supports bulk inserts for performance
- Maintains backward compatibility with CSV/Excel outputs
- Transaction management for data integrity
- Configurable table schemas
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError
import logging
from datetime import datetime
from typing import Optional, Dict, List
import warnings

warnings.filterwarnings('ignore')


class WRMMDatabaseManager:
    """
    Manager class for WRMM database operations.
    
    Usage:
        db_manager = WRMMDatabaseManager(
            host='C-GOA-APM-13251',
            port='5432',
            database='Main',
            user='postgres',
            password='IEMP_POSTGRES',
            schema='wrmm'
        )
        
        # Push DataFrame to database
        db_manager.push_dataframe(
            df=master_data_file,
            table_name='wrmmoutputs',
            if_exists='append'
        )
    """
    
    def __init__(self, host: str, port: str, database: str, 
                 user: str, password: str, schema: str = 'wrmm'):
        """
        Initialize database connection.
        
        Args:
            host: Database host address
            port: Database port
            database: Database name
            user: Database user
            password: Database password
            schema: Schema name (default: 'wrmm')
        """
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.schema = schema
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Create connection string
        self.connection_string = (
            f'postgresql://{user}:{password}@{host}:{port}/{database}'
        )
        
        # Create engine
        try:
            self.engine = create_engine(
                self.connection_string,
                pool_pre_ping=True,  # Verify connections before using
                pool_size=5,
                max_overflow=10
            )
            self.logger.info("Database engine created successfully")
        except Exception as e:
            self.logger.error(f"Failed to create database engine: {e}")
            raise
    
    def test_connection(self) -> bool:
        """
        Test database connection.
        
        Returns:
            bool: True if connection successful
        """
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            self.logger.info("Database connection test successful")
            return True
        except Exception as e:
            self.logger.error(f"Database connection test failed: {e}")
            return False
    
    def create_schema_if_not_exists(self):
        """Create schema if it doesn't exist."""
        try:
            with self.engine.connect() as conn:
                conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {self.schema}"))
                conn.commit()
            self.logger.info(f"Schema '{self.schema}' verified/created")
        except Exception as e:
            self.logger.error(f"Failed to create schema: {e}")
            raise
    
    def table_exists(self, table_name: str) -> bool:
        """
        Check if table exists.
        
        Args:
            table_name: Name of the table
            
        Returns:
            bool: True if table exists
        """
        inspector = inspect(self.engine)
        return inspector.has_table(table_name, schema=self.schema)
    
    def push_dataframe(self, df: pd.DataFrame, table_name: str, 
                       if_exists: str = 'append', 
                       column_mapping: Optional[Dict] = None,
                       batch_size: int = 1000) -> bool:
        """
        Push DataFrame to database table.
        
        Args:
            df: DataFrame to push
            table_name: Target table name
            if_exists: How to behave if table exists ('fail', 'replace', 'append')
            column_mapping: Optional column name mapping
            batch_size: Number of rows to insert per batch
            
        Returns:
            bool: True if successful
        """
        try:
            # Apply column mapping if provided
            if column_mapping:
                df = df.rename(columns=column_mapping)
            
            # Create a copy to avoid modifying original
            df_to_push = df.copy()
            
            # Convert datetime columns to proper format
            for col in df_to_push.columns:
                if df_to_push[col].dtype == 'datetime64[ns]':
                    df_to_push[col] = df_to_push[col].dt.strftime('%Y-%m-%d %H:%M:%S')
            
            # Replace NaN with None for database NULL
            df_to_push = df_to_push.replace({np.nan: None})
            
            # Push to database
            rows_written = df_to_push.to_sql(
                name=table_name,
                con=self.engine,
                schema=self.schema,
                if_exists=if_exists,
                index=False,
                method='multi',
                chunksize=batch_size
            )
            
            self.logger.info(
                f"Successfully pushed {len(df_to_push)} rows to "
                f"{self.schema}.{table_name} (mode: {if_exists})"
            )
            return True
            
        except Exception as e:
            self.logger.error(
                f"Failed to push data to {self.schema}.{table_name}: {e}"
            )
            return False
    
    def push_with_timestamp(self, df: pd.DataFrame, table_name: str,
                           run_timestamp: Optional[datetime] = None,
                           **kwargs) -> bool:
        """
        Push DataFrame with additional run timestamp column.
        
        Args:
            df: DataFrame to push
            table_name: Target table name
            run_timestamp: Timestamp for this run (default: now)
            **kwargs: Additional arguments for push_dataframe
            
        Returns:
            bool: True if successful
        """
        df_with_timestamp = df.copy()
        if run_timestamp is None:
            run_timestamp = datetime.now()
        df_with_timestamp.insert(0, 'run_timestamp', run_timestamp)
        
        return self.push_dataframe(df_with_timestamp, table_name, **kwargs)
    
    def execute_query(self, query: str) -> Optional[pd.DataFrame]:
        """
        Execute a query and return results as DataFrame.
        
        Args:
            query: SQL query to execute
            
        Returns:
            DataFrame with results or None if query fails
        """
        try:
            with self.engine.connect() as conn:
                result = pd.read_sql(query, conn)
            self.logger.info(f"Query executed successfully: {len(result)} rows returned")
            return result
        except Exception as e:
            self.logger.error(f"Query execution failed: {e}")
            return None
    
    def delete_run_data(self, table_name: str, start_week: int, end_week: int,
                       year: int) -> bool:
        """
        Delete data for a specific week range and year.
        Useful for reprocessing data.
        
        Args:
            table_name: Table to delete from
            start_week: Start week
            end_week: End week
            year: Year
            
        Returns:
            bool: True if successful
        """
        try:
            query = text(f"""
                DELETE FROM {self.schema}.{table_name}
                WHERE year = :year 
                AND interval >= :start_week 
                AND interval <= :end_week
            """)
            
            with self.engine.connect() as conn:
                result = conn.execute(query, {
                    'year': year,
                    'start_week': start_week,
                    'end_week': end_week
                })
                conn.commit()
                
            self.logger.info(
                f"Deleted data from {self.schema}.{table_name} for "
                f"Year {year}, Weeks {start_week}-{end_week}"
            )
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete data: {e}")
            return False
    
    def close(self):
        """Close database connection."""
        if self.engine:
            self.engine.dispose()
            self.logger.info("Database connection closed")


class WRMMOutputManager:
    """
    High-level manager for WRMM outputs.
    Handles both file and database outputs.
    """
    
    def __init__(self, output_dir: str, db_config: Optional[Dict] = None,
                 enable_database: bool = True, enable_files: bool = True):
        """
        Initialize output manager.
        
        Args:
            output_dir: Directory for file outputs
            db_config: Database configuration dict (host, port, database, user, password, schema)
            enable_database: Whether to push to database
            enable_files: Whether to create CSV/Excel files
        """
        self.output_dir = output_dir
        self.enable_database = enable_database
        self.enable_files = enable_files
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Initialize database manager if enabled
        self.db_manager = None
        if enable_database and db_config:
            try:
                self.db_manager = WRMMDatabaseManager(**db_config)
                self.db_manager.create_schema_if_not_exists()
                self.logger.info("Database manager initialized")
            except Exception as e:
                self.logger.error(f"Failed to initialize database: {e}")
                self.logger.warning("Continuing with file-only outputs")
                self.enable_database = False
    
    def save_output(self, df: pd.DataFrame, base_name: str, 
                   table_name: Optional[str] = None,
                   save_csv: bool = True, save_excel: bool = True,
                   db_if_exists: str = 'append',
                   column_mapping: Optional[Dict] = None) -> Dict[str, bool]:
        """
        Save output to files and/or database.
        
        Args:
            df: DataFrame to save
            base_name: Base filename (without extension)
            table_name: Database table name (uses base_name if None)
            save_csv: Whether to save CSV file
            save_excel: Whether to save Excel file
            db_if_exists: Database if_exists parameter
            column_mapping: Column name mapping for database
            
        Returns:
            Dict with success status for each output type
        """
        import os
        
        results = {
            'csv': False,
            'excel': False,
            'database': False
        }
        
        # Save to files
        if self.enable_files:
            if save_csv:
                try:
                    csv_path = os.path.join(self.output_dir, f'{base_name}.csv')
                    df.to_csv(csv_path, index=False)
                    self.logger.info(f"CSV saved: {csv_path}")
                    results['csv'] = True
                except Exception as e:
                    self.logger.error(f"Failed to save CSV: {e}")
            
            if save_excel:
                try:
                    excel_path = os.path.join(self.output_dir, f'{base_name}.xlsx')
                    df.to_excel(excel_path, index=False)
                    self.logger.info(f"Excel saved: {excel_path}")
                    results['excel'] = True
                except Exception as e:
                    self.logger.error(f"Failed to save Excel: {e}")
        
        # Save to database
        if self.enable_database and self.db_manager:
            if table_name is None:
                table_name = base_name.lower().replace(' ', '_')
            
            try:
                success = self.db_manager.push_dataframe(
                    df=df,
                    table_name=table_name,
                    if_exists=db_if_exists,
                    column_mapping=column_mapping
                )
                results['database'] = success
            except Exception as e:
                self.logger.error(f"Failed to save to database: {e}")
        
        return results
    
    def save_wrmm_outputs(self, master_data_file: pd.DataFrame,
                         outputs_for_powerbi: str,
                         start_week: int, end_week: int) -> Dict[str, bool]:
        """
        Save main WRMM outputs with proper column mapping.
        
        Args:
            master_data_file: Main WRMM output DataFrame
            outputs_for_powerbi: Base filename
            start_week: Start week
            end_week: End week
            
        Returns:
            Dict with success status for each output
        """
        # Column mapping to match your database schema
        column_mapping = {
            'Data_type': 'data_type',
            'ModelName': 'model_name',
            'ComponentType': 'component_type',
            'ComponentName': 'component_name',
            'ComponentNumber': 'component_number',
            'Year': 'year',
            'Interval': 'interval',
            'Date': 'date',
            'Value': 'value',
            'Unit': 'unit',
            'PerStorage': 'per_storage',
            'IO_Failed': 'io_failed',
            'WCO_Failed': 'wco_failed',
            'TotalIrrArea_Ha': 'total_irrigated_area_ha',
            'Comments': 'comments'
        }
        
        return self.save_output(
            df=master_data_file,
            base_name=outputs_for_powerbi,
            table_name='wrmmoutputs',
            save_csv=True,
            save_excel=True,
            db_if_exists='append',
            column_mapping=column_mapping
        )


# Example usage function
def example_integration():
    """
    Example of how to integrate into existing WRMM workflow.
    """
    # Database configuration
    db_config = {
        'host': 'C-GOA-APM-13251',
        'port': '5432',
        'database': 'Main',
        'user': 'postgres',
        'password': 'IEMP_POSTGRES',
        'schema': 'wrmm'
    }
    
    # Create output manager
    output_manager = WRMMOutputManager(
        output_dir='D:\Sopan\HGS_Data\Codes\WRMM\WRMM_Package\WRMM_SQL\WRMM_Package',
        db_config=db_config,
        enable_database=True,  # Set to False to disable database
        enable_files=True      # Set to False to disable file creation
    )
    
    # In your existing code, replace this:
    # master_data_file.to_csv(os.path.join(output_dir, outputs_for_powerbi + '.csv'), index=False)
    # master_data_file.to_excel(os.path.join(output_dir, outputs_for_powerbi + '.xlsx'), index=False)
    
    # With this:
    # results = output_manager.save_wrmm_outputs(
    #     master_data_file=master_data_file,
    #     outputs_for_powerbi=outputs_for_powerbi,
    #     start_week=start_week,
    #     end_week=end_week
    # )
    
    # Or for other outputs, use the generic save_output method:
    # output_manager.save_output(
    #     df=master_ex_summary,
    #     base_name='Executive_summary_table',
    #     table_name='executive_summary',
    #     save_excel=True,
    #     save_csv=False
    # )
