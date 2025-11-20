def auto_setup_input_files(base_dir):
    """
    Automatically detect week numbers and set up input file structure.

    Parameters:
    base_dir (Path): Base directory path

    Returns:
    tuple: (start_week, end_week, current_year) or None if setup fails
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
        'geps_start_date_obj': geps_start_date_obj,
        'geps_end_date_obj': geps_end_date_obj
    }


def fix_weather_forecast_overlap(output_dir, start_week, end_week):
    """
    Fix overlap in weather forecast data and convert to XLSX.
    """
    import pandas as pd
    import numpy as np
    from pathlib import Path

    print(f"\nFixing weather forecast overlap and converting to CSV...")

    base_dir_wsa = Path(r"D:\Sopan\HGS_Data\Codes\WRMM\WRMM_Package\WRMM_For BEN\WRMM_Package")
    forecast_input_dir = base_dir_wsa / f"INPUT_DATA_WK{start_week}_WK{end_week}" / f"Forecast_Summary_Data_Input_WK{start_week}_WK{end_week}"
    dashboard_files = list(forecast_input_dir.glob("WSA_forecast_Temp_Precip_*.xlsx"))

    if not dashboard_files:
        print(f"   - WSA_forecast_Temp_Precip file not found in: {forecast_input_dir}")
        return None

    dashboard_file = dashboard_files[0]
    print(f"   - Found file: {dashboard_file.name}")

    try:
        df = pd.read_excel(dashboard_file)
        print(f"   - Original data shape: {df.shape}")
        if 'Date' not in df.columns:
            print("   - Error: No 'Date' column found")
            return None
        df['Date'] = pd.to_datetime(df['Date'])
        processed_stations = []
        overlap_removed_count = 0

        for station in df['Station'].unique():
            station_data = df[df['Station'] == station].copy()
            historical_cols = [c for c in station_data.columns if c.startswith('Historical_')]
            forecast_cols = [c for c in station_data.columns
                             if not c.startswith('Historical_') and c not in ['Date', 'Station']
                             and any(s in c.lower() for s in ['tmax', 'tmin', 'precip', 'temp'])]

            if historical_cols and forecast_cols:
                historical_mask = station_data[historical_cols].notna().any(axis=1)
                if historical_mask.any():
                    last_historical_date = station_data.loc[historical_mask, 'Date'].max()
                    forecast_mask = station_data[forecast_cols].notna().any(axis=1)
                    if forecast_mask.any():
                        first_forecast_date = station_data.loc[forecast_mask, 'Date'].min()
                        if last_historical_date == first_forecast_date:
                            overlap_mask = (station_data['Date'] == last_historical_date)
                            for col in historical_cols:
                                station_data.loc[overlap_mask, col] = np.nan
                            overlap_removed_count += overlap_mask.sum()

            processed_stations.append(station_data)

        final_df = pd.concat(processed_stations, ignore_index=True)
        print(f"   - Total overlap records removed: {overlap_removed_count}")
        print(f"   - Final data shape: {final_df.shape}")

        xlsx_name = f"WSA_forecast_Temp_Precip_WK{start_week}_WK{end_week}.xlsx"
        xlsx_path = output_dir / xlsx_name
        with pd.ExcelWriter(xlsx_path, engine='openpyxl') as writer:
            final_df.to_excel(writer, sheet_name='WSA_forecast_Temp_Precip', index=False)

        print(f"   - xlsx saved: {xlsx_name}")
        return str(xlsx_path)

    except Exception as e:
        print(f"   - Error processing file: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


# -----------------------------
# Imports & setup
# -----------------------------
import pandas as pd
import os
import shutil
from datetime import datetime, timedelta
import numpy as np
import warnings
from pathlib import Path
import sys
warnings.filterwarnings('ignore')

# Import your custom modules
from WRMMDataProcessor import WRMMDataProcessor
from SummaryTableGenerator import SummaryTablesGenerator
from multistation_builder import build_multistation_file   # <-- NEW

print("="*60)
print("STARTING AUTOMATIC WRMM PROCESSING")
print("="*60)

# Define Base Path
base_dir = Path(r'D:/Sopan/HGS_Data/Codes/WRMM/WRMM_Package/WRMM_For BEN/WRMM_Package')

# Setup Working Directory and System Path
os.chdir(base_dir)
sys.path.append(str(base_dir))

# ===== STEP 0: AUTOMATIC INPUT FILE DETECTION AND SETUP =====
print("\n" + "="*50)
print("STEP 0: Automatic Input File Detection and Setup")
print("="*50)

setup_result = auto_setup_input_files(base_dir)

if setup_result is None:
    print(" SETUP FAILED: Could not automatically detect and setup input files")
    print("   Please check the source directory and file structure")
    exit(1)

# Extract automatically detected parameters
start_week, end_week, current_year = setup_result

print(f"\nAUTOMATIC SETUP SUCCESSFUL!")
print(f"   - Detected Week Range: WK{start_week} to WK{end_week}")
print(f"   - Year: {current_year}")

# ===== AUTOMATED FORECAST PARAMETER CALCULATION =====
print("\n" + "="*50)
print("AUTOMATED FORECAST PARAMETER CALCULATION")
print("="*50)

apptchl_id = 104
moving_average_days = 14
seconds_in_day = 24 * 3600

forecast_params = calculate_forecast_parameters(start_week, end_week, current_year)
forecast_start_date = forecast_params['forecast_start_date']
geps_start_date = forecast_params['geps_start_date']
geps_end_date = forecast_params['geps_end_date']
month = forecast_params['month']
date = forecast_params['date']
formatted_date = forecast_params['formatted_date']

print(f" Calculated Parameters for WK{start_week} to WK{end_week}:")
print(f"   - Forecast Start Date: {forecast_start_date}")
print(f"   - GEPS Start Date: {geps_start_date} (forecast + 1 day)")
print(f"   - GEPS End Date: {geps_end_date} (forecast + 39 days)")
print(f"   - Month: {month}")
print(f"   - Date: {date}")
print(f"   - Formatted Date: {formatted_date}")
print("")

# ===== PATHS =====
input_folder_name = f"INPUT_DATA_WK{start_week}_WK{end_week}"
input_data_dir = base_dir / input_folder_name
model_output_folder = input_data_dir / f"Results_week_WK{start_week}_to_WK{end_week}_{current_year}"
reference_file_base_dir = input_data_dir / f"Reference_File_WK{start_week}_WK{end_week}"
apportionment_base_dir = input_data_dir / f"Apportment_input_data_WK{start_week}_WK{end_week}"
forecast_constant_files_path = base_dir / "Forecast_Constant_files_1950_2019"
forecast_input_path = input_data_dir / f"Forecast_Summary_Data_Input_WK{start_week}_WK{end_week}"

# ===== OUTPUT DIR =====
outputs_for_powerbi = f'WK{start_week}_{end_week}_WrmmOutputs'
timestamp = datetime.now().strftime("%Y%m%d%H%M")
output_dir = base_dir / f'Dashboard_Data_WK_{start_week}_{end_week}_{timestamp}'
if output_dir.exists():
    shutil.rmtree(output_dir)
output_dir.mkdir(parents=True, exist_ok=True)


print("\n=== BUILDING Multistation_file.csv ===")
build_multistation_file(
    base_dir=base_dir,
    start_week=start_week,
    end_week=end_week,
    current_year=current_year,
    output_dir=output_dir,
    ppwb_path=base_dir / "Apportioment_excel_files" / "APPENDIX 3 2025 July.xlsx",
    ppwb_sheet="DATA",
    ppwb_station_map={
        # left = output base name → right = how it appears in PPWB headers (flexible)
        "05CK004": "C5C K04",
        "05AJ001": "C5A J01",
    },
)
print(f"   - Done: {output_dir / 'Multistation_file.csv'}")

# ===== FILE PATHS FOR REST OF PIPELINE =====
reference_file_names = [reference_file_base_dir / "Reference_file_S0.xlsx"]
apportioment_input_file = apportionment_base_dir / f"Apportionment_summary_WK{start_week}_WK{end_week}.xlsx"
apportioment_output_file = output_dir / f"Apportionment_Dashboard_summary_week{start_week}_{end_week}.csv"

print("="*60)
print("STARTING MAIN PROCESSING WITH AUTO-DETECTED PARAMETERS")
print("="*60)
print(f"Using automatically detected week range: WK{start_week} to WK{end_week}")
print(f" Using automatically calculated forecast_start_date: {forecast_start_date}")
print(f" GEPS Start Date: {geps_start_date}")
print(f" GEPS End Date: {geps_end_date}")
print(f" Model output folder: {model_output_folder}")
print(f" Input data directory: {input_data_dir}")
print("")

# Verify input structure
print(" VERIFYING INPUT FILE STRUCTURE:")
required_paths = [
    ("Model output folder", model_output_folder),
    ("Reference file directory", reference_file_base_dir),
    ("Apportionment directory", apportionment_base_dir),
    ("Forecast input directory", forecast_input_path),
    ("Reference file", reference_file_names[0]),
    ("Apportionment input file", apportioment_input_file)
]

all_paths_exist = True
for description, path in required_paths:
    if path.exists():
        print(f"    OK {description}: {path}")
    else:
        print(f"    MISSING {description}: {path}")
        all_paths_exist = False

if not all_paths_exist:
    print("\n ERROR: Some required input files or directories are missing!")
    print("   Please check the input file setup process.")
    exit(1)

print(f"\n ALL INPUT FILES VERIFIED - PROCEEDING WITH PROCESSING")
print("")

# === MAIN PROCESSING ===
def main_processing_with_wiski_integration():
    """
    Complete WRMM processing workflow
    """
    print("="*60)
    print("STARTING WRMM PROCESSING")
    print("="*60)

    # STEP 1: Process WRMM model outputs
    print("\n" + "="*50)
    print("STEP 1: Processing WRMM Model Outputs")
    print("="*50)

    results = SummaryTablesGenerator.process_model_outputs(
        model_output_folder=str(model_output_folder),
        reference_file_names=[str(f) for f in reference_file_names],
        output_dir=str(output_dir),
        outputs_for_powerbi=outputs_for_powerbi,
        current_year=current_year,
        start_week=start_week,
        end_week=end_week,
        seconds_in_day=seconds_in_day,
        apptchl_id=apptchl_id
    )

    print("\n" + "="*50)
    print("STEP 1.1: Updating Data Type Values")
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
        df.to_csv(wrmm_output_path, index=False)
        excel_path = os.path.join(output_dir, f'{outputs_for_powerbi}.xlsx')
        if os.path.exists(excel_path):
            df.to_excel(excel_path, index=False)
        print(f" Updated Data_type values in {outputs_for_powerbi} files")
    else:
        print(f" WRMM output file not found: {wrmm_output_path}")

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

    print("\n" + "="*50)
    print("STEP 3: Generating Standard Summary Tables")
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
            df3.to_excel(os.path.join(output_dir, "SummaryTable_Reservoir.xlsx"),
                         index=False, sheet_name='SummaryTable_Reservoir_new')
            print(" Reservoir summary table created: SummaryTable_Reservoir.xlsx")
        else:
            missing = []
            if not os.path.exists(res_stor_path): missing.append("SumTab_%ResStor.xlsx")
            if not os.path.exists(res_inflow_path): missing.append("SumTab_ResInflow.xlsx")
            print(f" Missing required files for reservoir summary: {', '.join(missing)}")
            print("   Skipping reservoir summary table creation.")
    except Exception as e:
        print(f" Error creating reservoir summary table: {str(e)}")
        print("   Continuing with remaining processing...")

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

    print("\n" + "="*50)
    print("STEP 4.1: Fixing Weather Forecast Overlap")
    print("="*50)

    csv_result = fix_weather_forecast_overlap(output_dir, start_week, end_week)
    if csv_result:
        print(f"SUCCESS: Weather forecast overlap fixed and CSV created")
    else:
        print("FAILED: Weather forecast processing failed")

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
                print(" WISKI integration successful!")
                analysis_file = output_dir / f"WISKI_Analysis_Summary_{today_date}.xlsx"
                wiski_summary = wiski_combined_data.groupby(['Station', 'DataSource']).agg({
                    'Value': ['count', 'mean', 'std'],
                    'Interval': ['min', 'max']
                }).round(2)
                with pd.ExcelWriter(analysis_file, engine='openpyxl') as writer:
                    wiski_combined_data.to_excel(writer, sheet_name='Combined_Data', index=False)
                    wiski_summary.to_excel(writer, sheet_name='Summary_Stats')
                print(f"   - Analysis saved: {analysis_file}")
            else:
                print(" WISKI integration completed but no data was combined")
        except Exception as e:
            print(f" WISKI integration failed: {str(e)}")
            print("   Continuing with standard processing...")
    else:
        print(f"WISKI station list not found at: {wiski_station_list_path}")
        print("   Skipping WISKI integration...")

    print("\n" + "="*50)
    print("STEP 6: Processing Summary")
    print("="*50)

    print(f" Output directory: {output_dir}")
    print(f" WRMM outputs processed: {outputs_for_powerbi}.csv")

    output_files = list(output_dir.glob("*"))
    print(f" Total files generated: {len(output_files)}")
    excel_files = [f for f in output_files if f.suffix == '.xlsx']
    csv_files = [f for f in output_files if f.suffix == '.csv']
    print(f"   - Excel files: {len(excel_files)}")
    print(f"   - CSV files: {len(csv_files)}")

    if weather_data is not None:
        print(f" Weather forecast: SUCCESS")
        print(f"   - {len(weather_data)} stations processed")

    reservoir_summary_path = output_dir / "SummaryTable_Reservoir.xlsx"
    if reservoir_summary_path.exists():
        print(f" Reservoir summary table: SUCCESS")

    print(f" Data type standardization: SUCCESS")
    print("\n" + "="*60)
    print("WRMM PROCESSING COMPLETED SUCCESSFULLY!")
    print("="*60)

    return generator, weather_data


# Run
seconds_in_day = 24 * 3600
main_processing_with_wiski_integration()
