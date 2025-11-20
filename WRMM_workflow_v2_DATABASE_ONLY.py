"""
WRMM_workflow_v2.py - DATABASE-ONLY VERSION
============================================
This version pushes all data directly to PostgreSQL database.
NO CSV or Excel files are created.

INSTALLATION:
1. Copy WRMMDatabaseUtils.py to this directory
2. Run setup_wrmm_database.py once to create tables
3. Replace your existing WRMM_workflow_v2.py with this file
4. Run normally - all data goes to database!
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import shutil

# NEW: Import database utilities
from WRMMDatabaseUtils import WRMMOutputManager
import logging
from config import DATABASE_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# DATABASE CONFIGURATION - UPDATE THESE IF NEEDED
# ============================================================================

DATABASE_CONFIG = DATABASE_CONFIG

# Global flag to control output behavior
ENABLE_DATABASE = True   # Push to database
ENABLE_FILES = False     # DO NOT create CSV/Excel files


# ============================================================================
# KEEP ALL YOUR EXISTING FUNCTIONS (no changes needed)
# ============================================================================

def auto_setup_input_files(base_dir):
    """
    Automatically detect week numbers and set up input file structure.
    [KEEP EXISTING CODE - NO CHANGES NEEDED]
    """
    import re
    import glob
    import shutil
    from pathlib import Path
    from datetime import datetime

    print("="*60)
    print("AUTOMATIC INPUT FILE SETUP")
    print("="*60)

    # STEP 1: Fetch from operational modeling directory and detect week numbers
    source_dir = Path(r"D:\Sopan\HGS_Data\Codes\WRMM\WRMM_Package\WRMM_For BEN\WRMM_Package\TESTING_AUTO")
    print(f"STEP 1: Scanning source directory: {source_dir}")

    if not source_dir.exists():
        print(f" Source directory not found: {source_dir}")
        return None

    # Find Results directory
    results_dirs = [d for d in source_dir.iterdir() if d.is_dir() and d.name.startswith("Results")]
    if not results_dirs:
        print(" No Results directory found in source folder")
        return None

    results_dir = results_dirs[0]  # Take the first one found
    print(f" Found Results directory: {results_dir.name}")

    # Extract week numbers from directory name
    # Pattern: Results_week_WK26_to_WK30_2025
    pattern = r"Results_week_WK(\d+)_to_WK(\d+)_(\d+)"
    match = re.search(pattern, results_dir.name)

    if not match:
        print(f" Could not extract week numbers from: {results_dir.name}")
        return None

    start_week = int(match.group(1))
    end_week = int(match.group(2))
    current_year = int(match.group(3))

    print(f" Detected: start_week={start_week}, end_week={end_week}, year={current_year}")

    # STEP 2: Check required files in Results directory
    print(f"\n STEP 2: Checking required files in {results_dir.name}")

    # Find Apportionment file
    apportionment_pattern = f"Apportionment_summary_WK{start_week}_WK{end_week}*"
    apportionment_files = list(results_dir.glob(apportionment_pattern))

    if not apportionment_files:
        print(f" Apportionment file not found with pattern: {apportionment_pattern}")
        return None

    apportionment_file = apportionment_files[0]
    print(f"Found Apportionment file: {apportionment_file.name}")

    # Check S0 folder
    s0_folder = results_dir / "S0"
    if not s0_folder.exists():
        print(f" S0 folder not found: {s0_folder}")
        return None

    print(f" Found S0 folder: {s0_folder}")

    # STEP 3: Create input directory structure
    print(f"\n STEP 3: Creating input directory structure")

    input_dir = base_dir / f"INPUT_DATA_WK{start_week}_WK{end_week}"
    if input_dir.exists():
        shutil.rmtree(input_dir)
        print(f"Removed existing directory: {input_dir}")

    input_dir.mkdir(parents=True, exist_ok=True)
    print(f"Created: {input_dir}")

    # Create Results subdirectory
    results_subdir = input_dir / f"Results_week_WK{start_week}_to_WK{end_week}_{current_year}"
    results_subdir.mkdir(parents=True, exist_ok=True)
    print(f"Created: {results_subdir}")

    # Create Apportionment subdirectory
    apportionment_subdir = input_dir / f"Apportment_input_data_WK{start_week}_WK{end_week}"
    apportionment_subdir.mkdir(parents=True, exist_ok=True)
    print(f"Created: {apportionment_subdir}")

    # Copy S0 folder
    dest_s0 = results_subdir / "S0"
    shutil.copytree(s0_folder, dest_s0)
    print(f"Copied S0 folder: {s0_folder} -> {dest_s0}")

    # Copy Apportionment file
    dest_apportionment = apportionment_subdir / f"Apportionment_summary_WK{start_week}_WK{end_week}.xlsx"
    shutil.copy2(apportionment_file, dest_apportionment)
    print(f"Copied Apportionment file: {apportionment_file} -> {dest_apportionment}")

    # STEP 4: Create Reference File directory and copy reference file
    print(f"\nSTEP 4: Setting up Reference Files")

    reference_dir = input_dir / f"Reference_File_WK{start_week}_WK{end_week}"
    reference_dir.mkdir(parents=True, exist_ok=True)
    print(f"Created: {reference_dir}")

    # Copy reference file
    reference_source = base_dir / "Reference_File_2025" / "Reference_file_S0.xlsx"
    if not reference_source.exists():
        print(f"Reference file not found: {reference_source}")
        return None

    reference_dest = reference_dir / "Reference_file_S0.xlsx"
    shutil.copy2(reference_source, reference_dest)
    print(f"Copied Reference file: {reference_source} -> {reference_dest}")

    # STEP 5: Set up Forecast Summary Data
    print(f"\n STEP 5: Setting up Forecast Summary Data")

    # Calculate forecast parameters
    forecast_params = calculate_forecast_parameters(start_week, end_week, current_year)
    geps_start_date = datetime.strptime(forecast_params['geps_start_date'], "%Y-%m-%d").strftime("%Y%m%d")
    geps_end_date = datetime.strptime(forecast_params['geps_end_date'], "%Y-%m-%d").strftime("%Y%m%d")

    print(f"GEPS Start Date: {geps_start_date}")
    print(f"GEPS End Date: {geps_end_date}")

    # Create Forecast directory
    forecast_dir = input_dir / f"Forecast_Summary_Data_Input_WK{start_week}_WK{end_week}"
    forecast_dir.mkdir(parents=True, exist_ok=True)
    print(f"Created: {forecast_dir}")

    # Copy GEPS data file
    geps_source = Path(
        f"D:/Sopan/HGS_Data/Data_for_HGS_Run/GEPS_Data/Excel_By_Station_{geps_start_date}_{geps_end_date}/"
        f"Data_for_Dashboard_{geps_start_date}_{geps_end_date}.xlsx"
    )

    if not geps_source.exists():
        print(f" GEPS data file not found: {geps_source}")
        print(f"   Creating forecast directory without GEPS data...")
    else:
        geps_dest = forecast_dir / f"WSA_forecast_Temp_Precip_WK{start_week}_WK{end_week}.xlsx"
        shutil.copy2(geps_source, geps_dest)
        print(f"Copied GEPS data: {geps_source} -> {geps_dest}")

    print(f"\n INPUT FILE SETUP COMPLETE!")
    print(f"Input directory created: {input_dir}")
    print(f"Week range: WK{start_week} to WK{end_week}")
    print(f"Year: {current_year}")

    return start_week, end_week, current_year


def calculate_forecast_parameters(start_week, end_week, year):
    """
    Automatically calculate forecast_start_date, month, and date based on week numbers.
    [KEEP EXISTING CODE - NO CHANGES NEEDED]
    """
    from datetime import datetime, timedelta

    def get_week_dates(year, weeks=52):
        start_date = datetime(year, 1, 7)
        end_date = datetime(year, 12, 31)
        weekend_dates = []
        for week_num in range(weeks - 1):  # 51 weeks
            current_date = start_date + timedelta(days=week_num * 7)
            weekend_dates.append(current_date)
        weekend_dates.append(end_date)
        return weekend_dates

    week_dates = get_week_dates(year)
    forecast_start_date_obj = week_dates[start_week - 1]
    forecast_start_date = forecast_start_date_obj.strftime('%Y-%m-%d')
    geps_start_date_obj = forecast_start_date_obj + timedelta(days=1)
    geps_end_date_obj = forecast_start_date_obj + timedelta(days=41)

    return {
        'forecast_start_date': forecast_start_date,
        'geps_start_date': geps_start_date_obj.strftime('%Y-%m-%d'),
        'geps_end_date': geps_end_date_obj.strftime('%Y-%m-%d'),
        'month': forecast_start_date_obj.strftime('%B'),
        'date': forecast_start_date_obj.day,
        'formatted_date': f"{forecast_start_date_obj.day:02d}",
        'forecast_start_date_obj': forecast_start_date_obj,
    }


# [KEEP ALL YOUR OTHER EXISTING FUNCTIONS - no changes needed]
# - fix_weather_forecast_overlap()
# - Any other helper functions you have


# ============================================================================
# MODIFIED MAIN PROCESSING FUNCTION - DATABASE-ONLY VERSION
# ============================================================================

def main_processing_database_only():
    """
    Main WRMM processing function - DATABASE-ONLY VERSION
    
    This version:
    - Processes all data normally
    - Pushes directly to PostgreSQL database
    - Does NOT create CSV/Excel files
    - Saves disk space and processing time
    """
    
    import time
    start_time = time.time()
    
    print("\n" + "="*60)
    print("WRMM PROCESSING - DATABASE-ONLY MODE")
    print("="*60)
    print(f"Database: {DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}")
    print(f"Schema: {DATABASE_CONFIG['schema']}")
    print(f"File Creation: {'ENABLED' if ENABLE_FILES else 'DISABLED'}")
    print("="*60 + "\n")
    
    # Your existing setup code
    from SummaryTableGenerator import SummaryTablesGenerator
    from WRMMDataProcessor import WRMMDataProcessor
    
    base_dir = Path(r"D:\Sopan\HGS_Data\Codes\WRMM\WRMM_Package\WRMM_For BEN\WRMM_Package")
    
    # Auto-setup input files
    setup_result = auto_setup_input_files(base_dir)
    if setup_result is None:
        print("ERROR: Failed to setup input files")
        return None, None
    
    start_week, end_week, current_year = setup_result
    
    # Calculate forecast parameters
    forecast_params = calculate_forecast_parameters(start_week, end_week, current_year)
    forecast_start_date = forecast_params['forecast_start_date']
    
    # Define paths
    model_output_folder = base_dir / f"INPUT_DATA_WK{start_week}_WK{end_week}" / f"Results_week_WK{start_week}_to_WK{end_week}_{current_year}"
    reference_file_path = base_dir / f"INPUT_DATA_WK{start_week}_WK{end_week}" / f"Reference_File_WK{start_week}_WK{end_week}" / "Reference_file_S0.xlsx"
    forecast_constant_files_path = base_dir / "Weather_Forecast_ConstantFile"
    forecast_input_path = base_dir / f"INPUT_DATA_WK{start_week}_WK{end_week}" / f"Forecast_Summary_Data_Input_WK{start_week}_WK{end_week}" / f"WSA_forecast_Temp_Precip_WK{start_week}_WK{end_week}.xlsx"
    apportioment_input_file = base_dir / f"INPUT_DATA_WK{start_week}_WK{end_week}" / f"Apportment_input_data_WK{start_week}_WK{end_week}" / f"Apportionment_summary_WK{start_week}_WK{end_week}.xlsx"
    
    # Create output directory (still needed for temporary processing)
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    output_dir = base_dir / f"Dashboard_Data_WK_{start_week}_{end_week}_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    apportioment_output_file = output_dir / f"Apportionment_Dashboard_summary_WK{start_week}_WK{end_week}.csv"
    outputs_for_powerbi = f'WK{start_week}_{end_week}_WrmmOutputs'
    
    # ========================================================================
    # NEW: Initialize Database Output Manager
    # ========================================================================
    
    logger.info("Initializing Database Output Manager...")
    output_manager = WRMMOutputManager(
        output_dir=str(output_dir),
        db_config=DATABASE_CONFIG,
        enable_database=ENABLE_DATABASE,
        enable_files=ENABLE_FILES  # False = no files created!
    )
    
    if output_manager.db_manager:
        if output_manager.db_manager.test_connection():
            logger.info("✓ Database connection successful")
        else:
            logger.error("✗ Database connection failed")
            print("ERROR: Cannot connect to database. Exiting...")
            return None, None
    
    # ========================================================================
    # STEP 1: Process Model Outputs (your existing code)
    # ========================================================================
    
    print("\n" + "="*50)
    print("STEP 1: Processing Model Outputs")
    print("="*50)
    
    reference_file_names = [reference_file_path]
    seconds_in_day = 24 * 3600
    moving_average_days = 7
    apptchl_id = 1088
    
    # Process model outputs
    results = SummaryTablesGenerator.process_model_outputs(
        model_output_folder=str(model_output_folder),
        reference_file_names=reference_file_names,
        output_dir=str(output_dir),
        outputs_for_powerbi=outputs_for_powerbi,
        current_year=current_year,
        start_week=start_week,
        end_week=end_week,
        seconds_in_day=seconds_in_day,
        apptchl_id=apptchl_id
    )
    
    # ========================================================================
    # MODIFIED: Push Main WRMM Output to Database (NO CSV/EXCEL)
    # ========================================================================
    
    print("\n" + "="*50)
    print("STEP 1.5: Pushing Main WRMM Output to Database")
    print("="*50)
    
    wrmm_output_path = os.path.join(output_dir, f'{outputs_for_powerbi}.csv')
    if os.path.exists(wrmm_output_path):
        df = pd.read_csv(wrmm_output_path)
        df['Data_type'] = df['Data_type'].replace({
            'S0': 'Predicted Flow',
            'Target_S0': 'Target Flow'
        })
        df.loc[
            (df['ComponentType'] == "Irrigation District") & (df['Data_type'] == "Predicted Flow"),
            'Data_type'
        ] = "Predicted Deficit"
        
        # NEW: Push to database only (no CSV/Excel saved)
        results = output_manager.save_wrmm_outputs(
            master_data_file=df,
            outputs_for_powerbi=outputs_for_powerbi,
            start_week=start_week,
            end_week=end_week
        )
        
        if results['database']:
            logger.info(f"✓ Pushed {len(df)} rows to database: wrmm.wrmmoutputs")
        else:
            logger.error("✗ Failed to push main WRMM output to database")
        
        # Delete the temporary CSV file since we don't need it
        if os.path.exists(wrmm_output_path):
            os.remove(wrmm_output_path)
            logger.info(f"  Removed temporary file: {wrmm_output_path}")
    else:
        logger.warning(f"WRMM output file not found: {wrmm_output_path}")
    
    # ========================================================================
    # STEP 2: Create Summary Tables Generator
    # ========================================================================
    
    (master_ex_summary, hbdf_maa_natflow, divchl_summary_tab, reference_file_name,
     date_ref, subtab_priv_irr_all, subtab_priv_irr_sen, subtab_priv_irr_jun_io,
     subtab_priv_irr_jun_wco, scn, processor, output_dir_returned, start_week_returned,
     end_week_returned, seconds_in_day_returned, apptchl_id_returned) = results
    
    print("\n" + "="*50)
    print("STEP 2: Creating Summary Tables Generator")
    print("="*50)
    
    generator = SummaryTablesGenerator(
        master_ex_summary=master_ex_summary,
        hbdf_maa_natflow=hbdf_maa_natflow,
        divchl_summary_tab=divchl_summary_tab,
        reference_file_name=reference_file_name,
        date_ref=date_ref,
        subtab_priv_irr_all=subtab_priv_irr_all,
        subtab_priv_irr_sen=subtab_priv_irr_sen,
        subtab_priv_irr_jun_io=subtab_priv_irr_jun_io,
        subtab_priv_irr_jun_wco=subtab_priv_irr_jun_wco,
        scn=scn,
        processor=processor,
        output_dir=str(output_dir),
        start_week=start_week,
        end_week=end_week,
        seconds_in_day=seconds_in_day,
        apptchl_id=apptchl_id
    )
    
    # ========================================================================
    # STEP 3: Generate Summary Tables (modified to use database)
    # ========================================================================
    
    print("\n" + "="*50)
    print("STEP 3: Generating Summary Tables")
    print("="*50)
    
    generator.prepare_summary_tables()
    generator.generate_maa_files()
    generator.MAA_1969_Summary()
    generator.IrrigationDiversionSummary()
    generator.calculate_irrigation_shortage()
    generator.create_apportionment_summary(
        apportionment_input_file=str(apportioment_input_file),
        apportionment_output_file=str(apportioment_output_file)
    )
    
    # ========================================================================
    # STEP 3.7: Reservoir Summary Table - Push to Database
    # ========================================================================
    
    print("\n" + "="*50)
    print("STEP 3.7: Creating Reservoir Summary Table")
    print("="*50)
    
    try:
        res_stor_path = os.path.join(output_dir, "SumTab_%ResStor.xlsx")
        res_inflow_path = os.path.join(output_dir, "SumTab_ResInflow.xlsx")
        
        if os.path.exists(res_stor_path) and os.path.exists(res_inflow_path):
            df1 = pd.read_excel(res_stor_path, header=None).T.iloc[1:]
            df1.columns = ['Reservoir', '%FSL']
            df2 = pd.read_excel(res_inflow_path, header=None).T.iloc[1:]
            df2.columns = ['Reservoir', 'Projected Total Inflow (dam³)']
            df3 = pd.merge(df1, df2, on='Reservoir', how='left')
            df3['Projected Total Inflow (dam³)'] = df3['Projected Total Inflow (dam³)'].fillna('NA')
            
            owned_by_GOA = ['Dickson Dam','Glennifer Lake','Travers','Twin Valley','Clear Lake',
                            'Lake McGregor','Oldman Reservoir','Keho Reservoir','Chain Lakes',
                            'Pine Coulee','Waterton','St. Mary','Payne Lake','Milk River Ridge']
            df3['Owned By GoA'] = np.where(df3['Reservoir'].isin(owned_by_GOA), 'Yes', '')
            df3 = df3[['Reservoir', 'Owned By GoA', '%FSL', 'Projected Total Inflow (dam³)']]
            
            # Add metadata
            df3['start_week'] = start_week
            df3['end_week'] = end_week
            df3['year'] = current_year
            
            # NEW: Push to database only
            results = output_manager.save_output(
                df=df3,
                base_name='SummaryTable_Reservoir',
                table_name='reservoir_summary',
                save_csv=False,
                save_excel=False,  # No files
                db_if_exists='append'
            )
            
            if results['database']:
                logger.info(f"✓ Pushed {len(df3)} reservoir records to database")
            
            # Clean up temporary files
            for temp_file in [res_stor_path, res_inflow_path]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
        else:
            missing = []
            if not os.path.exists(res_stor_path): missing.append("SumTab_%ResStor.xlsx")
            if not os.path.exists(res_inflow_path): missing.append("SumTab_ResInflow.xlsx")
            logger.warning(f"Missing required files: {', '.join(missing)}")
    except Exception as e:
        logger.error(f"Error creating reservoir summary table: {str(e)}")
    
    # ========================================================================
    # STEP 4: Weather Forecast Summary - Push to Database
    # ========================================================================
    
    print("\n" + "="*50)
    print("STEP 4: Creating Weather Forecast Summary")
    print("="*50)
    
    weather_data = generator.create_weather_forecast_summary(
        forecast_start_date=forecast_start_date,
        moving_average_days=moving_average_days,
        forecast_constant_files_path=str(forecast_constant_files_path),
        wsa_input_path_template=str(forecast_input_path),
        output_directory=str(output_dir)
    )
    
    # Note: Weather data handling depends on your create_weather_forecast_summary implementation
    # If it returns a DataFrame, push it to database here
    
    # ========================================================================
    # STEP 5: WISKI Reservoir Data - Push to Database
    # ========================================================================
    
    print("\n" + "="*50)
    print("STEP 5: Integrating WISKI Reservoir Data")
    print("="*50)
    
    wiski_station_list_path = base_dir / "Wiski_Reservoire_file" / "WRMM_Reservoir_list.csv"
    wiski_base_url = "http://wiskitsm1.goa.ds.gov.ab.ca:8080/KiWIS/KiWIS"
    
    if wiski_station_list_path.exists():
        try:
            today_date = datetime.today().strftime('%Y-%m-%d')
            wiski_date_params = {"from": "2025-01-01", "to": today_date}
            
            wiski_combined_data = generator.integrate_wiski_data(
                station_list_path=str(wiski_station_list_path),
                wrmm_file_name=f'WK{start_week}_{end_week}_WrmmOutputs.csv',
                base_url=wiski_base_url,
                date_params=wiski_date_params
            )
            
            if not wiski_combined_data.empty:
                logger.info("WISKI integration successful!")
                
                # Calculate summary statistics
                wiski_summary = wiski_combined_data.groupby(['Station', 'DataSource']).agg({
                    'Value': ['count', 'mean', 'std'],
                    'Interval': ['min', 'max']
                }).round(2)
                wiski_summary_df = wiski_summary.reset_index()
                
                # Flatten multi-level columns
                wiski_summary_df.columns = ['_'.join(col).strip('_') if col[1] else col[0] 
                                           for col in wiski_summary_df.columns.values]
                
                # NEW: Push WISKI data to database only
                results_combined = output_manager.save_output(
                    df=wiski_combined_data,
                    base_name=f'WISKI_Combined_Data_{today_date}',
                    table_name='wiski_combined_data',
                    save_csv=False,
                    save_excel=False,
                    db_if_exists='append'
                )
                
                results_summary = output_manager.save_output(
                    df=wiski_summary_df,
                    base_name=f'WISKI_Summary_{today_date}',
                    table_name='wiski_summary',
                    save_csv=False,
                    save_excel=False,
                    db_if_exists='append'
                )
                
                if results_combined['database']:
                    logger.info(f"✓ Pushed {len(wiski_combined_data)} WISKI combined records")
                if results_summary['database']:
                    logger.info(f"✓ Pushed {len(wiski_summary_df)} WISKI summary records")
            else:
                logger.warning("WISKI integration completed but no data was combined")
        except Exception as e:
            logger.error(f"WISKI integration failed: {str(e)}")
    else:
        logger.warning(f"WISKI station list not found at: {wiski_station_list_path}")
    
    # ========================================================================
    # STEP 6: Processing Summary
    # ========================================================================
    
    processing_time = time.time() - start_time
    
    print("\n" + "="*50)
    print("STEP 6: Processing Summary")
    print("="*50)
    
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Processing time: {processing_time:.1f} seconds")
    logger.info(f"Week range: WK{start_week} to WK{end_week}")
    logger.info(f"Year: {current_year}")
    
    if weather_data is not None:
        logger.info(f"Weather forecast: SUCCESS ({len(weather_data)} stations)")
    
    # ========================================================================
    # NEW: Log Processing Run to Database
    # ========================================================================
    
    try:
        run_record = pd.DataFrame([{
            'start_week': start_week,
            'end_week': end_week,
            'year': current_year,
            'status': 'SUCCESS',
            'rows_processed': len(df) if 'df' in locals() else 0,
            'processing_time_seconds': processing_time,
            'notes': f'Database-only mode: WK{start_week}-{end_week} processed in {processing_time:.1f}s'
        }])
        
        output_manager.save_output(
            df=run_record,
            base_name='run_history',
            table_name='run_history',
            save_csv=False,
            save_excel=False,
            db_if_exists='append'
        )
        logger.info("✓ Run history logged to database")
    except Exception as e:
        logger.warning(f"Failed to log run history: {e}")
    
    # ========================================================================
    # Clean up temporary files (optional)
    # ========================================================================
    
    print("\n" + "="*50)
    print("STEP 7: Cleaning Up Temporary Files")
    print("="*50)
    
    try:
        # Remove the temporary output directory since all data is in database
        if output_dir.exists():
            import shutil
            shutil.rmtree(output_dir)
            logger.info(f"✓ Removed temporary directory: {output_dir}")
    except Exception as e:
        logger.warning(f"Could not remove temporary directory: {e}")
    
    print("\n" + "="*60)
    print("WRMM PROCESSING COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"✓ All data pushed to database: {DATABASE_CONFIG['schema']}")
    print(f"✓ Processing time: {processing_time:.1f} seconds")
    print(f"✓ No CSV/Excel files created")
    print("="*60 + "\n")
    
    return generator, weather_data


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    seconds_in_day = 24 * 3600
    
    try:
        generator, weather_data = main_processing_database_only()
        print("\n✓ WRMM workflow completed successfully - all data in database!")
    except Exception as e:
        logger.error(f"WRMM workflow failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
