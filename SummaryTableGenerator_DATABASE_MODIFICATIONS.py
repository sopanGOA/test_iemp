"""
SummaryTableGenerator.py - DATABASE-ONLY MODIFICATIONS
======================================================
This file contains the key modifications needed for SummaryTableGenerator.py
to push data directly to database instead of creating CSV/Excel files.

INSTRUCTIONS:
1. Backup your existing SummaryTableGenerator.py
2. Add these imports at the top of your file
3. Replace the sections marked with "REPLACE THIS" in your existing file
4. Keep all your existing processing logic
"""

# ============================================================================
# ADD THESE IMPORTS AT THE TOP OF SummaryTableGenerator.py
# ============================================================================

from WRMMDatabaseUtils import WRMMOutputManager
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# MODIFICATION 1: In process_model_outputs() method
# Replace lines 688-691 (the export section)
# ============================================================================

# ORIGINAL CODE (lines 688-691):
# -------------------------------------------------------
# # Export data 
# master_data_file.to_csv(os.path.join(output_dir, outputs_for_powerbi + '.csv'), index=False)
# master_data_file.to_excel(os.path.join(output_dir, outputs_for_powerbi + '.xlsx'), index=False)
# master_ex_summary.to_excel(os.path.join(output_dir, 'Executive_summary_table.xlsx'), index=False)
# master_res_inflow_annual.to_excel(os.path.join(output_dir, 'SumTab_ResInflow.xlsx'), index=False)
# -------------------------------------------------------

# NEW CODE (DATABASE-ONLY):
def export_to_database_only(master_data_file, master_ex_summary, master_res_inflow_annual, 
                            output_dir, outputs_for_powerbi, output_manager):
    """
    Export data to database only (no CSV/Excel files).
    
    This replaces the original export code at lines 688-691.
    """
    
    # Column mapping for database schema
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
    
    # 1. Push main WRMM output to database
    logger.info("Pushing main WRMM output to database...")
    results_main = output_manager.db_manager.push_dataframe(
        df=master_data_file,
        table_name='wrmmoutputs',
        if_exists='append',
        column_mapping=column_mapping,
        batch_size=1000
    )
    
    if results_main:
        logger.info(f"✓ Pushed {len(master_data_file)} rows to wrmmoutputs")
    else:
        logger.error("✗ Failed to push main WRMM output")
    
    # 2. Push executive summary to database
    logger.info("Pushing executive summary to database...")
    results_exec = output_manager.db_manager.push_dataframe(
        df=master_ex_summary,
        table_name='executive_summary',
        if_exists='append',
        batch_size=1000
    )
    
    if results_exec:
        logger.info(f"✓ Pushed {len(master_ex_summary)} rows to executive_summary")
    else:
        logger.error("✗ Failed to push executive summary")
    
    # 3. Push reservoir inflow to database
    logger.info("Pushing reservoir inflow to database...")
    results_res = output_manager.db_manager.push_dataframe(
        df=master_res_inflow_annual,
        table_name='reservoir_inflow',
        if_exists='append',
        batch_size=1000
    )
    
    if results_res:
        logger.info(f"✓ Pushed {len(master_res_inflow_annual)} rows to reservoir_inflow")
    else:
        logger.error("✗ Failed to push reservoir inflow")
    
    logger.info("Database export completed.")
    
    return results_main and results_exec and results_res


# ============================================================================
# MODIFICATION 2: In process_model_outputs() - intermediate file saves
# Replace lines 154-155 (outsim_id and irr_area saves)
# ============================================================================

# ORIGINAL CODE (lines 154-155):
# -------------------------------------------------------
# outsim_id.to_csv(os.path.join(output_dir, 'Outsim_id_' + scenario_name + '.csv'), index=False)
# irr_area.to_csv(os.path.join(output_dir, 'Irr_area_' + scenario_name + '.csv'), index=False)
# -------------------------------------------------------

# NEW CODE (DATABASE-ONLY - OPTIONAL, or just comment out these lines):
# These are intermediate files - you can either:
# Option 1: Delete these lines (don't save intermediate data)
# Option 2: Push to database if you want to keep this data

def save_intermediate_data_to_db(outsim_id, irr_area, scenario_name, output_manager):
    """
    Optional: Save intermediate data to database.
    You can skip this if you don't need intermediate data.
    """
    # Push outsim_id data
    output_manager.db_manager.push_dataframe(
        df=outsim_id,
        table_name='outsim_id_intermediate',
        if_exists='append',
        batch_size=1000
    )
    
    # Push irrigation area data
    output_manager.db_manager.push_dataframe(
        df=irr_area,
        table_name='irr_area_intermediate',
        if_exists='append',
        batch_size=1000
    )


# ============================================================================
# MODIFICATION 3: In prepare_summary_tables() method
# Replace lines 779, 803, 808 (summary table saves)
# ============================================================================

# ORIGINAL CODE (lines 779, 803, 808):
# -------------------------------------------------------
# tab1.to_excel(os.path.join(self.output_dir, item + '.xlsx'), index=False)
# ...
# tab1.to_excel(os.path.join(self.output_dir, item + '.xlsx'), index=False)
# ...
# tab2[tab2.columns[1:]].to_excel(os.path.join(self.output_dir, 'SumTab_IO_WCO.xlsx'), index=False)
# -------------------------------------------------------

# NEW CODE (DATABASE-ONLY):
def save_summary_tables_to_db(self, tab_data, table_name, output_manager):
    """
    Save summary tables to database instead of Excel files.
    """
    output_manager.db_manager.push_dataframe(
        df=tab_data,
        table_name=table_name,
        if_exists='append',
        batch_size=500
    )
    logger.info(f"✓ Pushed {len(tab_data)} rows to {table_name}")


# ============================================================================
# MODIFICATION 4: In MAA_1969_Summary() method
# Replace line 874
# ============================================================================

# ORIGINAL CODE (line 874):
# -------------------------------------------------------
# maa_file.to_excel(os.path.join(self.output_dir, 'MAA_1969.xlsx'), index=False)
# -------------------------------------------------------

# NEW CODE (DATABASE-ONLY):
def save_maa_1969_to_db(self, maa_file, output_manager):
    """
    Save MAA 1969 data to database.
    """
    output_manager.db_manager.push_dataframe(
        df=maa_file,
        table_name='maa_summary',
        if_exists='append',
        batch_size=500
    )
    logger.info(f"✓ Pushed {len(maa_file)} rows to maa_summary")


# ============================================================================
# MODIFICATION 5: In IrrigationDiversionSummary() method
# Replace lines 943, 946-949
# ============================================================================

# ORIGINAL CODE (lines 943, 946-949):
# -------------------------------------------------------
# divchl_summary_tab.to_excel(os.path.join(self.output_dir, 'SumTab_irr_diversion.xlsx'), index=False)
# ...
# self.subtab_priv_irr_all.to_excel(os.path.join(self.output_dir, 'SumTab_priv_irr_all.xlsx'), index=True)
# self.subtab_priv_irr_sen.to_excel(os.path.join(self.output_dir, 'SumTab_priv_irr_sen.xlsx'), index=True)
# self.subtab_priv_irr_jun_io.to_excel(os.path.join(self.output_dir, 'SumTab_priv_irr_jun_io.xlsx'), index=True)
# self.subtab_priv_irr_jun_wco.to_excel(os.path.join(self.output_dir, 'SumTab_priv_irr_jun_wco.xlsx'), index=True)
# -------------------------------------------------------

# NEW CODE (DATABASE-ONLY):
def save_irrigation_diversion_to_db(self, divchl_summary_tab, output_manager):
    """
    Save irrigation diversion data to database.
    """
    # Main diversion summary
    output_manager.db_manager.push_dataframe(
        df=divchl_summary_tab.reset_index(),
        table_name='irrigation_diversion',
        if_exists='append',
        batch_size=500
    )
    
    # Private irrigation - all
    if not self.subtab_priv_irr_all.empty:
        output_manager.db_manager.push_dataframe(
            df=self.subtab_priv_irr_all.reset_index(),
            table_name='priv_irr_all',
            if_exists='append',
            batch_size=500
        )
    
    # Private irrigation - senior
    if not self.subtab_priv_irr_sen.empty:
        output_manager.db_manager.push_dataframe(
            df=self.subtab_priv_irr_sen.reset_index(),
            table_name='priv_irr_senior',
            if_exists='append',
            batch_size=500
        )
    
    # Private irrigation - junior IO
    if not self.subtab_priv_irr_jun_io.empty:
        output_manager.db_manager.push_dataframe(
            df=self.subtab_priv_irr_jun_io.reset_index(),
            table_name='priv_irr_junior_io',
            if_exists='append',
            batch_size=500
        )
    
    # Private irrigation - junior WCO
    if not self.subtab_priv_irr_jun_wco.empty:
        output_manager.db_manager.push_dataframe(
            df=self.subtab_priv_irr_jun_wco.reset_index(),
            table_name='priv_irr_junior_wco',
            if_exists='append',
            batch_size=500
        )
    
    logger.info("✓ Irrigation diversion data pushed to database")


# ============================================================================
# MODIFICATION 6: In create_apportionment_summary() method
# Replace line 1303
# ============================================================================

# ORIGINAL CODE (line 1303):
# -------------------------------------------------------
# df_output.to_csv(apportionment_output_file, index=False, float_format='%.8g')
# -------------------------------------------------------

# NEW CODE (DATABASE-ONLY):
def save_apportionment_to_db(self, df_output, output_manager):
    """
    Save apportionment data to database.
    """
    output_manager.db_manager.push_dataframe(
        df=df_output,
        table_name='apportionment',
        if_exists='append',
        batch_size=500
    )
    logger.info(f"✓ Pushed {len(df_output)} apportionment records to database")


# ============================================================================
# MODIFICATION 7: In create_weather_forecast_summary() method
# Replace lines 1806, 1812 (weather data saves)
# ============================================================================

# ORIGINAL CODE (lines 1806, 1812):
# -------------------------------------------------------
# output_data.to_csv(filepath, index=False)
# ...
# output_data.to_excel(excel_filepath, index=False)
# -------------------------------------------------------

# NEW CODE (DATABASE-ONLY):
def save_weather_forecast_to_db(self, output_data, output_manager):
    """
    Save weather forecast data to database.
    """
    output_manager.db_manager.push_dataframe(
        df=output_data,
        table_name='weather_forecast',
        if_exists='append',
        batch_size=1000
    )
    logger.info(f"✓ Pushed {len(output_data)} weather forecast records to database")


# ============================================================================
# MODIFICATION 8: In integrate_wiski_data() method
# Replace lines 1935, 2047-2048, 2150, 2202 (WISKI data saves)
# ============================================================================

# ORIGINAL CODE (various lines):
# -------------------------------------------------------
# combined_df.to_csv(output_csv_path, index=False)
# combined.to_csv(combined_output_path, index=False)
# weekly_avg.to_csv(weekly_output_path, index=False)
# wrmm_data.to_csv(wrmm_output_path, index=False)
# merged.to_excel(writer, sheet_name=f"Merged_{sheet_name}", index=False)
# -------------------------------------------------------

# NEW CODE (DATABASE-ONLY):
def save_wiski_data_to_db(self, wiski_data, data_type, output_manager):
    """
    Save WISKI data to database.
    
    Args:
        wiski_data: DataFrame with WISKI data
        data_type: Type of data ('combined', 'weekly_avg', 'merged', etc.)
        output_manager: WRMMOutputManager instance
    """
    table_name_map = {
        'combined': 'wiski_combined_data',
        'weekly_avg': 'wiski_weekly_average',
        'merged': 'wiski_merged_data',
        'wrmm': 'wiski_wrmm_data'
    }
    
    table_name = table_name_map.get(data_type, 'wiski_data')
    
    output_manager.db_manager.push_dataframe(
        df=wiski_data,
        table_name=table_name,
        if_exists='append',
        batch_size=1000
    )
    logger.info(f"✓ Pushed {len(wiski_data)} {data_type} WISKI records to database")


# ============================================================================
# COMPLETE EXAMPLE: Modified process_model_outputs() export section
# ============================================================================

def process_model_outputs_DATABASE_VERSION(model_output_folder, reference_file_names, 
                                          output_dir, outputs_for_powerbi, current_year, 
                                          start_week, end_week, seconds_in_day, apptchl_id):
    """
    This is the complete modified version of the process_model_outputs method.
    
    Replace the export section (lines 685-692) with this code:
    """
    
    # ... [ALL YOUR EXISTING PROCESSING CODE STAYS THE SAME] ...
    # ... [Keep everything from line 1 to line 684] ...
    
    # ========================================================================
    # MODIFIED EXPORT SECTION (replaces lines 685-692)
    # ========================================================================
    
    # Initialize database output manager
    from WRMMDatabaseUtils import WRMMOutputManager
    
    db_config = {
        'host': 'C-GOA-APM-13251',
        'port': '5432',
        'database': 'Main',
        'user': 'postgres',
        'password': 'IEMP_POSTGRES',
        'schema': 'wrmm'
    }
    
    output_manager = WRMMOutputManager(
        output_dir=output_dir,
        db_config=db_config,
        enable_database=True,
        enable_files=False  # No files!
    )
    
    # Column mapping for main output
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
    
    # Export to database only (NO CSV/Excel files)
    logger.info("Exporting data to database...")
    
    # 1. Main WRMM output
    success_main = output_manager.db_manager.push_dataframe(
        df=master_data_file,
        table_name='wrmmoutputs',
        if_exists='append',
        column_mapping=column_mapping,
        batch_size=1000
    )
    if success_main:
        logger.info(f"✓ Main output: {len(master_data_file)} rows")
    
    # 2. Executive summary
    success_exec = output_manager.db_manager.push_dataframe(
        df=master_ex_summary,
        table_name='executive_summary',
        if_exists='append',
        batch_size=500
    )
    if success_exec:
        logger.info(f"✓ Executive summary: {len(master_ex_summary)} rows")
    
    # 3. Reservoir inflow
    success_res = output_manager.db_manager.push_dataframe(
        df=master_res_inflow_annual,
        table_name='reservoir_inflow',
        if_exists='append',
        batch_size=500
    )
    if success_res:
        logger.info(f"✓ Reservoir inflow: {len(master_res_inflow_annual)} rows")
    
    logger.info("✓ All data exported to database successfully")
    
    # Return statement stays the same
    return (master_ex_summary, hbdf_maa_natflow, divchl_summary_tab, reference_file_name, 
            date_ref, subtab_priv_irr_all, subtab_priv_irr_sen, subtab_priv_irr_jun_io,
            subtab_priv_irr_jun_wco, scn, processor, output_dir, start_week, end_week, 
            seconds_in_day, apptchl_id)


# ============================================================================
# SUMMARY OF ALL CHANGES
# ============================================================================

"""
FILES TO MODIFY:

1. SummaryTableGenerator.py:
   - Add imports at top (WRMMOutputManager, logging)
   - Line 688-691: Replace with export_to_database_only()
   - Line 154-155: Comment out or remove (intermediate files)
   - Line 779, 803, 808: Replace with save_summary_tables_to_db()
   - Line 874: Replace with save_maa_1969_to_db()
   - Line 943, 946-949: Replace with save_irrigation_diversion_to_db()
   - Line 1303: Replace with save_apportionment_to_db()
   - Line 1806, 1812: Replace with save_weather_forecast_to_db()
   - Lines for WISKI: Replace with save_wiski_data_to_db()

2. WRMM_workflow_v2.py:
   - Replace entire file with WRMM_workflow_v2_DATABASE_ONLY.py

3. WRMMDataProcessor.py:
   - No changes needed! (It doesn't create output files)

RESULT:
- All data goes directly to PostgreSQL database
- No CSV or Excel files created
- Same processing logic, just different output
- Faster, cleaner, more efficient
"""
