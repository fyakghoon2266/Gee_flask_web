from flask import session
import pandas as pd
import glob
import os

def cbind_chirsp(statics):

    all_files = glob.glob(os.path.join(session['user_id'],"Prec_{}*.csv".format(statics)))

    df_from_each_file = (pd.read_csv(f, sep = ",") for f in all_files)
    df_merged = pd.concat(df_from_each_file, ignore_index = True)
    if 'precipitation' in df_merged.columns.tolist():
        df_merged.rename(columns={'precipitation' : 'precipitation_' + str(statics)}, inplace = True)
    else:
        pass

    df_merged.to_csv(session['user_id'] + '/final.csv', index=False)

def cbind_era5(statics):

    all_files = glob.glob(os.path.join(session['user_id'],"era5_{}*.csv".format(statics)))

    df_from_each_file = (pd.read_csv(f, sep = ",") for f in all_files)
    df_merged = pd.concat(df_from_each_file, ignore_index = True)
    if 'Air_2m_T_C_mean' in df_merged.columns.tolist():
        df_merged.rename(columns={'Air_2m_T_C_mean' : 'Air_2m_T_C_mean_' + str(statics)}, inplace = True)
    else:
        pass
    if 'Air_2m_T_C_min' in df_merged.columns.tolist():
        df_merged.rename(columns={'Air_2m_T_C_min' : 'Air_2m_T_C_min_' + str(statics)}, inplace = True)
    else:
        pass
    if 'Air_2m_T_C_max' in df_merged.columns.tolist():
        df_merged.rename(columns={'Air_2m_T_C_max' : 'Air_2m_T_C_max_' + str(statics)}, inplace = True)
    else:
        pass
    if 'dewpoint_2m_C' in df_merged.columns.tolist():
        df_merged.rename(columns={'dewpoint_2m_C' : 'dewpoint_2m_C_' + str(statics)}, inplace = True)
    else:
        pass
    if 'RH' in df_merged.columns.tolist():
        df_merged.rename(columns={'RH' : 'RH_' + str(statics)}, inplace = True)
    else:
        pass
    if 'mean_2m_air_temperature' in df_merged.columns.tolist():
        df_merged.rename(columns={'mean_2m_air_temperature' : 'mean_2m_air_temperature_' + str(statics)}, inplace = True)
    else:
        pass
    if 'minimum_2m_air_temperature' in df_merged.columns.tolist():
        df_merged.rename(columns={'minimum_2m_air_temperature' : 'minimum_2m_air_temperature_' + str(statics)}, inplace = True)
    else:
        pass
    if 'maximum_2m_air_temperature' in df_merged.columns.tolist():
        df_merged.rename(columns={'maximum_2m_air_temperature' : 'maximum_2m_air_temperature_' + str(statics)}, inplace = True)
    else:
        pass
    if 'dewpoint_2m_temperature' in df_merged.columns.tolist():
        df_merged.rename(columns={'dewpoint_2m_temperature' : 'dewpoint_2m_temperature_' + str(statics)}, inplace = True)
    else:
        pass
    if 'total_precipitation' in df_merged.columns.tolist():
        df_merged.rename(columns={'total_precipitation' : 'total_precipitation_' + str(statics)}, inplace = True)
    else:
        pass
    if 'surface_pressure' in df_merged.columns.tolist():
        df_merged.rename(columns={'surface_pressure' : 'surface_pressure_' + str(statics)}, inplace = True)
    else:
        pass
    if 'mean_sea_level_pressure' in df_merged.columns.tolist():
        df_merged.rename(columns={'mean_sea_level_pressure' : 'mean_sea_level_pressure_' + str(statics)}, inplace = True)
    else:
        pass
    if 'u_component_of_wind_10m' in df_merged.columns.tolist():
        df_merged.rename(columns={'u_component_of_wind_10m' : 'u_component_of_wind_10m_' + str(statics)}, inplace = True)
    else:
        pass
    if 'v_component_of_wind_10m' in df_merged.columns.tolist():
        df_merged.rename(columns={'v_component_of_wind_10m' : 'v_component_of_wind_10m_' + str(statics)}, inplace = True)
    else:
        pass

    df_merged.to_csv(session['user_id'] + '/final.csv', index=False)
    

def cbind_Modis_NDVI_EVI(statics):

    all_files = glob.glob(os.path.join(session['uder_id'],"Modis_NDVI_EVI_{}*.csv".format(statics)))

    df_from_each_file = (pd.read_csv(f, sep = ",") for f in all_files)
    df_merged = pd.concat(df_from_each_file, ignore_index=True)
    if 'NDVI' in df_merged.columns.tolist():
        df_merged.rename(columns={'NDVI' : 'NDVI_' + str(statics)}, inplace=True)
    else:
        pass
    if 'EVI' in df_merged.columns.tolist():
        df_merged.rename(columns={'EVI' : 'EVI_' + str(statics)}, inplace=True)
    else:
        pass
    
    df_merged.to_csv(session['user_id'] + '/final.csv',index=False)


def cbind_Modis_LST(statics):

    all_files = glob.glob(os.path.join(session['user_id'],"Modis_LST_{}*.csv".format(statics)))

    df_from_each_file = (pd.read_csv(f, sep = ",") for f in all_files)
    df_merged = pd.concat(df_from_each_file, ignore_index=True)
    if 'LST_Day' in df_merged.columns.tolist():
        df_merged.rename(columns={'LST_Day' : 'LST_Day_' + str(statics)}, inplace=True)
    else:
        pass
    if 'LST_Night' in df_merged.columns.tolist():
        df_merged.rename(columns={'LST_Night' : 'LST_Night_' + str(statics)}, inplace=True)
    else:
        pass
    if 'LST_Mean' in df_merged.columns.tolist():
        df_merged.rename(columns={'LST_Mean' : 'LST_Mean_' + str(statics)}, inplace=True)
    else:
        pass

    df_merged.to_csv(session['user_id'] + '/final.csv', index=False)


#Combine date csv files and combine them according to different statistical values.

def cbind_Modis_Nadir(statics):

    all_files = glob.glob(os.path.join(session['user_id'],"Modis_Nadir_{}*.csv".format(statics)))

    df_from_each_file = (pd.read_csv(f, sep = ",") for f in all_files)
    df_merged = pd.concat(df_from_each_file, ignore_index = True)
    if 'ndvi' in df_merged.columns.tolist():
        df_merged.rename(columns={'ndvi' : 'NDVI_' + str(statics)}, inplace = True)
    else:
        pass
    if 'evi' in df_merged.columns.tolist():
        df_merged.rename(columns={'evi' : 'EVI_' + str(statics)}, inplace = True)
    else:
        pass
    if 'savi' in df_merged.columns.tolist():
        df_merged.rename(columns={'savi' : 'SAVI_' + str(statics)}, inplace = True)
    else:
        pass
    if 'NDWI_Gao' in df_merged.columns.tolist():
        df_merged.rename(columns={'NDWI_Gao' : 'NDWI_Gao_' + str(statics)}, inplace = True)
    else:
        pass
    if 'NDWI_Mc' in df_merged.columns.tolist():
        df_merged.rename(columns={'NDWI_Mc' : 'NDWI_Mc_' + str(statics)}, inplace = True)
    else:
        pass
    if 'MNDWI' in df_merged.columns.tolist():
        df_merged.rename(columns={'MNDWI' : 'MNDWI_' + str(statics)}, inplace = True)
    else:
        pass

    df_merged.to_csv(session['user_id'] + '/final.csv', index=False)
