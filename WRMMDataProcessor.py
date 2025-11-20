# Import necessary libraries
import pyodbc
import pandas as pd
import os
import shutil
from datetime import datetime, timedelta
import re
import numpy as np
import math
import warnings
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

warnings.filterwarnings('ignore')


#### New Optimized functions

class WRMMDataProcessor:
    """
    A class for processing and analyzing data from Water Resources Management Model (WRMM).

    This class provides methods for reading, processing, and analyzing various types of data
    related to water resources management, including irrigation, reservoirs, and water conservation objectives.

    Attributes:
        model_dir (str): Directory containing the model files.
        path_name_list (list): List of path names for different model scenarios.
        reference_file_name (str): Name of the reference file.
        seconds_in_day (int): Number of seconds in a day.
    """
    def __init__(self, model_dir, path_name_list, reference_file_name, seconds_in_day):
        """
        Initialize the WRMMDataProcessor with model directory and parameters.

        Args:
            model_dir (str): Directory containing the model files.
            path_name_list (list): List of path names for different model scenarios.
            reference_file_name (str): Name of the reference file.
            seconds_in_day (int): Number of seconds in a day.
        """
        self.model_dir = model_dir
        self.path_name_list = path_name_list
        self.reference_file_name = reference_file_name
        self.seconds_in_day = seconds_in_day

    def get_weekend_dates(self, year, weeks=52):
        """
        Generate a list of weekly dates starting from January 7th of the given year,
        with exactly 52 weeks ending on December 31st.
        
        Parameters:
        year (int): The year for which to generate the weekend dates.
        weeks (int): Number of weeks to generate. Default is 52.
        
        Returns:
        list of str: A list of formatted date strings with exactly 52 entries
        """
        # Define the specific dates for 52 weeks
        start_date = datetime(year, 1, 7)
        end_date = datetime(year, 12, 31)
        
        weekend_dates = []
        
        # Generate first 51 weeks (regular 7-day intervals)
        for week_num in range(weeks - 1):  # 51 weeks
            current_date = start_date + timedelta(days=week_num * 7)
            weekend_dates.append(current_date.strftime('%d-%b'))
        
        # Add December 31st as the 52nd week
        weekend_dates.append(end_date.strftime('%d-%b'))
        
        return weekend_dates


    def read_mdb(self,mdb_file, table_name):
        """
        Read a table from an MDB file and return it as a DataFrame.

        Args:
            mdb_file (str): Path to the MDB file.
            table_name (str): Name of the table to read.

        Returns:
            pandas.DataFrame: The contents of the specified table.
        """
        drv = '{Microsoft Access Driver (*.mdb, *.accdb)}'
        con = pyodbc.connect(f'DRIVER={drv};DBQ={mdb_file};')
        
        query = f'SELECT * FROM {table_name}'
        df = pd.read_sql(query, con)
        
        con.close()
        return df


    ### Modified by Sopan to get only weeks data
    def read_OutsimOutid(self, model_dir, path_name_list,start_week,end_week):
        """
        Read OutsimOutid data from MDB files for specified weeks.

        Args:
            model_dir (str): Directory containing the model files.
            path_name_list (list): List of path names for different model scenarios.
            start_week (int): Start week for data filtering.
            end_week (int): End week for data filtering.

        Returns:
            pandas.DataFrame: Combined OutsimOutid data for all models and specified weeks.
        """              
        outsim_id_list = []
        
        for path_name in path_name_list:
            mdb_file = os.path.join(model_dir, path_name, 'OutsimOutid.mdb')
            
            # Read tables
            id_table = self.read_mdb(mdb_file, 'OutputID').set_index('ID')
            outsim_table = self.read_mdb(mdb_file, 'Outsim')
            outid_table = self.read_mdb(mdb_file, 'Outid')
            
            # Rename columns
            outsim_table.columns = ['ID', 'Year', 'Interval', 'Simulated']
            outsim_table=outsim_table[(outsim_table.Interval >= start_week) & (outsim_table.Interval <= end_week)]
            outid_table.columns = ['ID', 'Year', 'Interval', 'IdealCondition']
            outid_table=outid_table[(outid_table.Interval >= start_week) & (outid_table.Interval <= end_week)]
            
            # Merge tables
            
            merged = outsim_table.merge(outid_table, on=['ID', 'Year', 'Interval'])
            merged = merged.merge(id_table, left_on='ID', right_index=True)
            
            # Add ModelName and drop ID
            merged['ModelName'] = path_name
            merged = merged.drop('ID', axis=1)
            
            outsim_id_list.append(merged)
        
        # Combine all model outputs
        outsim_id = pd.concat(outsim_id_list, ignore_index=True)
        outsim_id=outsim_id[(outsim_id.Interval >= start_week) & (outsim_id.Interval <= end_week)]
        return outsim_id
    
    
        #### Sopan added it for Full year

    ##### Create a function to read the Whole year of Data
    def read_OutsimOutid_full_year(self, model_dir, path_name_list):
        """
        Read OutsimOutid data from MDB files for specified weeks.

        Args:
            model_dir (str): Directory containing the model files.
            path_name_list (list): List of path names for different model scenarios.
            start_week (int): Start week for data filtering.
            end_week (int): End week for data filtering.

        Returns:
            pandas.DataFrame: Combined OutsimOutid data for all models and specified weeks.
        """              
        outsim_id_list = []
        
        for path_name in path_name_list:
            mdb_file = os.path.join(model_dir, path_name, 'OutsimOutid.mdb')
            
            # Read tables
            id_table = self.read_mdb(mdb_file, 'OutputID').set_index('ID')
            outsim_table = self.read_mdb(mdb_file, 'Outsim')
            outid_table = self.read_mdb(mdb_file, 'Outid')
            
            # Rename columns
            outsim_table.columns = ['ID', 'Year', 'Interval', 'Simulated']
            outid_table.columns = ['ID', 'Year', 'Interval', 'IdealCondition']
            
            # Merge tables
            
            merged = outsim_table.merge(outid_table, on=['ID', 'Year', 'Interval'])
            merged = merged.merge(id_table, left_on='ID', right_index=True)
            
            # Add ModelName and drop ID
            merged['ModelName'] = path_name
            merged = merged.drop('ID', axis=1)
            
            outsim_id_list.append(merged)
        
        # Combine all model outputs
        outsim_id = pd.concat(outsim_id_list, ignore_index=True)
        return outsim_id
    

    def read_irrigation_area(self,model_dir, path_name_list):
        """
            Read irrigation area data from multiple .mdb files and combine them into a single DataFrame.

            This method processes multiple .mdb files located in subdirectories of the given model directory.
            It extracts irrigation area data from each file, combines them, and returns a consolidated DataFrame.

            Parameters:
            -----------
            model_dir : str
                The base directory containing subdirectories with .mdb files.
            path_name_list : list of str
                List of subdirectory names within the model_dir to process.

            Returns:
            --------
            pd.DataFrame
                A DataFrame containing combined irrigation area data with columns:
                - 'ModelName': Name of the subdirectory (model)
                - 'ComponentNumber': Identifier for each irrigation block
                - 'Area_Ha': Area of the irrigation block in hectares

            Notes:
            ------
            - The method reads the 'IrrigationBlocks' table from each .mdb file.
            - The 'LandUseFactor' column is dropped if present.
            - The method assumes the existence of a self.read_mdb method to read .mdb files.
        """
        data_frames = []

        for path_name in path_name_list:
            mdb_file = os.path.join(model_dir, path_name, 'OutsimOutid.mdb')  # Construct the path to the .mdb file

            # Read the irrigation area table from the .mdb file
            area_table = self.read_mdb(mdb_file, 'IrrigationBlocks')

            # Drop the 'LandUseFactor' column
            if 'LandUseFactor' in area_table.columns:
                area_table.drop('LandUseFactor', axis=1, inplace=True)

            # Insert 'ModelName' column
            area_table.insert(0, 'ModelName', path_name)

            # Append the DataFrame to the list
            data_frames.append(area_table)

        # Concatenate all DataFrames in the list into a single DataFrame
        irr_area = pd.concat(data_frames, axis=0, ignore_index=True)

        # Rename columns
        irr_area.columns = ['ModelName', 'ComponentNumber', 'Area_Ha']

        return irr_area


    def read_divchl_maxcap(self,model_dir, path_name_list):
        """
        Read diversion channels maximum annual capacity for multiple paths and combine them.

        Args:
            model_dir (str): Directory containing the model files.
            path_name_list (list): List of path names for different model scenarios.

        Returns:
            pandas.DataFrame: Combined diversion channel capacity data for all models.
        """
        div_cap_list = []
        
        for path_name in path_name_list:
            mdb_file = os.path.join(model_dir, path_name, 'OutsimOutid.mdb')
            
            # Read DiversionChannels table
            div_table = self.read_mdb(mdb_file, 'DiversionChannels')
            div_table['ModelName'] = path_name
            
            div_cap_list.append(div_table)
        
        # Combine all diversion channel data
        div_cap = pd.concat(div_cap_list, ignore_index=True)
        
        return div_cap

    def filter_intervals(self, outsim_id, start_interval, end_interval):
        """
        Filter outsim_id DataFrame based on specified interval range.

        Args:
            outsim_id (pandas.DataFrame): The OutsimOutid data.
            start_interval (int): Start interval for filtering.
            end_interval (int): End interval for filtering.

        Returns:
            pandas.DataFrame: Filtered OutsimOutid data.
        """
        mask = (outsim_id['Interval'] >= start_interval) & (outsim_id['Interval'] <= end_interval)
        return outsim_id[mask].reset_index(drop=True)


    # Update major ideal condition

    def revise_major_idealcondition_data(self, major_mdb, major_div_cap, seconds_in_day, start_week, end_week):
        """
        Update major ideal condition data based on annual diversion capacity.

        Args:
            major_mdb (pandas.DataFrame): Major MDB data.
            major_div_cap (pandas.DataFrame): Major diversion capacity data.
            seconds_in_day (int): Number of seconds in a day.
            start_week (int): Start week for data processing.
            end_week (int): End week for data processing.

        Returns:
            pandas.DataFrame: Updated major ideal condition data.
        """
        # Set index and rename columns
        major_mdb = major_mdb.set_index(['ModelName', 'ComponentNumber'])
        major_mdb = major_mdb.rename(columns={'Simulated': 'Simulated_cms', 'IdealCondition': 'IdealCondition_cms'})

        # Calculate volume in dam3
        seconds_per_interval = np.where(major_mdb.Interval == end_week, 8*seconds_in_day, 7*seconds_in_day)
        major_mdb['Simulated_dam3'] = (major_mdb.Simulated_cms * seconds_per_interval) / 1000
        major_mdb['IdealCondition_dam3'] = (major_mdb.IdealCondition_cms * seconds_per_interval) / 1000

        # Filter data for specified week range
        major_mdb = major_mdb[(major_mdb.Interval >= start_week) & (major_mdb.Interval <= end_week)]

        # Join with major_div_cap
        major_mdb = major_mdb.join(major_div_cap.set_index(['ModelName', 'ComponentNumber']))

        # Calculate annual simulated volume
        annual_sum = major_mdb.groupby(level=[0, 1])['Simulated_dam3'].sum().round(3)
        major_mdb['AnnualSum_Simulated_dam3'] = major_mdb.index.map(annual_sum)

        # Update IdealCondition based on Annual Diversion Capacity
        condition = major_mdb.AnnualSum_Simulated_dam3 >= major_mdb.DivCap_dam3
        major_mdb['IdealCondition_cms'] = np.where(condition, major_mdb.Simulated_cms, major_mdb.IdealCondition_cms)

        # Rename columns back to original
        major_mdb = major_mdb.rename(columns={'Simulated_cms': 'Simulated', 'IdealCondition_cms': 'IdealCondition'})

        # Reset index and select required columns
        result = major_mdb.reset_index()[['ModelName', 'ComponentNumber', 'Year', 'Interval', 'ComponentType',
                                        'Units', 'ComponentDescription', 'Simulated', 'IdealCondition']]

        return result


    def get_demand_deficit_data(self,category, data_type, df, scn_name):
        """
        Extract demand or deficit data from the input DataFrame.

        Args:
            category (str): Category of the data (e.g., 'Irrigation', 'Non-irrigation').
            data_type (str): Type of data to extract ('Demand' or 'Deficit').
            df (pandas.DataFrame): Input DataFrame containing the data.
            scn_name (str): Scenario name.

        Returns:
            pandas.DataFrame: Extracted demand or deficit data.
        """
        if data_type == 'Demand':
            value_col = 'IdealCondition'
            drop_cols = ['Simulated', 'Deficit']
            data_type_prefix = 'Demand_'
            comment_suffix = ' demand'
        else:
            value_col = 'Deficit'
            drop_cols = ['IdealCondition', 'Simulated']
            data_type_prefix = ''
            comment_suffix = ' deficit'

        result = df.drop(columns=drop_cols)
        result['Data_type'] = data_type_prefix + scn_name
        result['Comments'] = category + comment_suffix
        result = result.rename(columns={value_col: 'Value'})

        column_order = ['Data_type', 'ModelName', 'ComponentType', 'ComponentName',
                        'ComponentNumber', 'Year', 'Interval', 'Value', 'Unit', 'Comments']
        
        return result[column_order]

    def process_private_irrigation(self,irr_ref_file, outsim_id, irr_area, name_tag, scenario_name):
        """
        Process private irrigation data and generate summary statistics.

        Args:
            irr_ref_file (pandas.DataFrame): Irrigation reference file.
            outsim_id (pandas.DataFrame): OutsimOutid data.
            irr_area (pandas.DataFrame): Irrigation area data.
            name_tag (str): Tag for naming components.
            scenario_name (str): Name of the scenario.

        Returns:
            pandas.DataFrame: Summary of private irrigation data.
        """
        # Set index and join data
        irr_ref_file = irr_ref_file.set_index(['ModelName', 'ComponentNumber'])
        outsim_id_irr = outsim_id.set_index(['ModelName', 'ComponentNumber']).join(irr_ref_file)
        
        # Filter for irrigation components and join with irrigation area
        irr_table = outsim_id_irr[outsim_id_irr.ComponentType == 'IRRIGAT'].join(
            irr_area.set_index(['ModelName', 'ComponentNumber'])
        )
        
        # Calculate irrigation volume
        irr_table['Simulated_m3'] = (irr_table['Simulated'] / 1000) * (irr_table['Area_Ha'] * 10000)
        irr_table['IdealCondition_m3'] = (irr_table['IdealCondition'] / 1000) * (irr_table['Area_Ha'] * 10000)
        
        # Filter for private irrigation
        irr_table_priv = irr_table[irr_table.IrrigationType == 'Private'].reset_index()
        
        # Group by SubBasin, Year, and Interval
        grouped = irr_table_priv.groupby(['SubBasin', 'Year', 'Interval'])
        
        # Aggregate data
        agg_data = grouped.agg({
            'Area_Ha': 'sum',
            'Simulated_m3': 'sum',
            'IdealCondition_m3': 'sum'
        }).reset_index()
        
        # Calculate allocated and demand
        agg_data['Allocated'] = (agg_data['Simulated_m3'] / (agg_data['Area_Ha'] * 10000)) * 1000
        agg_data['Demand'] = (agg_data['IdealCondition_m3'] / (agg_data['Area_Ha'] * 10000)) * 1000
        
        # Prepare final dataframe
        df4 = pd.DataFrame({
            'ModelName': 'NaN',
            'ComponentType': 'Private Irrigation',
            'ComponentName': agg_data['SubBasin'].str.upper() + ' ' + name_tag,
            'ComponentNumber': 'NaN',
            'Year': agg_data['Year'],
            'Interval': agg_data['Interval'],
            'IdealCondition': agg_data['Demand'],
            'Simulated': agg_data['Allocated'],
            'Unit': 'mm',
            'TotalIrrArea_Ha': agg_data['Area_Ha']
        })
        
        df4['Deficit'] = df4['IdealCondition'] - df4['Simulated']
        
        # Generate summary dataframes
        df5 = df4.groupby(['ComponentName', 'Year'])['Deficit'].sum().round().reset_index()
        df6 = df4.groupby(['ComponentName', 'Year'])['TotalIrrArea_Ha'].mean().round().reset_index()
        
        # Create final summary
        df7 = pd.pivot_table(
            pd.merge(df5, df6, on=['ComponentName', 'Year']),
            values=['Deficit', 'TotalIrrArea_Ha'],
            index='Year',
            columns='ComponentName'
        ).reset_index()
        
        df7.columns = [f"{col[1]}_{col[0]}" if col[1] else col[0] for col in df7.columns]
        df7.insert(0, 'Scenario', scenario_name)
        
        return df7


    def process_irrigation_data(self, reference_file_name, outsim_id, irr_area):
        """
        Process irrigation data for different scales (district, sub-basin, basin).

        Args:
            reference_file_name (str): Name of the reference file.
            outsim_id (pandas.DataFrame): OutsimOutid data.
            irr_area (pandas.DataFrame): Irrigation area data.

        Returns:
            pandas.DataFrame: Processed irrigation data for different scales.
        """       

        # Read reference file for irrigation
        irr_ref_file = pd.read_excel(reference_file_name, sheet_name='Irrigation')
        irr_ref_file = irr_ref_file.iloc[:, :-2]  # Remove last two columns

        # Set index and join data
        index_cols = ['ModelName', 'ComponentNumber']
        irr_table = (outsim_id.set_index(index_cols)
                    .join(irr_ref_file.set_index(index_cols))
                    .join(irr_area.set_index(index_cols)))

        # Filter for irrigation components and calculate volumes
        irr_table = irr_table[irr_table.ComponentType == 'IRRIGAT'].reset_index()
        irr_table['Simulated_m3'] = (irr_table['Simulated'] / 1000) * (irr_table['Area_Ha'] * 10000)
        irr_table['IdealCondition_m3'] = (irr_table['IdealCondition'] / 1000) * (irr_table['Area_Ha'] * 10000)

        # Function to process irrigation data for different scales
        def process_scale(data, scale_column, component_type, name_suffix=''):
            grouped = data.groupby([scale_column, 'Year', 'Interval'])
            agg_data = grouped.agg({
                'Area_Ha': 'sum',
                'Simulated_m3': 'sum',
                'IdealCondition_m3': 'sum',
                'ModelName': 'first'
            }).reset_index()

            agg_data['Simulated'] = (agg_data['Simulated_m3'] / (agg_data['Area_Ha'] * 10000)) * 1000
            agg_data['IdealCondition'] = (agg_data['IdealCondition_m3'] / (agg_data['Area_Ha'] * 10000)) * 1000

            result = pd.DataFrame({
                'ModelName': agg_data['ModelName'],
                'ComponentType': component_type,
                'ComponentName': agg_data[scale_column].str.upper() + name_suffix,
                'ComponentNumber': 'NaN',
                'Year': agg_data['Year'],
                'Interval': agg_data['Interval'],
                'IdealCondition': agg_data['IdealCondition'],
                'Simulated': agg_data['Simulated'],
                'Unit': 'mm',
                'TotalIrrArea_Ha': agg_data['Area_Ha']
            })
            return result

        # Process data for different scales
        df1 = process_scale(irr_table, 'DistrictName', 'Irrigation District')
        df2 = process_scale(irr_table, 'SubBasin', 'Priv. and Dist. Irrigation')
        df3 = process_scale(irr_table, 'Basin', 'Priv. and Dist. Irrigation')
        df4 = process_scale(irr_table[irr_table.IrrigationType == 'Private'], 'SubBasin', 'Private Irrigation', ' (PRIVATE)')

        # Combine all irrigation data
        irr_data = pd.concat([df1, df2, df3, df4], axis=0)
        irr_data['Deficit'] = irr_data['IdealCondition'] - irr_data['Simulated']

        return irr_data


    # # Read all SCFs and reservoir elevation and storage data
    def get_reservoir_elevation_storage(self):
        """
        Read all SCFs and reservoir elevation and storage data.

        Returns:
            pandas.DataFrame: Reservoir elevation and storage data for all models.
        """
        # Read all SCFs and reservoir elevation and storage data
        res_elev_stor = pd.DataFrame([])
        for model in self.path_name_list:
            # get model and scf directory
            scf_dir = os.path.join(self.model_dir, model, 'SCF.txt')

            # read scf
            scf = []
            with open (scf_dir) as file:
                lines = file.readlines()
                for line in lines:
                    line_trimmed = line.strip('\n')
                    scf.append(line_trimmed)

            # get reservoir index
            res_idx = [scf.index(element) for element in scf if 'RESERV    ' in element if len(element)>=50]


            for idx in res_idx:
                # get number of data points in reservoir $PHYSYS table
                data_points = int(scf[idx].split()[-2])

                # estimate number of line to read data
                line_number = math.ceil((data_points / 4))

                # get elevation and storage data
                res_data = scf[idx+1 : idx+line_number+1]
                res_data = [item.split() for item in res_data]

                # to dataframe
                res_data = pd.DataFrame(res_data)
                res_data.columns =list(('Storage', 'Elevation')*int(len(res_data.columns)/2))
                res_data = pd.melt(res_data, ignore_index=True)
                elev = res_data[res_data['variable'] == 'Elevation']['value'].reset_index(drop=True)
                stor = res_data[res_data['variable'] == 'Storage']['value'].reset_index(drop=True)

                # get reservoir number and model name
                res_num = []
                res_num.append(int(scf[idx].split()[1]))
                res_num = res_num * len(elev)

                # get model name
                model_name = [model for n in range(len(elev))]

                # concate
                table = pd.concat([elev, stor], axis=1, ignore_index = True)
                table.columns = ['Elevation', 'Storage']
                table.sort_values(by = ['Elevation'], inplace=True)
                table.reset_index(inplace=True, drop=True)
                table.insert(0, 'ComponentNumber', res_num)
                table.insert(0, 'ModelName', model_name)
                table.dropna(inplace=True)


                res_elev_stor = pd.concat([res_elev_stor, table], axis=0, ignore_index = True)
                print("res_elev_stor: ",res_elev_stor.head())
                
        return res_elev_stor

    ## Estimate percetage of storage
    #### Sopan added this on 16th September, this part of code takes the maximum of 52 weeks
    def estimate_percent_of_storage(self,res_lst, res_elev_stor,res_data,outsim_id_full):
        """
        Estimate percentage of storage for reservoirs. This percentage storage calculated 
        using the maximum from the 52 weeks.

        Args:
            res_lst (list): List of reservoir identifiers.
            res_elev_stor (pandas.DataFrame): Reservoir elevation and storage data.
            res_data (pandas.DataFrame): Reservoir data.
            outsim_id_full (pandas.DataFrame): Reservoir data for 52 weeks.

        Returns:
            pandas.DataFrame: Updated reservoir data with percentage of storage.
        """
        for item in res_lst:
            elev = res_elev_stor.loc[item].Elevation
            stor = res_elev_stor.loc[item].Storage
            
            # get full supply level
            fs_elev = max(outsim_id_full.loc[item].IdealCondition)

            # get simulated data ## from Katherine !!!!! HG from the spreadsheet
            sim_elev = res_data.loc[item].Simulated

            # estimate full supply storage (dam3)
            fs_stor = np.interp(fs_elev, pd.to_numeric(elev), pd.to_numeric(stor))
            sim_stor = np.interp(sim_elev, pd.to_numeric(elev), pd.to_numeric(stor))

            # estimate percentage of storage
            stor_per = np.round((sim_stor/fs_stor)*100, 2)

            # add percetage of storage data in reservoir data
            res_data.loc[item, 'PerStorage'] = stor_per    
        
        return res_data
    
#### This is more robust approach
    def read_hbdf_based_on_ref(self, hbdf_dir, ref_file, model_name, col_name):
        """
        Read HBDF data based on given reference file - robust year-agnostic version.
        """
        hbdf = []
        file_dir = os.path.join(hbdf_dir, 'HBDF.txt')
        
        with open(file_dir) as file:
            lines = file.readlines()
            for line in lines:
                line_trimmed = line.strip('\n')
                hbdf.append(line_trimmed)  

        # Process and store hbdf data
        hbdf_df = pd.DataFrame([])  

        # Prepare a list of ids
        hbdf_id_list = ref_file.ComponentNumber.to_list()
        
        for idx, number in enumerate(hbdf_id_list):
            component_name = ref_file.iloc[idx]['ComponentName']
            hbdf_key = ref_file.set_index('ComponentNumber').loc[number, 'HBDF_Key']
            
            # Clean the HBDF key
            hbdf_key = str(hbdf_key).strip()
            
            # Find lines that match the HBDF data header pattern
            # Pattern: starts with HBDF key, followed by whitespace, 4-digit year, whitespace, number, whitespace, "CMS"
            import re
            pattern = rf'^{re.escape(hbdf_key)}\s+\d{{4}}\s+\d+\s+CMS'
            
            matching_lines = []
            for i, line in enumerate(hbdf):
                if re.match(pattern, line.strip()):
                    matching_lines.append((i, line))
            
            if not matching_lines:
                print(f"WARNING: No matching line found for {component_name} with key '{hbdf_key}'")
                # Add empty row with zeros
                empty_values = ['0'] + ['0.000'] * 52
                df = pd.DataFrame([empty_values])
                hbdf_df = pd.concat([hbdf_df, df], axis=0)
                continue
            
            # Use the first valid matching line
            hbdf_key_index, hbdf_line = matching_lines[0]
            
            # Extract the year from the header line
            header_parts = hbdf_line.strip().split()
            year_from_header = None
            for part in header_parts:
                if part.isdigit() and len(part) == 4:
                    year_from_header = part
                    break
            
            # Find the data line
            # Standard HBDF format has data 5 lines after header
            data_line_index = hbdf_key_index + 5
            
            if data_line_index >= len(hbdf):
                print(f"ERROR: Data line index {data_line_index} out of bounds for {component_name}")
                empty_values = [year_from_header or '0'] + ['0.000'] * 52
                df = pd.DataFrame([empty_values])
                hbdf_df = pd.concat([hbdf_df, df], axis=0)
                continue
            
            data_line = hbdf[data_line_index]
            values = data_line.split()
            
            # Validate data line: should start with a 4-digit year and have 53 values total
            if len(values) < 53 or not (values[0].isdigit() and len(values[0]) == 4):
                # Try to find the correct data line by pattern
                found_data = False
                for offset in range(-2, 10):  # Look both before and after
                    test_index = data_line_index + offset
                    if 0 <= test_index < len(hbdf):
                        test_line = hbdf[test_index]
                        test_values = test_line.split()
                        # Check if this looks like a data line
                        if (len(test_values) >= 53 and 
                            test_values[0].isdigit() and 
                            len(test_values[0]) == 4 and
                            all(self._is_numeric(v) for v in test_values[1:20])):  # Check first 20 values are numeric
                            values = test_values
                            found_data = True
                            break
                
                if not found_data:
                    print(f"ERROR: Could not find valid data line for {component_name}")
                    values = [year_from_header or '0'] + ['0.000'] * 52
            
            df = pd.DataFrame([values])
            hbdf_df = pd.concat([hbdf_df, df], axis=0)

        if hbdf_df.empty:
            return pd.DataFrame()

        # Process the data
        try:
            # Reset index
            hbdf_df = hbdf_df.reset_index(drop=True)
            
            # The first column is the year, rest are weeks 1-52
            hbdf_df.columns = ['Year'] + [n for n in range(1, len(hbdf_df.columns))]
            hbdf_df.insert(0, 'ComponentNumber', hbdf_id_list[:len(hbdf_df)])
            
            # Melt the dataframe
            hbdf_data = pd.melt(hbdf_df, id_vars=['Year', 'ComponentNumber'], 
                                value_vars=list(hbdf_df.columns[2:]), 
                                var_name='Interval', value_name=col_name)
            hbdf_data.insert(0, 'ModelName', model_name)
            
            # Filter for valid years (4-digit years)
            hbdf_data = hbdf_data[hbdf_data['Year'].astype(str).str.match(r'^\d{4}$', na=False)]
            
            # Clean up data types
            hbdf_data = hbdf_data[['ModelName','ComponentNumber','Year','Interval',col_name]]
            hbdf_data['Year'] = pd.to_numeric(hbdf_data['Year'], errors='coerce')
            hbdf_data['Interval'] = pd.to_numeric(hbdf_data['Interval'])
            hbdf_data[col_name] = pd.to_numeric(hbdf_data[col_name], errors='coerce')
            
            return hbdf_data
            
        except Exception as e:
            print(f"ERROR during data processing: {str(e)}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
        
        def _is_numeric(self, value):
            """Helper method to check if a string represents a number."""
            try:
                float(value)
                return True
            except ValueError:
                return False

        
    

    # Process wco data
    def process_wco_data(self,natchl_wco_data,wco_ref_file, hbdf_wco):
        """
        Process Water Conservation Objective (WCO) data.

        Args:
            natchl_wco_data (pandas.DataFrame): Natural channel WCO data.
            wco_ref_file (pandas.DataFrame): WCO reference file.
            hbdf_wco (pandas.DataFrame): HBDF WCO data.

        Returns:
            pandas.DataFrame: Processed WCO data.
        """
        # WCO df to store all data
        wco_data = pd.DataFrame([])

        # Update simulated flow (both regular and parallel channels) based on reference file
        for item in tuple(zip(wco_ref_file.ModelName, wco_ref_file.ComponentNumber)):

            # Prepare a lsit for normal and parallel channels
            natchl_lst = list(wco_ref_file.set_index(['ModelName','ComponentNumber']).loc[item][1:5].dropna())
            natchl_lst = [int(n) for n in natchl_lst]

            # Combine parallel channels simulated flow (normal channel data will be same as original simulated)
            df_combined = pd.DataFrame([])
            for natchl in natchl_lst:
                sim_data = natchl_wco_data.loc[item[0],natchl].Simulated.reset_index(drop=True)

                df_combined = pd.concat([df_combined, sim_data], axis=1)

            df_combined = list(df_combined.sum(axis=1).round(4)) 

            # Update main data file
            natchl_wco_data.loc[item, 'Simulated'] = df_combined

            # Obtain WCO data 
            data = hbdf_wco.set_index(['ModelName', 'ComponentNumber']).loc[[item]]

            # Add component name
            com_name = wco_ref_file.set_index(['ModelName', 'ComponentNumber']).loc[[item]].ComponentName[0]
            data['ComponentName'] = com_name

            wco_data = pd.concat([data, wco_data])  

        # Combine natchl_wco_data and WCO data
        wco_data.reset_index(inplace=True)
        natchl_wco_data.reset_index(inplace=True)

        idx_col = ['ModelName','ComponentNumber', 'Year', 'Interval']
        natchl_wco_data.set_index(idx_col, inplace=True)
        wco_data.set_index(idx_col, inplace=True)

        natchl_wco_data = natchl_wco_data.join(wco_data)

        natchl_wco_data.reset_index(inplace=True)
        natchl_wco_data['ComponentType'] = 'Water Conservation Objective (WCO)' 

        # Drop unnecessary data
        natchl_wco_data = natchl_wco_data.dropna(subset= 'WCO')
        natchl_wco_data.reset_index(drop=True, inplace=True)
        del natchl_wco_data['ComponentDescription']
        natchl_wco_data = natchl_wco_data.rename(columns = {'Units': 'Unit'})
        
        # Add WcO failure frequency (failed = 1, else = 0)
        natchl_wco_data['Simulated'] = pd.to_numeric(natchl_wco_data['Simulated'])
        natchl_wco_data['WCO'] = pd.to_numeric(natchl_wco_data['WCO'])
        
        natchl_wco_data['WCO_Failed'] = np.where((natchl_wco_data['Simulated'] >= natchl_wco_data['WCO']), 0, 1)

        return natchl_wco_data


    # Process io data
    def process_io_data(self,io_ref_file,hbdf_io,reference_file_name,natchl_io_data,start_week,end_week):
        """
        Process Instream Objective (IO) data.

        Args:
            io_ref_file (pandas.DataFrame): IO reference file.
            hbdf_io (pandas.DataFrame): HBDF IO data.
            reference_file_name (str): Name of the reference file.
            natchl_io_data (pandas.DataFrame): Natural channel IO data.
            start_week (int): Start week for data processing.
            end_week (int): End week for data processing.

        Returns:
            pandas.DataFrame: Processed IO data.
        """
        hbdf_io_data = hbdf_io 

        ref_file = io_ref_file.dropna(subset=['IO_Reference'])   
        excel_data = pd.read_excel(reference_file_name, sheet_name = 'IO_reference_data')
        excel_data=excel_data[(excel_data.Interval >= start_week) & (excel_data.Interval <= end_week)]
        io_natc_lst = list(ref_file.ComponentNumber.unique())   
        io_data_scf = pd.DataFrame([])
        for natc in io_natc_lst:
            io_ref_col = ref_file.set_index('ComponentNumber').loc[natc].IO_Reference
            io_ref_data = excel_data[io_ref_col]
            model_name = [ref_file.set_index('ComponentNumber').loc[natc].ModelName for n in range(len(io_ref_data))]
            component_num = [natc for n in range(len(io_ref_data))]
            year_col = [hbdf_io_data.Year.unique()[0] for n in range(len(io_ref_data))]
            interval = excel_data.Interval

            # additional io data
            add_io_data = pd.DataFrame(zip(model_name,component_num,year_col,interval,io_ref_data))
            io_data_scf = pd.concat([io_data_scf, add_io_data], axis=0)

        io_data_scf.columns = hbdf_io_data.columns  
        io_ref_data = pd.concat([hbdf_io_data, io_data_scf], axis=0, ignore_index = True)


        # IO file path and df to store all data
        io_data = pd.DataFrame([])

        # Update simulated flow (both regular and parallel channels) based on reference file
        for item in tuple(zip(io_ref_file.ModelName, io_ref_file.ComponentNumber)):

            # Prepare a lsit for normal and parallel channels
            natchl_lst = list(io_ref_file.set_index(['ModelName','ComponentNumber']).loc[item][1:5].dropna())
            natchl_lst = [int(n) for n in natchl_lst]

            # Combine parallel channels simulated flow (normal channel data will be same as original simulated)
            df_combined = pd.DataFrame([])
            for natchl in natchl_lst:
                sim_data = natchl_io_data.loc[item[0],natchl].Simulated.reset_index(drop=True)
                df_combined = pd.concat([df_combined, sim_data], axis=1)

            df_combined = list(df_combined.sum(axis=1).round(4)) 

            # Update main data file
            natchl_io_data.loc[item, 'Simulated'] = df_combined


        natchl_io_data.reset_index(inplace=True)
        idx_col = ['ModelName', 'ComponentNumber', 'Year', 'Interval']
        natchl_io_data = natchl_io_data.set_index(idx_col).join(io_ref_data.set_index(idx_col))
        natchl_io_data = natchl_io_data.dropna(subset = ['IO'])
        natchl_io_data.reset_index(inplace=True)
        natchl_io_data = natchl_io_data.set_index(['ModelName','ComponentNumber']).join(io_ref_file.set_index(['ModelName','ComponentNumber']).ComponentName)
        natchl_io_data.reset_index(inplace=True)
        del natchl_io_data['ComponentDescription']
        natchl_io_data = natchl_io_data.rename(columns = {'Units': 'Unit'})
        natchl_io_data['ComponentType'] = 'Instream Objective (IO)' 
        # Add IO failure frequency (failed = 1, else = 0)
        natchl_io_data['Simulated'] = pd.to_numeric(natchl_io_data['Simulated'])
        natchl_io_data['IO'] = pd.to_numeric(natchl_io_data['IO'])
        natchl_io_data['IO_Failed'] = np.where((natchl_io_data['Simulated'] >= natchl_io_data['IO']), 0, 1)

        return natchl_io_data

### NEW ResInflow Clode
    def estimate_res_annual_inflow_volume(self, ref_file, link_data, seconds_in_day, year_num, start_week, end_week):
        """
        Estimate annual inflow volume for reservoirs with debugging for Waterton.
        """


        waterton_in_ref = ref_file[ref_file['ComponentName'] == 'Waterton']
        if not waterton_in_ref.empty:
            print(f" Waterton found in reference file:")
            print(f"  ComponentNumber: {waterton_in_ref['ComponentNumber'].values}")
            print(f"  ModelName: {waterton_in_ref['ModelName'].values}")
        else:
            print(" Waterton NOT found in reference file!")
        
        # Process link inflows
        ref_file = ref_file.dropna(how='all', subset=list(ref_file.columns)[3:])
        
        df1 = link_data.copy()
        mdb_tab = df1.rename(columns={'Simulated': 'Simulated_cms'})
        if end_week == 52:
            mdb_tab['Simulated_dam3'] = np.where(
                (mdb_tab.Interval == end_week),
                (mdb_tab.Simulated_cms * 8 * seconds_in_day) / 1000,
                (mdb_tab.Simulated_cms * 7 * seconds_in_day) / 1000
            )
        else:
            mdb_tab['Simulated_dam3'] = (mdb_tab.Simulated_cms * 7 * seconds_in_day) / 1000

        mdb_tab = mdb_tab[(mdb_tab.Interval >= start_week) & (mdb_tab.Interval <= end_week)]
        
        mdb_tab.reset_index(inplace=True)
        
        df_tem = mdb_tab.groupby(['ModelName', 'ComponentNumber']).sum()['Simulated_dam3'].reset_index()
        df_tem.set_index(['ModelName', 'ComponentNumber'], inplace=True)
        
        sum_tab1 = ref_file.copy()
        
        total_supply = []
        for idx1 in ref_file.index:
            total_supply_temp = []
            sup_lst = list(ref_file.loc[idx1].iloc[3:-1].dropna())
            model_name = ref_file.loc[idx1].ModelName
            component_name = ref_file.loc[idx1].ComponentName
            
            if component_name == 'Waterton':
                print(f"\n--- Processing Waterton link inflows ---")
                print(f"  Link components: {sup_lst}")
            
            supply = []
            for n in sup_lst:
                try:
                    supply.append(df_tem.loc[(model_name, n)].Simulated_dam3)
                except:
                    supply.append(0)
            
            total_supply_temp.append(sum(supply))
            total_supply.append(total_supply_temp[0])
            
            if component_name == 'Waterton':
                print(f"  Total link inflow: {total_supply_temp[0]}")
        
        sum_tab1['Total_annual_link_inflow_dam3'] = total_supply
        sum_tab1['Year'] = int(year_num)
        sum_tab1 = sum_tab1[['ModelName', 'ComponentNumber', 'ComponentName', 'Year', 'Total_annual_link_inflow_dam3']]
        
        # Process HBDF direct inflows
        hbdf_ref_file = ref_file.dropna(subset='HBDF_Key')
        
        print("\n Checking HBDF reference for Waterton ")
        waterton_hbdf = hbdf_ref_file[hbdf_ref_file['ComponentName'] == 'Waterton']
        if not waterton_hbdf.empty:
            print(f" Waterton has HBDF key: '{waterton_hbdf['HBDF_Key'].values[0]}'")
        else:
            print(" Waterton does NOT have HBDF key!")
        
        hbdf_inflow = pd.DataFrame([])
        
        for model in hbdf_ref_file.ModelName.unique():
            hbdf_dir = os.path.join(self.model_dir, model)
            inflow_hbdf_ref_file = hbdf_ref_file[hbdf_ref_file.ModelName == model]
            
            # print(f"\n--- Processing HBDF for model: {model} ---")
            # print("Components with HBDF keys:")
            for idx, row in inflow_hbdf_ref_file.iterrows():
                print(f"  {row['ComponentName']}: {row['HBDF_Key']}")
            
            sum_tab2 = self.read_hbdf_based_on_ref(hbdf_dir, inflow_hbdf_ref_file, model, 'Flow_cms')
            
            if not sum_tab2.empty:
                # Check for Waterton data
                waterton_data = sum_tab2[sum_tab2['ComponentNumber'] == 206]  # Assuming 206 is Waterton
                if not waterton_data.empty:
                    print(f"\n Waterton HBDF data found ")
                    print("Week 22-26 raw data:")
                    week_data = waterton_data[waterton_data['Interval'].between(start_week, end_week)].sort_values('Interval')
                    for idx, row in week_data.iterrows():
                        print(f"  Week {row['Interval']}: {row['Flow_cms']} cms")
                
                sum_tab2['Flow_cms'] = pd.to_numeric(sum_tab2['Flow_cms'])
                # sum_tab2['Flow_dam3'] = np.where((sum_tab2.Interval == end_week),
                #                                 (sum_tab2.Flow_cms * 8*seconds_in_day)/1000,
                #                                 (sum_tab2.Flow_cms * 7*seconds_in_day)/1000)

                if end_week == 52:
                    sum_tab2['Flow_dam3'] = np.where(
                        (sum_tab2.Interval == end_week),
                        (sum_tab2.Flow_cms * 8 * seconds_in_day) / 1000,
                        (sum_tab2.Flow_cms * 7 * seconds_in_day) / 1000
                    )
                else:
                    sum_tab2['Flow_dam3'] = (sum_tab2.Flow_cms * 7 * seconds_in_day) / 1000
                
                # Filter for weeks
                sum_tab2 = sum_tab2[(sum_tab2.Interval >= start_week) & (sum_tab2.Interval <= end_week)]
                
                # Check Waterton after filtering
                waterton_filtered = sum_tab2[sum_tab2['ComponentNumber'] == 206]
                if not waterton_filtered.empty:
                    print("\nWaterton Week 22-26 flow volumes (dam3):")
                    for idx, row in waterton_filtered.iterrows():
                        print(f"  Week {row['Interval']}: {row['Flow_cms']} cms = {row['Flow_dam3']:.2f} dam3")
                
                # Group and sum
                sum_tab2 = sum_tab2.groupby(['ModelName', 'ComponentNumber', 'Year']).sum()
                
                # Check Waterton sum
                if (model, 206, year_num) in sum_tab2.index:
                    waterton_total = sum_tab2.loc[(model, 206, year_num), 'Flow_dam3']
                    print(f"\nWaterton total HBDF inflow (weeks {start_week}-{end_week}): {waterton_total:.2f} dam3")
                
                del sum_tab2['Flow_cms']
                sum_tab2.reset_index(inplace=True)
                sum_tab2 = sum_tab2.rename(columns={'Flow_dam3': 'Direct_annual_inflow_dam3'})
                
                hbdf_inflow = pd.concat([hbdf_inflow, sum_tab2], axis=0, ignore_index=True)
        
        # print(f"\nAll component numbers in HBDF inflow: {hbdf_inflow['ComponentNumber'].unique()}")
        
        # Join link and HBDF inflows
        res_inflow_sumtab = sum_tab1.set_index(['ModelName', 'ComponentNumber', 'Year']).join(
            hbdf_inflow.set_index(['ModelName', 'ComponentNumber', 'Year'])
        )
        
        res_inflow_sumtab.reset_index(inplace=True)
        res_inflow_sumtab = res_inflow_sumtab.fillna(0)
        
        # Calculate total
        res_inflow_sumtab['Reservoir_annual_inflow_dam3'] = (
            res_inflow_sumtab.Total_annual_link_inflow_dam3 + 
            res_inflow_sumtab.Direct_annual_inflow_dam3
        )
        
        # Final check for Waterton
        waterton_final = res_inflow_sumtab[res_inflow_sumtab['ComponentName'] == 'Waterton']
        if not waterton_final.empty:
            print("\n FINAL Waterton results ---")
        else:
            print("\n Waterton NOT in final results!")
        
        
        return res_inflow_sumtab



    ### Summary Function
    def prepare_summary(self, res_data, irr_data, major_data, major_data_io, major_data_wco, natchl_io_data, natchl_wco_data, scenario_name, year, start_week, end_week):
        """
        Prepare summary of various water resource management components.

        Args:
            res_data (pandas.DataFrame): Reservoir data.
            irr_data (pandas.DataFrame): Irrigation data.
            major_data (pandas.DataFrame): Major water use data.
            major_data_io (pandas.DataFrame): Major water use data subject to IO.
            major_data_wco (pandas.DataFrame): Major water use data subject to WCO.
            natchl_io_data (pandas.DataFrame): Natural channel IO data.
            natchl_wco_data (pandas.DataFrame): Natural channel WCO data.
            scenario_name (str): Name of the scenario.
            year (int): Year for summary.
            start_week (int): Start week for summary period.
            end_week (int): End week for summary period.

        Returns:
            pandas.DataFrame: Summary of various water resource management components.
        """
        year = int(year)
        
        def filter_and_sum(df, data_type, value_col='Value'):
            mask = (df['Data_type'] == data_type) & (df['Year'] == year) & (df['Interval'].between(start_week, end_week))
            return df[mask].groupby('ComponentName')[value_col].sum().reset_index()

        def create_summary(data, component_type, comment, value_col='Value'):
            summary = data.copy()
            summary.columns = ['ComponentName', f'Value_{scenario_name}']
            summary.insert(0, 'Year', year)
            summary.insert(0, 'Scenario', scenario_name)
            summary['Comments'] = comment
            summary.insert(0, 'Component_type', component_type)
            return summary

        # Reservoir summary
        res_summary = res_data.set_index(['Data_type', 'Year', 'Interval']).loc[(scenario_name, year, end_week), ['ComponentName', 'PerStorage']].reset_index()
        res_summary = create_summary(res_summary[['ComponentName', 'PerStorage']], 'Reservoir', f'% of full storage at week {end_week}')

        # Irrigation summary
        irr_summary = filter_and_sum(irr_data, scenario_name)
        irr_summary = create_summary(irr_summary, 'Irrigation', f'Irrigation deficit (mm) for weeks {start_week} to {end_week}')

        # Irrigation area summary
        irr_summary_area = irr_data[(irr_data['Data_type'] == scenario_name) & (irr_data['Year'] == year) & (irr_data['Interval'] == end_week)][['ComponentName', 'TotalIrrArea_Ha']].groupby('ComponentName').first().reset_index()
        irr_summary_area = create_summary(irr_summary_area, 'Irrigation Area', 'Total irrigation area (Ha)', 'TotalIrrArea_Ha')

        # Non-irrigation summaries
        def calculate_deficit_percentage(data, data_io):
            total_deficit = filter_and_sum(data, scenario_name)
            total_demand = filter_and_sum(data, f'Demand_{scenario_name}')
            summary = pd.merge(total_deficit, total_demand, on='ComponentName', suffixes=('_deficit', '_demand'))
            summary[f'Value_{scenario_name}'] = (summary['Value_deficit'] / summary['Value_demand']) * 100
            return summary[['ComponentName', f'Value_{scenario_name}']]

        major_summary = calculate_deficit_percentage(major_data, major_data_io)
        major_summary = create_summary(major_summary, 'Non-irrigation', f'Annual non-irrigation deficit (%) for weeks {start_week} to {end_week}')

        major_summary_io = calculate_deficit_percentage(major_data_io, major_data_io)
        major_summary_io = create_summary(major_summary_io, 'Non-irrigation Subject to IO', f'Annual non-irrigation deficit (%) s/t IO for weeks {start_week} to {end_week}')

        major_summary_wco = calculate_deficit_percentage(major_data_wco, major_data_wco)
        major_summary_wco = create_summary(major_summary_wco, 'Non-irrigation Subject to WCO', f'Annual non-irrigation deficit (%) s/t WCO for weeks {start_week} to {end_week}')

        # IO and WCO summaries
        io_summary = filter_and_sum(natchl_io_data, scenario_name, 'IO_Failed')
        io_summary = create_summary(io_summary, 'IO Failure Frequency', f'Number of weeks IO failed for weeks {start_week} to {end_week}')

        wco_summary = filter_and_sum(natchl_wco_data, scenario_name, 'WCO_Failed')
        wco_summary = create_summary(wco_summary, 'WCO Failure Frequency', f'Number of weeks WCO failed for weeks {start_week} to {end_week}')

        # Combine all summaries
        summary = pd.concat([res_summary, irr_summary, irr_summary_area, major_summary, major_summary_io, major_summary_wco, io_summary, wco_summary], axis=0, ignore_index=True)
        
        return summary



    # MAJOR
    def process_major_data(self,major_table):
        """
        Process major water use data at sub-basin and SSRB scales.

        Args:
            major_table (pandas.DataFrame): Major water use data table.

        Returns:
            pandas.DataFrame: Processed major water use data.
        """        
        # Organize major outputs at sub-basin scale (Red Deer, Bow, Oldman, and SSR)
        # Create empty lists to store data
        subbasin_name=[]
        year_num=[]
        interval_num=[]
        simulated=[]
        ideal=[]
        unit=[]
        ctype=[]
        cnum=[]
        model_name=[]

        for sbasin in [x for x in major_table.SubBasin.unique() if type(x) == str]:
            for year in list(major_table.Year.unique()):
                for interval in list(major_table.Interval.unique()):
                    subbasin_name.append(sbasin.upper())
                    year_num.append(year)
                    interval_num.append(interval)

                    # Sub-basin scale total volume (dam3)
                    allocated = ((major_table[(major_table.SubBasin == sbasin) &\
                                    (major_table.Year == year) &\
                                    (major_table.Interval== interval)].Simulated.sum()))
                    demand = ((major_table[(major_table.SubBasin == sbasin) &\
                                    (major_table.Year == year) &\
                                    (major_table.Interval== interval)].IdealCondition.sum()))

                    simulated.append(allocated)
                    ideal.append(demand)
                    unit.append('Dam3')
                    ctype.append('Non-Irrigation')
                    cnum.append('NaN')
                    model_name.append('NaN')

        major_data1 = pd.DataFrame(zip(model_name, ctype, subbasin_name, cnum, year_num, interval_num, ideal, simulated, unit))
        major_data1.columns = ['ModelName', 'ComponentType','ComponentName', 'ComponentNumber', 'Year', 'Interval', 'IdealCondition', 'Simulated', 'Unit']
        
        # Organize major outputs for entire SSRB
        # Create empty lists to store data
        subbasin_name=[]
        year_num=[]
        interval_num=[]
        simulated=[]
        ideal=[]
        unit=[]
        ctype=[]
        cnum=[]
        model_name=[]

        for year in list(major_table.Year.unique()):
            for interval in list(major_table.Interval.unique()):
                subbasin_name.append('SSRB')
                year_num.append(year)
                interval_num.append(interval)

                # SSRB total volume (dam3)
                allocated = ((major_table[(major_table.Year == year) &\
                                (major_table.Interval== interval)].Simulated.sum()))
                demand = ((major_table[(major_table.Year == year) &\
                                (major_table.Interval== interval)].IdealCondition.sum()))

                simulated.append(allocated)
                ideal.append(demand)
                unit.append('Dam3')
                ctype.append('Non-Irrigation')
                cnum.append('NaN')
                model_name.append('NaN')

        major_data2 = pd.DataFrame(zip(model_name, ctype, subbasin_name, cnum, year_num, interval_num, ideal, simulated, unit))
        major_data2.columns = ['ModelName', 'ComponentType','ComponentName', 'ComponentNumber', 'Year', 'Interval', 'IdealCondition', 'Simulated', 'Unit']   
        
        # Combine all major_data
        major_data = pd.concat([major_data1, major_data2], axis=0)
        major_data['Deficit'] = major_data.IdealCondition - major_data.Simulated # suggested by Tom on Jan 03, 2024
        
        return major_data


    ## Sopan edit starts
    def estimate_annual_div_vol(self, divchl_mdb, div_ref_file,seconds_in_day, start_week, end_week):
        """
        Estimate annual diversion volume.

        Args:
            divchl_mdb (pandas.DataFrame): Diversion channel MDB data.
            div_ref_file (pandas.DataFrame): Diversion reference file.
            start_week (int): Start week for data processing.
            end_week (int): End week for data processing.

        Returns:
            pandas.DataFrame: Estimated annual diversion volume.
        """
        divchl_mdb = divchl_mdb.rename(columns = {'Simulated':'Simulated_cms'})
        # divchl_mdb['Simulated_dam3'] = np.where((divchl_mdb.Interval == end_week),
        #                                     (divchl_mdb.Simulated_cms * 8*seconds_in_day)/1000,
        #                                     (divchl_mdb.Simulated_cms * 7*seconds_in_day)/1000)



        if end_week == 52:
            divchl_mdb['Simulated_dam3'] = np.where(
                (divchl_mdb.Interval == end_week),
                (divchl_mdb.Simulated_cms * 8 * seconds_in_day) / 1000,
                (divchl_mdb.Simulated_cms * 7 * seconds_in_day) / 1000
            )
        else:
            divchl_mdb['Simulated_dam3'] = (divchl_mdb.Simulated_cms * 7 * seconds_in_day) / 1000
        
        # Filter data for specified week range
        divchl_mdb = divchl_mdb[(divchl_mdb.Interval >= start_week) & (divchl_mdb.Interval <= end_week)]
        
        divchl_mdb.reset_index(inplace=True)

        df_tem = divchl_mdb.groupby(['ModelName', 'ComponentNumber']).sum()['Simulated_dam3'].reset_index()
        df_tem.set_index(['ModelName', 'ComponentNumber'], inplace=True)

        div_sumtab = div_ref_file.copy()
        total_supply = []
        for idx1 in div_ref_file.index:
            total_supply_temp = []
            div_sup_lst = list(div_ref_file.loc[idx1].dropna().iloc[2:])
            model_name = div_ref_file.loc[idx1].dropna().ModelName
    #        print("Model Name from estimate_annual_div_vol: ", model_name)
            supply = []
            for n in div_sup_lst:
                supply.append(df_tem.loc[(model_name, n)].Simulated_dam3)

            total_supply_temp.append(sum(supply))
            total_supply.append(total_supply_temp[0])
        div_sumtab['Total_supply_dam3'] = total_supply
        div_sumtab = div_sumtab[['ComponentName', 'Total_supply_dam3']]
        div_sumtab = div_sumtab.round()
        
        # Update the column name to reflect the week range
        div_sumtab = div_sumtab.rename(columns={'Total_supply_dam3': f'Total_supply_dam3_week{start_week}_to_{end_week}'})
        
        return div_sumtab


    #######

    def get_major_div_cap(self,model_dir, path_name_list):
        """
        Get major diversion capacity data from SCF files.

        Args:
            model_dir (str): Directory containing the model files.
            path_name_list (list): List of path names for different model scenarios.

        Returns:
            pandas.DataFrame: Major diversion capacity data for all models.
        """
        model_list = path_name_list
        all_model_major_div_cap = pd.DataFrame([])
        for model in model_list:
            file_dir = os.path.join(model_dir, model, 'SCF.txt')
            
            # read scf
            # ----------------------------
            scf = []
            with open(file_dir) as file:
                lines = file.readlines()
                for line in lines:
                    line_trimmed = line.strip('\n')
                    scf.append(line_trimmed) 

            # ----------------------------       
            # find MAJOR ids
            major_physys = [int(item.split()[1]) for item in scf if 'WITHDR      ' in item]

            # create a df
            major_physys = pd.DataFrame({'Major_physys_id': major_physys})

            # find all divchl in physys
            divchl_physys = [item for item in scf if 'DIVCHL' in item if len(item) == 70]

            # group divchl id and downstream node id
            divchl_physys_id =[]
            divchl_physys_dsnode =[]
            for item in divchl_physys:
                data = item.split()
                if 'CL' in data:
                    data.remove('CL')
                divchl_physys_id.append(int(data[1]))
                divchl_physys_dsnode.append(int(data[-2]))

            # make a df
            divchl_scf_physys = pd.DataFrame(zip(divchl_physys_id,divchl_physys_dsnode))
            # add columns
            divchl_scf_physys.columns = ['Divchl_physys_id','Divchl_physys_dsnode']
            # join major id and associated divchl id
            major_div_cap = major_physys.set_index('Major_physys_id').join(divchl_scf_physys.set_index('Divchl_physys_dsnode'))
            # drop major which is not receiving water from divchl
            major_div_cap = major_div_cap.dropna()
            major_div_cap.reset_index(inplace=True)
            major_div_cap = major_div_cap.rename(columns = {'index': 'Major_physys_id'})

            # remove duplicates based on all columns
            major_div_cap = major_div_cap.drop_duplicates()

            major_div_cap.reset_index(drop=True, inplace=True)

            scf_pensys = scf[scf.index('$PENSYS'):scf.index('$WATDEM')]

            # get divchl start index in pensys
            div_start_idx = scf_pensys.index([item for item in scf_pensys if 'DIVCHL' in item][0])

            # slice only divchl pensys
            scf_pensys = scf_pensys[div_start_idx:]

            # find divchl id number and annual cap column
            scf_pensys = [item for item in scf_pensys if 'DIVCHL' not in item if len(item) == 35]

            divchl_id_pensys =[] # to store diversion channel id#
            divchl_cap_dam3 = [] # to store diversion channel annual capacity (unit is dam3)
            for item in scf_pensys:
                divchl_id_pensys.append(int(item.split()[0]))
                divchl_cap_dam3.append(float(item.split()[-1]))

            scf_div_cap = pd.DataFrame(zip(divchl_id_pensys, divchl_cap_dam3))
            scf_div_cap.columns = ['Divchl_id_pensys', 'Divchl_cap_dam3']

            # drop large dummy cap channels
            scf_div_cap = scf_div_cap.drop(scf_div_cap[(scf_div_cap['Divchl_cap_dam3'] == 100000.00) |\
                                                    (scf_div_cap['Divchl_cap_dam3'] == 200000000.00)].index)
            scf_div_cap.reset_index(drop=True, inplace=True)

            # ---------------------------- 

            # join div cap id and vol
            major_div_cap = major_div_cap.set_index('Divchl_physys_id').join(\
                            scf_div_cap.set_index('Divchl_id_pensys'))

            # drop major nodes which does not have any div cap
            try:
                major_div_cap = major_div_cap.dropna()
            except:
                pass

            # re org
            major_div_cap.reset_index(drop=True, inplace=True)
            
            # add model name
            major_div_cap.insert(0, 'ModelName', model)
            all_model_major_div_cap = pd.concat([all_model_major_div_cap, major_div_cap], axis=0)
        
        all_model_major_div_cap.reset_index(drop=True, inplace=True)
        
        all_model_major_div_cap = all_model_major_div_cap.rename(columns = {'Major_physys_id': 'ComponentNumber'})
        all_model_major_div_cap = all_model_major_div_cap.rename(columns = {'Divchl_cap_dam3': 'DivCap_dam3'})
        
    #    print("Hello from the END !!!: ",all_model_major_div_cap)
        return all_model_major_div_cap
    
    def combine_files(self,output_dir, output_file):
        """
        Combine multiple Excel (.xlsx) and CSV files into a single Excel workbook.

        This function reads all .xlsx and .csv files from the specified directory,
        creates a new Excel workbook, and adds each file's content as a separate
        worksheet in the new workbook. The worksheets are named after their source
        files (truncated to 31 characters to comply with Excel's limit).

        Parameters:
        output_dir (str): The directory path containing the input files and where
                        the output file will be saved.
        output_file (str): The name of the output Excel file (including .xlsx extension).

        Returns:
        None

        """
        
        # Get a list of all .xlsx and .csv files in the directory
        input_files = [f for f in os.listdir(output_dir) if f.endswith(('.xlsx', '.csv'))]

        # Create a new workbook
        wb = Workbook()
        wb.remove(wb.active)  # Remove the default sheet

        # Loop through all input files
        for file in input_files:
            file_path = os.path.join(output_dir, file)
            file_name, file_extension = os.path.splitext(file)
            
            # Read the file based on its extension
            if file_extension.lower() == '.xlsx':
                df = pd.read_excel(file_path)
            elif file_extension.lower() == '.csv':
                df = pd.read_csv(file_path)
            else:
                print(f"Skipping unsupported file: {file}")
                continue
            
            # Create a new worksheet for each file
            ws = wb.create_sheet(title=file_name[:61])  # Excel has a 31 character limit for sheet names
            
            # Write the dataframe to the worksheet
            for r in dataframe_to_rows(df, index=False, header=True):
                ws.append(r)

        # Save the workbook
        wb.save(os.path.join(output_dir,output_file))
        
        
    def process_and_save_data(self,output_dir, filters, out_xls):
        """
        Process non-irrigation data from an Excel file, transform it, and save the results.

        This function reads an Excel file containing water resource management data,
        filters it based on specified component types, transforms the data into a pivoted
        format, and saves the results as separate Excel files.

        Parameters:
        wrmmout_path (str): Path to the directory containing the input Excel file.
        filters (list): List of component types to filter the data.
        out_xls (list): List of output file suffixes corresponding to each filter.

        Returns:
        None
        """
        
        file_path = os.path.join(output_dir, "Executive_summary_table.xlsx")
        
        # Read the Excel file
        df = pd.read_excel(file_path)
        
        
        for filter_value, output_file in zip(filters, out_xls):
            # Filter the DataFrame
            filtered_df = df[df['Component_type'] == filter_value]
            
            # Extract scenario name from the column name
            scenario = filtered_df.filter(regex='^Value_').columns[0].split('_')[1]
            
            # Pivot the DataFrame
            pivoted = filtered_df.pivot(index='Component_type', columns='ComponentName', values=f'Value_{scenario}')
            
            # Round the values
            pivoted = pivoted.round().astype(int)
            
            # Reorder the columns based on the specified order
            order = ['1. RED DEER SUB-BASIN', '2. BOW SUB-BASIN', '3. OLDMAN SUB-BASIN', '4. SS SUB-BASIN', 'SSRB']
            pivoted = pivoted.reindex(columns=order)
            
            # Create a new DataFrame with the scenario as the index
            result_df = pd.DataFrame(pivoted.values, columns=pivoted.columns, index=[scenario])
            
            # Save to Excel
            output_path = os.path.join(output_dir,f'SumTab_SBasinNON{output_file}.xlsx')
            result_df.to_excel(output_path, index=True)
            
