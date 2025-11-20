# # Import necessary libraries
# import pyodbc
# import pandas as pd
# import os
# import shutil
# import re
# import numpy as np
# import math
# import warnings
# from openpyxl import Workbook
# from openpyxl.utils.dataframe import dataframe_to_rows
# import requests
# import io
# from datetime import datetime



# warnings.filterwarnings('ignore')

# #### New Optimized functions

# import pandas as pd
# import numpy as np
# import os
# from WRMMDataProcessor import WRMMDataProcessor

# ##### Integrate WISKI Data
# import requests
# import io


# class SummaryTablesGenerator:
#     """
#     A class for generating and processing summary tables from model outputs.

#     This class provides methods to process model outputs, prepare summary tables
#     """
    
#     @staticmethod
#     def process_model_outputs(model_output_folder, reference_file_names, output_dir, outputs_for_powerbi,current_year, start_week, end_week, seconds_in_day, apptchl_id):
#         """
#         Process model outputs and generate summary data.

#         Args:
#             model_output_folder (str): Path to the folder containing model outputs.
#             reference_file_names (list): List of reference file names.
#             output_dir (str): Directory to save output files.
#             outputs_for_powerbi (str): Name of the output file for Power BI.
#             current_year (int): The current year for processing.
#             start_week (int): Start week for data processing.
#             end_week (int): End week for data processing.
#             seconds_in_day (int): Number of seconds in a day.
#             apptchl_id (int): ID for the apportionable channel.

#         Returns:
#             tuple: Contains processed data and parameters for further analysis.
#         """
#         # Model outputs folder
#         model_output_dir = os.path.join(os.getcwd(), model_output_folder)

#         # Empty df to store data
#         master_outsim_id = pd.DataFrame([])
#         master_data_file = pd.DataFrame([])
#         master_ex_summary = pd.DataFrame([])
#         master_ex_summary2= pd.DataFrame([])
#         hbdf_maa_natflow = pd.DataFrame([])
#         divchl_summary_tab = pd.DataFrame([])
#         master_res_inflow_annual = pd.DataFrame([])
#         master_major_data_io = pd.DataFrame([])
#         master_major_data_wco = pd.DataFrame([])
#         master_major_cap_tab = pd.DataFrame([])

#         subtab_priv_irr_all = pd.DataFrame([])
#         subtab_priv_irr_sen = pd.DataFrame([])
#         subtab_priv_irr_jun_io = pd.DataFrame([])
#         subtab_priv_irr_jun_wco = pd.DataFrame([])

#         # Get scenario folder dir
#         scn_dir = [folder for folder in os.listdir(model_output_dir)]
#         for scn, reference_file_name in zip(scn_dir, reference_file_names):
#             # scenario_name = scn.split('_')[1] # scenario_short_name
#             scenario_name = scn # scenario_short_name
#             ex_summary = pd.DataFrame([])
#             hbdf_io = pd.DataFrame([])
#             hbdf_wco = pd.DataFrame([])
#             divchl_year = pd.DataFrame([])
#             res_inflow_year = pd.DataFrame([])
            
#             # Get sub-folder dir
#             sub_dir = [folder for folder in os.listdir(os.path.join(os.getcwd(), model_output_folder, scn))]
#             for year in sub_dir:
#                 # Get model name dir (# name of the mdb data folder)
#                 model_dir = os.path.join(os.getcwd(), model_output_folder, scn, year)
#                 path_name_list = [folder for folder in os.listdir(model_dir)]
                
#                 # Create an instance of SSRBDataProcessor
#                 processor = WRMMDataProcessor(model_dir, path_name_list, reference_file_name, seconds_in_day)
                
#                 full_wk_end_date = processor.get_weekend_dates(current_year)
                
#                 # Read all outsimoutid mdb files and make a df
#                 outsim_id = processor.read_OutsimOutid(model_dir, path_name_list,start_week,end_week)
                
#             ##### SOPAN ADDEDDDD
#                 outsim_id_full = processor.read_OutsimOutid_full_year(model_dir, path_name_list)
#                 # print("OUSTDIM_ID: ", outsim_id_full)
#                 outsim_id_full = outsim_id_full.loc[((outsim_id_full.ComponentType == 'MAJOR')|\
#                             (outsim_id_full.ComponentType == 'RESERV')|\
#                             (outsim_id_full.ComponentType == 'IRRIGAT')|\
#                             (outsim_id_full.ComponentType == 'DIVCHL')|\
#                             (outsim_id_full.ComponentType == 'RETURN')|\
#                             (outsim_id_full.ComponentType == 'NATCHL'))]
                            
#                 # Prepare a df for irrigation area based on respective model's SCF
#                 irr_area = processor.read_irrigation_area(model_dir, path_name_list)
                
#                 # Read DIVCHL annual maximum capacity
#                 ## Sopan --- Looks like divchl_cap hasnt been used anywhere
                
#                 divchl_cap = processor.read_divchl_maxcap(model_dir, path_name_list) 

#                 # Keep selected components from conponent type list
#                 outsim_id = outsim_id.loc[((outsim_id.ComponentType == 'MAJOR')|\
#                             (outsim_id.ComponentType == 'RESERV')|\
#                             (outsim_id.ComponentType == 'IRRIGAT')|\
#                             (outsim_id.ComponentType == 'DIVCHL')|\
#                             (outsim_id.ComponentType == 'RETURN')|\
#                             (outsim_id.ComponentType == 'NATCHL'))]

#                 # get major div cap volume in dam3
#                 major_div_cap = processor.get_major_div_cap(model_dir, path_name_list) 
                
#                 # get major data
#                 major_mdb = outsim_id[outsim_id.ComponentType == 'MAJOR']
                
#                 # get data without major
#                 df_without_major = outsim_id[outsim_id.ComponentType != 'MAJOR']
#                 df_without_major=df_without_major[(df_without_major.Interval >= start_week) & (df_without_major.Interval <= end_week)]
                
#                 # revise major IdealCondition data 
#                 # Sopan --- 52 week summation takes place in the following function SUM
            
#                 revised_major_ideal = processor.revise_major_idealcondition_data(major_mdb, major_div_cap,seconds_in_day, start_week, end_week)
#                 # add back major to the main df
#                 df_with_revised_major = pd.concat([df_without_major,revised_major_ideal], axis=0)
                
#                 # update outsim_id data
#                 outsim_id = df_with_revised_major

#                 # Create temporary outsim_id to store data
#                 outsim_id_temp = outsim_id.copy()
#                 outsim_id_temp.insert(0, 'Scenario', scenario_name + '_' + str(year))
#                 master_outsim_id = pd.concat([master_outsim_id, outsim_id_temp], axis=0)

#                 # Export data
#                 outsim_id.to_csv(os.path.join(output_dir, 'Outsim_id_' + scenario_name + '.csv'), index=False)
#                 irr_area.to_csv(os.path.join(output_dir, 'Irr_area_' + scenario_name + '.csv'), index=False)

#                 # Diversion
#                 divchl_mdb = outsim_id[outsim_id.ComponentType == 'DIVCHL']
#                 div_ref_file = pd.read_excel(reference_file_name, 'Irrigation_diversion')
                
#                 # Sopan --- Calculating Annual Summary .. Scope for 5 weeks
                
#                 # diversion_summary = estimate_annual_div_vol(divchl_mdb, div_ref_file)
#                 diversion_summary = processor.estimate_annual_div_vol(divchl_mdb, div_ref_file, seconds_in_day,start_week, end_week)
                
#                 diversion_summary.columns = ['Component Name', scenario_name]
#                 diversion_summary['Diversion Year'] = year
#                 diversion_summary['Diversion Year'] = pd.to_numeric(diversion_summary['Diversion Year'])
#                 diversion_summary.set_index(['Component Name', 'Diversion Year'],  inplace=True)
#                 divchl_summary_tab = pd.concat([divchl_summary_tab, diversion_summary], axis=1)


#                 # Irrigation
#                 # ------------------------------------------------------
#                 # Process irrigation data
                
#                 # private irrigation - all
#                 #Sopan --- Why don't just drop the columns instead of converting to the list
                
#                 irr_ref_file = pd.read_excel(reference_file_name, sheet_name = 'Irrigation')
#                 irr_priv_all = irr_ref_file[irr_ref_file.columns.to_list()[:-2]]

#                 # private irrigation - senior
#                 irr_priv_sen = irr_ref_file[irr_ref_file.Private_priority == 'Senior']
#                 irr_priv_sen = irr_priv_sen[irr_priv_sen.columns.to_list()[:-2]]

#                 # private irrigation - junior - io
#                 irr_priv_jun_io = irr_ref_file[irr_ref_file.Private_Junior_ST == 'Subject to IO']
#                 irr_priv_jun_io = irr_priv_jun_io[irr_priv_jun_io.columns.to_list()[:-2]]

#                 # private irrigation - junior - wco
#                 irr_priv_jun_wco = irr_ref_file[irr_ref_file.Private_Junior_ST == 'Subject to WCO']
#                 irr_priv_jun_wco = irr_priv_jun_wco[irr_priv_jun_wco.columns.to_list()[:-2]]
                
#                 try:
#                     # private irrigation - all
#                     irr_priv_all = processor.process_private_irrigation(irr_priv_all, outsim_id, irr_area, 'PI', scenario_name)
#                     subtab_priv_irr_all = pd.concat([subtab_priv_irr_all,irr_priv_all], axis=0)
#                 except:
#                     pass
                
#                 try:
#                     # private irrigation - senior
#                     irr_priv_sen = processor.process_private_irrigation(irr_priv_sen, outsim_id, irr_area, 'PI-SEN', scenario_name)
#                     subtab_priv_irr_sen = pd.concat([subtab_priv_irr_sen,irr_priv_sen], axis=0)  
#                 except:
#                     pass
                
#                 try:
#                     # private irrigation - junior - io
#                     irr_priv_jun_io = processor.process_private_irrigation(irr_priv_jun_io, outsim_id, irr_area, 'PI-IO', scenario_name)
#                     subtab_priv_irr_jun_io = pd.concat([subtab_priv_irr_jun_io,irr_priv_jun_io], axis=0)
#                 except:
#                     pass
                
#                 try:
#                     # private irrigation - junior - wco
#                     irr_priv_jun_wco = processor.process_private_irrigation(irr_priv_jun_wco, outsim_id, irr_area, 'PI-WCO', scenario_name)
#                     subtab_priv_irr_jun_wco = pd.concat([subtab_priv_irr_jun_wco,irr_priv_jun_wco], axis=0)
#                 except:
#                     pass

#                 irr_data_with_area = processor.process_irrigation_data(reference_file_name,outsim_id, irr_area)

#                 irr_data = irr_data_with_area[['ModelName', 'ComponentType', 'ComponentName', 'ComponentNumber',
#             'Year', 'Interval', 'IdealCondition', 'Simulated', 'Unit','Deficit']]


#                 # Seperate demand and deficit data
#                 irr_ideal = processor.get_demand_deficit_data(category='Irrigation',data_type='Demand',df=irr_data,scn_name=scenario_name)
#                 irr_deficit = processor.get_demand_deficit_data(category='Irrigation',data_type='Deficit',df=irr_data,scn_name=scenario_name)

#                 # Combine irrigation demand and deficit data
#                 irr_data = pd.concat([irr_ideal, irr_deficit], axis = 0)
                
#                 # add irrigation area
#                 irr_data = irr_data.set_index(['ModelName', 'ComponentType', 'ComponentName', 'Year', 'Interval']).\
#                     join(irr_data_with_area.set_index(['ModelName', 'ComponentType', \
#                                                     'ComponentName', 'Year', 'Interval'])['TotalIrrArea_Ha'])
#                 irr_data.reset_index(inplace=True)
                

#                 # Non-irrigation: MAJOR except MW 642
#                 # ------------------------------------------------------
#                 # Process non-irrigation data
                

#                 # Get data for major only
#                 major = outsim_id.reset_index()[['ModelName', 'Year', 'Interval', 'ComponentType', 'ComponentNumber',
#                     'Units', 'ComponentDescription', 'Simulated', 'IdealCondition']]
#                 major = major[major['ComponentType']== 'MAJOR']
#                 major_col = list(major.columns) # get column names
#                 if end_week == 52:
#                     major['Simulated_dam3'] = np.where(
#                         (major.Interval == end_week),
#                         (major.Simulated * 8 * seconds_in_day) / 1000,  # 8 days for the last week
#                         (major.Simulated * 7 * seconds_in_day) / 1000   # 7 days for other weeks
#                     )

#                     major['IdealCondition_dam3'] = np.where(
#                         (major.Interval == end_week),
#                         (major.IdealCondition * 8 * seconds_in_day) / 1000,  # 8 days for the last week
#                         (major.IdealCondition * 7 * seconds_in_day) / 1000   # 7 days for other weeks
#                     )
#                 else:
#                     major['Simulated_dam3'] = (major.Simulated * 7 * seconds_in_day) / 1000
#                     major['IdealCondition_dam3'] = (major.IdealCondition * 7 * seconds_in_day) / 1000


#                 major = major[(major['Interval'] >= start_week) & (major['Interval'] <= end_week)]

#                 major.reset_index(inplace = True)
#                 major = major[major_col]

#                 # Delete Unit column
#                 del major['Units']

#                 # Read reference file for major
#                 major_ref_file = pd.read_excel(reference_file_name, sheet_name = 'Major')
#                 major_ref_file = major_ref_file[major_ref_file.columns.to_list()[:-2]]

#                 # Set index to join data
#                 major_ref_file.set_index(['ModelName', 'ComponentNumber'], inplace = True)
#                 major.set_index(['ModelName', 'ComponentNumber'], inplace = True)

#                 # Add component's name and sub-basin
#                 major_table = major.join(major_ref_file)
                
#                 # Remove unused data (removed MW 642)
#                 major_table = major_table.dropna(subset= 'SubBasin')
                
#                 # Process mejor data
#                 ### Sopan Edited
#                 major_data = processor.process_major_data(major_table)

#                 # Seperate demand and deficit
#                 major_ideal = processor.get_demand_deficit_data(category='Non-irrigation',data_type='Demand',df=major_data,scn_name=scenario_name)
#                 major_deficit = processor.get_demand_deficit_data(category='Non-irrigation',data_type='Deficit',df=major_data,scn_name=scenario_name)

#                 # Combine major demand and deficit data
#                 major_data = pd.concat([major_ideal, major_deficit], axis = 0)
                
#                 # Major Subject to IO and WCO
#                 # ---------------------------
#                 # Read reference file for major s/t IO
#                 major_ref_file = pd.read_excel(reference_file_name, sheet_name = 'Major')
#                 # Keep only junior data
#                 major_ref_file = major_ref_file[major_ref_file.Priority == 'Junior']
#                 del major_ref_file['Priority']
                
#                 major_ref_file_io = major_ref_file[major_ref_file.Junior_ST == 'Subject to IO']
#                 major_table_io = major_table.loc[major_ref_file_io.set_index(['ModelName', 'ComponentNumber']).index]

#         ## Sopan Edited
#                 major_data_io = processor.process_major_data(major_table_io)
                
#                 # Seperate demand and deficit
#                 major_ideal_io = processor.get_demand_deficit_data(category='Non-irrigation',data_type='Demand',df=major_data_io,scn_name=scenario_name)
#                 major_deficit_io = processor.get_demand_deficit_data(category='Non-irrigation',data_type='Deficit',df=major_data_io,scn_name=scenario_name)
                
#                 # Combine major demand and deficit data
#                 major_data_io = pd.concat([major_ideal_io, major_deficit_io], axis = 0)
                
                
#                 # Read reference file for major s/t WCO
#                 major_ref_file_wco = major_ref_file[major_ref_file.Junior_ST == 'Subject to WCO']
#                 major_table_wco = major_table.loc[major_ref_file_wco.set_index(['ModelName', 'ComponentNumber']).index]
            
#                 # major_data_wco = process_major_data(major_table_wco)   
#                 ### Sopan Edition
#                 major_data_wco = processor.process_major_data(major_table_wco)
                
#                 # Seperate demand and deficit
#                 major_ideal_wco = processor.get_demand_deficit_data(category='Non-irrigation',data_type='Demand',df=major_data_wco,scn_name=scenario_name)
#                 major_deficit_wco = processor.get_demand_deficit_data(category='Non-irrigation',data_type='Deficit',df=major_data_wco,scn_name=scenario_name) 
#                 major_data_wco = pd.concat([major_ideal_wco, major_deficit_wco], axis = 0)
                
                
#                 # Reservoir:
#                 # ------------------------------------------------------
#                 # Process reservoir elevatiuon data
#                 res_elev_stor = processor.get_reservoir_elevation_storage()

#                 # Read reference file
#                 res_ref_file = pd.read_excel(reference_file_name, sheet_name = 'Reservoir')

#                 # Drop dummy reservoir data
#                 res_ref_file = res_ref_file[res_ref_file.columns[:3]]
#                 res_ref_file.drop(res_ref_file[res_ref_file.ComponentName == 'Drop'].index, inplace=True)
#                 res_ref_file.set_index(['ModelName','ComponentNumber'], inplace=True)

#                 # Add reference names
#                 outsim_id.set_index(['ModelName','ComponentNumber'], inplace=True)
#                 res_data = outsim_id.join(res_ref_file)
#         #### Sopan Edited
#                 res_data = res_data[(res_data.Interval >= start_week) & (res_data.Interval <= end_week)]

#                 # Drop unnecessary data
#                 res_data = res_data.dropna(subset= 'ComponentName')
#                 res_data.reset_index(inplace=True)

#                 # Rearrange data
#                 res_data = res_data[['ModelName','ComponentType','ComponentName','ComponentNumber', 'Year', 'Interval','IdealCondition','Simulated']]
#                 res_data['Unit']='Meter'

#                 # Get reservoir list to estimate storage
#                 res_lst = [(model, number) for model in res_data.ModelName.unique() for number in res_data[res_data['ModelName'] == model].ComponentNumber.unique()]

#                 # Set identical index
#                 res_elev_stor.set_index(['ModelName', 'ComponentNumber'], inplace=True)
#                 res_data.set_index(['ModelName', 'ComponentNumber'], inplace=True)
#                 RESSS_1 = res_data.copy()

#         #### Sopan CODE for estimated Percentatge

#                 # Drop unnecessary data
#                 outsim_id_full.reset_index(inplace=True)

#                 # Rearrange data
#                 outsim_id_full = outsim_id_full[['ModelName','ComponentType','ComponentNumber', 'Year', 'Interval','IdealCondition','Simulated']]
#                 outsim_id_full['Unit']='Meter'

#                 # Set identical index
#                 outsim_id_full.set_index(['ModelName', 'ComponentNumber'], inplace=True)

#         ### percentage modified code ends
            
#                 res_data = processor.estimate_percent_of_storage(res_lst, res_elev_stor,res_data,outsim_id_full)
#                 res_data.reset_index(inplace=True)
                
#                 # Data for reservoir target/ideal condition
#                 res_data_target = res_data.copy()
#                 res_data_target.insert(0, 'Data_type', ['Target_' + scenario_name for n in range(len(res_data_target.Interval))])
#                 res_data_target = res_data_target.drop(['Simulated', 'PerStorage'], axis=1)
#                 res_data_target['Comments'] = ['Reservoir rule curve' for n in range(len(res_data_target.Interval))]  
#                 res_data_target.columns = ['Data_type', 'ModelName', 'ComponentNumber', 'ComponentType',
#                     'ComponentName', 'Year', 'Interval', 'Value', 'Unit','Comments'] 
#                 res_data_target = res_data_target[['Data_type', 'ModelName', 'ComponentType', 'ComponentName',
#                     'ComponentNumber', 'Year', 'Interval', 'Value', 'Unit', 'Comments']]

#                 # Data for reservoir simulated elevation
#                 res_data_simulated = res_data.copy()
#                 res_data_simulated = res_data_simulated.drop('IdealCondition', axis=1)
#                 res_data_simulated.insert(0, 'Data_type', [scenario_name for n in range(len(res_data_simulated.Interval))])
#                 res_data_simulated['Comments'] = ['Simulated elevation and % of storage' for n in range(len(res_data_simulated.Interval))]
#                 res_data_simulated = res_data_simulated.rename(columns = {'Simulated': 'Value'})

#                 # Combine reservoir target and simulation data
#                 res_data = pd.concat([res_data_target, res_data_simulated], axis=0)
                
#         # WCO Data
#                 # ------------------------------------------------------
#                 # Read WCO reference file
#                 wco_ref_file = pd.read_excel(reference_file_name, sheet_name = 'WCO')
#                 model_wco_lst = list(wco_ref_file.ModelName.unique())
                
#                 # get all wco data from hbdfs
#                 for model in model_wco_lst:
#                     hbdf_dir = os.path.join(model_dir, model) # get model path to read hbdf file
#                     wco_ref_file = wco_ref_file[wco_ref_file.ModelName == model]

#                     hbdf_df = processor.read_hbdf_based_on_ref(hbdf_dir, wco_ref_file, model, 'WCO')
#                     hbdf_wco = pd.concat([hbdf_wco, hbdf_df], axis=0)

#                 # Read WCO reference file
#                 wco_ref_file = pd.read_excel(reference_file_name, sheet_name = 'WCO')
                    
#                 # Get natural channel data
#                 natchl_wco_data = outsim_id[outsim_id.ComponentType == 'NATCHL']
            
#         ### Sopan Edited    
#                 natchl_wco_data = natchl_wco_data[(natchl_wco_data.Interval >= start_week) & (natchl_wco_data.Interval <= end_week)]
            
#                 # Process wco data
#                 natchl_wco_data = processor.process_wco_data(natchl_wco_data,wco_ref_file, hbdf_wco)
                
#                 # WCO Target
#                 natchl_wco_data_target = natchl_wco_data[['ModelName','ComponentType','ComponentName','ComponentNumber','Year','Interval',
#             'WCO','Unit']]

#                 natchl_wco_data_target = natchl_wco_data_target.rename(columns = {'WCO': 'Value'})
#                 natchl_wco_data_target['Comments'] = 'WCO Target'
#                 natchl_wco_data_target.insert(0, 'Data_type', ['Target_' + scenario_name for n in range(len(natchl_wco_data_target.Interval))])

#                 # WCO Simulated
#                 natchl_wco_data_sim = natchl_wco_data[['ModelName','ComponentType','ComponentName','ComponentNumber','Year','Interval',
#             'Simulated','Unit', 'WCO_Failed']]

#                 natchl_wco_data_sim = natchl_wco_data_sim.rename(columns = {'Simulated': 'Value'})
#                 natchl_wco_data_sim['Comments'] = 'WCO Simulated'
#                 natchl_wco_data_sim.insert(0, 'Data_type', [scenario_name for n in range(len(natchl_wco_data_sim.Interval))])

#                 # Combine wco data
#                 natchl_wco_data = pd.concat([natchl_wco_data_target, natchl_wco_data_sim], axis=0)
                
                

#                 # IO Data
#                 # ------------------------------------------------------
                
#                 # read io reference file
#                 io_ref_file = pd.read_excel(reference_file_name, sheet_name = 'IO')

#                 # keep data which has only hbdf value
#                 io_ref_file = io_ref_file.dropna(subset=['HBDF_Key'])

#                 # get model name for respective hbdfs
#                 model_io_lst = list(io_ref_file.ModelName.unique())

#                 # combine all hbdf io value
#                 for model in model_io_lst:
#                     hbdf_dir = os.path.join(model_dir, model) # get model path to read hbdf file
#                     io_ref_file = io_ref_file[io_ref_file.ModelName == model]
#                     hbdf_io_data = processor.read_hbdf_based_on_ref(hbdf_dir, io_ref_file, model, 'IO') 
#                     hbdf_io = pd.concat([hbdf_io, hbdf_io_data], axis=0)        
                    
#                 # restore IO reference file
#                 io_ref_file = pd.read_excel(reference_file_name, sheet_name = 'IO')

#                 # Get natural channel data
#                 natchl_io_data = outsim_id[outsim_id.ComponentType == 'NATCHL']

#         ### Sopan Edited
#                 natchl_io_data = natchl_io_data[(natchl_io_data.Interval >= start_week) & (natchl_io_data.Interval <= end_week)]      
#                 io_data = processor.process_io_data(io_ref_file,hbdf_io,reference_file_name,natchl_io_data, start_week,end_week)

#                 # IO Target
#                 io_data_target = io_data[['ModelName','ComponentType','ComponentName','ComponentNumber','Year','Interval',
#                 'IO','Unit']]

#                 io_data_target = io_data_target.rename(columns = {'IO': 'Value'})
#                 io_data_target['Comments'] = 'IO Target'
#                 io_data_target.insert(0, 'Data_type', ['Target_' + scenario_name for n in range(len(io_data_target.Interval))])

#                 # IO Simulated
#                 io_data_sim = io_data[['ModelName','ComponentType','ComponentName','ComponentNumber','Year','Interval',
#                 'Simulated','Unit', 'IO_Failed']]

#                 io_data_sim = io_data_sim.rename(columns = {'Simulated': 'Value'})
#                 io_data_sim['Comments'] = 'IO Simulated'
#                 io_data_sim.insert(0, 'Data_type', [scenario_name for n in range(len(io_data_sim.Interval))])

#                 # Combine io data
#                 natchl_io_data = pd.concat([io_data_target, io_data_sim], axis=0)


#                 # Combine data for Power BI Dashboard:
#                 # ------------------------------------------------------
#                 # Combine data
#                 data_file = pd.concat([irr_data,natchl_io_data,natchl_wco_data, res_data, major_data], axis=0)
#                 data_file_1 = data_file.copy()
                
#                 # # Create year-interval-week_end_date
#                 wk_end_date = full_wk_end_date[start_week-1:end_week]
#                 interval = list(range(start_week, end_week + 1))


#                 year_lst = []
#                 for item in list(data_file.Year.unique()):
#                     year_lst2 = [item for n in range(len(wk_end_date))]
#                     year_lst = year_lst + year_lst2


#                 wk_end_date = wk_end_date * len(data_file.Year.unique())
#                 interval = interval * len(data_file.Year.unique())

#                 date_ref = pd.DataFrame(zip(year_lst,interval,wk_end_date), columns = ['Year','Interval','Wk_end_date'])
#                 date_ref['Date'] = date_ref['Wk_end_date'] + '-' + date_ref['Year'].astype(str)
                

#                 # add date column to the final data table
#                 data_file = data_file.set_index(['Year','Interval']).join(date_ref.set_index(['Year','Interval']).Date)
#                 data_file.reset_index(inplace=True)


#                 data_file = data_file[['Data_type','ModelName','ComponentType','ComponentName','ComponentNumber','Year',\
#                                     'Interval','Date','Value','Unit','PerStorage','IO_Failed','WCO_Failed',\
#                                     'TotalIrrArea_Ha','Comments']]
            

            
#                 # Combine all data for different scenarios
#                 master_data_file = pd.concat([master_data_file, data_file], axis=0, ignore_index = True)
        
#                 # Read MAA 1969 ref file
#                 maa_ref_file = pd.read_excel(reference_file_name, sheet_name = 'MAA_1969')
                
#                 # Keep data which has only hbdf value
#                 maa_ref_file = maa_ref_file.dropna(subset=['HBDF_Key'])
                
#                 # Get model path to read hbdf file
#                 hbdf_dir = os.path.join(model_dir, model) 
                
#                 # Read Hbdf based on given HBDF_Key
#                 hbdf_maa = processor.read_hbdf_based_on_ref(hbdf_dir, maa_ref_file, model, 'Nat_flow_cms')
#                 hbdf_maa = hbdf_maa[(hbdf_maa.Interval >= start_week) & (hbdf_maa.Interval <= end_week)]        
#                 # Covert to number
#                 hbdf_maa.Nat_flow_cms = pd.to_numeric(hbdf_maa.Nat_flow_cms)

#                 # Estimate apptchl natflow
#                 temp_df_104 = hbdf_maa[(hbdf_maa.ComponentNumber == 101) |\
#                                     (hbdf_maa.ComponentNumber == 469)].reset_index(drop=True)

#                 df = pd.DataFrame([])
#                 for idx in range(len(temp_df_104.ComponentNumber.unique())):
#                     data = pd.DataFrame(temp_df_104.set_index('ComponentNumber').loc[temp_df_104.ComponentNumber.unique()[idx]].Nat_flow_cms)
#                     data.reset_index(drop=True, inplace=True)
#                     df = pd.concat([df, data], axis=1)
                
                
#                 df2 = hbdf_maa.set_index('ComponentNumber').loc[hbdf_maa.ComponentNumber.unique()[idx]]
                
#                 df2.Nat_flow_cms = list(df.sum(axis=1))
                
#                 df2.reset_index(inplace=True)
#                 df2.ComponentNumber = apptchl_id

#                 hbdf_maa = pd.concat([hbdf_maa, df2], axis=0, ignore_index = True)
                
#                 df3 = hbdf_maa.set_index('ComponentNumber').loc[hbdf_maa.ComponentNumber.unique()[idx]]
                
#                 df3 = df3.rename(columns = {'Nat_flow_cms': 'Sim_flow_cms'})
#                 df3.reset_index(inplace=True)
                
#                 maa_ref_file = pd.read_excel(reference_file_name, sheet_name = 'MAA_1969')
#                 df4 = pd.DataFrame([])
#                 for com_num in maa_ref_file.ComponentNumber.unique():
#                     df3.ComponentNumber = com_num
#                     if com_num == 104:
#                         df3.Sim_flow_cms = list(outsim_id.loc[('SSRB', com_num)].Simulated)
#                     else:
#                         df3.Sim_flow_cms = list(io_data_sim[io_data_sim.ComponentNumber == com_num].Value)
                    
#                     df4 = pd.concat([df4, df3], axis=0)

#                 idx_col = ['ModelName', 'ComponentNumber', 'Year', 'Interval']
#                 hbdf_maa = pd.concat([hbdf_maa.set_index(idx_col), df4.set_index(idx_col)], axis=1)
#                 hbdf_maa.reset_index(inplace=True)
                
#                 # Add scenario information
#                 hbdf_maa.insert(0, 'Data_type', [scenario_name for n in range(len(hbdf_maa.Interval))])
#                 # Combine scenario data
#                 hbdf_maa_natflow = pd.concat([hbdf_maa_natflow, hbdf_maa], axis=0)
                
#                 # Reservoir inflow
                
#                 # Estimate reservoir inflow
#                 link_data = outsim_id[(outsim_id.ComponentType == 'DIVCHL')|\
#                         (outsim_id.ComponentType == 'NATCHL')|\
#                         (outsim_id.ComponentType == 'RETURN')]

#                 res_inflow_ref_file = pd.read_excel(reference_file_name, sheet_name = 'Reservoir')
#                 res_inflow_data = processor.estimate_res_annual_inflow_volume(res_inflow_ref_file, link_data,seconds_in_day, year, start_week, end_week)

#                 res_inflow_data = res_inflow_data[['Year', 'ComponentName', 'Reservoir_annual_inflow_dam3']]
#                 res_inflow_data = res_inflow_data.rename(columns = {'Reservoir_annual_inflow_dam3': scenario_name})
#                 res_inflow_data = res_inflow_data.rename(columns = {'ComponentName': 'Scenario'})
#                 res_inflow_data.insert(0, 'Folder_year', year)

#                 res_inflow_year = pd.concat([res_inflow_year, res_inflow_data], axis =0)

#         # #        ---------------------------
                
#         #        Executive summary
#                 summary = processor.prepare_summary(res_data,irr_data,major_data,major_data_io,major_data_wco,natchl_io_data,natchl_wco_data,scenario_name, year,start_week, end_week)
#                 ex_summary = pd.concat([ex_summary, summary], axis=0, ignore_index = True)
                
#             # Combine data for all scenarios
#             master_ex_summary = pd.concat([master_ex_summary, ex_summary[ex_summary.columns.tolist()[-2]]], axis=1, ignore_index = False)
            
#             # Combine all res inflow data
#             res_inflow_year.set_index(['Folder_year', 'Year', 'Scenario'], inplace=True)
#             master_res_inflow_annual = pd.concat([master_res_inflow_annual, res_inflow_year], axis=1)
            

#         # Format ex summary   
#         info_col = ex_summary[['Component_type', 'Year', 'ComponentName','Comments']]
#         master_ex_summary = pd.concat([info_col, master_ex_summary], axis=1, ignore_index=False)

#         # -------------------------------------------------------
#         # Please don't run this section if:
#             # 1) irrigation and non-irrigation demand changes in scenarios
#             # 2) reservoir rule curve changes in scenarios
#         # Things to do:
#             # Remove 'Demand_S1' and 'Target_S1'
#             # Rename 'Demand_S0' and 'Target_S0' to 'Demand' and 'Target', respectively
#         # -------------------------------------------------------

#         # remove 'Demand_S1'
#         master_data_file = master_data_file.drop(master_data_file[master_data_file.Data_type == 'Demand_S1'].index)
#         master_data_file.reset_index(drop=True, inplace=True)

#         # remove 'Target_S1'
#         master_data_file = master_data_file.drop(master_data_file[(master_data_file.Comments == 'Reservoir rule curve') &\
#                         (master_data_file.Data_type == 'Target_S1')].index)
#         master_data_file.reset_index(drop=True, inplace=True)

#         # rename 'Demand_S0' to 'Demand'
#         master_data_file.set_index('Comments', inplace=True)
#         master_data_file.loc[['Irrigation demand','Non-irrigation demand'], 'Data_type'] = 'Demand'

#         # rename 'Target_S0' to 'Target'
#         master_data_file.loc['Reservoir rule curve', 'Data_type'] = 'Target'

#         master_data_file.reset_index(inplace=True)

#         # move comments column 
#         master_data_file = master_data_file[list(master_data_file.columns[1:]) + [master_data_file.columns[0]]]
#         # -------------------------------------------------------

#         # Res inflow
#         master_res_inflow_annual.reset_index(inplace=True)
#         master_res_inflow_annual = master_res_inflow_annual[list(master_res_inflow_annual.columns[2:])]
#         master_res_inflow_annual = master_res_inflow_annual.T.reset_index()
#         master_res_inflow_annual.columns = master_res_inflow_annual.iloc[0]
#         master_res_inflow_annual = master_res_inflow_annual.iloc[1:]
#         master_res_inflow_annual = master_res_inflow_annual.set_index('Scenario').apply(pd.to_numeric).round()
#         master_res_inflow_annual.reset_index(inplace=True)

#         # -------------------------------------------------------

#         # Export data 
#         master_data_file.to_csv(os.path.join(output_dir, outputs_for_powerbi + '.csv'), index=False)
#         master_data_file.to_excel(os.path.join(output_dir, outputs_for_powerbi + '.xlsx'), index=False)
#         master_ex_summary.to_excel(os.path.join(output_dir, 'Executive_summary_table.xlsx'), index=False)
#         master_res_inflow_annual.to_excel(os.path.join(output_dir, 'SumTab_ResInflow.xlsx'), index=False)
#         print("FInish creating Summary Files.")
#         return( master_ex_summary, hbdf_maa_natflow, divchl_summary_tab, reference_file_name, date_ref, subtab_priv_irr_all,subtab_priv_irr_sen, subtab_priv_irr_jun_io,subtab_priv_irr_jun_wco, scn, processor,output_dir,start_week,end_week,seconds_in_day,apptchl_id)


#     def __init__(self, master_ex_summary, hbdf_maa_natflow, divchl_summary_tab, reference_file_name, 
#                  date_ref, subtab_priv_irr_all, subtab_priv_irr_sen, subtab_priv_irr_jun_io, 
#                  subtab_priv_irr_jun_wco, scn, processor, output_dir, start_week, 
#                  end_week, seconds_in_day, apptchl_id):
#         self.master_ex_summary = master_ex_summary
#         self.hbdf_maa_natflow = hbdf_maa_natflow
#         self.divchl_summary_tab = divchl_summary_tab
#         self.reference_file_name = reference_file_name
#         self.date_ref = date_ref
#         self.subtab_priv_irr_all = subtab_priv_irr_all
#         self.subtab_priv_irr_sen = subtab_priv_irr_sen
#         self.subtab_priv_irr_jun_io = subtab_priv_irr_jun_io
#         self.subtab_priv_irr_jun_wco = subtab_priv_irr_jun_wco
#         self.scn = scn
#         self.processor = processor
#         self.output_dir = output_dir
#         self.start_week = start_week
#         self.end_week = end_week
#         self.seconds_in_day = seconds_in_day
#         self.apptchl_id = apptchl_id

#     def prepare_summary_tables(self):
#         """
#         Prepare summary tables for dashboard presentation.

#         This method processes the master executive summary and creates various
#         summary tables based on different criteria.
#         """
#         # Prepare summary tables for dashboard
#         master_ex_summary2 = self.master_ex_summary.copy()
        
#         # Round to 0 dec place
#         master_ex_summary2 = master_ex_summary2.round()
        
#         # Delete 'comments' col which is not required for the dashboard
#         del master_ex_summary2['Comments']
        
#         # Update column names as required for dashboard
#         col_names = []
#         for col in master_ex_summary2.columns:
#             name = col
#             if '_S' in col:
#                 name = col.split('_')[1]
#                 col_names.append(name)
#             elif 'ComponentName' in col:
#                 name = 'Component Name'
#                 col_names.append(name)
#             else:
#                 col_names.append(name)
#         # Update column names
#         master_ex_summary2.columns = col_names
        
#         # Read summary table reference file
#         sum_ref_file = pd.read_excel(self.reference_file_name, sheet_name='Ex_summary')
        
#         # Keep selected items based on summary reference table
#         master_ex_summary2 = master_ex_summary2.set_index(['Component_type', 'Year', 'Component Name']).join(
#             sum_ref_file.set_index(['Component_type', 'Year', 'Component Name']))
#         master_ex_summary2 = master_ex_summary2.dropna(subset='Table_type')
        
#         # Export data for dashboard summary tables
#         master_ex_summary2.reset_index(inplace=True)
        
#         # Df to store Io and WCO in one df
#         tab2 = pd.DataFrame([])
#         for item in master_ex_summary2.Table_type.unique():
#             if (item == 'SumTab_ID') or (item == 'SumTab_SBasinIrr') or (item == 'SumTab_SBasinIrr_Priv'):
#                 tab1 = master_ex_summary2.set_index('Table_type').loc[item]
#                 tab1 = tab1[tab1.columns[2:]]
#                 idx_lst = [('SumTab_IrrArea', n) for n in tab1['Component Name']]
#                 area = list(master_ex_summary2.set_index(['Table_type', 'Component Name']).loc[idx_lst][self.scn])
                
#                 tab1.insert(1, 'Total Irrigation Area (Ha)', area)
                
#                 # make table horizontal
#                 tab1.reset_index(inplace=True)
#                 del tab1['Table_type']
#                 tab1 = tab1.T.reset_index()
#                 tab1.columns = tab1.iloc[0]
#                 tab1 = tab1.iloc[1:]
#                 # rename 'Component Name' to 'Scenario' (Katherine asked)
#                 tab1 = tab1.rename(columns={'Component Name': 'Scenario'})
                
#                 tab1.to_excel(os.path.join(self.output_dir, item + '.xlsx'), index=False)
                
#             elif (item == 'SumTab_IO') or (item == 'SumTab_WCO'):
#                 tab1 = master_ex_summary2.set_index('Table_type').loc[item]
#                 tab1 = tab1[tab1.columns[2:]]
                
#                 tab1.reset_index(inplace=True)
#                 tab1.columns = [item.split('_')[1] + ' ' + col if col.startswith('S') else col for col in tab1.columns]
#                 tab1.Table_type = 'SumTab_IO_WCO'
#                 tab1.set_index(['Table_type', 'Component Name'], inplace=True)
#                 tab2 = pd.concat([tab2, tab1], axis=1)
                
#             else:
#                 tab1 = master_ex_summary2.set_index('Table_type').loc[item]
#                 tab1 = tab1[tab1.columns[2:]]
                
#                 # make table horizontal
#                 tab1.reset_index(inplace=True)
#                 del tab1['Table_type']
#                 tab1 = tab1.T.reset_index()
#                 tab1.columns = tab1.iloc[0]
#                 tab1 = tab1.iloc[1:]
#                 # rename 'Component Name' to 'Scenario' (Katherine asked)
#                 tab1 = tab1.rename(columns={'Component Name': 'Scenario'})
#                 tab1.to_excel(os.path.join(self.output_dir, item + '.xlsx'), index=False)
        
#         tab2.reset_index(inplace=True)
#         tab2 = tab2.rename(columns={'Component Name': 'Reach Name'})
#         tab2.columns = tab2.columns.str.replace(r' S\d+$', '', regex=True)
#         tab2[tab2.columns[1:]].to_excel(os.path.join(self.output_dir, 'SumTab_IO_WCO.xlsx'), index=False)

#     def generate_maa_files(self):
#         """
#         Generate Master Apportionment Agreement (MAA) files.

#         This method calculates flow volumes, cumulative flows, and other MAA-related
#         metrics, saving the results to an Excel file.
#         """
#         # Generate maa_file
#         # estimate flow volume (dam3), week 52 is 8 days
#         self.hbdf_maa_natflow['Nat_flow_dam3'] = np.where((self.hbdf_maa_natflow.Interval == self.end_week),
#                                                     (self.hbdf_maa_natflow.Nat_flow_cms * 8 * self.seconds_in_day) / 1000,
#                                                     (self.hbdf_maa_natflow.Nat_flow_cms * 7 * self.seconds_in_day) / 1000)
        
#         self.hbdf_maa_natflow['Sim_flow_dam3'] = np.where((self.hbdf_maa_natflow.Interval == self.end_week),
#                                                     (self.hbdf_maa_natflow.Sim_flow_cms * 8 * self.seconds_in_day) / 1000,
#                                                     (self.hbdf_maa_natflow.Sim_flow_cms * 7 * self.seconds_in_day) / 1000)
        
#         self.hbdf_maa_natflow = self.hbdf_maa_natflow[(self.hbdf_maa_natflow.Interval >= self.start_week) & (self.hbdf_maa_natflow.Interval <= self.end_week)]
        
#         # estimate cumulative flow volume (dam3)
#         self.hbdf_maa_natflow['Cumulative_nat_flow_dam3'] = 'NaN'
#         self.hbdf_maa_natflow['Cumulative_sim_flow_dam3'] = 'NaN'
        
#         maa_file = pd.DataFrame([])
        
#         for scn in self.hbdf_maa_natflow.Data_type.unique():
#             df1 = self.hbdf_maa_natflow.set_index(['Data_type', 'ComponentNumber']).loc[(scn, self.apptchl_id)].reset_index()
#             data_cumu_nat = df1.set_index('Interval').loc[self.start_week].Nat_flow_dam3
#             data_cumu_sim = df1.set_index('Interval').loc[self.start_week].Sim_flow_dam3
            
#             cumu_nat = [data_cumu_nat]
#             cumu_sim = [data_cumu_sim]
            
#             for n in df1.Interval[1:]:
#                 data_cumu_nat += df1.set_index('Interval').loc[n].Nat_flow_dam3
#                 cumu_nat.append(data_cumu_nat)
                
#                 data_cumu_sim += df1.set_index('Interval').loc[n].Sim_flow_dam3
#                 cumu_sim.append(data_cumu_sim)
            
#             df1.Cumulative_nat_flow_dam3 = cumu_nat
#             df1.Cumulative_sim_flow_dam3 = cumu_sim
        
#             # add minimum flow
#             df1['Minimum_flow_cms'] = 42.5
#             # estimate minimum flow violation, if flow is below 42.5 cms, violation of maa 1969
#             df1['Minimum_flow_failed'] = np.where((df1['Sim_flow_cms'] >= df1['Minimum_flow_cms']), 0, 1)
#             # estimate % of delivered flow to SK
#             df1['Delivered_flow_%'] = (df1.Sim_flow_dam3 / df1.Nat_flow_dam3) * 100
#             # estimate cumulative delivered flow % to SK
#             df1['Cumulative_delivered_flow_%'] = (df1.Cumulative_sim_flow_dam3 / df1.Cumulative_nat_flow_dam3) * 100
            
#             # combine all data in one df
#             maa_file = pd.concat([maa_file, df1], axis=0, ignore_index=True)
        
#         maa_file = maa_file.round(1)
#         # add date column to the final data table
#         maa_file = maa_file.set_index(['Year', 'Interval']).join(self.date_ref.set_index(['Year', 'Interval']).Date)
#         maa_file.reset_index(inplace=True)
#         maa_file = maa_file[['Data_type', 'ComponentNumber', 'ModelName', 'Year', 'Interval', 'Date',
#             'Nat_flow_cms', 'Sim_flow_cms', 'Nat_flow_dam3', 'Sim_flow_dam3',
#             'Cumulative_nat_flow_dam3', 'Cumulative_sim_flow_dam3',
#             'Minimum_flow_cms', 'Minimum_flow_failed', 'Delivered_flow_%',
#             'Cumulative_delivered_flow_%']]
#         maa_file.to_excel(os.path.join(self.output_dir, 'MAA_1969.xlsx'), index=False)
        
        
#     def MAA_1969_Summary(self):
#         """
#         Generate a summary of the 1969 Master Apportionment Agreement data.

#         This method processes the MAA data, creating summaries for different
#         components and saving them to separate Excel files.
#         """
#         # MAA_1969 annual summary
#         df1 = self.hbdf_maa_natflow.groupby(['Data_type', 'ComponentNumber', 'Year']).sum().reset_index()
#         df1.set_index('ComponentNumber', inplace=True)
        
#         com_name = []
#         for idx in df1.index:
#             if idx == 104:
#                 com_name.append('SumTab_maa_SSRB')
#             elif idx == 101:
#                 com_name.append('SumTab_maa_RedDeer')
#             elif idx == 469:
#                 com_name.append('SumTab_maa_BowOldmanSSK')
#             elif idx == 103:
#                 com_name.append('SumTab_maa_Bow')
#             elif idx == 976:
#                 com_name.append('SumTab_maa_Oldman')
#             else:
#                 pass
        
#         df1['ComponentName'] = com_name
#         df1.reset_index(inplace=True)
        
#         df1_nat = df1[['Data_type', 'ComponentName', 'Nat_flow_dam3']]
#         df1_nat = pd.pivot_table(df1_nat, values='Nat_flow_dam3', index=['Data_type'], columns=['ComponentName']).round()
#         df1_nat.reset_index(inplace=True)
        
#         df1_sim = df1[['Data_type', 'ComponentName', 'Sim_flow_dam3']]
#         df1_sim = pd.pivot_table(df1_sim, values='Sim_flow_dam3', index=['Data_type'], columns=['ComponentName']).round()
#         df1_sim.reset_index(inplace=True)
        
#         df2 = df1[['Data_type', 'ComponentName', 'Nat_flow_dam3', 'Sim_flow_dam3']]
#         df2.columns = ['Data_type', 'ComponentName', 'Natural Flow (Dam3)', 'Delivered Flow (Dam3)']
#         df2['Delivered Flow (% of Natural Flow)'] = (df2['Delivered Flow (Dam3)'] / df2['Natural Flow (Dam3)'])*100
#         df2 = df2.round()
#         df2 = df2.rename(columns={'Data_type': 'Scenario'})
#         for item in df2.ComponentName.unique():
#             data = df2.set_index('ComponentName').loc[item].reset_index(drop=True)
#             data.to_excel(os.path.join(self.output_dir, item + '.xlsx'), index=False, sheet_name=item)

#     def IrrigationDiversionSummary(self):
#         """
#         Generate a summary of irrigation diversion data.

#         This method processes irrigation diversion data and creates summary
#         Excel files for various irrigation categories.
#         """
#         # Generate irrigation diversion summary file
#         divchl_summary_tab = self.divchl_summary_tab.round()
#         divchl_summary_tab.reset_index(inplace=True)
#         divchl_summary_tab = divchl_summary_tab[divchl_summary_tab['Diversion Year'] == 2025]
#         del divchl_summary_tab['Diversion Year']
        
#         # make horizontal table
#         divchl_summary_tab = divchl_summary_tab.T.reset_index()
#         divchl_summary_tab.columns = divchl_summary_tab.iloc[0]
#         divchl_summary_tab = divchl_summary_tab.iloc[1:]
#         divchl_summary_tab = divchl_summary_tab.rename(columns={'Component Name': 'Scenario'})
        
#         # export data
#         divchl_summary_tab.to_excel(os.path.join(self.output_dir, 'SumTab_irr_diversion.xlsx'), index=False)
        
#         # export data
#         self.subtab_priv_irr_all.to_excel(os.path.join(self.output_dir, 'SumTab_priv_irr_all.xlsx'), index=True)
#         self.subtab_priv_irr_sen.to_excel(os.path.join(self.output_dir, 'SumTab_priv_irr_sen.xlsx'), index=True)
#         self.subtab_priv_irr_jun_io.to_excel(os.path.join(self.output_dir, 'SumTab_priv_irr_jun_io.xlsx'), index=True)
#         self.subtab_priv_irr_jun_wco.to_excel(os.path.join(self.output_dir, 'SumTab_priv_irr_jun_wco.xlsx'), index=True)


#     def calculate_irrigation_shortage(self):
#         """
#         Calculate irrigation water shortage percentages for different irrigation districts.
        
#         This method processes irrigation demand and deficit data to compute water shortage
#         percentages in both mm and dam3 units for each irrigation district.
#         Returns only the deficit rows with all calculated fields.
        
#         Returns:
#             pandas.DataFrame: Irrigation deficit data with shortage calculations.
#         """
#         # Load the processed WRMM outputs
#         data_path = os.path.join(self.output_dir, f'WK{self.start_week}_{self.end_week}_WrmmOutputs.csv')
#         dataset = pd.read_csv(data_path)
        
#         # Define irrigation district component names
#         component_names = ['AID', 'BRID', 'EID', 'LID', 'LNID', 'MID', 'MVID', 'RID', 'SMRID', 'TID', 'UID', 'WID']
        
#         def process_filtered_data(filtered_data, comment_type):
#             """Helper function to process filtered irrigation data."""
#             required_columns = ['Value', 'TotalIrrArea_Ha', 'ComponentName']
#             missing_columns = [col for col in required_columns if col not in filtered_data.columns]
            
#             if missing_columns:
#                 print(f"Warning: Missing columns for '{comment_type}': {', '.join(missing_columns)}")
#                 return None
#             elif filtered_data.empty:
#                 print(f"Warning: No data found for '{comment_type}'")
#                 return None
            
#             # Group by ComponentName and calculate aggregated values
#             grouped_data = filtered_data.groupby('ComponentName').agg(
#                 mm=('Value', 'sum'),
#                 TotalIrrArea_Ha=('TotalIrrArea_Ha', 'mean')
#             ).reset_index()
            
#             # Calculate derived columns
#             grouped_data['Comments'] = comment_type
#             grouped_data['m'] = grouped_data['mm'] / 1000
#             grouped_data['m2'] = grouped_data['TotalIrrArea_Ha'] * 10000
#             grouped_data['m3'] = grouped_data['m'] * grouped_data['m2']
#             grouped_data['dam3'] = grouped_data['m3'] / 1000
            
#             return grouped_data
        
#         # Process irrigation demand data (for calculations only)
#         filtered_demand = dataset[
#             (dataset['ComponentName'].isin(component_names)) & 
#             (dataset['Comments'] == 'Irrigation demand')
#         ]
#         demand_output = process_filtered_data(filtered_demand, 'Irrigation demand')
        
#         # Process irrigation deficit data
#         filtered_deficit = dataset[
#             (dataset['ComponentName'].isin(component_names)) & 
#             (dataset['Comments'] == 'Irrigation deficit')
#         ]
#         deficit_output = process_filtered_data(filtered_deficit, 'Irrigation deficit')
        
#         # Create final output with only deficit rows but include all calculations
#         if demand_output is not None and deficit_output is not None:
#             # Create a copy of deficit output to modify
#             final_output = deficit_output.copy()
            
#             # Initialize new columns
#             final_output['watershortage_%_mm'] = 0.0
#             final_output['watershortage_%_dam3'] = 0.0
#             final_output['deficit_mm'] = final_output['mm']
#             final_output['deficit_dam3'] = final_output['dam3']
#             final_output['demand_mm'] = 0.0
#             final_output['demand_dam3'] = 0.0
            
#             # Calculate shortage percentages for each component
#             for component in component_names:
#                 # Get demand values
#                 demand_row = demand_output[demand_output['ComponentName'] == component]
#                 # Get deficit values
#                 deficit_row = final_output[final_output['ComponentName'] == component]
                
#                 if not demand_row.empty and not deficit_row.empty:
#                     # Get demand values
#                     demand_mm = demand_row['mm'].values[0]
#                     demand_dam3 = demand_row['dam3'].values[0]
                    
#                     # Get deficit values
#                     deficit_mm = deficit_row['mm'].values[0]
#                     deficit_dam3 = deficit_row['dam3'].values[0]
                    
#                     # Calculate shortage percentages (avoid division by zero)
#                     if demand_mm > 0:
#                         watershortage_mm = (deficit_mm / demand_mm) * 100
#                     else:
#                         watershortage_mm = 0
                        
#                     if demand_dam3 > 0:
#                         watershortage_dam3 = (deficit_dam3 / demand_dam3) * 100
#                     else:
#                         watershortage_dam3 = 0
                    
#                     # Update the final output with calculated values
#                     idx = final_output['ComponentName'] == component
#                     final_output.loc[idx, 'watershortage_%_mm'] = watershortage_mm
#                     final_output.loc[idx, 'watershortage_%_dam3'] = watershortage_dam3
#                     final_output.loc[idx, 'demand_mm'] = demand_mm
#                     final_output.loc[idx, 'demand_dam3'] = demand_dam3
            
#             # Reorder columns to match your desired output format
#             column_order = [
#                 'ComponentName', 'mm', 'TotalIrrArea_Ha', 'Comments', 'm', 'm2', 'm3', 'dam3',
#                 'watershortage_%_mm', 'watershortage_%_dam3', 'deficit_mm', 'deficit_dam3', 
#                 'demand_mm', 'demand_dam3'
#             ]
            
#             # Only include columns that exist in the dataframe
#             existing_columns = [col for col in column_order if col in final_output.columns]
#             final_output = final_output[existing_columns]
            
#             # Save the output
#             save_path = os.path.join(
#                 self.output_dir, 
#                 f"SumTab_IrrShortage.xlsx"
#             )
#             final_output.to_excel(save_path, index=False)
#             print(f"Irrigation shortage summary saved to: {save_path}")
#             print(f"Output contains {len(final_output)} irrigation district deficit records")
            
#             return final_output
#         else:
#             print("Error: Could not process irrigation data")
#             return None

#     def create_apportionment_summary(self, apportionment_input_file=None, apportionment_output_file=None):
#         """
#         Creates an apportionment summary CSV file based on the input Excel file.
#         The output contains three sections: Simulated Flow, 50% Nat Flow, and Target Min Flow
        
#         Parameters:
#         apportionment_input_file: Path to the input Excel file (Apportionment_summary_original.xlsx)
#         apportionment_output_file: Path to the output CSV file
        
#         Returns:
#         pandas.DataFrame: The generated apportionment summary dataframe
#         """
        
#         # Set default file paths if not provided
#         if apportionment_input_file is None:
#             apportionment_input_file = os.path.join(self.output_dir, 'Apportionment_summary_original.xlsx')
#         if apportionment_output_file is None:
#             apportionment_output_file = os.path.join(self.output_dir, f'Apportionment_summary_week{self.start_week}_{self.end_week}.csv')
        
#         # Check if input file exists
#         if not os.path.exists(apportionment_input_file):
#             print(f"Warning: Input file {apportionment_input_file} not found. Skipping apportionment summary.")
#             return None
        
#         # Read the input Excel file
#         df_input = pd.read_excel(apportionment_input_file)
        
#         # Ensure date column is datetime
#         df_input['Date'] = pd.to_datetime(df_input['Date'])
        
#         # Constants from the calculations
#         SECONDS_PER_WEEK = 7 * 24 * 3600  # 604800 seconds
#         CONVERSION_FACTOR = 1000  # m³ to dam³ conversion
        
#         # Find the last row with simulated data (non-zero simulated flow)
#         last_simulated_idx = None
#         for idx in range(len(df_input) - 1, -1, -1):
#             if pd.notna(df_input.iloc[idx]['Simulated_flow_cms']) and df_input.iloc[idx]['Simulated_flow_cms'] > 0:
#                 last_simulated_idx = idx
#                 break
        
#         # Initialize output dataframe list
#         all_sections = []
        
#         # Variables to store the final cumulative values for annual delivery calculation
#         final_cum_delivered_volume = 0
#         final_cum_apportionable_volume = 0
        
#         # First pass: Calculate final cumulative values from the Simulated Flow section
#         temp_cum_apportionable_volume = 0
#         temp_cum_delivered_volume = 0
        
#         for idx, row in df_input.iterrows():
#             simulated_flow = float(row['Simulated_flow_cms']) if pd.notna(row['Simulated_flow_cms']) else 0.0
#             natural_flow = float(row['Natural_flow_cms']) if pd.notna(row['Natural_flow_cms']) else 0.0
            
#             # Check if we're past the last simulated data point
#             is_after_last_simulated = idx > last_simulated_idx if last_simulated_idx is not None else False
            
#             if not is_after_last_simulated:
#                 weekly_natural_volume = natural_flow * SECONDS_PER_WEEK / CONVERSION_FACTOR
#                 weekly_delivered_volume = simulated_flow * SECONDS_PER_WEEK / CONVERSION_FACTOR
                
#                 temp_cum_apportionable_volume += weekly_natural_volume
#                 temp_cum_delivered_volume += weekly_delivered_volume
                
#                 # Capture the final values at the last simulated data point
#                 if idx == last_simulated_idx:
#                     final_cum_delivered_volume = temp_cum_delivered_volume
#                     final_cum_apportionable_volume = temp_cum_apportionable_volume
        
#         # Create three sections: Simulated Flow, 50% Nat Flow, Target Min Flow
#         for section_type in ['Simulated Flow', '50% Nat Flow', 'Target Min Flow']:
#             section_data = []
            
#             # Initialize cumulative variables
#             cum_apportionable_volume = 0
#             cum_50_percent_volume = 0
#             cum_delivered_volume = 0
            
#             for idx, row in df_input.iterrows():
#                 record = {}
                
#                 # Basic information
#                 record['Description/Date'] = row['Date'].strftime('%Y-%m-%d')
#                 record['Parameters'] = section_type
#                 record['Data_Type'] = '5wks'
                
#                 # Flow data - handle NaN values
#                 simulated_flow = float(row['Simulated_flow_cms']) if pd.notna(row['Simulated_flow_cms']) else 0.0
#                 natural_flow = float(row['Natural_flow_cms']) if pd.notna(row['Natural_flow_cms']) else 0.0
                
#                 # Check if we're past the last simulated data point
#                 is_after_last_simulated = idx > last_simulated_idx if last_simulated_idx is not None else False
                
#                 # For Simulated Flow section
#                 if section_type == 'Simulated Flow':
#                     if is_after_last_simulated:
#                         record['Simulated Flows (cms)'] = np.nan
#                     else:
#                         record['Simulated Flows (cms)'] = simulated_flow if simulated_flow > 0 else np.nan
#                     record['S.Sask Nat Flow at the Border (cms)'] = np.nan
#                     record['50% Nat Flow (cms)'] = np.nan
#                     record['Target Min. Flow (cms)'] = np.nan
                
#                 # For 50% Nat Flow section
#                 elif section_type == '50% Nat Flow':
#                     record['Simulated Flows (cms)'] = np.nan
#                     record['S.Sask Nat Flow at the Border (cms)'] = np.nan
#                     if is_after_last_simulated:
#                         record['50% Nat Flow (cms)'] = np.nan
#                     else:
#                         fifty_percent_flow = natural_flow * 0.5
#                         record['50% Nat Flow (cms)'] = fifty_percent_flow if natural_flow > 0 else np.nan
#                     record['Target Min. Flow (cms)'] = np.nan
                
#                 # For Target Min Flow section
#                 else:  # Target Min Flow
#                     record['Simulated Flows (cms)'] = np.nan
#                     record['S.Sask Nat Flow at the Border (cms)'] = np.nan
#                     record['50% Nat Flow (cms)'] = np.nan
                    
#                     if is_after_last_simulated:
#                         record['Target Min. Flow (cms)'] = np.nan
#                     else:
#                         target_flow = min(natural_flow * 0.5, 42.5) if natural_flow > 0 else 0.0
#                         record['Target Min. Flow (cms)'] = target_flow
                
#                 # Calculate weekly volumes only if we have data
#                 if not is_after_last_simulated:
#                     weekly_natural_volume = natural_flow * SECONDS_PER_WEEK / CONVERSION_FACTOR
#                     weekly_delivered_volume = simulated_flow * SECONDS_PER_WEEK / CONVERSION_FACTOR
                    
#                     # Update cumulative volumes
#                     cum_apportionable_volume += weekly_natural_volume
#                     cum_50_percent_volume = cum_apportionable_volume * 0.5
#                     cum_delivered_volume += weekly_delivered_volume
                
#                 # Set cumulative values (they remain constant after last simulated data)
#                 if is_after_last_simulated:
#                     record['Cum. Apptortionable Volume (dam3)'] = np.nan
#                     record[' 50% Cum. Apptortionable Volume (dam3)'] = np.nan
#                     record['Cum. Delivered Volume (dam3)'] = np.nan
#                 else:
#                     record['Cum. Apptortionable Volume (dam3)'] = round(cum_apportionable_volume, 5)
#                     record[' 50% Cum. Apptortionable Volume (dam3)'] = round(cum_50_percent_volume, 5)
#                     record['Cum. Delivered Volume (dam3)'] = round(cum_delivered_volume, 5)
                
#                 # Calculate cumulative depletion (natural - delivered)
#                 cum_depletion = cum_apportionable_volume - cum_delivered_volume if not is_after_last_simulated else np.nan
                
#                 # Only show these columns for Simulated Flow section
#                 if section_type == 'Simulated Flow':
#                     if is_after_last_simulated:
#                         record['Cum % of Natural Flow Delivered to SK'] = np.nan
#                         record['Minimu_failed'] = np.nan
#                         record['Annually_Delivered_%'] = np.nan
#                         record['Cumulative_Alberta_Depletion'] = np.nan
#                         record['Cum_%_Natural_Flow_Delivered'] = np.nan
#                         record['Cum. Depleted Flows (dam3)'] = np.nan
#                     else:
#                         record['Cum % of Natural Flow Delivered to SK'] = int(round(cum_depletion))
                        
#                         # Minimu_failed - only for first row
#                         if idx == 0:
#                             record['Minimu_failed'] = 0
#                         else:
#                             record['Minimu_failed'] = np.nan
                        
#                         # Annual delivered percentage - only for first row, calculated using final values
#                         if idx == 0:
#                             # Use the pre-calculated final values
#                             if final_cum_apportionable_volume > 0:
#                                 annually_delivered_pct = (final_cum_delivered_volume / final_cum_apportionable_volume) * 100
#                             else:
#                                 annually_delivered_pct = 0
#                             record['Annually_Delivered_%'] = round(annually_delivered_pct, 2)
#                         else:
#                             record['Annually_Delivered_%'] = np.nan
                            
#                         record['Cumulative_Alberta_Depletion'] = round(cum_depletion, 5)
                        
#                         # Calculate percentage of natural flow delivered
#                         if cum_apportionable_volume > 0:
#                             percent_delivered = (cum_delivered_volume / cum_apportionable_volume) * 100
#                         else:
#                             percent_delivered = 0
                        
#                         record['Cum_%_Natural_Flow_Delivered'] = int(round(percent_delivered))
#                         record['Cum. Depleted Flows (dam3)'] = int(round(cum_depletion))
#                 else:
#                     record['Cum % of Natural Flow Delivered to SK'] = np.nan
#                     record['Minimu_failed'] = np.nan
#                     record['Annually_Delivered_%'] = np.nan
#                     record['Cumulative_Alberta_Depletion'] = np.nan
#                     record['Cum_%_Natural_Flow_Delivered'] = np.nan
#                     record['Cum. Depleted Flows (dam3)'] = np.nan
                
#                 section_data.append(record)
            
#             all_sections.extend(section_data)
        
#         # Create output dataframe
#         df_output = pd.DataFrame(all_sections)
        
#         # Define the exact column order to match the expected output
#         column_order = [
#             'Description/Date', 'Parameters', 'Data_Type',
#             'Simulated Flows (cms)', 'S.Sask Nat Flow at the Border (cms)',
#             '50% Nat Flow (cms)', 'Target Min. Flow (cms)',
#             'Cum. Apptortionable Volume (dam3)', ' 50% Cum. Apptortionable Volume (dam3)',
#             'Cum. Delivered Volume (dam3)', 'Cum % of Natural Flow Delivered to SK',
#             'Minimu_failed', 'Annually_Delivered_%', 'Cumulative_Alberta_Depletion',
#             'Cum_%_Natural_Flow_Delivered', 'Cum. Depleted Flows (dam3)'
#         ]
        
#         # Reorder columns
#         df_output = df_output[column_order]
        
#         # Save to CSV with specific formatting
#         df_output.to_csv(apportionment_output_file, index=False, float_format='%.8g')
#         print(f"Apportionment summary saved to {apportionment_output_file}")
        
#         # Display statistics
#         print("\nGenerated sections:")
#         for param_type in df_output['Parameters'].unique():
#             count = len(df_output[df_output['Parameters'] == param_type])
#             print(f"- {param_type}: {count} rows")
        
#         # Find where data ends
#         sim_flow_section = df_output[df_output['Parameters'] == 'Simulated Flow']
#         last_data_row = None
#         for idx, row in sim_flow_section.iterrows():
#             if pd.notna(row['Simulated Flows (cms)']):
#                 last_data_row = idx
        
#         if last_data_row is not None:
#             last_date = sim_flow_section.iloc[last_data_row % len(sim_flow_section)]['Description/Date']
#             print(f"\nSimulated data ends at: {last_date}")
        
#         # Display the calculated annual delivery percentage
#         annually_delivered_value = df_output[
#             (df_output['Parameters'] == 'Simulated Flow') & 
#             (pd.notna(df_output['Annually_Delivered_%']))
#         ]['Annually_Delivered_%'].iloc[0] if len(df_output[
#             (df_output['Parameters'] == 'Simulated Flow') & 
#             (pd.notna(df_output['Annually_Delivered_%']))
#         ]) > 0 else None
        
#         if annually_delivered_value is not None:
#             print(f"Calculated Annually_Delivered_%: {annually_delivered_value:.2f}%")
#             print(f"Formula: ({final_cum_delivered_volume:.5f} / {final_cum_apportionable_volume:.5f}) * 100")
        
#         return df_output

# #### Summary Weather Forecast Generator 
# # Add this method to the SummaryTablesGenerator class in SummaryTableGenerator.py
#     def create_weather_forecast_summary(self, 
#                                         forecast_start_date="2025-06-11",
#                                         moving_average_days=14,
#                                         forecast_constant_files_path=None,
#                                         wsa_input_path_template=None,
#                                         output_directory=None):
#             """
#             Create weather forecast summary based on historical percentiles and WSA forecast data.
            
#             Args:
#                 forecast_start_date (str): Start date for forecast in YYYY-MM-DD format
#                 moving_average_days (int): Window size in days for moving average
#                 forecast_constant_files_path (str): Path to constant weather files (1950-2019)
#                 wsa_input_path_template (str): Template path for WSA input data
#                 output_directory (str): Directory to save output files
            
#             Returns:
#                 pd.DataFrame: Weather forecast summary data
#             """
            
#             print("\n" + "="*60)
#             print("Creating Weather Forecast Summary")
#             print("="*60 + "\n")
            
#             # Import required libraries for weather processing
#             import pandas as pd
#             import numpy as np
#             from datetime import datetime, timedelta
#             import os
            
#             # Helper function to check leap year
#             def is_leap_year(year):
#                 """Check if a year is a leap year"""
#                 return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
            
#             # Set default paths if not provided
#             if forecast_constant_files_path is None:
#                 forecast_constant_files_path = rf"D:\Sopan\HGS_Data\Codes\WRMM\WRMM_Package\WRMM_For BEN\WRMM_Package\Forecast_Constant_files_1950_2019"
            
#             if wsa_input_path_template is None:
#                 wsa_input_path_template = rf"D:\Sopan\HGS_Data\Codes\WRMM\WRMM_Package\WRMM_For BEN\WRMM_Package\INPUT_DATA_WK{self.start_week}_WK{self.end_week}\Forecast_Summary_Data_Input_WK{self.start_week}_WK{self.end_week}"
            
#             if output_directory is None:
#                 output_directory = self.output_dir
            
#             # Parse the forecast start date
#             try:
#                 current_date = datetime.strptime(forecast_start_date, '%Y-%m-%d').date()
#                 print(f"Using forecast start date: {current_date}")
#             except ValueError:
#                 print(f"Error: Invalid date format in forecast_start_date: {forecast_start_date}")
#                 print("Please use YYYY-MM-DD format.")
#                 return None
            
#             forecast_period = moving_average_days
#             print(f"Using moving average window: {forecast_period} days")
            
#             # Calculate date ranges
#             past_start = current_date - timedelta(days=forecast_period)
#             past_end = current_date - timedelta(days=1)
#             future_start = current_date
#             future_end = current_date + timedelta(days=forecast_period - 1)
            
#             print(f"\nDate ranges:")
#             print(f"Past period: {past_start} to {past_end}")
#             print(f"Future period: {future_start} to {future_end}")
            
#             # Load weather data
#             print("\nLoading weather data from constant files directory...")
#             print(f"Path: {forecast_constant_files_path}")
            
#             try:
#                 # Read CSV files from the specified directory
#                 data_prcp = pd.read_csv(os.path.join(forecast_constant_files_path, 'Prcp_Aggre_29STN.csv'))
#                 data_tmin = pd.read_csv(os.path.join(forecast_constant_files_path, 'Tmin_Aggre_29STN.csv'))
#                 data_tmax = pd.read_csv(os.path.join(forecast_constant_files_path, 'Tmax_Aggre_29STN.csv'))
#                 data_tave = pd.read_csv(os.path.join(forecast_constant_files_path, 'Tave_Aggre_29STN.csv'))
                
#                 # Convert date column to datetime
#                 data_prcp['Date'] = pd.to_datetime(data_prcp['Date'])
#                 data_tmin['Date'] = pd.to_datetime(data_tmin['Date'])
#                 data_tmax['Date'] = pd.to_datetime(data_tmax['Date'])
#                 data_tave['Date'] = pd.to_datetime(data_tave['Date'])
                
#                 # Get station names (all columns except 'Date')
#                 station_names = [col for col in data_prcp.columns if col != 'Date']
                
#                 print(f"Loaded data for {len(station_names)} stations")
#                 print(f"Date range: {data_prcp['Date'].min()} to {data_prcp['Date'].max()}")
                
#                 # Create data dictionary
#                 data_dict = {
#                     'prcp': data_prcp,
#                     'tmin': data_tmin,
#                     'tmax': data_tmax,
#                     'tave': data_tave,
#                     'stations': station_names
#                 }
                
#             except FileNotFoundError as e:
#                 print(f"\nError: Could not find required data files in {forecast_constant_files_path}")
#                 print(f"Error details: {e}")
#                 return None
            
#             # Load WSA forecast data
#             wsa_data = None
#             try:
#                 # Construct the WSA file path
#                 wsa_path = os.path.join(
#                     wsa_input_path_template,
#                     f'WSA_forecast_Temp_Precip_WK{self.start_week}_WK{self.end_week}.xlsx'
#                 )
                
#                 print(f"\nLoading WSA forecast data from:")
#                 print(f"Path: {wsa_path}")
                
#                 # wsa_data = pd.read_csv(wsa_path)
#                 wsa_data = pd.read_excel(wsa_path)
                
#                 # Try multiple date formats
#                 date_formats = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d']
#                 date_parsed = False
                
#                 for fmt in date_formats:
#                     try:
#                         wsa_data['Date'] = pd.to_datetime(wsa_data['Date'], format=fmt)
#                         date_parsed = True
#                         print(f"Successfully parsed dates using format: {fmt}")
#                         break
#                     except:
#                         continue
                
#                 if not date_parsed:
#                     wsa_data['Date'] = pd.to_datetime(wsa_data['Date'], errors='coerce')
#                     print("Used automatic date parsing")
                
#                 # Remove any rows with invalid dates
#                 valid_dates = wsa_data['Date'].notna()
#                 if not valid_dates.all():
#                     print(f"Warning: Removed {(~valid_dates).sum()} rows with invalid dates")
#                     wsa_data = wsa_data[valid_dates]
                
#                 print(f"Loaded WSA forecast data: {len(wsa_data)} records")
#                 print(f"Date range: {wsa_data['Date'].min()} to {wsa_data['Date'].max()}")
                
#                 # Check for required columns
#                 required_cols = ['Historical_Tmin', 'Historical_Tmax', 'Historical_Precip']
#                 missing_cols = [col for col in required_cols if col not in wsa_data.columns]
#                 if missing_cols:
#                     print(f"Warning: Missing required columns in WSA data: {missing_cols}")
#                     wsa_data = None
                
#             except FileNotFoundError:
#                 print(f"\nWarning: WSA forecast file not found at expected location.")
#                 print(f"Expected path: {wsa_path}")
#                 print("WSA integration will be skipped.")
#                 wsa_data = None
            
#             # Function to calculate percentiles for a single station
#             def calculate_percentiles_for_station(data_dict, station_name, current_date, forecast_period, 
#                                                 start_year=1950, end_year=2019):
#                 """Calculate percentiles for a single station"""
                
#                 # Define date ranges
#                 date_start = current_date - timedelta(days=forecast_period)
#                 date_end = current_date + timedelta(days=forecast_period - 1)
                
#                 # Get the month-day format for the period - need 29 days
#                 date_range = pd.date_range(date_start, date_start + timedelta(days=28))
#                 month_days = [d.strftime('%m-%d') for d in date_range]
                
#                 # Initialize arrays to store accumulated values
#                 years = range(start_year, end_year + 1)
#                 accumulated_prcp = np.full((len(years), 2), np.nan)  # Past, Future
#                 accumulated_tmin = np.full((len(years), 2), np.nan)
#                 accumulated_tmax = np.full((len(years), 2), np.nan)
#                 accumulated_tave = np.full((len(years), 2), np.nan)
                
#                 # Calculate for each year
#                 for i, year in enumerate(years):
#                     try:
#                         # Create dates for this year
#                         first_date = datetime.strptime(f"{year}-{month_days[0]}", '%Y-%m-%d')
                        
#                         # Handle leap year edge case
#                         if month_days[0] == '02-29' and not is_leap_year(year):
#                             continue
                            
#                         # Get data for this period - extract 29 days
#                         mask = (data_dict['prcp']['Date'] >= first_date) & \
#                             (data_dict['prcp']['Date'] < first_date + timedelta(days=29))
                        
#                         if mask.sum() == 29:  # Ensure we have complete data
#                             # Extract data
#                             prcp_data = data_dict['prcp'].loc[mask, station_name].values
#                             tmin_data = data_dict['tmin'].loc[mask, station_name].values
#                             tmax_data = data_dict['tmax'].loc[mask, station_name].values
#                             tave_data = data_dict['tave'].loc[mask, station_name].values
                            
#                             # Past period (first 15 days)
#                             accumulated_prcp[i, 0] = np.sum(prcp_data[:15])
#                             accumulated_tmin[i, 0] = np.mean(tmin_data[:15])
#                             accumulated_tmax[i, 0] = np.mean(tmax_data[:15])
#                             accumulated_tave[i, 0] = np.mean(tave_data[:15])
                            
#                             # Future period (last 14 days)
#                             accumulated_prcp[i, 1] = np.sum(prcp_data[15:])
#                             accumulated_tmin[i, 1] = np.mean(tmin_data[15:])
#                             accumulated_tmax[i, 1] = np.mean(tmax_data[15:])
#                             accumulated_tave[i, 1] = np.mean(tave_data[15:])
                            
#                     except Exception as e:
#                         continue
                
#                 # Calculate percentiles
#                 percentiles = [0, 25, 50, 75, 100]
                
#                 results = {
#                     'prcp': np.zeros((len(percentiles), 2)),
#                     'tmin': np.zeros((len(percentiles), 2)),
#                     'tmax': np.zeros((len(percentiles), 2)),
#                     'tave': np.zeros((len(percentiles), 2))
#                 }
                
#                 for period in range(2):  # Past and Future
#                     results['prcp'][:, period] = np.percentile(accumulated_prcp[:, period][~np.isnan(accumulated_prcp[:, period])], percentiles)
#                     results['tmin'][:, period] = np.percentile(accumulated_tmin[:, period][~np.isnan(accumulated_tmin[:, period])], percentiles)
#                     results['tmax'][:, period] = np.percentile(accumulated_tmax[:, period][~np.isnan(accumulated_tmax[:, period])], percentiles)
#                     results['tave'][:, period] = np.percentile(accumulated_tave[:, period][~np.isnan(accumulated_tave[:, period])], percentiles)
                
#                 return results
            
#             # Function to calculate WSA metrics
#             def calculate_wsa_metrics(wsa_data, station_name, current_date, window_size):
#                 """Calculate WSA forecast metrics for a specific station"""
                
#                 if wsa_data is None:
#                     return None
                
#                 # Filter by station
#                 station_data = wsa_data[wsa_data['Station'] == station_name].copy()
                
#                 if len(station_data) == 0:
#                     return None
                
#                 # Define date ranges
#                 # Past period: window_size days before current_date
#                 past_start = current_date - timedelta(days=window_size)
#                 past_end = current_date - timedelta(days=1)
                
#                 # Future period: from current_date to window_size-1 days ahead
#                 future_start = current_date
#                 future_end = current_date + timedelta(days=window_size - 1)
                
#                 # Get data for past period (historical)
#                 past_mask = (station_data['Date'] >= pd.Timestamp(past_start)) & (station_data['Date'] <= pd.Timestamp(past_end))
#                 past_data = station_data[past_mask]
                
#                 # Get data for future period (forecast)
#                 future_mask = (station_data['Date'] >= pd.Timestamp(future_start)) & (station_data['Date'] <= pd.Timestamp(future_end))
#                 future_data = station_data[future_mask]
                
#                 # Calculate historical metrics (for the past period)
#                 if len(past_data) > 0:
#                     # Sum precipitation over the period
#                     hist_precip_sum = past_data['Historical_Precip'].sum()
#                     # Average temperatures over the period
#                     hist_tmax_avg = past_data['Historical_Tmax'].mean()
#                     hist_tmin_avg = past_data['Historical_Tmin'].mean()
#                 else:
#                     hist_precip_sum = np.nan
#                     hist_tmax_avg = np.nan
#                     hist_tmin_avg = np.nan
                
#                 # Get forecast metrics from the last day of forecast period
#                 forecast_last_day = station_data[station_data['Date'] == pd.Timestamp(future_end)]
                
#                 if len(forecast_last_day) > 0:
#                     fcst_cumulative_precip_median = forecast_last_day['Cum Precip M'].iloc[0]
#                     fcst_average_tempmax_median = forecast_last_day['AvgTempMax'].iloc[0]
#                     fcst_average_tempmin_median = forecast_last_day['AvgTempMin'].iloc[0]
#                 else:
#                     fcst_cumulative_precip_median = np.nan
#                     fcst_average_tempmax_median = np.nan
#                     fcst_average_tempmin_median = np.nan
                
#                 return {
#                     'fcst_Precipitation_last': round(hist_precip_sum, 2) if not np.isnan(hist_precip_sum) else np.nan,
#                     'fcst_TmaxValue_last': round(hist_tmax_avg, 1) if not np.isnan(hist_tmax_avg) else np.nan,
#                     'fcst_TminValue_last': round(hist_tmin_avg, 1) if not np.isnan(hist_tmin_avg) else np.nan,
#                     'fcst_Cumulative_Precip_Forecast_Median': round(fcst_cumulative_precip_median, 2) if not np.isnan(fcst_cumulative_precip_median) else np.nan,
#                     'fcst_Average_TempMax_Forecast_Median': round(fcst_average_tempmax_median, 1) if not np.isnan(fcst_average_tempmax_median) else np.nan,
#                     'fcst_Average_TempMin_Forecast_Median': round(fcst_average_tempmin_median, 1) if not np.isnan(fcst_average_tempmin_median) else np.nan
#                 }
            
#             # Function to determine comparison
#             def determine_comparison(value, lower_bound, upper_bound):
#                 """Determine if value is below, within, or above the range"""
#                 if pd.isna(value) or pd.isna(lower_bound) or pd.isna(upper_bound):
#                     return ""
                
#                 if value < lower_bound:
#                     return "below normal"
#                 elif value > upper_bound:
#                     return "above normal"
#                 else:
#                     return "normal"
            
#             # Calculate percentiles for all stations
#             print(f"\nCalculating percentiles for {len(station_names)} stations...")
            
#             # Sort stations alphabetically
#             station_names_sorted = sorted(station_names)
            
#             # Check station match with WSA data
#             if wsa_data is not None:
#                 wsa_stations = set(wsa_data['Station'].unique())
#                 matching_stations = set(station_names_sorted) & wsa_stations
#                 print(f"\nStation matching: {len(matching_stations)} out of {len(station_names_sorted)} stations found in WSA data")
#                 if len(matching_stations) == 0:
#                     print("WARNING: No matching stations found between main data and WSA data!")
            
#             all_percentiles = []
            
#             for i, station in enumerate(station_names_sorted):
#                 print(f"Processing station {i+1}/{len(station_names_sorted)}: {station}")
#                 percentiles = calculate_percentiles_for_station(
#                     data_dict, station, current_date, forecast_period
#                 )
#                 all_percentiles.append(percentiles)
            
#             # Format output data
#             print("\nGenerating enhanced output with WSA integration...")
            
#             # Create date labels - MODIFIED TO CREATE SEPARATE FROM/TO DATES
#             date_start = current_date - timedelta(days=forecast_period)
#             date_end = current_date + timedelta(days=forecast_period-1)
#             date_mid = current_date - timedelta(days=1)
            
#             # Create individual date components
#             # hist_from = date_start.strftime('%m-%d')
#             # hist_to = date_mid.strftime('%m-%d')
#             # forecast_from = current_date.strftime('%m-%d')
#             # forecast_to = date_end.strftime('%m-%d')
#             hist_from = date_start.strftime('%#m/%#d/%Y')
#             hist_to = date_mid.strftime('%#m/%#d/%Y')
#             forecast_from = current_date.strftime('%#m/%#d/%Y')
#             forecast_to = date_end.strftime('%#m/%#d/%Y')

            
#             # Initialize lists for the enhanced output
#             rows = []
            
#             # Process each station
#             for i, station in enumerate(station_names_sorted):
#                 # Base percentile values
#                 prcp_lower_past = np.round(all_percentiles[i]['prcp'][1, 0], 2)
#                 prcp_upper_past = np.round(all_percentiles[i]['prcp'][3, 0], 2)
#                 tmax_lower_past = np.round(all_percentiles[i]['tmax'][1, 0], 1)
#                 tmax_upper_past = np.round(all_percentiles[i]['tmax'][3, 0], 1)
#                 tmin_lower_past = np.round(all_percentiles[i]['tmin'][1, 0], 1)
#                 tmin_upper_past = np.round(all_percentiles[i]['tmin'][3, 0], 1)
                
#                 prcp_lower_forecast = np.round(all_percentiles[i]['prcp'][1, 1], 2)
#                 prcp_upper_forecast = np.round(all_percentiles[i]['prcp'][3, 1], 2)
#                 tmax_lower_forecast = np.round(all_percentiles[i]['tmax'][1, 1], 1)
#                 tmax_upper_forecast = np.round(all_percentiles[i]['tmax'][3, 1], 1)
#                 tmin_lower_forecast = np.round(all_percentiles[i]['tmin'][1, 1], 1)
#                 tmin_upper_forecast = np.round(all_percentiles[i]['tmin'][3, 1], 1)
                
#                 # Get WSA metrics (both historical and forecast)
#                 wsa_metrics = calculate_wsa_metrics(wsa_data, station, current_date, forecast_period)
                
#                 # Initialize row with base data - MODIFIED TO USE SEPARATE DATE COLUMNS
#                 row = {
#                     'Date_hist_from': hist_from,
#                     'Date_hist_to': hist_to,
#                     'Station': station,
#                     'r_PrcipValue_Lower_last': prcp_lower_past,
#                     'r_PrcipValue_Upper_last': prcp_upper_past,
#                     'r_TmaxValue_Lower_last': tmax_lower_past,
#                     'r_TmaxValue_Upper_last': tmax_upper_past,
#                     'r_TminValue_Lower_last': tmin_lower_past,
#                     'r_TminValue_Upper_last': tmin_upper_past,
#                     'Date_forecast_from': forecast_from,
#                     'Date_forecast_to': forecast_to,
#                     'r_PrcipValue_Lower_forecast': prcp_lower_forecast,
#                     'r_PrcipValue_Upper_forecast': prcp_upper_forecast,
#                     'r_TmaxValue_Lower_forecast': tmax_lower_forecast,
#                     'r_TmaxValue_Upper_forecast': tmax_upper_forecast,
#                     'r_TminValue_Lower_forecast': tmin_lower_forecast,
#                     'r_TminValue_Upper_forecast': tmin_upper_forecast
#                 }
                
#                 # Always add WSA columns, either with values or NaN
#                 if wsa_metrics:
#                     row['fcst_Precipitation_last'] = wsa_metrics.get('fcst_Precipitation_last', np.nan)
#                     row['fcst_TmaxValue_last'] = wsa_metrics.get('fcst_TmaxValue_last', np.nan)
#                     row['fcst_TminValue_last'] = wsa_metrics.get('fcst_TminValue_last', np.nan)
#                     row['fcst_Cumulative_Precip_Forecast_Median'] = wsa_metrics.get('fcst_Cumulative_Precip_Forecast_Median', np.nan)
#                     row['fcst_Average_TempMax_Forecast_Median'] = wsa_metrics.get('fcst_Average_TempMax_Forecast_Median', np.nan)
#                     row['fcst_Average_TempMin_Forecast_Median'] = wsa_metrics.get('fcst_Average_TempMin_Forecast_Median', np.nan)
#                 else:
#                     row['fcst_Precipitation_last'] = np.nan
#                     row['fcst_TmaxValue_last'] = np.nan
#                     row['fcst_TminValue_last'] = np.nan
#                     row['fcst_Cumulative_Precip_Forecast_Median'] = np.nan
#                     row['fcst_Average_TempMax_Forecast_Median'] = np.nan
#                     row['fcst_Average_TempMin_Forecast_Median'] = np.nan
                
#                 # Add range values
#                 row['PrcipValue_Range_last'] = f"{prcp_lower_past} to {prcp_upper_past}"
#                 row['TmaxValue_Range_last'] = f"{tmax_lower_past} to {tmax_upper_past}"
#                 row['TminValue_Range_last'] = f"{tmin_lower_past} to {tmin_upper_past}"
#                 row['PrcipValue_Range_forecast'] = f"{prcp_lower_forecast} to {prcp_upper_forecast}"
#                 row['TmaxValue_Range_forecast'] = f"{tmax_lower_forecast} to {tmax_upper_forecast}"
#                 row['TminValue_Range_forecast'] = f"{tmin_lower_forecast} to {tmin_upper_forecast}"
                
#                 # Add comparison labels
#                 row['Last_Precip_Comparison'] = determine_comparison(
#                     row.get('fcst_Precipitation_last', np.nan), prcp_lower_past, prcp_upper_past)
#                 row['Forecast_Precip_Comparison'] = determine_comparison(
#                     row.get('fcst_Cumulative_Precip_Forecast_Median', np.nan), prcp_lower_forecast, prcp_upper_forecast)
#                 row['Last_Tmax_Comparison'] = determine_comparison(
#                     row.get('fcst_TmaxValue_last', np.nan), tmax_lower_past, tmax_upper_past)
#                 row['Forecast_Tmax_Comparison'] = determine_comparison(
#                     row.get('fcst_Average_TempMax_Forecast_Median', np.nan), tmax_lower_forecast, tmax_upper_forecast)
#                 row['Last_Tmin_Comparison'] = determine_comparison(
#                     row.get('fcst_TminValue_last', np.nan), tmin_lower_past, tmin_upper_past)
#                 row['Forecast_Tmin_Comparison'] = determine_comparison(
#                     row.get('fcst_Average_TempMin_Forecast_Median', np.nan), tmin_lower_forecast, tmin_upper_forecast)
                
#                 rows.append(row)
            
#             # Create DataFrame
#             output_data = pd.DataFrame(rows)
            
#             # Ensure column order matches the expected output - MODIFIED COLUMN ORDER
#             column_order = [
#                 'Date_hist_from', 'Date_hist_to', 'Station', 
#                 'r_PrcipValue_Lower_last', 'r_PrcipValue_Upper_last',
#                 'r_TmaxValue_Lower_last', 'r_TmaxValue_Upper_last',
#                 'r_TminValue_Lower_last', 'r_TminValue_Upper_last',
#                 'Date_forecast_from', 'Date_forecast_to',
#                 'r_PrcipValue_Lower_forecast', 'r_PrcipValue_Upper_forecast',
#                 'r_TmaxValue_Lower_forecast', 'r_TmaxValue_Upper_forecast',
#                 'r_TminValue_Lower_forecast', 'r_TminValue_Upper_forecast',
#                 'fcst_Precipitation_last', 'fcst_TmaxValue_last', 'fcst_TminValue_last',
#                 'fcst_Cumulative_Precip_Forecast_Median',
#                 'fcst_Average_TempMax_Forecast_Median',
#                 'fcst_Average_TempMin_Forecast_Median',
#                 'PrcipValue_Range_last', 'TmaxValue_Range_last', 'TminValue_Range_last',
#                 'PrcipValue_Range_forecast', 'TmaxValue_Range_forecast', 'TminValue_Range_forecast',
#                 'Last_Precip_Comparison', 'Forecast_Precip_Comparison',
#                 'Last_Tmax_Comparison', 'Forecast_Tmax_Comparison',
#                 'Last_Tmin_Comparison', 'Forecast_Tmin_Comparison'
#             ]
            
#             # Reorder columns
#             output_data = output_data[column_order]
            
#             # Save to file
#             date_str = current_date.strftime('%Y-%m-%d')
#             filename = f'Final_Temp_Prcp_{date_str}.csv'
#             filepath = os.path.join(output_directory, filename)
            
#             output_data.to_csv(filepath, index=False)
#             print(f"\nSaved enhanced file: {filepath}")
            
#             # Also save as Excel for better readability
#             excel_filename = f'Final_Temp_Prcp_{date_str}.xlsx'
#             excel_filepath = os.path.join(output_directory, excel_filename)
#             output_data.to_excel(excel_filepath, index=False)
#             print(f"Saved Excel file: {excel_filepath}")
            
#             # Display summary statistics
#             print("\nSummary Statistics:")
#             print(f"Total stations processed: {len(output_data)}")
            
#             # Check if WSA historical data was integrated
#             wsa_count = output_data['fcst_Precipitation_last'].notna().sum()
#             if wsa_count > 0:
#                 print(f"\nWSA historical data integrated for {wsa_count} stations")
#                 print("\nSample WSA historical values (first 3 stations with data):")
#                 sample_data = output_data[output_data['fcst_Precipitation_last'].notna()].head(3)
#                 for _, row in sample_data.iterrows():
#                     print(f"  Station {row['Station']}:")
#                     print(f"    Precip (sum): {row['fcst_Precipitation_last']:.2f}")
#                     print(f"    Tmax (avg): {row['fcst_TmaxValue_last']:.1f}")
#                     print(f"    Tmin (avg): {row['fcst_TminValue_last']:.1f}")
#             else:
#                 print("\nWarning: No WSA historical data was integrated. Check if:")
#                 print("  1. WSA_forecast_Temp_Precip.csv file exists")
#                 print("  2. Station names match between files")
#                 print("  3. Date ranges overlap correctly")
            
#             # Count comparisons
#             valid_comparisons = output_data['Last_Precip_Comparison'].str.len().gt(0).sum()
#             if valid_comparisons > 0:
#                 print(f"\nComparison analysis completed for {valid_comparisons} stations")
#                 print("\nLast Period Comparisons:")
#                 print(output_data['Last_Precip_Comparison'].value_counts())
#                 print("\nForecast Period Comparisons:")
#                 print(output_data['Forecast_Precip_Comparison'].value_counts())
            
#             print("\nWeather forecast summary creation completed!")
#             print(f"\nDate columns have been split:")
#             print(f"Historical period: {hist_from} to {hist_to}")
#             print(f"Forecast period: {forecast_from} to {forecast_to}")
            
#             return output_data

# ##### Katherine's Code WISKI

#     def fetch_wiski_data(self, station_paths, data_type, base_url, common_params, date_params, today_date):
#         """Fetch data from WISKI API for given station paths and data type"""
#         import requests
#         import io
        
#         print(f"\n=== FETCHING {data_type.upper()} DATA FROM WISKI ===")
        
#         # Create output path based on data type
#         if data_type == 'water_level':
#             output_csv_path = os.path.join(self.output_dir, f'Reservoir_wl_{today_date}.csv')
#         elif data_type == 'storage':
#             output_csv_path = os.path.join(self.output_dir, f'Reservoir_storage_{today_date}.csv')
#         elif data_type == 'percentage':
#             output_csv_path = os.path.join(self.output_dir, f'Reservoir_precent_{today_date}.csv')
        
#         combined_data = []
        
#         for station_path in station_paths:
#             params = {**common_params, "ts_path": station_path}
#             params.update(date_params)

#             try:
#                 r = requests.get(base_url, params=params, timeout=30)
#                 r.raise_for_status()
                
#                 csv_lines = r.text.splitlines()
#                 print(f"Processing station: {station_path}")
                
#                 # Extract metadata
#                 metadata = {}
#                 for line in csv_lines:
#                     if line.startswith("#station_name;"):
#                         metadata['station_name'] = line.split(';')[1]
#                     elif line.startswith("#station_latitude;"):
#                         metadata['station_latitude'] = line.split(';')[1]
#                     elif line.startswith("#station_longitude;"):
#                         metadata['station_longitude'] = line.split(';')[1]
#                     elif line.startswith("#station_no;"):
#                         metadata['station_no'] = line.split(';')[1]

#                 # Extract actual data lines
#                 data_lines = [line for line in csv_lines if not line.startswith('#')]

#                 if not data_lines:
#                     print(f"No data available for station '{station_path}'")
#                     continue

#                 # Read the actual data into a DataFrame
#                 data_csv = io.StringIO('\n'.join(data_lines))
#                 df = pd.read_csv(data_csv, names=['Timestamp', 'Value'], sep=';')

#                 # Convert the 'Timestamp' column to date format only
#                 df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce').dt.date
#                 df = df.dropna(subset=['Timestamp'])

#                 if 'Value' in df.columns:
#                     df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
#                     df = df.dropna(subset=['Value'])
#                 else:
#                     print(f"'Value' column not found in data for station '{station_path}'")
#                     continue

#                 # Group by 'Timestamp' and calculate the last of 'Value'
#                 df = df.groupby('Timestamp', as_index=False).last()

#                 # Add the metadata columns to the DataFrame
#                 df['Station Name'] = metadata.get('station_name', '')
#                 df['Latitude'] = metadata.get('station_latitude', '')
#                 df['Longitude'] = metadata.get('station_longitude', '')
#                 df['Station Number'] = metadata.get('station_no', '')

#                 combined_data.append(df)
#                 print(f"Data for station '{station_path}' processed successfully.")

#             except Exception as e:
#                 print(f"Error processing station '{station_path}': {e}")

#         # Combine all DataFrames
#         if combined_data:
#             combined_df = pd.concat(combined_data, ignore_index=True)
#             if not combined_df.empty:
#                 combined_df.to_csv(output_csv_path, index=False)
#                 print(f"CSV file '{output_csv_path}' saved successfully.")
#                 return combined_df
        
#         return pd.DataFrame()

#     def combine_wiski_and_wrmm_data(self, today_date):
#         """Combine WISKI and WRMM reservoir data"""
#         print("\n=== COMBINING WISKI DATA AND CALCULATING WEEKLY AVERAGES ===")
        
#         wl_path = os.path.join(self.output_dir, f"Reservoir_wl_{today_date}.csv")
#         storage_path = os.path.join(self.output_dir, f"Reservoir_storage_{today_date}.csv")
#         percent_path = os.path.join(self.output_dir, f"Reservoir_precent_{today_date}.csv")
        
#         try:
#             # Read WISKI CSVs
#             wl_df = pd.read_csv(wl_path, parse_dates=['Timestamp'], dayfirst=True)
#             storage_df = pd.read_csv(storage_path, parse_dates=['Timestamp'], dayfirst=True)
#             percent_df = pd.read_csv(percent_path, parse_dates=['Timestamp'], dayfirst=True)
            
#             # Merge on station info and Timestamp
#             merge_cols = ['Station Number', 'Station Name', 'Latitude', 'Longitude', 'Timestamp']
#             combined = wl_df.merge(storage_df, on=merge_cols, how='outer') \
#                             .merge(percent_df, on=merge_cols, how='outer')
            
#             # Rename columns for clarity
#             combined.rename(columns={
#                 'Value_x': 'Water Level',
#                 'Value_y': 'Storage',
#                 'Value': 'Percent'
#             }, inplace=True)
            
#             # Ensure Timestamp is datetime
#             combined['Timestamp'] = pd.to_datetime(combined['Timestamp'])
            
#             # Calculate weekly averages using custom week grouping based on start_week
#             def create_week_groups_for_wiski(df, start_date_str="2025-01-01"):
#                 df = df.copy()
#                 fixed_start = pd.to_datetime(start_date_str)
                
#                 # Only include data from the start date onwards
#                 df = df[df['Timestamp'] >= fixed_start]
                
#                 # Calculate days from start (0-based: Jan 1 = day 0)
#                 df['days_from_start'] = (df['Timestamp'] - fixed_start).dt.days
#                 # Week grouping: days 0-6 = week 1, days 7-13 = week 2, etc.
#                 df['week_group'] = (df['days_from_start'] // 7) + 1
                
#                 # Filter to only include weeks up to start_week (which is when WRMM starts)
#                 df = df[df['week_group'] <= self.start_week]
                
#                 return df
            
#             combined_with_weeks = create_week_groups_for_wiski(combined, "2025-01-01")
            
#             if combined_with_weeks.empty:
#                 print("Warning: No WISKI data found within the specified week range")
#                 return pd.DataFrame()
            
#             weekly_avg = combined_with_weeks.groupby([
#                 'Station Number', 'Station Name', 'Latitude', 'Longitude', 'week_group'
#             ]).agg({
#                 'Water Level': 'last',
#                 'Storage': 'last', 
#                 'Percent': 'last'
#             }).reset_index()
            
#             # Calculate the proper end date for each week period
#             start_date = pd.to_datetime("2025-01-01")
            
#             # For WISKI data, we want the timestamp to represent the END of each week
#             # Week 1: Jan 1-7 -> timestamp = Jan 7
#             # Week 2: Jan 8-14 -> timestamp = Jan 14
#             # etc.
#             weekly_avg['Timestamp'] = start_date + pd.to_timedelta(weekly_avg['week_group'] * 7 - 1, unit='D')
            
#             # For the last week (start_week), make sure it ends on the correct date
#             # If start_week is 26, week 26 should end on June 30, 2025
#             max_week = weekly_avg['week_group'].max()
#             if max_week == self.start_week:
#                 # Calculate the expected end date for the start_week
#                 expected_end_date = start_date + pd.to_timedelta(self.start_week * 7 - 1, unit='D')
                
#                 # Special handling for week 26 to end on June 30
#                 if self.start_week == 26:
#                     expected_end_date = pd.to_datetime("2025-06-30")
                
#                 # Update the timestamp for the last week
#                 mask = weekly_avg['week_group'] == max_week
#                 weekly_avg.loc[mask, 'Timestamp'] = expected_end_date
                
#                 print(f"WISKI data ends at week {max_week} on {expected_end_date.strftime('%Y-%m-%d')}")
            
#             # Use the week group number as interval
#             weekly_avg['Week Interval'] = weekly_avg['week_group']
#             weekly_avg['DataSource'] = 'WISKI'
#             weekly_avg['StationNumber_name'] = (weekly_avg['Station Number'].astype(str) + 
#                                             " " + weekly_avg['Station Name'])
            
#             # Rename columns for clarity
#             weekly_avg = weekly_avg.rename(columns={
#                 'Station Number': 'Station',
#                 'Week Interval': 'Interval',
#                 'Water Level': 'Monitoring_WL',
#                 'Storage': 'Monitoring_Storage',
#                 'Percent': 'Monitoring_%Full',
#             })
            
#             # Save combined data
#             combined_output_path = os.path.join(self.output_dir, f"Reservoir_combined_{today_date}.csv")
#             weekly_output_path = os.path.join(self.output_dir, f"Reservoir_weekly_{today_date}.csv")
            
#             combined.to_csv(combined_output_path, index=False)
#             weekly_avg.to_csv(weekly_output_path, index=False)
            
#             print(f"Combined data saved: {len(combined)} rows -> {combined_output_path}")
#             print(f"Weekly averages saved: {len(weekly_avg)} rows -> {weekly_output_path}")
#             print(f"WISKI weeks included: {sorted(weekly_avg['Interval'].unique())}")
            
#             return weekly_avg
            
#         except FileNotFoundError as e:
#             print(f"Error: Could not find required files: {e}")
#             return pd.DataFrame()
#         except Exception as e:
#             print(f"Error processing WISKI data: {e}")
#             return pd.DataFrame()
        

#     def integrate_wiski_data(self, 
#                         station_list_path=None, 
#                         wrmm_file_name=None,
#                         base_url="http://wiskitsm1.goa.ds.gov.ab.ca:8080/KiWIS/KiWIS",
#                         date_params=None):
#         """Main method to integrate WISKI data with WRMM outputs"""
#         from datetime import datetime, timedelta
        
#         print("=== STARTING WISKI-WRMM INTEGRATION ===")
        
#         # Set default paths if not provided
#         if station_list_path is None:
#             station_list_path = os.path.join(
#                 os.path.dirname(os.path.dirname(self.output_dir)), 
#                 "Wiski_Reservoire_file", 
#                 "WRMM_Reservoir_list.csv"
#             )
        
#         if wrmm_file_name is None:
#             wrmm_file_name = f'WK{self.start_week}_{self.end_week}_WrmmOutputs.csv'

#         if date_params is None:
#             # Calculate the correct end date for WISKI based on start_week
#             wiski_end_date = self.calculate_wiski_end_date(self.start_week, year=2025)
#             date_params = {
#                 "from": "2025-01-01",
#                 "to": wiski_end_date
#             }
#             print(f"Auto-calculated WISKI end date: {wiski_end_date} (day before week {self.start_week})")

#         # Use week range for file naming instead of today's date
#         date_identifier = f"WK{self.start_week}_{self.end_week}"
        
#         # Store end date for use in other methods
#         self.wiski_end_date = date_params.get('to', None)
        
#         print(f"Station list path: {station_list_path}")
#         print(f"WRMM file: {wrmm_file_name}")
#         print(f"Output directory: {self.output_dir}")
        
#         try:
#             # Load station configuration
#             stations_df = pd.read_csv(station_list_path)
#             print(f" Station list loaded: {len(stations_df)} stations")
            
#             # Base URL and common parameters for WISKI API
#             common_params = {
#                 "service": "kisters",
#                 "type": "queryServices",
#                 "request": "getTimeseriesValues",
#                 "datasource": 0,
#                 "format": "csv",
#                 "metadata": "true"
#             }
            
#             # Extract station paths
#             wl_paths = stations_df['wl_path'].tolist()
#             storage_paths = stations_df['storage_path'].tolist()
#             percent_paths = stations_df['precent_path'].tolist()
            
#             print(f"Water level paths: {len(wl_paths)} stations")
#             print(f"Storage paths: {len(storage_paths)} stations") 
#             print(f"Percentage paths: {len(percent_paths)} stations")
            
#             wl_data = self.fetch_wiski_data(wl_paths, 'water_level', base_url, common_params, date_params, date_identifier)
#             storage_data = self.fetch_wiski_data(storage_paths, 'storage', base_url, common_params, date_params, date_identifier)
#             percent_data = self.fetch_wiski_data(percent_paths, 'percentage', base_url, common_params, date_params, date_identifier)

#             # Process and combine WISKI data
#             wiski_weekly_data = self.combine_wiski_and_wrmm_data(date_identifier)
            
#         except FileNotFoundError:
#             print(f" Error: Could not find station list file: {station_list_path}")
#             wiski_weekly_data = pd.DataFrame()
#         except Exception as e:
#             print(f" Error processing WISKI data: {e}")
#             wiski_weekly_data = pd.DataFrame()
        
#         try:
#             # Process WRMM data
#             wrmm_data_path = os.path.join(self.output_dir, wrmm_file_name)
#             wrmm_data = self.process_wrmm_reservoir_data(wrmm_data_path)
            
#             # Save WRMM data
#             wrmm_output_path = os.path.join(self.output_dir, 'wrmm_res_extract.csv')
#             wrmm_data.to_csv(wrmm_output_path, index=False)
#             print(f" WRMM data saved to: {wrmm_output_path}")
            
#         except FileNotFoundError:
#             print(f" Error: Could not find WRMM data file: {wrmm_data_path}")
#             wrmm_data = pd.DataFrame()
#         except Exception as e:
#             print(f" Error processing WRMM data: {e}")
#             wrmm_data = pd.DataFrame()
        
#         # Combine WRMM and WISKI data
#         if not wrmm_data.empty and not wiski_weekly_data.empty:
#             print("\n=== COMBINING WRMM AND WISKI DATA ===")
            
#             # Combine the DataFrames
#             combined_df = pd.concat([wrmm_data, wiski_weekly_data], ignore_index=True)
            
#             print(f"Combined data shape: {combined_df.shape}")
#             print("Combined unique stations:", sorted(combined_df['Station'].unique()) if 'Station' in combined_df.columns else "Station column not found")
            
#             # === ADJUST WISKI TIMESTAMPS FOR START_WEEK (REMOVED) ===
#             print(f"\n=== SKIPPING WISKI TIMESTAMP ADJUSTMENT FOR START_WEEK ({self.start_week}) ===")
#             print("Timestamp adjustment removed to prevent date issues with WISKI data")
            
#             # === REMOVE BADGER STATION ROWS ===
#             print(f"\n=== REMOVING BADGER STATION ROWS ===")

#             if 'StationName' in combined_df.columns:
#                 # Count rows before removal
#                 initial_count = len(combined_df)
                
#                 # Remove rows where StationName contains "Badger"
#                 combined_df = combined_df[combined_df['StationName'] != 'Badger']
                
#                 # Report the removal
#                 removed_count = initial_count - len(combined_df)
#                 if removed_count > 0:
#                     print(f" Removed {removed_count} rows with StationName = 'Badger'")
#                 else:
#                     print(f" No 'Badger' station rows found to remove")
#             else:
#                 print(f" Column 'StationName' not found - cannot remove Badger rows")

            
#             # Save the final combined file
#             # final_output_path = os.path.join(self.output_dir, f'WISKI_WRMM_{today_date}.csv')
#             # Save the final combined file
#             print("DATE IDENTIFIER: ",date_identifier)
            
#             combined_df['Timestamp'] = pd.to_datetime(combined_df['Timestamp']).dt.strftime('%m/%d/%Y')

#             final_output_path = os.path.join(self.output_dir, f'WISKI_WRMM_{date_identifier}.csv')
#             combined_df.to_csv(final_output_path, index=False)
            
#             print(f"\n WISKI-WRMM INTEGRATION COMPLETE!")
#             print(f" Final file saved: {final_output_path}")
#             print(f" Total rows in output: {len(combined_df)}")
#             print(f" Total unique stations: {len(combined_df['Station'].unique())}")
            
#             return combined_df
            
#         else:
#             print(" ERROR: Missing required data to combine WRMM and WISKI datasets")
#             if wrmm_data.empty:
#                 print("   - WRMM data is empty")
#             if wiski_weekly_data.empty:
#                 print("   - WISKI data is empty")
#             return pd.DataFrame()
        

#     def calculate_wiski_end_date(self, start_week, year=2025):
#         """Calculate the end date for WISKI data based on start_week."""
#         from datetime import datetime, timedelta
        
#         # Week 1 starts on January 7, 2025 (Tuesday) - matches your week calculation logic
#         week_1_start = datetime(year, 1, 7)
        
#         # Calculate the start date of the target week
#         target_week_start = week_1_start + timedelta(weeks=start_week - 1)
        
#         # WISKI should end the day before the target week starts
#         wiski_end_date = target_week_start - timedelta(days=1)
        
#         return wiski_end_date.strftime('%Y-%m-%d')

#     def process_wrmm_reservoir_data(self, wrmm_data_path):
#         """Process WRMM model data for reservoir information"""
#         print("\n=== PROCESSING WRMM RESERVOIR DATA ===")
        
#         df = pd.read_csv(wrmm_data_path)
        
#         reservoir_names = ['Gleniffer Lake', 'Lake McGregor', 'Travers', 'Oldman', 'Pine Coulee',
#                         'Waterton', 'St. Mary', 'Glenmore', 'Twin Valley',
#                         'Badger', 'Keho Lake', 'Chain Lakes', 'Crawling Valley',
#                         'Lake Newell', 'Chestermere Lake', 'Payne Lake', 'Milk River Ridge', 'Chin']
        
#         # Normalize the case
#         df['ComponentType'] = df['ComponentType'].str.strip().str.upper()
#         df['ComponentName'] = df['ComponentName'].str.strip().str.lower()
#         reservoir_names = [name.lower() for name in reservoir_names]
        
#         # Filter for reservoir data
#         reservoir_value = df[(df['ComponentType'] == 'RESERV') & (df['ComponentName'].isin(reservoir_names))]
#         reservoir_value = reservoir_value[['Date', 'Value', 'ComponentName', 'Interval', 'Year', 'PerStorage', 'Data_type']]
        
#         # Convert 'Date' column to datetime format
#         reservoir_value['Date'] = pd.to_datetime(reservoir_value['Date'], errors='coerce')
#         reservoir_value = reservoir_value.sort_values(by='Date', ascending=True)
#         reservoir_value['Date'] = reservoir_value['Date'].dt.strftime('%Y-%m-%d')
        
#         # Station mapping functions
#         def get_station_number(component_name):
#             station_mapping = {
#                 'gleniffer lake': '05CB006', 'lake mcgregor': '05AC022', 'travers': '05AC921',
#                 'oldman': '05AA032', 'pine coulee': '05AB044', 'waterton': '05AD026',
#                 'st. mary': '05AE025', 'glenmore': '05BJ008', 'twin valley': '05AC940',
#                 'badger': '', 'keho lake': '05AC919', 'chain lakes': '05AB037',
#                 'crawling valley': '05BM908', 'lake newell': '05BN901', 'chestermere lake': '05BM904',
#                 'payne lake': '05AD940', 'milk river ridge': '05AF030', 'chin': '05AG901'
#             }
#             return station_mapping.get(component_name.lower(), '')
        
#         def get_station_name(component_name):
#             station_mapping = {
#                 'gleniffer lake': 'Gleniffer Reservoir near Dickson - WSC',
#                 'lake mcgregor': 'Lake Mcgregor at South Dam - EPA',
#                 'travers': 'Travers Reservoir near Enchant - EPA',
#                 'oldman': 'Oldman Reservoir near Pincher Creek - WSC',
#                 'pine coulee': 'Pine Coulee Reservoir near Stavely - WSC',
#                 'waterton': 'Waterton Reservoir - WSC',
#                 'st. mary': 'St. Mary Reservoir near Spring Coulee - WSC',
#                 'glenmore': 'Glenmore Reservoir at Calgary - COC',
#                 'twin valley': 'Twin Valley Reservoir - EPA',
#                 'badger': 'Badger',
#                 'keho lake': 'Keho Lake near Nobleford - EPA',
#                 'chain lakes': 'Chain Lakes Reservoir near Nanton - WSC',
#                 'crawling valley': 'Crawling Valley Reservoir - EID',
#                 'lake newell': 'Lake Newell - EID',
#                 'chestermere lake': 'Chestermere Lake at South Outlet - EPA',
#                 'payne lake': 'Payne Lake Reservoir near Mountain View - EPA',
#                 'milk river ridge': 'Milk River Ridge Reservoir',
#                 'chin': 'Chin Reservoir - SMRID'
#             }
#             return station_mapping.get(component_name.lower(), '')
        
#         # Add station information
#         reservoir_value['StationNumber'] = reservoir_value['ComponentName'].apply(get_station_number)
#         reservoir_value['StationName'] = reservoir_value['ComponentName'].apply(get_station_name)
        
#         # Create Target_value and S0_value columns
#         reservoir_value['Target_value'] = reservoir_value.apply(
#             lambda row: row['Value'] if row['Data_type'] == 'Target' else None, axis=1
#         )
#         reservoir_value['Predicted Flow'] = reservoir_value.apply(
#             lambda row: row['Value'] if row['Data_type'] == 'Predicted Flow' else None, axis=1
#         )
        
#         # Drop ComponentName column
#         reservoir_value = reservoir_value.drop(columns=['ComponentName'])
        
#         # Group and aggregate data
#         reservoir_consolidated = reservoir_value.groupby(['Date', 'Interval', 'Year', 'StationNumber', 'StationName']).agg({
#             'Target_value': lambda x: x.dropna().iloc[0] if not x.dropna().empty else None,
#             'Predicted Flow': lambda x: x.dropna().iloc[0] if not x.dropna().empty else None,
#             'PerStorage': lambda x: x.dropna().iloc[0] if not x.dropna().empty else None
#         }).reset_index()
        
#         # Rename columns
#         reservoir_consolidated = reservoir_consolidated.rename(columns={
#             'StationNumber': 'Station',
#             'Date': 'Timestamp',
#             'Predicted Flow': 'Value',
#             'PerStorage': 'Storage'
#         })
        
#         # Add additional columns
#         reservoir_consolidated['DataSource'] = 'WRMM'
#         reservoir_consolidated['StationNumber_name'] = (reservoir_consolidated['Station'].astype(str) + 
#                                                     ' ' + reservoir_consolidated['StationName'].astype(str))
        
#         print(f"WRMM reservoir data processed: {len(reservoir_consolidated)} rows")
#         return reservoir_consolidated

# #### Summary Table IC/WCO for Ben

#     def create_io_wco_summary(self, 
#                             input_file4_path=None,
#                             input_file5_path=None,
#                             output_directory=None):
#         """
#         Create IO (Instream Objectives) and WCO (Water Conservation Objectives) summary analysis.
        
#         This method processes WSA datasets to analyze compliance with instream objectives
#         and water conservation objectives, generating detailed reports and summary tables.
        
#         Args:
#             input_file4_path (str): Path to WSA_4_2025.csv file
#             input_file5_path (str): Path to WSA_5_2025.csv file  
#             output_directory (str): Directory to save output files
            
#         Returns:
#             pandas.DataFrame: Final IO/WCO summary table
#         """
        
#         print("\n" + "="*60)
#         print("Creating IO/WCO Summary Analysis")
#         print("="*60 + "\n")
        
#         # Set default paths if not provided
#         if output_directory is None:
#             output_directory = self.output_dir
            
#         if input_file4_path is None:
#             input_file4_path = r"\\C-GOA-APM-13251\WaterManagementDashboard_13251\PBI_Data\WSA_4_2025.csv"
            
#         if input_file5_path is None:
#             input_file5_path = r"\\C-GOA-APM-13251\WaterManagementDashboard_13251\PBI_Data\WSA_5_2025.csv"
        
#         try:
#             # Load the datasets
#             print(f"Loading WSA datasets...")
#             print(f"File 4: {input_file4_path}")
#             print(f"File 5: {input_file5_path}")
            
#             df4 = pd.read_csv(input_file4_path, parse_dates=["Date"])
#             df5 = pd.read_csv(input_file5_path, parse_dates=["Date"])
            
#             print(f" Dataset 4 loaded: {len(df4)} rows")
#             print(f" Dataset 5 loaded: {len(df5)} rows")
            
#         except FileNotFoundError as e:
#             print(f" Error: Could not find required WSA files: {e}")
#             return None
#         except Exception as e:
#             print(f" Error loading WSA data: {e}")
#             return None
        
#         # Report date ranges
#         oldest_date = df4["Date"].min()
#         newest_date = df4["Date"].max()
#         days_diff = (newest_date - oldest_date).days
        
#         print(f"\nDataset Date Analysis:")
#         print(f"Oldest date in dataset: {oldest_date.date()}")
#         print(f"Newest date in dataset: {newest_date.date()}")
#         print(f"Number of days in record: {days_diff}")
        
#         # Separate data in WSA_5_2025 by ts_name
#         print(f"\nProcessing data by ts_name groups...")
#         grouped = df5.groupby('ts_name')
#         print(f"Found {len(grouped)} unique ts_name groups")
        
#         # Create intermediate sorted file
#         ct = 1
#         sorted_output_file = os.path.join(output_directory, 'sorted_by_ts_name.xlsx')
        
#         with pd.ExcelWriter(sorted_output_file, engine='openpyxl') as writer:
#             for ts_name, group in grouped:
#                 sheet_name = f'ts_name{ct}'
#                 group.to_excel(writer, sheet_name=sheet_name, index=False)
#                 ct += 1
        
#         print(f" Intermediate file created: {sorted_output_file}")
        
#         # Load the sorted workbook and process each sheet
#         excel_file = pd.ExcelFile(sorted_output_file)
#         summary_list = []  # Initialize list to store all summaries
        
#         print(f"\nProcessing {len(excel_file.sheet_names)} sheets for merge and analysis...")
        
#         # Create merged output file
#         merged_output_file = os.path.join(output_directory, 'merged_output.xlsx')
        
#         with pd.ExcelWriter(merged_output_file, engine='openpyxl') as writer:
#             for i, sheet_name in enumerate(excel_file.sheet_names):
#                 print(f"Processing sheet {i+1}/{len(excel_file.sheet_names)}: {sheet_name}")
                
#                 df_sheet = excel_file.parse(sheet_name)
                
#                 # Merge with df4 — adjust join columns as needed
#                 merged = pd.merge(
#                     df_sheet, 
#                     df4, 
#                     left_on=["WB_station", "Date"],
#                     right_on=["REF_Station", "Date"],
#                     how="inner"
#                 )
                
#                 if len(merged) == 0:
#                     print(f"  Warning: No matching records found for {sheet_name}")
#                     continue
                
#                 # Add computed columns
                
#                 # Days_IO: 'Y' if Value and IO_Value are present
#                 merged["Days_IO"] = merged.apply(
#                     lambda row: "Y" if pd.notnull(row.get("IO_Value")) and pd.notnull(row.get("Value")) else "",
#                     axis=1
#                 )
                
#                 # Days_WCO: 'Y' if Value and WCO_Value are present  
#                 merged["Days_WCO"] = merged.apply(
#                     lambda row: "Y" if pd.notnull(row.get("WCO_Value")) and pd.notnull(row.get("Value")) else "",
#                     axis=1
#                 )
                
#                 # IO_Not_Met: 'Y' if IFN_Value > Value (corrected from original code)
#                 merged["IO_Not_Met"] = merged.apply(
#                     lambda row: "Y" if (pd.notnull(row.get("IO_Value")) and 
#                                     pd.notnull(row.get("Value")) and 
#                                     pd.notnull(row.get("IFN_Value")) and
#                                     row["IFN_Value"] > row["Value"]) else "",
#                     axis=1
#                 )
                
#                 # WCO_Not_Met: 'Y' if IFN_Value > Value (when WCO_Value and Value are not null)
#                 merged["WCO_Not_Met"] = merged.apply(
#                     lambda row: "Y" if (pd.notnull(row.get("WCO_Value")) and 
#                                     pd.notnull(row.get("Value")) and 
#                                     pd.notnull(row.get("IFN_Value")) and
#                                     row["IFN_Value"] > row["Value"]) else "",
#                     axis=1
#                 )
                
#                 # Write merged sheet
#                 merged.to_excel(writer, sheet_name=f"Merged_{sheet_name}", index=False)
                
#                 # Generate summary table for this sheet
#                 try:
#                     # Ensure we have the required columns for grouping
#                     group_cols = []
#                     if "REF_Station" in merged.columns:
#                         group_cols.append("REF_Station")
#                     if "StationName_x" in merged.columns:
#                         group_cols.append("StationName_x")
#                     elif "StationName" in merged.columns:
#                         group_cols.append("StationName")
#                     if "WB_station" in merged.columns:
#                         group_cols.append("WB_station")
                    
#                     if len(group_cols) >= 2:  # Need at least station identifiers
#                         summary = merged.groupby(group_cols).agg(
#                             IO_Not_Met_Count=("IO_Not_Met", lambda x: (x == "Y").sum()),
#                             Days_IO_Count=("Days_IO", lambda x: (x == "Y").sum()),
#                             WCO_Not_Met_Count=("WCO_Not_Met", lambda x: (x == "Y").sum()),
#                             Days_WCO_Count=("Days_WCO", lambda x: (x == "Y").sum())
#                         ).reset_index()
                        
#                         summary["SourceSheet"] = sheet_name  # Add identifier for traceability
#                         summary_list.append(summary)  # Collect for global summary
                        
#                         print(f"  Summary created: {len(summary)} station records")
#                     else:
#                         print(f"   Insufficient columns for summary in {sheet_name}")
                        
#                 except Exception as e:
#                     print(f"   Error creating summary for {sheet_name}: {e}")
#                     continue
        
#         print(f" Merged data saved: {merged_output_file}")
        
#         # Combine all summaries and create final output
#         if not summary_list:
#             print("No summary data generated. Check data compatibility.")
#             return None
        
#         print(f"\nCombining summaries from {len(summary_list)} sheets...")
        
#         # Combine all summaries
#         summary_all = pd.concat(summary_list, ignore_index=True)
        
#         # Save intermediate summary
#         intermediate_summary_file = os.path.join(output_directory, 'WSA_2025_Summary_Table.xlsx')
#         summary_all_sorted = summary_all.sort_values(by=summary_all.columns[1])  # Sort by station name column
#         summary_all_sorted.to_excel(intermediate_summary_file, index=False)
#         print(f" Intermediate summary saved: {intermediate_summary_file}")
        
#         # Create final consolidated summary
#         print(f"Creating final consolidated summary...")
        
#         # Determine grouping columns dynamically
#         group_cols_final = []
#         for col in ["REF_Station", "StationName_x", "StationName", "WB_station"]:
#             if col in summary_all.columns:
#                 group_cols_final.append(col)
        
#         if len(group_cols_final) < 2:
#             print(" Error: Insufficient columns for final grouping")
#             return summary_all
        
#         # Group and aggregate to collapse duplicates across sheets
#         summary_final = summary_all.groupby(group_cols_final, as_index=False).agg(
#             IO_Not_Met_Count=("IO_Not_Met_Count", "sum"),
#             Days_IO_Count=("Days_IO_Count", "sum"),
#             WCO_Not_Met_Count=("WCO_Not_Met_Count", "sum"),
#             Days_WCO_Count=("Days_WCO_Count", "sum")
#         )
        
#         # Sort for readability
#         summary_final = summary_final.sort_values(by=summary_final.columns[1])
        
#         # Convert columns to object type so they can hold both int and str
#         for col in ["IO_Not_Met_Count", "Days_IO_Count", "WCO_Not_Met_Count", "Days_WCO_Count"]:
#             if col in summary_final.columns:
#                 summary_final[col] = summary_final[col].astype("object")
        
#         # Replace IO-related values with "NA" where Days_IO_Count < 1
#         if "Days_IO_Count" in summary_final.columns:
#             io_mask = summary_final["Days_IO_Count"] < 1
#             summary_final.loc[io_mask, ["IO_Not_Met_Count", "Days_IO_Count"]] = "NA"
        
#         # Replace WCO-related values with "NA" where Days_WCO_Count < 1  
#         if "Days_WCO_Count" in summary_final.columns:
#             wco_mask = summary_final["Days_WCO_Count"] < 1
#             summary_final.loc[wco_mask, ["WCO_Not_Met_Count", "Days_WCO_Count"]] = "NA"
        
#         # Create clean column mapping for final output
#         column_mapping = {}
#         final_columns = []
        
#         # Map columns based on what exists
#         if "REF_Station" in summary_final.columns:
#             column_mapping["REF_Station"] = "WSC ID"
#             final_columns.append("REF_Station")
        
#         if "StationName_x" in summary_final.columns:
#             column_mapping["StationName_x"] = "Station Name"
#             final_columns.append("StationName_x")
#         elif "StationName" in summary_final.columns:
#             column_mapping["StationName"] = "Station Name"
#             final_columns.append("StationName")
        
#         # Add metric columns if they exist
#         for old_col, new_col in [
#             ("IO_Not_Met_Count", "# Days IO Not Met"),
#             ("Days_IO_Count", "Total # Days - IO"),
#             ("WCO_Not_Met_Count", "# Days WCO Not Met"),
#             ("Days_WCO_Count", "Total # Days - WCO")
#         ]:
#             if old_col in summary_final.columns:
#                 column_mapping[old_col] = new_col
#                 final_columns.append(old_col)
        
#         # Select and rename columns
#         summary_final_clean = summary_final[final_columns].rename(columns=column_mapping)
        
#         # Save the final condensed summary
#         final_output_file = os.path.join(output_directory, "IO_WCO_Summary_Table_Final.xlsx")
#         summary_final_clean.to_excel(
#             final_output_file, 
#             sheet_name="IO_WCO_Summary_Table_Final", 
#             index=False
#         )
        
#         print(f"Final IO/WCO summary saved: {final_output_file}")
        
#         # Display summary statistics
#         print(f"\n" + "="*50)
#         print("IO/WCO Analysis Summary")
#         print("="*50)
#         print(f"Total stations analyzed: {len(summary_final_clean)}")
        
#         # Count stations with IO data
#         if "Total # Days - IO" in summary_final_clean.columns:
#             io_stations = summary_final_clean["Total # Days - IO"] != "NA"
#             io_count = io_stations.sum() if hasattr(io_stations, 'sum') else 0
#             print(f"Stations with IO objectives: {io_count}")
        
#         # Count stations with WCO data  
#         if "Total # Days - WCO" in summary_final_clean.columns:
#             wco_stations = summary_final_clean["Total # Days - WCO"] != "NA"
#             wco_count = wco_stations.sum() if hasattr(wco_stations, 'sum') else 0
#             print(f"Stations with WCO objectives: {wco_count}")
        
#         print(f"\nOutput files created:")
#         print(f"  1. {sorted_output_file}")
#         print(f"  2. {merged_output_file}")
#         print(f"  3. {intermediate_summary_file}")
#         print(f"  4. {final_output_file}")
        
#         print(f"\n IO/WCO Analysis completed successfully!")
#         # After saving the final summary, delete intermediate files
#         excel_file.close()
#         try:
#             os.remove(sorted_output_file)
#             os.remove(merged_output_file)
#             os.remove(intermediate_summary_file)
#             print("\n Intermediate files deleted successfully.")
#         except Exception as e:
#             print(f" Error while deleting intermediate files: {e}")

#         return summary_final_clean



# ==========================================
# PART 1: DATABASE IMPORTS
# ==========================================
# Add this after line 16 (after warnings.filterwarnings('ignore'))

# DATABASE INTEGRATION - Added for direct PostgreSQL push
from WRMMDatabaseUtils import WRMMOutputManager
import logging

logger = logging.getLogger(__name__)

# ==========================================
# PART 2: DATABASE EXPORT SECTION
# ==========================================
# REPLACE lines 688-692 (the export section) WITH THIS COMPLETE BLOCK:

        # Export data to DATABASE
        # Initialize database output manager
        db_config = {
            'host': 'C-GOA-APM-13251',
            'port': '5432',
            'database': 'Main',
            'user': 'postgres',
            'password': 'IEMP_POSTGRES',
            'schema': 'wrmm_sopan'  # YOUR SCHEMA NAME - CHANGE IF DIFFERENT
        }
        
        output_manager = WRMMOutputManager(
            output_dir=output_dir,
            db_config=db_config,
            enable_database=True,
            enable_files=False  # Database-only mode
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
            logger.info(f"✓ Main output: {len(master_data_file)} rows pushed to database")
        
        # 2. Executive summary
        success_exec = output_manager.db_manager.push_dataframe(
            df=master_ex_summary,
            table_name='executive_summary',
            if_exists='append',
            batch_size=500
        )
        if success_exec:
            logger.info(f"✓ Executive summary: {len(master_ex_summary)} rows pushed to database")
        
        # 3. Reservoir inflow
        success_res = output_manager.db_manager.push_dataframe(
            df=master_res_inflow_annual,
            table_name='reservoir_inflow',
            if_exists='append',
            batch_size=500
        )
        if success_res:
            logger.info(f"✓ Reservoir inflow: {len(master_res_inflow_annual)} rows pushed to database")
        
        logger.info("✓ All data exported to database successfully")