# # def auto_setup_input_files(base_dir):
# #     """
# #     Automatically detect week numbers and set up input file structure.
    
# #     Parameters:
# #     base_dir (Path): Base directory path
    
# #     Returns:
# #     tuple: (start_week, end_week, current_year) or None if setup fails
# #     """
# #     import re
# #     import glob
    
# #     print("="*60)
# #     print("AUTOMATIC INPUT FILE SETUP")
# #     print("="*60)
    
# #     # STEP 1: Fetch from operational modeling directory and detect week numbers
# #     source_dir = Path(r"D:\Sopan\HGS_Data\Codes\WRMM\WRMM_Package\WRMM_For BEN\WRMM_Package\TESTING_AUTO")
# #     print(f"STEP 1: Scanning source directory: {source_dir}")
    
# #     if not source_dir.exists():
# #         print(f" Source directory not found: {source_dir}")
# #         return None
    
# #     # Find Results directory
# #     results_dirs = [d for d in source_dir.iterdir() if d.is_dir() and d.name.startswith("Results")]
# #     if not results_dirs:
# #         print(" No Results directory found in source folder")
# #         return None
    
# #     results_dir = results_dirs[0]  # Take the first one found
# #     print(f" Found Results directory: {results_dir.name}")
    
# #     # Extract week numbers from directory name
# #     # Pattern: Results_week_WK26_to_WK30_2025
# #     pattern = r"Results_week_WK(\d+)_to_WK(\d+)_(\d+)"
# #     match = re.search(pattern, results_dir.name)
    
# #     if not match:
# #         print(f" Could not extract week numbers from: {results_dir.name}")
# #         return None
    
# #     start_week = int(match.group(1))
# #     end_week = int(match.group(2))
# #     current_year = int(match.group(3))
    
# #     print(f" Detected: start_week={start_week}, end_week={end_week}, year={current_year}")
    
# #     # STEP 2: Check required files in Results directory
# #     print(f"\n STEP 2: Checking required files in {results_dir.name}")
    
# #     # Find Apportionment file
# #     apportionment_pattern = f"Apportionment_summary_WK{start_week}_WK{end_week}*"
# #     apportionment_files = list(results_dir.glob(apportionment_pattern))
    
# #     if not apportionment_files:
# #         print(f" Apportionment file not found with pattern: {apportionment_pattern}")
# #         return None
    
# #     apportionment_file = apportionment_files[0]
# #     print(f"Found Apportionment file: {apportionment_file.name}")
    
# #     # Check S0 folder
# #     s0_folder = results_dir / "S0"
# #     if not s0_folder.exists():
# #         print(f" S0 folder not found: {s0_folder}")
# #         return None
    
# #     print(f" Found S0 folder: {s0_folder}")
    
# #     # STEP 3: Create input directory structure
# #     print(f"\n STEP 3: Creating input directory structure")
    
# #     input_dir = base_dir / f"INPUT_DATA_WK{start_week}_WK{end_week}"
# #     if input_dir.exists():
# #         shutil.rmtree(input_dir)
# #         print(f"Removed existing directory: {input_dir}")
    
# #     input_dir.mkdir(parents=True, exist_ok=True)
# #     print(f"Created: {input_dir}")
    
# #     # Create Results subdirectory
# #     results_subdir = input_dir / f"Results_week_WK{start_week}_to_WK{end_week}_{current_year}"
# #     results_subdir.mkdir(parents=True, exist_ok=True)
# #     print(f"Created: {results_subdir}")
    
# #     # Create Apportionment subdirectory
# #     apportionment_subdir = input_dir / f"Apportment_input_data_WK{start_week}_WK{end_week}"
# #     apportionment_subdir.mkdir(parents=True, exist_ok=True)
# #     print(f"Created: {apportionment_subdir}")
    
# #     # Copy S0 folder
# #     dest_s0 = results_subdir / "S0"
# #     shutil.copytree(s0_folder, dest_s0)
# #     print(f"Copied S0 folder: {s0_folder} {dest_s0}")
    
# #     # Copy Apportionment file
# #     dest_apportionment = apportionment_subdir / f"Apportionment_summary_WK{start_week}_WK{end_week}.xlsx"
# #     shutil.copy2(apportionment_file, dest_apportionment)
# #     print(f"Copied Apportionment file: {apportionment_file} {dest_apportionment}")
    
# #     # STEP 4: Create Reference File directory and copy reference file
# #     print(f"\nSTEP 4: Setting up Reference Files")
    
# #     reference_dir = input_dir / f"Reference_File_WK{start_week}_WK{end_week}"
# #     reference_dir.mkdir(parents=True, exist_ok=True)
# #     print(f"Created: {reference_dir}")
    
# #     # Copy reference file
# #     reference_source = base_dir / "Reference_File_2025" / "Reference_file_S0.xlsx"
# #     if not reference_source.exists():
# #         print(f"Reference file not found: {reference_source}")
# #         return None
    
# #     reference_dest = reference_dir / "Reference_file_S0.xlsx"
# #     shutil.copy2(reference_source, reference_dest)
# #     print(f"Copied Reference file: {reference_source} {reference_dest}")
    
# #     # STEP 5: Set up Forecast Summary Data
# #     print(f"\n STEP 5: Setting up Forecast Summary Data")
    
# #     # Calculate forecast parameters
# #     forecast_params = calculate_forecast_parameters(start_week, end_week, current_year)
# #     geps_start_date = datetime.strptime(forecast_params['geps_start_date'], "%Y-%m-%d").strftime("%Y%m%d")
# #     geps_end_date = datetime.strptime(forecast_params['geps_end_date'], "%Y-%m-%d").strftime("%Y%m%d")
    
# #     print(f"GEPS Start Date: {geps_start_date}")
# #     print(f"GEPS End Date: {geps_end_date}")
    
# #     # Create Forecast directory
# #     forecast_dir = input_dir / f"Forecast_Summary_Data_Input_WK{start_week}_WK{end_week}"
# #     forecast_dir.mkdir(parents=True, exist_ok=True)
# #     print(f"Created: {forecast_dir}")
    
# #     # Copy GEPS data file
# #     geps_source = Path(f"D:/Sopan/HGS_Data/Data_for_HGS_Run/GEPS_Data/Excel_By_Station_{geps_start_date}_{geps_end_date}/Data_for_Dashboard_{geps_start_date}_{geps_end_date}.xlsx")
    
# #     if not geps_source.exists():
# #         print(f" GEPS data file not found: {geps_source}")
# #         print(f"   Creating forecast directory without GEPS data...")
# #     else:
# #         geps_dest = forecast_dir / f"WSA_forecast_Temp_Precip_WK{start_week}_WK{end_week}.xlsx"
# #         shutil.copy2(geps_source, geps_dest)
# #         print(f"Copied GEPS data: {geps_source} {geps_dest}")
    
# #     print(f"\n INPUT FILE SETUP COMPLETE!")
# #     print(f"Input directory created: {input_dir}")
# #     print(f"Week range: WK{start_week} to WK{end_week}")
# #     print(f"Year: {current_year}")
    
# #     return start_week, end_week, current_year


# def auto_setup_input_files(base_dir):
#     """
#     Automatically detect week numbers and set up input file structure.
#     ALSO: build a combined weekly CSV with recorded & simulated values:
#       Date, Week#, Recorded_flow_wiski_05AJ001, Recorded_flow_wiski_05CK004,
#       Simulated_C5CK04, Simulated_C5HBU1
#     """
#     import re
#     import glob
#     import shutil
#     from pathlib import Path
#     from datetime import datetime, timedelta
#     import numpy as np
#     import pandas as pd

#     print("="*60)
#     print("AUTOMATIC INPUT FILE SETUP")
#     print("="*60)

#     # -----------------------------
#     # Local helpers (week calendar + HBDF extractor)
#     # -----------------------------
    
#     def extract_multiple_stations_from_hbdf(
#         model_output_folder, current_year, start_week, end_week, output_dir, station_list
#     ):
#         """
#         Returns a DataFrame with columns: Year, Week, Simulated_<station-without-spaces>...
#         DOES NOT WRITE ANY FILES.
#         """
#         import re
#         from pathlib import Path
#         import pandas as pd

#         if isinstance(station_list, str):
#             stations_to_find = [s.strip() for s in station_list.split(",") if s.strip()]
#         else:
#             stations_to_find = [str(s).strip() for s in station_list]

#         # Locate HBDF
#         hbdf_file_path = (
#             Path(model_output_folder) / "S0" / str(current_year) / "SSRB" / "HBDF.txt"
#         )
#         if not hbdf_file_path.exists():
#             for alt in [
#                 Path(model_output_folder) / "S0" / "HBDF.txt",
#                 Path(model_output_folder) / "HBDF.txt",
#                 Path(model_output_folder) / "S0" / str(current_year) / "HBDF.txt",
#             ]:
#                 if alt.exists():
#                     hbdf_file_path = alt
#                     break
#         if not hbdf_file_path.exists():
#             print("   - ERROR: HBDF file not found.")
#             return pd.DataFrame()

#         with open(hbdf_file_path, "r", encoding="utf-8", errors="ignore") as f:
#             lines = f.readlines()

#         station_header_any_re = re.compile(r"^\s*[A-Z0-9]{3}\s+[A-Z0-9]{2,3}\s+\d{4}\s+", re.ASCII)
#         year_row_re = re.compile(rf"^\s*{current_year}\s+")
#         header_indices = [i for i, raw in enumerate(lines) if station_header_any_re.match(raw)]
#         header_indices.append(len(lines))

#         def _extract_block(station_code: str):
#             station_header_exact_re = re.compile(
#                 rf"^\s*{re.escape(station_code)}\s+\d{{4}}\s+\d+\s+[A-Z]+", re.ASCII
#             )
#             block_start = None
#             for i in range(len(lines)):
#                 if station_header_exact_re.match(lines[i]):
#                     block_start = i
#                     break
#             if block_start is None:
#                 norm_target = " ".join(station_code.split())
#                 for i in range(len(lines)):
#                     norm_line = " ".join(lines[i].strip().split())
#                     if norm_line.startswith(norm_target + " ") and re.search(r"\b\d{4}\b", norm_line):
#                         block_start = i
#                         break
#             if block_start is None:
#                 return None

#             next_headers = [h for h in header_indices if h > block_start]
#             block_end = next_headers[0] if next_headers else len(lines)
#             block = lines[block_start:block_end]

#             data_row_line = None
#             for k, raw in enumerate(block):
#                 if year_row_re.match(raw):
#                     data_row_line = k
#                     break
#             if data_row_line is None:
#                 for k, raw in enumerate(block):
#                     if str(current_year) in raw[:10] and re.match(rf"^\s*{current_year}\s+", raw):
#                         data_row_line = k
#                         break
#             if data_row_line is None:
#                 return None

#             parts = block[data_row_line].split()
#             if len(parts) < 53:
#                 return None

#             try:
#                 week_vals = [float(x) for x in parts[1:53]]
#             except ValueError:
#                 return None
#             return week_vals

#         per_station = {}
#         found = []
#         for st in stations_to_find:
#             vals = _extract_block(st)
#             if vals is not None:
#                 per_station[st] = vals
#                 found.append(st)

#         if not found:
#             return pd.DataFrame()

#         records = []
#         for wk in range(start_week, end_week + 1):
#             row = {"Year": int(current_year), "Week": int(wk)}
#             for st in found:
#                 col = f"Simulated_{st.replace(' ', '')}"
#                 row[col] = per_station[st][wk - 1]
#             records.append(row)

#         return pd.DataFrame.from_records(records).sort_values(["Year", "Week"]).reset_index(drop=True)

#     # -------------------------------------------------------
#     # STEP 1: detect Results folder and week numbers
#     # -------------------------------------------------------
#     source_dir = Path(r"D:\Sopan\HGS_Data\Codes\WRMM\WRMM_Package\WRMM_For BEN\WRMM_Package\TESTING_AUTO")
#     print(f"STEP 1: Scanning source directory: {source_dir}")

#     if not source_dir.exists():
#         print(f" Source directory not found: {source_dir}")
#         return None

#     results_dirs = [d for d in source_dir.iterdir() if d.is_dir() and d.name.startswith("Results")]
#     if not results_dirs:
#         print(" No Results directory found in source folder")
#         return None

#     results_dir = results_dirs[0]
#     print(f" Found Results directory: {results_dir.name}")

#     pattern = r"Results_week_WK(\d+)_to_WK(\d+)_(\d+)"
#     match = re.search(pattern, results_dir.name)
#     if not match:
#         print(f" Could not extract week numbers from: {results_dir.name}")
#         return None

#     start_week = int(match.group(1))
#     end_week = int(match.group(2))
#     current_year = int(match.group(3))
#     print(f" Detected: start_week={start_week}, end_week={end_week}, year={current_year}")

#     # -------------------------------------------------------
#     # STEP 2: verify files / S0
#     # -------------------------------------------------------
#     print(f"\n STEP 2: Checking required files in {results_dir.name}")
#     apportionment_pattern = f"Apportionment_summary_WK{start_week}_WK{end_week}*"
#     apportionment_files = list(results_dir.glob(apportionment_pattern))
#     if not apportionment_files:
#         print(f" Apportionment file not found with pattern: {apportionment_pattern}")
#         return None
#     apportionment_file = apportionment_files[0]
#     print(f"Found Apportionment file: {apportionment_file.name}")

#     s0_folder = results_dir / "S0"
#     if not s0_folder.exists():
#         print(f" S0 folder not found: {s0_folder}")
#         return None
#     print(f" Found S0 folder: {s0_folder}")

#     # -------------------------------------------------------
#     # STEP 3: create input directory tree and copy files
#     # -------------------------------------------------------
#     print(f"\n STEP 3: Creating input directory structure")
#     input_dir = base_dir / f"INPUT_DATA_WK{start_week}_WK{end_week}"
#     if input_dir.exists():
#         shutil.rmtree(input_dir)
#         print(f"Removed existing directory: {input_dir}")
#     input_dir.mkdir(parents=True, exist_ok=True)
#     print(f"Created: {input_dir}")

#     results_subdir = input_dir / f"Results_week_WK{start_week}_to_WK{end_week}_{current_year}"
#     results_subdir.mkdir(parents=True, exist_ok=True)
#     print(f"Created: {results_subdir}")

#     apportionment_subdir = input_dir / f"Apportment_input_data_WK{start_week}_WK{end_week}"
#     apportionment_subdir.mkdir(parents=True, exist_ok=True)
#     print(f"Created: {apportionment_subdir}")

#     dest_s0 = results_subdir / "S0"
#     shutil.copytree(s0_folder, dest_s0)
#     print(f"Copied S0 folder: {s0_folder} -> {dest_s0}")

#     dest_apportionment = apportionment_subdir / f"Apportionment_summary_WK{start_week}_WK{end_week}.xlsx"
#     shutil.copy2(apportionment_file, dest_apportionment)
#     print(f"Copied Apportionment file: {apportionment_file} -> {dest_apportionment}")

#     # -------------------------------------------------------
#     # STEP 4: reference file
#     # -------------------------------------------------------
#     print(f"\nSTEP 4: Setting up Reference Files")
#     reference_dir = input_dir / f"Reference_File_WK{start_week}_WK{end_week}"
#     reference_dir.mkdir(parents=True, exist_ok=True)
#     print(f"Created: {reference_dir}")

#     reference_source = base_dir / "Reference_File_2025" / "Reference_file_S0.xlsx"
#     if not reference_source.exists():
#         print(f"Reference file not found: {reference_source}")
#         return None
#     reference_dest = reference_dir / "Reference_file_S0.xlsx"
#     shutil.copy2(reference_source, reference_dest)
#     print(f"Copied Reference file: {reference_source} -> {reference_dest}")

#     # -------------------------------------------------------
#     # STEP 5: Forecast summary scaffolding (unchanged)
#     # -------------------------------------------------------
#     print(f"\n STEP 5: Setting up Forecast Summary Data")
#     forecast_params = calculate_forecast_parameters(start_week, end_week, current_year)
#     geps_start_date = datetime.strptime(forecast_params['geps_start_date'], "%Y-%m-%d").strftime("%Y%m%d")
#     geps_end_date = datetime.strptime(forecast_params['geps_end_date'], "%Y-%m-%d").strftime("%Y%m%d")
#     print(f"GEPS Start Date: {geps_start_date}")
#     print(f"GEPS End Date: {geps_end_date}")

#     forecast_dir = input_dir / f"Forecast_Summary_Data_Input_WK{start_week}_WK{end_week}"
#     forecast_dir.mkdir(parents=True, exist_ok=True)
#     print(f"Created: {forecast_dir}")

#     geps_source = Path(f"D:/Sopan/HGS_Data/Data_for_HGS_Run/GEPS_Data/Excel_By_Station_{geps_start_date}_{geps_end_date}/Data_for_Dashboard_{geps_start_date}_{geps_end_date}.xlsx")
#     if not geps_source.exists():
#         print(f"   - GEPS data file not found: {geps_source}")
#         print(f"   - Creating forecast directory without GEPS data...")
#     else:
#         geps_dest = forecast_dir / f"WSA_forecast_Temp_Precip_WK{start_week}_WK{end_week}.xlsx"
#         shutil.copy2(geps_source, geps_dest)
#         print(f"Copied GEPS data: {geps_source} -> {geps_dest}")

#     # -------------------------------------------------------
#     # NEW STEP 6: Build the combined weekly CSV (Recorded + Simulated)
#     # -------------------------------------------------------

#     print("\n STEP 6: Building combined weekly CSV (Recorded + Simulated)")
#     CSV_PATH = r"\\c-goa-apm-13251\WaterManagementDashboard_13251\PBI_Data\W_MGMT_4_2025.csv"
#     REC_STATIONS = ["05AJ001", "05CK004"]          # recorded (WISKI)
#     SIM_STATION_LIST = ["C5C K04", "C5H BU1"]      # simulated (HBDF headers)

#     def get_weekend_dates(year: int):
#         weekends = [datetime(year, 1, 7) + timedelta(days=7*i) for i in range(51)]
#         weekends.append(datetime(year, 12, 31))
#         return weekends

#     def assign_custom_week(dates: pd.Series, weekend_dates):
#         arr = np.array(weekend_dates, dtype="datetime64[ns]")
#         idx = np.searchsorted(arr, dates.values.astype("datetime64[ns]"), side="right")
#         return np.clip(idx, 1, 52)

#     # 6.1 skeleton (Dates every 7 days from Jan 1) + Week#
#     skeleton = pd.DataFrame({
#         "Date": [datetime(current_year, 1, 1) + timedelta(days=7*i) for i in range(52)]
#     })
#     skeleton["Week#"] = np.arange(1, 53, dtype=int)

#     # 6.2 Recorded weekly means
#     try:
#         df_rec = pd.read_csv(CSV_PATH)
#         df_rec["Date"] = pd.to_datetime(df_rec["Date"], errors="coerce")
#         df_rec = df_rec.dropna(subset=["Date"])
#         df_rec = df_rec[(df_rec["StationNumber"].isin(REC_STATIONS)) &
#                         (df_rec["Date"].dt.year == current_year)].copy()

#         weekend_dates = get_weekend_dates(current_year)
#         df_rec["Week#"] = assign_custom_week(df_rec["Date"], weekend_dates)

#         weekly_rec = (df_rec.groupby(["StationNumber", "Week#"], as_index=False)["Value"]
#                             .mean().rename(columns={"Value": "WeeklyMean"}))
#         wide_rec = weekly_rec.pivot_table(index="Week#", columns="StationNumber", values="WeeklyMean").reset_index()

#         out = skeleton.merge(wide_rec, on="Week#", how="left")
#         out = out.rename(columns={
#             "05AJ001": "Recorded_flow_wiski_05AJ001",
#             "05CK004": "Recorded_flow_wiski_05CK004",
#         })
#     except Exception as e:
#         print(f"   - ERROR computing recorded weekly means: {e}")
#         out = skeleton.copy()
#         out["Recorded_flow_wiski_05AJ001"] = np.nan
#         out["Recorded_flow_wiski_05CK004"] = np.nan

#     # 6.3 Simulated weekly values from HBDF (no extra files)
#     sim_df = extract_multiple_stations_from_hbdf(
#         model_output_folder=results_subdir,   # the copied Results folder inside INPUT_DATA
#         current_year=current_year,
#         start_week=start_week,                # we will also enforce masking below
#         end_week=end_week,
#         output_dir=None,                      # <--- IMPORTANT: no output_dir here
#         station_list=SIM_STATION_LIST
#     )

#     # Merge simulated → mask outside [start_week, end_week] (Simulated ONLY)
#     if not sim_df.empty:
#         sim_aligned = sim_df.rename(columns={"Week": "Week#"})[
#             ["Week#", "Simulated_C5CK04", "Simulated_C5HBU1"]
#         ]
#         out = out.merge(sim_aligned, on="Week#", how="left")
#     else:
#         out["Simulated_C5CK04"] = np.nan
#         out["Simulated_C5HBU1"] = np.nan

#     mask_before = out["Week#"] < start_week
#     mask_after  = out["Week#"] > end_week
#     for col in ["Simulated_C5CK04", "Simulated_C5HBU1"]:
#         out.loc[mask_before | mask_after, col] = np.nan

#     # Format Date and order columns
#     out["Date"] = out["Date"].dt.strftime("%m/%d/%Y").str.replace(r"^0", "", regex=True).str.replace("/0", "/", regex=False)
#     out = out[[
#         "Date", "Week#",
#         "Recorded_flow_wiski_05AJ001", "Recorded_flow_wiski_05CK004",
#         "Simulated_C5CK04", "Simulated_C5HBU1"
#     ]]

#     # Save TEMP in INPUT folder (since output_dir doesn't exist yet here)
#     temp_multistation = input_dir / "Multistation_file.csv"
#     out.to_csv(temp_multistation, index=False)
#     print(f"   - Temp saved: {temp_multistation}")

#     return start_week, end_week, current_year


# # ... you already built `out` with Recorded_* and Simulated_* above this

# # 6.4  PPWB Excel (APPENDIX 3 2025 July.xlsx -> sheet 'DATA')



# def calculate_forecast_parameters(start_week, end_week, year):
#     """
#     Automatically calculate forecast_start_date, month, and date based on week numbers.
    
#     Parameters:
#     start_week (int): Starting week number (e.g., 26)
#     end_week (int): Ending week number (e.g., 30)
#     year (int): Year (e.g., 2025)
    
#     Returns:
#     dict: Contains forecast_start_date, month, date, formatted_date
#     """
#     from datetime import datetime, timedelta
    
#     # Generate the week dates using Option 2 method
#     def get_week_dates(year, weeks=52):
#         start_date = datetime(year, 1, 7)
#         end_date = datetime(year, 12, 31)
        
#         weekend_dates = []
        
#         # Generate first 51 weeks (regular 7-day intervals)
#         for week_num in range(weeks - 1):  # 51 weeks
#             current_date = start_date + timedelta(days=week_num * 7)
#             weekend_dates.append(current_date)
        
#         # Add December 31st as the 52nd week
#         weekend_dates.append(end_date)
        
#         return weekend_dates
    
#     # Get all week dates for the year
#     week_dates = get_week_dates(year)
    
#     # Get the date for the start_week (subtract 1 because list is 0-indexed)
#     forecast_start_date_obj = week_dates[start_week - 1]
    
#     # Format the forecast start date
#     forecast_start_date = forecast_start_date_obj.strftime('%Y-%m-%d')
    
#     # Calculate GEPS dates (add 1 day for start, add 39 days for end)
#     geps_start_date_obj = forecast_start_date_obj + timedelta(days=1)
#     geps_end_date_obj = forecast_start_date_obj + timedelta(days=41)
    
#     geps_start_date = geps_start_date_obj.strftime('%Y-%m-%d')
#     geps_end_date = geps_end_date_obj.strftime('%Y-%m-%d')
    
#     # Extract month name and date
#     month = forecast_start_date_obj.strftime('%B')  # Full month name (e.g., 'July')
#     date = forecast_start_date_obj.day
#     formatted_date = f"{date:02d}"
    
#     return {
#         'forecast_start_date': forecast_start_date,
#         'geps_start_date': geps_start_date,
#         'geps_end_date': geps_end_date,
#         'month': month,
#         'date': date,
#         'formatted_date': formatted_date,
#         'forecast_start_date_obj': forecast_start_date_obj,
#         'geps_start_date_obj': geps_start_date_obj,
#         'geps_end_date_obj': geps_end_date_obj
#     }


# def fix_weather_forecast_overlap(output_dir, start_week, end_week):
#     """
#     Fix overlap in weather forecast data and convert to CSV
    
#     Parameters:
#     output_dir (Path): Output directory path
#     start_week (int): Start week number  
#     end_week (int): End week number
#     """
#     import pandas as pd
#     import numpy as np
#     from pathlib import Path
    
#     print(f"\nFixing weather forecast overlap and converting to CSV...")
    
#     # Look for the copied Data_for_Dashboard file in forecast input directory
#     # forecast_input_dir = Path(str(output_dir).replace('Dashboard_Data', f'INPUT_DATA_WK{start_week}_WK{end_week}')).parent / f"Forecast_Summary_Data_Input_WK{start_week}_WK{end_week}"
#     # Set the base directory (adjust this if needed)
#     base_dir_wsa = Path(r"D:\Sopan\HGS_Data\Codes\WRMM\WRMM_Package\WRMM_For BEN\WRMM_Package")

#     # Build the forecast input directory directly
#     forecast_input_dir = base_dir_wsa / f"INPUT_DATA_WK{start_week}_WK{end_week}" / f"Forecast_Summary_Data_Input_WK{start_week}_WK{end_week}"


#     # Find the actual file (handles dynamic date naming)
#     dashboard_files = list(forecast_input_dir.glob("WSA_forecast_Temp_Precip_*.xlsx"))
    
#     if not dashboard_files:
#         print(f"   - WSA_forecast_Temp_Precip file not found in: {forecast_input_dir}")
#         return None
    
#     dashboard_file = dashboard_files[0]
#     print(f"   - Found file: {dashboard_file.name}")
    
#     try:
#         # Read the Excel file
#         df = pd.read_excel(dashboard_file)
#         print(f"   - Original data shape: {df.shape}")
#         print(f"   - Columns: {list(df.columns)}")
        
#         # Convert Date column to datetime
#         if 'Date' in df.columns:
#             df['Date'] = pd.to_datetime(df['Date'])
#         else:
#             print("   - Error: No 'Date' column found")
#             return None
        
#         # Process each station
#         processed_stations = []
#         overlap_removed_count = 0
        
#         for station in df['Station'].unique():
#             station_data = df[df['Station'] == station].copy()
#             print(f"   - Processing station: {station}")
            
#             # Identify Historical columns (columns starting with 'Historical_')
#             historical_cols = [col for col in station_data.columns if col.startswith('Historical_')]
#             print(f"     - Historical columns: {historical_cols}")
            
#             # Identify Forecast columns (all non-historical columns that contain forecast data)
#             forecast_cols = [col for col in station_data.columns 
#                            if not col.startswith('Historical_') 
#                            and col not in ['Date', 'Station']
#                            and any(substring in col.lower() for substring in ['tmax', 'tmin', 'precip', 'temp'])]
#             print(f"     - Forecast columns: {forecast_cols[:5]}...")  # Show first 5
            
#             if historical_cols and forecast_cols:
#                 # Find last date with historical data (non-null values)
#                 historical_mask = station_data[historical_cols].notna().any(axis=1)
#                 if historical_mask.any():
#                     last_historical_date = station_data.loc[historical_mask, 'Date'].max()
#                     print(f"     - Last historical date: {last_historical_date}")
                    
#                     # Find first date with forecast data (non-null values)
#                     forecast_mask = station_data[forecast_cols].notna().any(axis=1)
#                     if forecast_mask.any():
#                         first_forecast_date = station_data.loc[forecast_mask, 'Date'].min()
#                         print(f"     - First forecast date: {first_forecast_date}")
                        
#                         # Check for overlap (same date)
#                         if last_historical_date == first_forecast_date:
#                             print(f"     - OVERLAP DETECTED on {last_historical_date}")
#                             print(f"     - Removing historical data for this date...")
                            
#                             # Find rows with the overlapping date for this station
#                             overlap_mask = (station_data['Date'] == last_historical_date)
#                             rows_to_modify = station_data.index[overlap_mask]
                            
#                             print(f"     - Found {len(rows_to_modify)} rows to modify")
                            
#                             # Set historical data to NaN for overlapping date
#                             for col in historical_cols:
#                                 before_count = station_data.loc[overlap_mask, col].notna().sum()
#                                 station_data.loc[overlap_mask, col] = np.nan
#                                 after_count = station_data.loc[overlap_mask, col].notna().sum()
#                                 if before_count > 0:
#                                     print(f"       - {col}: cleared {before_count} values")
                            
#                             overlap_removed_count += len(rows_to_modify)
#                         else:
#                             print(f"     - No overlap detected")
#                     else:
#                         print(f"     - No forecast data found")
#                 else:
#                     print(f"     - No historical data found")
#             else:
#                 print(f"     - Could not identify historical/forecast columns")
            
#             processed_stations.append(station_data)
        
#         # Combine all stations
#         final_df = pd.concat(processed_stations, ignore_index=True)
        
#         print(f"   - Total overlap records removed: {overlap_removed_count}")
#         print(f"   - Final data shape: {final_df.shape}")
        
#         # Save as CSV with the required name
#         csv_filename = f"WSA_forecast_Temp_Precip_WK{start_week}_WK{end_week}.xlsx"
#         csv_output_path = output_dir / csv_filename
        
#         # final_df.to_excel(csv_output_path, index=False)
#         # Use ExcelWriter to specify sheet name
#         with pd.ExcelWriter(csv_output_path, engine='openpyxl') as writer:
#             final_df.to_excel(writer, sheet_name='WSA_forecast_Temp_Precip', index=False)

#         print(f"   - xlsx saved: {csv_filename}")
        
#         # Verify the fix worked by checking a sample
#         if overlap_removed_count > 0:
#             print(f"   - Verification: Checking overlap removal...")
#             sample_station = final_df['Station'].iloc[0]
#             sample_data = final_df[final_df['Station'] == sample_station]
#             historical_cols = [col for col in final_df.columns if col.startswith('Historical_')]
#             if historical_cols:
#                 last_hist_date = sample_data[sample_data[historical_cols].notna().any(axis=1)]['Date'].max()
#                 first_forecast_date = sample_data[sample_data[[col for col in final_df.columns if not col.startswith('Historical_') and col not in ['Date', 'Station']]].notna().any(axis=1)]['Date'].min()
#                 print(f"     - Sample station {sample_station}: last hist={last_hist_date}, first forecast={first_forecast_date}")
        
#         return str(csv_output_path)
        
#     except Exception as e:
#         print(f"   - Error processing file: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return None


# def main_processing_with_wiski_integration():
#     """
#     Complete WRMM processing workflow
#     """
    
#     print("="*60)
#     print("STARTING WRMM PROCESSING")
#     print("="*60)
    
#     # STEP 1: Process WRMM model outputs (your existing workflow)
#     print("\n" + "="*50)
#     print("STEP 1: Processing WRMM Model Outputs")
#     print("="*50)
    
#     results = SummaryTablesGenerator.process_model_outputs(
#         model_output_folder=str(model_output_folder),
#         reference_file_names=[str(f) for f in reference_file_names],
#         output_dir=str(output_dir),
#         outputs_for_powerbi=outputs_for_powerbi,
#         current_year=current_year,
#         start_week=start_week,
#         end_week=end_week,
#         seconds_in_day=seconds_in_day,
#         apptchl_id=apptchl_id
#     )
    

#     # === NEW STEP 1.2: EXTRACT STATION DATA ===
#     # station_data = extract_multiple_stations_from_hbdf(
#     #         model_output_folder, current_year, start_week, end_week, output_dir, 
#     #         "C5C K04,C5A J01"
#     #     )

#     # == NEW STEP 1.3: Extract Data from WRM_4.csv

#     # === UPDATE DATA_TYPE VALUES ===
#     print("\n" + "="*50)
#     print("STEP 1.1: Updating Data Type Values")
#     print("="*50)
    
#     wrmm_output_path = os.path.join(output_dir, f'{outputs_for_powerbi}.csv')
#     if os.path.exists(wrmm_output_path):
#         # Load the CSV
#         df = pd.read_csv(wrmm_output_path)
        
#         # Replace values in Data_type column
#         df['Data_type'] = df['Data_type'].replace({
#             'S0': 'Predicted Flow',
#             'Target_S0': 'Target Flow'
#         })
        
#         df.loc[
#             (df['ComponentType'] == "Irrigation District") & (df['Data_type'] == "Predicted Flow"),
#             'Data_type'
#         ] = "Predicted Deficit"
        
#         # Save the updated CSV
#         df.to_csv(wrmm_output_path, index=False)
        
#         # Also update the Excel file if it exists
#         excel_path = os.path.join(output_dir, f'{outputs_for_powerbi}.xlsx')
#         if os.path.exists(excel_path):
#             df.to_excel(excel_path, index=False)
        
#         print(f" Updated Data_type values in {outputs_for_powerbi} files:")
#         print("   - 'S0' 'Predicted Flow'")
#         print("   - 'Target_S0' 'Target Flow'")
#         print("   - Irrigation Districts: 'Predicted Flow' 'Predicted Deficit'")
#     else:
#         print(f" WRMM output file not found: {wrmm_output_path}")
    
#     # Unpack results
#     (master_ex_summary, hbdf_maa_natflow, divchl_summary_tab, reference_file_name,
#      date_ref, subtab_priv_irr_all, subtab_priv_irr_sen, subtab_priv_irr_jun_io,
#      subtab_priv_irr_jun_wco, scn, processor, output_dir_returned, start_week_returned,
#      end_week_returned, seconds_in_day_returned, apptchl_id_returned) = results
    
#     # STEP 2: Create generator instance
#     print("\n" + "="*50)
#     print("STEP 2: Creating Summary Tables Generator")
#     print("="*50)
    
#     generator = SummaryTablesGenerator(
#         master_ex_summary=master_ex_summary,
#         hbdf_maa_natflow=hbdf_maa_natflow,
#         divchl_summary_tab=divchl_summary_tab,
#         reference_file_name=reference_file_name,
#         date_ref=date_ref,
#         subtab_priv_irr_all=subtab_priv_irr_all,
#         subtab_priv_irr_sen=subtab_priv_irr_sen,
#         subtab_priv_irr_jun_io=subtab_priv_irr_jun_io,
#         subtab_priv_irr_jun_wco=subtab_priv_irr_jun_wco,
#         scn=scn,
#         processor=processor,
#         output_dir=str(output_dir),
#         start_week=start_week,
#         end_week=end_week,
#         seconds_in_day=seconds_in_day,
#         apptchl_id=apptchl_id
#     )
    
#     # STEP 3: Generate all standard summary tables
#     print("\n" + "="*50)
#     print("STEP 3: Generating Standard Summary Tables")
#     print("="*50)
    
#     print("3.1: Preparing summary tables...")
#     generator.prepare_summary_tables()
    
#     print("3.2: Generating MAA files...")
#     generator.generate_maa_files()
    
#     print("3.3: Creating MAA 1969 summary...")
#     generator.MAA_1969_Summary()
    
#     print("3.4: Creating irrigation diversion summary...")
#     generator.IrrigationDiversionSummary()
    
#     print("3.5: Calculating irrigation shortage...")
#     generator.calculate_irrigation_shortage()
    
#     print("3.6: Creating apportionment summary...")
#     generator.create_apportionment_summary(
#         apportionment_input_file=str(apportioment_input_file),
#         apportionment_output_file=str(apportioment_output_file)
#     )
    
#     # === CREATE RESERVOIR SUMMARY TABLE ===
#     print("\n" + "="*50)
#     print("STEP 3.7: Creating Reservoir Summary Table")
#     print("="*50)
    
#     try:
#         # Check if required files exist
#         res_stor_path = os.path.join(output_dir, "SumTab_%ResStor.xlsx")
#         res_inflow_path = os.path.join(output_dir, "SumTab_ResInflow.xlsx")
        
#         if os.path.exists(res_stor_path) and os.path.exists(res_inflow_path):
#             # Read the Excel files
#             df1 = pd.read_excel(res_stor_path, header=None)
#             df2 = pd.read_excel(res_inflow_path, header=None)
            
#             # Transpose the DataFrames
#             df1_T = df1.T
#             df1_T = df1_T.iloc[1:]
#             df1_T.columns = ['Reservoir', '%FSL']
            
#             df2_T = df2.T
#             df2_T = df2_T.iloc[1:]
#             df2_T.columns = ['Reservoir', 'Projected Total Inflow (dam³)']
            
#             # Merge the DataFrames
#             df3 = pd.merge(df1_T, df2_T, on='Reservoir', how='left')
            
#             # Fill NaNs in 'Projected Total Inflow (dam³)' with 'NA'
#             df3['Projected Total Inflow (dam³)'] = df3['Projected Total Inflow (dam³)'].fillna('NA')
            
#             # Build dictionary of reservoirs owned by GoA
#             owned_by_GOA = ['Dickson Dam',
#                            'Glennifer Lake',
#                            'Travers',
#                            'Twin Valley',
#                            'Clear Lake',
#                            'Lake McGregor',
#                            'Oldman Reservoir',
#                            'Keho Reservoir',
#                            'Chain Lakes',
#                            'Pine Coulee',
#                            'Waterton',
#                            'St. Mary',
#                            'Payne Lake',
#                            'Milk River Ridge'
#                            ]
            
#             # Add a column with checkmark if in the list
#             df3['Owned By GoA'] = np.where(df3['Reservoir'].isin(owned_by_GOA), 'Yes', '')
            
#             # Reorder columns
#             df3 = df3[['Reservoir', 'Owned By GoA', '%FSL', 'Projected Total Inflow (dam³)']]
            
#             # Write results to Excel
#             output_file = os.path.join(output_dir, "SummaryTable_Reservoir.xlsx")
#             df3.to_excel(output_file, index=False, sheet_name='SummaryTable_Reservoir_new')
            
#             print(f" Reservoir summary table created: SummaryTable_Reservoir.xlsx")
            
#         else:
#             missing_files = []
#             if not os.path.exists(res_stor_path):
#                 missing_files.append("SumTab_%ResStor.xlsx")
#             if not os.path.exists(res_inflow_path):
#                 missing_files.append("SumTab_ResInflow.xlsx")
            
#             print(f" Missing required files for reservoir summary: {', '.join(missing_files)}")
#             print("   Skipping reservoir summary table creation.")
            
#     except Exception as e:
#         print(f" Error creating reservoir summary table: {str(e)}")
#         print("   Continuing with remaining processing...")
    
#     # STEP 4: Create weather forecast summary
#     print("\n" + "="*50)
#     print("STEP 4: Creating Weather Forecast Summary")
#     print("="*50)
    
#     weather_data = generator.create_weather_forecast_summary(
#         forecast_start_date=forecast_start_date,
#         moving_average_days=moving_average_days,
#         forecast_constant_files_path=str(forecast_constant_files_path),
#         wsa_input_path_template=str(forecast_input_path),
#         output_directory=str(output_dir)
#     )
    
#     # STEP 4.1: Fix weather forecast overlap and convert to CSV
#     print("\n" + "="*50)
#     print("STEP 4.1: Fixing Weather Forecast Overlap")
#     print("="*50)
    
#     csv_result = fix_weather_forecast_overlap(output_dir, start_week, end_week)
    
#     if csv_result:
#         print(f"SUCCESS: Weather forecast overlap fixed and CSV created")
#     else:
#         print("FAILED: Weather forecast processing failed")
    
#     # STEP 5: Integrate WISKI data
#     print("\n" + "="*50)
#     print("STEP 5: Integrating WISKI Reservoir Data")
#     print("="*50)
    
#     # Check if WISKI integration should be attempted
#     wiski_station_list_path = base_dir / "Wiski_Reservoire_file" / "WRMM_Reservoir_list.csv"
#     wiski_base_url = "http://wiskitsm1.goa.ds.gov.ab.ca:8080/KiWIS/KiWIS"
    
#     if wiski_station_list_path.exists():
#         try:
#             # Set up date parameters for WISKI data fetch
#             today_date = datetime.today().strftime('%Y-%m-%d')
#             wiski_date_params = {
#                 "from": "2025-01-01",
#                 "to": today_date
#             }
            
#             # Integrate WISKI data
#             wiski_combined_data = generator.integrate_wiski_data(
#                 station_list_path=str(wiski_station_list_path),
#                 wrmm_file_name=f'WK{start_week}_{end_week}_WrmmOutputs.csv',
#                 base_url=wiski_base_url,
#                 date_params=wiski_date_params
#             )
            
#             if not wiski_combined_data.empty:
#                 print(f" WISKI integration successful!")
#                 print(f"   - Combined dataset: {len(wiski_combined_data)} rows")
#                 print(f"   - Unique stations: {len(wiski_combined_data['Station'].unique())}")
                
#                 # Save additional analysis file
#                 analysis_file = output_dir / f"WISKI_Analysis_Summary_{today_date}.xlsx"
                
#                 # Create summary statistics
#                 wiski_summary = wiski_combined_data.groupby(['Station', 'DataSource']).agg({
#                     'Value': ['count', 'mean', 'std'],
#                     'Interval': ['min', 'max']
#                 }).round(2)
                
#                 with pd.ExcelWriter(analysis_file, engine='openpyxl') as writer:
#                     wiski_combined_data.to_excel(writer, sheet_name='Combined_Data', index=False)
#                     wiski_summary.to_excel(writer, sheet_name='Summary_Stats')
                
#                 print(f"   - Analysis saved: {analysis_file}")
                
#             else:
#                 print(" WISKI integration completed but no data was combined")
#                 wiski_combined_data = pd.DataFrame()
                
#         except Exception as e:
#             print(f" WISKI integration failed: {str(e)}")
#             print("   Continuing with standard processing...")
#             wiski_combined_data = pd.DataFrame()
#     else:
#         print(f"WISKI station list not found at: {wiski_station_list_path}")
#         print("   Skipping WISKI integration...")
#         wiski_combined_data = pd.DataFrame()
    
#     # STEP 6: Summary of completed processing
#     print("\n" + "="*50)
#     print("STEP 6: Processing Summary")
#     print("="*50)
    
#     print(f" Output directory: {output_dir}")
#     print(f" WRMM outputs processed: {outputs_for_powerbi}.csv")
    
#     # List all generated files
#     output_files = list(output_dir.glob("*"))
#     print(f" Total files generated: {len(output_files)}")
    
#     # Categorize files
#     excel_files = [f for f in output_files if f.suffix == '.xlsx']
#     csv_files = [f for f in output_files if f.suffix == '.csv']
    
#     print(f"   - Excel files: {len(excel_files)}")
#     print(f"   - CSV files: {len(csv_files)}")
    
#     # Enhanced reporting
#     if 'wiski_combined_data' in locals() and not wiski_combined_data.empty:
#         print(f" WISKI integration: SUCCESS")
#         print(f"   - Reservoir data combined from WISKI and WRMM")
    
#     if weather_data is not None:
#         print(f" Weather forecast: SUCCESS")
#         print(f"   - {len(weather_data)} stations processed")
    
#     # Check if reservoir summary was created
#     reservoir_summary_path = output_dir / "SummaryTable_Reservoir.xlsx"
#     if reservoir_summary_path.exists():
#         print(f" Reservoir summary table: SUCCESS")
#         print(f"   - Combined reservoir storage and inflow data")
    
#     print(f" Data type standardization: SUCCESS")
#     print(f"   - Updated terminology for better clarity")
    
#     print("\n" + "="*60)
#     print("WRMM PROCESSING COMPLETED SUCCESSFULLY!")
#     print("="*60)
    
#     return generator, weather_data


# ######################### Apportioment Automation

# # def extract_multiple_stations_from_hbdf(
# #     model_output_folder, current_year, start_week, end_week, output_dir, station_list
# # ):
# #     """
# #     Extract weekly data for selected stations from HBDF.txt into one CSV.
# #     Columns will be Year, Week, Simulated_<stationIdNoSpaces> for each requested station.

# #     - Matches station headers like: "C5C K04  2025   1 CMS"
# #     - Finds the 'YEAR ... Wk01..Wk52' header
# #     - Reads the row that starts with <current_year>
# #     - Keeps only weeks in [start_week, end_week]
# #     """
# #     import re
# #     from pathlib import Path
# #     import pandas as pd

# #     # Normalize stations input
# #     if isinstance(station_list, str):
# #         stations_to_find = [s.strip() for s in station_list.split(",") if s.strip()]
# #     else:
# #         stations_to_find = [str(s).strip() for s in station_list]

# #     print("\n" + "=" * 60)
# #     print("SIMPLE MULTI-STATION HBDF DATA EXTRACTION (robust)")
# #     print("=" * 60)
# #     print(f"   - Target stations: {stations_to_find}")
# #     print(f"   - Year: {current_year} | Week range: {start_week}..{end_week}")

# #     # Locate HBDF file
# #     hbdf_file_path = (
# #         Path(model_output_folder) / "S0" / str(current_year) / "SSRB" / "HBDF.txt"
# #     )
# #     if not hbdf_file_path.exists():
# #         for alt in [
# #             Path(model_output_folder) / "S0" / "HBDF.txt",
# #             Path(model_output_folder) / "HBDF.txt",
# #             Path(model_output_folder) / "S0" / str(current_year) / "HBDF.txt",
# #         ]:
# #             if alt.exists():
# #                 hbdf_file_path = alt
# #                 break
# #     if not hbdf_file_path.exists():
# #         print("   - ERROR: HBDF file not found in expected locations.")
# #         return pd.DataFrame()

# #     print(f"   - Using HBDF file: {hbdf_file_path}")

# #     # Read file into memory
# #     with open(hbdf_file_path, "r", encoding="utf-8", errors="ignore") as f:
# #         lines = f.readlines()

# #     # Helper regexes
# #     # A station header looks like: "C5C K04  2025   1 CMS"
# #     # We'll detect any station header line to know where a station block starts/ends.
# #     station_header_any_re = re.compile(r"^\s*[A-Z0-9]{3}\s+[A-Z0-9]{2,3}\s+\d{4}\s+", re.ASCII)
# #     # Data header line starts with "YEAR" then Wk01..Wk52 labels (but we only need to know where it is)
# #     year_header_re = re.compile(r"^\s*YEAR\s+", re.IGNORECASE)
# #     # Data row for a specific year
# #     year_row_re = re.compile(rf"^\s*{current_year}\s+")

# #     # Build a quick index of all station-header line numbers (for block slicing)
# #     header_indices = []
# #     for idx, raw in enumerate(lines):
# #         if station_header_any_re.match(raw):
# #             header_indices.append(idx)
# #     header_indices.append(len(lines))  # sentinel for last block end

# #     # Extractor for one station block
# #     def extract_station_for_year(station_code: str):
# #         """
# #         Finds the block for `station_code` and returns a list of 52 floats for current_year,
# #         or None if not found.
# #         """
# #         # Match the exact station header like: "C5C K04  2025   1 CMS"
# #         station_header_exact_re = re.compile(
# #             rf"^\s*{re.escape(station_code)}\s+\d{{4}}\s+\d+\s+[A-Z]+", re.ASCII
# #         )

# #         # Find the block start index
# #         block_start = None
# #         for i in range(len(lines)):
# #             if station_header_exact_re.match(lines[i]):
# #                 block_start = i
# #                 break
# #         if block_start is None:
# #             # Try a normalized match: collapse multiple spaces
# #             norm_target = " ".join(station_code.split())
# #             for i in range(len(lines)):
# #                 norm_line = " ".join(lines[i].strip().split())
# #                 if norm_line.startswith(norm_target + " "):  # followed by year
# #                     # still ensure year immediately follows
# #                     if re.search(r"\b\d{4}\b", norm_line):
# #                         block_start = i
# #                         break
# #         if block_start is None:
# #             print(f"     - Station '{station_code}' not found.")
# #             return None

# #         # Determine block end = next station header after block_start
# #         next_headers = [h for h in header_indices if h > block_start]
# #         block_end = next_headers[0] if next_headers else len(lines)

# #         # Now search inside block for the 'YEAR' header and the row for current_year
# #         block = lines[block_start:block_end]

# #         # Find the line index of YEAR header within block (optional but helpful sanity)
# #         # Not strictly required—some HBDFs skip printing the labels—but we proceed even if not found
# #         data_row_line = None
# #         for k, raw in enumerate(block):
# #             if year_row_re.match(raw):
# #                 data_row_line = k
# #                 break

# #         if data_row_line is None:
# #             # Some files might wrap or have extra spaces; try a forgiving search
# #             for k, raw in enumerate(block):
# #                 if str(current_year) in raw[:10]:
# #                     # make sure it starts the row
# #                     if re.match(rf"^\s*{current_year}\s+", raw):
# #                         data_row_line = k
# #                         break

# #         if data_row_line is None:
# #             print(f"     - Year {current_year} row not found for '{station_code}'.")
# #             return None

# #         # Parse the year row into 52 floats
# #         parts = block[data_row_line].split()
# #         # Expect 1 (year) + 52 week values = 53 tokens
# #         if len(parts) < 53:
# #             print(f"     - Warning: Expected 53 columns, got {len(parts)} for '{station_code}'. Skipping.")
# #             return None

# #         try:
# #             week_vals = [float(x) for x in parts[1:53]]
# #         except ValueError:
# #             print(f"     - Warning: Non-numeric week value in '{station_code}' row. Skipping.")
# #             return None

# #         return week_vals

# #     # Gather all data
# #     per_station_values = {}
# #     found = []
# #     for st in stations_to_find:
# #         vals = extract_station_for_year(st)
# #         if vals is not None:
# #             per_station_values[st] = vals
# #             found.append(st)

# #     if not found:
# #         print("   - ERROR: No requested stations were found with data.")
# #         return pd.DataFrame()

# #     # Build output rows for requested week window
# #     # Weeks are 1-based, so slice indices are start_week-1 : end_week
# #     records = []
# #     for wk in range(start_week, end_week + 1):
# #         row = {"Year": int(current_year), "Week": int(wk)}
# #         for st in found:
# #             col = f"Simulated_{st.replace(' ', '')}"
# #             row[col] = per_station_values[st][wk - 1]  # 0-based index
# #         records.append(row)

# #     df = pd.DataFrame.from_records(records).sort_values(["Year", "Week"]).reset_index(drop=True)

# #     # Save CSV
# #     safe_name = "_".join(s.replace(" ", "") for s in stations_to_find)
# #     if len(safe_name) > 50:
# #         safe_name = f"{len(stations_to_find)}stations"
# #     out_name = f"MultiStation_{safe_name}_WK{start_week}_WK{end_week}_Data.csv"
# #     out_path = Path(output_dir) / out_name
# #     df.to_csv(out_path, index=False)

# #     print("\n" + "=" * 60)
# #     print("EXTRACTION SUMMARY")
# #     print("=" * 60)
# #     print(f"   • Stations found: {found}")
# #     print(f"   • Rows written: {len(df)}")
# #     print(f"   • Output: {out_path.name}")
# #     print(f"   • Columns: {list(df.columns)}")

# #     return df

# #### Apportioment Step-2

# # --- inputs ---


# #### 


# ############################### Apportioment Ends


# # Add these imports at the beginning of your code
# import pandas as pd
# import os
# import shutil
# from datetime import datetime, timedelta
# import numpy as np
# import warnings
# from pathlib import Path
# import sys
# warnings.filterwarnings('ignore')

# # Import your custom modules
# from WRMMDataProcessor import WRMMDataProcessor
# from SummaryTableGenerator import SummaryTablesGenerator

# # ===== AUTOMATIC INPUT FILE SETUP =====
# print("="*60)
# print("STARTING AUTOMATIC WRMM PROCESSING")
# print("="*60)

# # Define Base Path
# base_dir = Path(r'D:/Sopan/HGS_Data/Codes/WRMM/WRMM_Package/WRMM_For BEN/WRMM_Package')

# # Setup Working Directory and System Path
# os.chdir(base_dir)
# sys.path.append(str(base_dir))

# # ===== STEP 0: AUTOMATIC INPUT FILE DETECTION AND SETUP =====
# print("\n" + "="*50)
# print("STEP 0: Automatic Input File Detection and Setup")
# print("="*50)

# setup_result = auto_setup_input_files(base_dir)

# if setup_result is None:
#     print(" SETUP FAILED: Could not automatically detect and setup input files")
#     print("   Please check the source directory and file structure")
#     exit(1)

# # Extract automatically detected parameters
# start_week, end_week, current_year = setup_result

# print(f"\nAUTOMATIC SETUP SUCCESSFUL!")
# print(f"   - Detected Week Range: WK{start_week} to WK{end_week}")
# print(f"   - Year: {current_year}")

# # ===== AUTOMATED CONFIGURATION BASED ON DETECTED WEEK NUMBERS =====
# print("\n" + "="*50)
# print("AUTOMATED FORECAST PARAMETER CALCULATION")
# print("="*50)

# # Configuration variables (some automatic, some manual)
# apptchl_id = 104
# moving_average_days = 14
# seconds_in_day = 24 * 3600

# # ===== AUTOMATICALLY CALCULATE FORECAST PARAMETERS =====
# forecast_params = calculate_forecast_parameters(start_week, end_week, current_year)

# # Extract calculated values
# forecast_start_date = forecast_params['forecast_start_date']
# geps_start_date = forecast_params['geps_start_date']
# geps_end_date = forecast_params['geps_end_date']
# month = forecast_params['month']
# date = forecast_params['date']
# formatted_date = forecast_params['formatted_date']

# print(f" Calculated Parameters for WK{start_week} to WK{end_week}:")
# print(f"   - Forecast Start Date: {forecast_start_date}")
# print(f"   - GEPS Start Date: {geps_start_date} (forecast + 1 day)")
# print(f"   - GEPS End Date: {geps_end_date} (forecast + 39 days)")
# print(f"   - Month: {month}")
# print(f"   - Date: {date}")
# print(f"   - Formatted Date: {formatted_date}")
# print("")

# # ===== AUTOMATED PATH GENERATION BASED ON DETECTED PARAMETERS =====
# input_folder_name = f"INPUT_DATA_WK{start_week}_WK{end_week}"
# input_data_dir = base_dir / input_folder_name

# # ===== AUTOMATED MODEL OUTPUT FOLDER NAMING =====
# model_output_folder = input_data_dir / f"Results_week_WK{start_week}_to_WK{end_week}_{current_year}"

# reference_file_base_dir = input_data_dir / f"Reference_File_WK{start_week}_WK{end_week}"
# apportionment_base_dir = input_data_dir / f"Apportment_input_data_WK{start_week}_WK{end_week}"
# forecast_constant_files_path = base_dir / "Forecast_Constant_files_1950_2019"
# forecast_input_path = input_data_dir / f"Forecast_Summary_Data_Input_WK{start_week}_WK{end_week}"

# # ===== AUTOMATED OUTPUT DIRECTORY PREPARATION =====
# outputs_for_powerbi = f'WK{start_week}_{end_week}_WrmmOutputs'
# timestamp = datetime.now().strftime("%Y%m%d%H%M")
# output_dir = base_dir / f'Dashboard_Data_WK_{start_week}_{end_week}_{timestamp}'
# if output_dir.exists():
#     shutil.rmtree(output_dir)
# output_dir.mkdir(parents=True, exist_ok=True)

# # ==== Move Apportioment Data file from Input to Output =====
# # After you create output_dir
# temp_multistation = input_data_dir / "Multistation_file.csv"
# final_multistation = output_dir / "Multistation_file.csv"

# if temp_multistation.exists():
#     shutil.move(str(temp_multistation), str(final_multistation))
#     print(f"Moved Multistation_file.csv to: {final_multistation}")
# else:
#     print("WARNING: temp Multistation_file.csv not found in INPUT directory.")


# # ===== AUTOMATED FILE PATH GENERATION =====
# reference_file_names = [reference_file_base_dir / "Reference_file_S0.xlsx"]
# apportioment_input_file = apportionment_base_dir / f"Apportionment_summary_WK{start_week}_WK{end_week}.xlsx"
# apportioment_output_file = output_dir / f"Apportionment_Dashboard_summary_week{start_week}_{end_week}.csv"

# print("="*60)
# print("STARTING MAIN PROCESSING WITH AUTO-DETECTED PARAMETERS")
# print("="*60)
# print(f"Using automatically detected week range: WK{start_week} to WK{end_week}")
# print(f" Using automatically calculated forecast_start_date: {forecast_start_date}")
# print(f" GEPS Start Date: {geps_start_date}")
# print(f" GEPS End Date: {geps_end_date}")
# print(f" Model output folder: {model_output_folder}")
# print(f" Input data directory: {input_data_dir}")
# print("")

# # Verify all required directories exist before processing
# print(" VERIFYING INPUT FILE STRUCTURE:")
# required_paths = [
#     ("Model output folder", model_output_folder),
#     ("Reference file directory", reference_file_base_dir),
#     ("Apportionment directory", apportionment_base_dir),
#     ("Forecast input directory", forecast_input_path),
#     ("Reference file", reference_file_names[0]),
#     ("Apportionment input file", apportioment_input_file)
# ]

# all_paths_exist = True
# for description, path in required_paths:
#     if path.exists():
#         print(f"    OK {description}: {path}")
#     else:
#         print(f"    MISSING {description}: {path}")
#         all_paths_exist = False

# if not all_paths_exist:
#     print("\n ERROR: Some required input files or directories are missing!")
#     print("   Please check the input file setup process.")
#     exit(1)

# print(f"\n ALL INPUT FILES VERIFIED - PROCEEDING WITH PROCESSING")
# print("")

# # Execute the main processing
# main_processing_with_wiski_integration()



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

# ==== Build Multistation_file.csv directly in output_dir ====
# print("\n=== BUILDING Multistation_file.csv ===")
# build_multistation_file(
#     base_dir=base_dir,
#     start_week=start_week,
#     end_week=end_week,
#     current_year=current_year,
#     output_dir=output_dir,
#     # Optional overrides if needed:
#     # csv_path_override=r"\\c-goa-apm-13251\WaterManagementDashboard_13251\PBI_Data\W_MGMT_4_2025.csv",
#     # ppwb_path=base_dir / "APPENDIX 3 2025 July.xlsx",
# )
# print(f"   - Done: {output_dir / 'Multistation_file.csv'}")

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
