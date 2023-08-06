import os
from collections import namedtuple
from pathlib import Path

import numpy as np
import pandas as pd
import xlrd

from common.file_management import fetch, write_df, float_to_int, _uncompress_file


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


DatasetInfo = namedtuple('DatasetInfo', ['name', 'urlinfos', 'main_file', 'source'])
UrlInfo = namedtuple('UrlInfo', ['url', 'filenames', 'uncompress'])

ROAD_SAFETY_CONFIG = DatasetInfo(
    name='road_safety',
    urlinfos=(
        UrlInfo(
            url="http://data.dft.gov.uk/road-accidents-safety-data/"
                "RoadSafetyData_2015.zip",
            filenames=(
                "Casualties_2015.csv",
                "Vehicles_2015.csv",
                "Accidents_2015.csv"
            ),
            uncompress=True),
        UrlInfo(
            url="http://data.dft.gov.uk/road-accidents-safety-data/"
                "MakeModel2015.zip",
            filenames=("2015_Make_Model.csv",),
            uncompress=True
        ),
        UrlInfo(
            url="http://data.dft.gov.uk/road-accidents-safety-data/"
                "Road-Accident-Safety-Data-Guide.xls",
            filenames=("Road-Accident-Safety-Data-Guide.xls",),
            uncompress=False
        )
    ),
    main_file="road_safety_2015.csv",
    source="https://data.gov.uk/dataset/road-accidents-safety-data"
)

MAPPING_COL_TO_DESCR = {
    'Vehicle_Type': 'Vehicle Type',
    'Towing_and_Articulation': 'Towing and Articulation',
    'Vehicle_Manoeuvre': 'Vehicle Manoeuvre',
    'Junction_Location': 'Junction Location',
    'Vehicle_Location-Restricted_Lane': 'Vehicle Location',
    'Skidding_and_Overturning': 'Skidding and Overturning',
    'Hit_Object_in_Carriageway': 'Hit Object in Carriageway',
    'Vehicle_Leaving_Carriageway': 'Veh Leaving Carriageway',
    'Hit_Object_off_Carriageway': 'Hit Object Off Carriageway',
    '1st_Point_of_Impact': '1st Point of Impact',
    'Was_Vehicle_Left_Hand_Drive?': 'Was Vehicle Left Hand Drive',
    'Was_Vehicle_Left_Hand_Drive': 'Was Vehicle Left Hand Drive',
    'Journey_Purpose_of_Driver': 'Journey Purpose',
    'Sex_of_Driver': 'Sex of Driver',
    'Age_Band_of_Driver': 'Age Band',
    'Propulsion_Code': 'Vehicle Propulsion Code',
    'Driver_IMD_Decile': 'IMD Decile',
    'Driver_Home_Area_Type': 'Home Area Type',
    'Casualty_Class': 'Casualty Class',
    'Sex_of_Casualty': 'Sex of Casualty',
    'Age_Band_of_Casualty': 'Age Band',
    'Casualty_Severity': 'Casualty Severity',
    'Pedestrian_Location': 'Ped Location',
    'Pedestrian_Movement': 'Ped Movement',
    'Car_Passenger': 'Car Passenger',
    'Bus_or_Coach_Passenger': 'Bus Passenger',
    'Pedestrian_Road_Maintenance_Worker': 'Ped Road Maintenance Worker',
    'Casualty_Type': 'Casualty Type',
    'Casualty_Home_Area_Type': 'Home Area Type',
    'Casualty_IMD_Decile': 'IMD Decile',
    'Police_Force': 'Police Force',
    'Accident_Severity': 'Accident Severity',
    'Day_of_Week': 'Day of Week',
    'Local_Authority_(District)': 'Local Authority (District)',
    'Local_Authority_(Highway)': 'Local Authority (Highway)',
    '1st_Road_Class': '1st Road Class',
    '2nd_Road_Class': '2nd Road Class',
    'Road_Type': 'Road Type',
    'Junction_Detail': 'Junction Detail',
    'Junction_Control': 'Junction Control',
    'Pedestrian_Crossing-Physical_Facilities': 'Ped Cross - Physical',
    'Pedestrian_Crossing-Human_Control': 'Ped Cross - Human',
    'Light_Conditions': 'Light Conditions',
    'Weather_Conditions': 'Weather',
    'Road_Surface_Conditions': 'Road Surface',
    'Special_Conditions_at_Site': 'Special Conditions at Site',
    'Carriageway_Hazards': 'Carriageway Hazards',
    'Urban_or_Rural_Area': 'Urban Rural',
    'Did_Police_Officer_Attend_Scene_of_Accident': 'Police Officer Attend'
}


MAPPING_COL_TO_TYPE = {
    'Location_Easting_OSGR': 'int',
    'Location_Northing_OSGR': 'int',
    'Longitude': 'float',
    'Latitude': 'float',
    'Police_Force': 'int',
    'Accident_Severity': 'int',
    'Number_of_Vehicles': 'int',
    'Number_of_Casualties': 'int',
    'Date': 'object',
    'Day_of_Week': 'int',
    'Time': 'object',
    'Local_Authority_(District)': 'int',
    'Local_Authority_(Highway)': 'object',
    '1st_Road_Class': 'int',
    '1st_Road_Number': 'int',
    'Road_Type': 'int',
    'Speed_limit': 'int',
    'Junction_Detail': 'int',
    'Junction_Control': 'int',
    '2nd_Road_Class': 'int',
    '2nd_Road_Number': 'int',
    'Pedestrian_Crossing-Human_Control': 'int',
    'Pedestrian_Crossing-Physical_Facilities': 'int',
    'Light_Conditions': 'int',
    'Weather_Conditions': 'int',
    'Road_Surface_Conditions': 'int',
    'Special_Conditions_at_Site': 'int',
    'Carriageway_Hazards': 'int',
    'Urban_or_Rural_Area': 'int',
    'Did_Police_Officer_Attend_Scene_of_Accident': 'int',
    'LSOA_of_Accident_Location': 'object',
    'Vehicle_Reference_df_res': 'int',
    'Casualty_Reference': 'int',
    'Casualty_Class': 'int',
    'Sex_of_Casualty': 'int',
    'Age_of_Casualty': 'int',
    'Age_Band_of_Casualty': 'int',
    'Casualty_Severity': 'int',
    'Pedestrian_Location': 'int',
    'Pedestrian_Movement': 'int',
    'Car_Passenger': 'int',
    'Bus_or_Coach_Passenger': 'int',
    'Pedestrian_Road_Maintenance_Worker': 'int',
    'Casualty_Type': 'int',
    'Casualty_Home_Area_Type': 'int',
    'Casualty_IMD_Decile': 'int',
    'Vehicle_Reference_df': 'int',
    'Vehicle_Type': 'int',
    'Towing_and_Articulation': 'int',
    'Vehicle_Manoeuvre': 'int',
    'Vehicle_Location-Restricted_Lane': 'int',
    'Junction_Location': 'int',
    'Skidding_and_Overturning': 'int',
    'Hit_Object_in_Carriageway': 'int',
    'Vehicle_Leaving_Carriageway': 'int',
    'Hit_Object_off_Carriageway': 'int',
    '1st_Point_of_Impact': 'int',
    'Was_Vehicle_Left_Hand_Drive?': 'int',
    'Journey_Purpose_of_Driver': 'int',
    'Sex_of_Driver': 'int',
    'Age_of_Driver': 'int',
    'Age_Band_of_Driver': 'int',
    'Engine_Capacity_(CC)': 'int',
    'Propulsion_Code': 'int',
    'Age_of_Vehicle': 'int',
    'Driver_Home_Area_Type': 'int',
}


def _get_file_paths(directory):
    f = dict(description=os.path.join(directory, "Road-Accident-Safety-Data-Guide.xls"),
             data=[os.path.join(directory, elt) for elt in os.listdir(directory) if
                   elt != "Road-Accident-Safety-Data-Guide.xls"])
    return f


def _denormalize(df, descr):
    print(f"descr: {descr!r}")
    description = xlrd.open_workbook(descr)

    for name in df.keys():
        if name in MAPPING_COL_TO_DESCR:
            sheet = description.sheet_by_name(MAPPING_COL_TO_DESCR[name])
            x = sheet.first_visible_rowx + 1
            mapping = {sheet.cell_value(j, 0): sheet.cell_value(j, 1) for j in range(x, sheet.nrows)}
            result_array = []

            for r in df[name]:
                try:
                    result_array.append(mapping[r])
                except KeyError:
                    result_array.append("Nan")

            df[name] = result_array

    return df


def _process_df(files):
    res_df = pd.DataFrame()
    for file in files:
        print(f"UI: {file=}")
        df = pd.read_csv(file)

        if 'Accidents_2015.csv' not in file:
            df['Vehicle_Reference'] = (df['Vehicle_Reference'].map(str))

        df['Accident_Index'] = df['Accident_Index'].astype(str)
        df = df.set_index('Accident_Index')
        if '2015_Make_Model.csv' in file:
            df = df.dropna(axis=0, how='any', subset=['make'])

        #df = _denormalize(df, files['description'])

        if res_df.empty:
            res_df = df
        else:
            res_df = res_df.join(df, how='left', lsuffix='_df_res', rsuffix='_df')

    #res_df = res_df.dropna(axis=0, how='any', subset=['make'])
    return res_df


def get_road_safety_df(save=True):
    data_dir = fetch(ROAD_SAFETY_CONFIG)
    files = _get_file_paths(data_dir[0])["data"]
    output_dir = Path('.').resolve() / 'src' / 'data' / 'road_safety' / 'output'
    print(f"{files=}")
    for fl in files:
        _uncompress_file(fl, output_dir, False)
    files = [os.path.join(output_dir, f) for f in os.listdir(output_dir)]
    print(f"{files=}")
    df = _process_df(files)
    f_to_i = ['1st_Road_Number', '2nd_Road_Number', 'Location_Easting_OSGR', 'Location_Northing_OSGR',
              'Number_of_Vehicles', 'Number_of_Casualties', 'Speed_limit', 'accyr', 'Engine_Capacity_(CC)_df',
              'Age_of_Vehicle_df']
    str_to_i = ['Vehicle_Reference', 'Vehicle_Reference_df', 'Vehicle_Reference_df_res']
    to_del = ['data missing or out of range', 'none', -1, 'unknown or other', 'not known', 'unclassified', 'unknown',
              'nan']

    for c in df:
        tab = []
        for elt in df[c]:
            if (isinstance(elt, str) and elt.lower() in to_del) or elt in to_del:
                tab.append(np.nan)
            else:
                tab.append(elt)
        df[c] = pd.Series(tab, dtype=np.object, index=df.index)

    #for c in f_to_i:
    #    df[c] = float_to_int(df[c], df.index)

    #for c in str_to_i:
    #    tab = []
    #    for elt in df[c]:
    #        if isinstance(elt, str):
    #            tab.append(int(elt))
    #        else:
    #            tab.append(elt)
    #    df[c] = pd.Series(tab, dtype=np.object, index=df.index)

    for c in df:
        if len(df[c].unique()) == 1 and str(df[c].unique()[0]) == 'nan':
            df.drop([c], 1, inplace=True)

    #print(df.head(50))
    #for col in df.columns:
    #    print(col, df[col].unique())

    #df = df.astype(MAPPING_COL_TO_TYPE)
    df = df.convert_dtypes()

    # Convert dtypes string to object
    convert_mapping = {col: 'object' for col in df.select_dtypes(include='string').columns}
    df = df.astype(convert_mapping)

    #print('Missing values in y before replacing: ', sum(df['Sex_of_Driver'].isna()))
    # Drop rows with missing y
    df = df.drop(df.index[df['Sex_of_Driver'].isna()], axis=0)
    #print('Missing values in y after replacing: ', sum(df['Sex_of_Driver'].isna()))

    write_df(save, df, data_dir[1], ROAD_SAFETY_CONFIG.main_file)
    return df
