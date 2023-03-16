from flask import session, request, Blueprint
from random import Random
from datetime import timedelta, datetime
from view_form import ProductForm
from cbind import cbind_chirsp, cbind_era5, cbind_Modis_NDVI_EVI, cbind_Modis_LST, cbind_Modis_Nadir
from bands import *
import pandas as pd
import io
import os
import glob
import geemap
import ee


routes = Blueprint('routes', __name__)

# path function that generates random numbers
def str_random():
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(20):
        str+=chars[random.randint(0,length)]
    return str

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
    return next_month - timedelta(days=next_month.day)

def monthlist(begin,end):
    # begin = datetime.strptime(begin, "%Y-%m-%d")
    # end = datetime.strptime(end, "%Y-%m-%d")

    result = []
    while True:
        if begin.month == 12:
            next_month = begin.replace(year=begin.year+1,month=1, day=1)
        else:
            next_month = begin.replace(month=begin.month+1, day=1)
        if next_month > end:
            break
        result.append ([begin.strftime("%Y-%m-%d"),last_day_of_month(begin).strftime("%Y-%m-%d")])
        begin = next_month
    result.append ([begin.strftime("%Y-%m-%d"),end.strftime("%Y-%m-%d")])
    return result


def trans_date(input_date):
    t1 = input_date
    t2 = datetime.strptime(t1, '%Y%m%d').strftime('%Y/%m/%d')
    return t2

def trans_date_LST(input_date):
    t1 = input_date
    t2 = datetime.strptime(t1, '%Y_%m_%d').strftime('%Y/%m/%d')
    return t2

def trans_date_Nadir(input_date):
    t1 = input_date
    t2 = datetime.strptime(t1, '%Y_%m_%d').strftime('%Y/%m/%d')
    return t2

@routes.route("/zonal_Chirsp", methods=["POST"])
def zonal_Chirsp():
    # 先從表單中提取使用者給予的資料
    form = ProductForm(request.form)
    # star the google earth engine
    ee.Initialize()
    # shp file from the user
    crs = 'EPSG:4326'


    time_list =monthlist(form.Star_Date.data, form.End_Date.data)
    states = geemap.shp_to_ee("".join(glob.glob(os.path.join(session['user_id'],'*.shp'))))
    for i in range(0, len(time_list)):
        Chirsp = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY') \
                .filter(ee.Filter.date(datetime.strptime(time_list[i][0], "%Y-%m-%d"), datetime.strptime(time_list[i][1],"%Y-%m-%d")+ timedelta(days=1))) \
                .map(lambda img: img.select(list(form.Bands_Chirps.data))) \
                .map(lambda image: image.clip(states)) \
                .map(lambda image: image.reproject(crs=crs))

        
        Chirsp = Chirsp.toBands()
        out_dir = os.path.expanduser(session['user_id'])
        out_dem_stats = os.path.join(out_dir, 'Prec_{}_{}.csv'.format(form.Statics.data,time_list[i]))

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        geemap.zonal_statistics(Chirsp, states, out_dem_stats, statistics_type=form.Statics.data, scale=1000)

        data_temp = pd.read_csv(out_dem_stats)


        column_name_list = data_temp.columns.tolist()
        c = []
        d = []
        for k in zip(column_name_list[:]):
            c.append(k[0][0:8])
            d.append(k[0])
        data = []
        for j in range(0, len(column_name_list),len(form.Bands_Chirps.data)):
            if all(m.isdigit() for m in c[j:j+len(form.Bands_Chirps.data)]) == True:

                df = data_temp.loc[:,d[j:j+len(form.Bands_Chirps.data)]]
                df[form.Regional_category.data] = data_temp.loc[:,[form.Regional_category.data]]
                text = column_name_list[j][0:8]
                df.insert(0, 'Date', '')
                df['Date'] = trans_date(text)
                df.insert(1, 'Doy', '')
                df['Doy'] = datetime.strptime(text, '%Y%m%d').strftime('%j')
                colnames=['Date','Doy']
                colnames.extend(list(form.Bands_Chirps.data))
                colnames.append(form.Regional_category.data)
                df.columns=[colnames]
                data.append(df)
            else:
                continue

        appended_data = pd.concat(data, axis=0,ignore_index = True)

        appended_data.to_csv(out_dem_stats,index=False)#Output the file with date and doy back

    cbind_chirsp(form.Statics.data)

def zonal_era5():
    # 先從表單中提取使用者給予的資料
    form = ProductForm(request.form)
    # star the google earth engine
    ee.Initialize()
    # shp file from the user
    states = geemap.shp_to_ee("".join(glob.glob(os.path.join(session['user_id'],'*.shp'))))
    # Time list
    time_list =monthlist(form.Star_Date.data, form.End_Date.data)
    crs = 'EPSG:4326'

    for i in range(0,len(time_list)):
            
        era5 = ee.ImageCollection("ECMWF/ERA5/DAILY") \
            .filter(ee.Filter.date(time_list[i][0],datetime.strptime(time_list[i][1],"%Y-%m-%d")+ timedelta(days=1))) \
            .filterBounds(states) \
            .map(getRH) \
            .map(getC_air_mean) \
            .map(getC_air_min) \
            .map(getC_air_max) \
            .map(getC_dewpoint) \
            .select(list(form.Bands_Era5.data)) \
            .map(lambda image: image.clip(states)) \
            .map(lambda image: image.reproject(crs=crs))


        era5 = era5.toBands()
            
        out_dir = os.path.expanduser(session['user_id'])
        out_dem_stats = os.path.join(out_dir, 'era5_{}_{}.csv'.format(form.Statics.data,time_list[i]))

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        geemap.zonal_statistics(era5, states, out_dem_stats, statistics_type=form.Statics.data, scale=1000)
            
        data_temp = pd.read_csv(out_dem_stats)
        column_name_list = data_temp.columns.tolist()
        c = []
        d = []
        for k in zip(column_name_list[:]):
            c.append(k[0][0:8])
            d.append(k[0])
                
        data = []
        for j in range(0, len(column_name_list),len(form.Bands_Era5.data)):            
            if all(m.isdigit() for m in c[j:j+len(form.Bands_Era5.data)]) == True:
                    
                df = data_temp.loc[:,d[j:j+len(form.Bands_Era5.data)]]
                df[form.Regional_category.data] = data_temp.loc[:,[form.Regional_category.data]]
                text = column_name_list[j][0:8]
                df.insert(0, 'Date', '')
                df['Date'] = trans_date(text)
                df.insert(1, 'Doy', '')
                df['Doy'] = datetime.strptime(text, '%Y%m%d').strftime('%j')
                colnames=['Date','Doy']
                colnames.extend(list(form.Bands_Era5.data))
                colnames.append(form.Regional_category.data)
                df.columns=[colnames]
                data.append(df)
            else:
                continue
        appended_data = pd.concat(data, axis=0, ignore_index=True)
        
                
        appended_data.to_csv(out_dem_stats,index=False)

    cbind_era5(form.Statics.data)

def zonal_Modis_NDVI_EVI():
    # 先從表單中提取使用者給予的資料
    form = ProductForm(request.form)
    # star the google earth engine
    ee.Initialize()
    # shp file from the user
    states = geemap.shp_to_ee("".join(glob.glob(os.path.join(session['user_id'],'*.shp'))))
    # Time list
    time_list =monthlist(form.Star_Date.data, form.End_Date.data)
    crs = 'EPSG:4326'

    for i in range(0,len(time_list)):

        Modis_NDVI_EVI = ee.ImageCollection("MODIS/061/MOD13Q1") \
            .filter(ee.Filter.date(time_list[i][0],datetime.strptime(time_list[i][1],"%Y-%m-%d")+ timedelta(days=1))) \
            .filterBounds(states) \
            .map(maskModisQA) \
            .select(list(form.Bands_Modis_NDVI_EVI.data)) \
            .map(lambda image: image.clip(states)) \
            .map(lambda image: image.reproject(crs=crs))



        Modis_NDVI_EVI = Modis_NDVI_EVI.toBands()
            
        out_dir = os.path.expanduser(session['user_id'])
        out_dem_stats = os.path.join(out_dir, 'Modis_NDVI_EVI_{}_{}.csv'.format(form.Statics.data,time_list[i]))

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        geemap.zonal_statistics(Modis_NDVI_EVI, states, out_dem_stats, statistics_type=form.Statics.data, scale=1000)
        data_temp = pd.read_csv(out_dem_stats)
        column_name_list = data_temp.columns.tolist()
        c = []
        d = []
        for k in zip(column_name_list[:]):
            c.append(k[0][0])
            d.append(k[0])
        data = []
        for j in range(0, len(column_name_list),len(form.Bands_Modis_NDVI_EVI.data)):            
            if all(m.isdigit() for m in c[j:j+len(form.Bands_Modis_NDVI_EVI.data)]) == True:
                        
                df = data_temp.loc[:,d[j:j+len(form.Bands_Modis_NDVI_EVI.data)]]
                df[form.Regional_category.data] = data_temp.loc[:,[form.Regional_category.data]]
                text = column_name_list[j][0:10]
                df.insert(0, 'Date', '')
                df['Date'] = trans_date(text)
                df.insert(1, 'Doy', '')
                df['Doy'] = datetime.strptime(text, '%Y_%m_%d').strftime('%j')
                colnames=['Date','Doy']
                colnames.extend(list(form.Bands_Modis_NDVI_EVI.data))
                colnames.append(form.Regional_category.data)
                df.columns=[colnames]
                data.append(df)
            else:
                continue
                        
        appended_data = pd.concat(data, axis=0, ignore_index=True)
            #cols = appended_data.columns.to_list()
            #cols.insert(len(appended_data.columns), cols.pop(cols.index(file_name)))
            #appended_data = appended_data[cols]
                
        appended_data.to_csv(out_dem_stats,index=False)#Output the file with date and doy back

    cbind_Modis_NDVI_EVI(form.Statics.data)


def zonal_Modis_LST():
    # 先從表單中提取使用者給予的資料
    form = ProductForm(request.form)
    # star the google earth engine
    ee.Initialize()
    # shp file from the user
    states = geemap.shp_to_ee("".join(glob.glob(os.path.join(session['user_id'],'*.shp'))))
    # Time list
    time_list = monthlist(form.Star_Date.data, form.End_Date.data)
    crs = 'EPSG:4326'
    
    for i in range(0,len(time_list)):

        Modis_LST = ee.ImageCollection('MODIS/006/MOD11A2') \
            .filter(ee.Filter.date(time_list[i][0],datetime.strptime(time_list[i][1],"%Y-%m-%d")+ timedelta(days=1))) \
            .filterBounds(states) \
            .map(lst_filter) \
            .map(lst_day) \
            .map(lst_night) \
            .map(lst_mean) \
            .select(list(form.Bands_Modis_LST.data)) \
            .map(lambda image: image.clip(states)) \
            .map(lambda image: image.reproject(crs=crs))


        Modis_LST = Modis_LST.toBands()
        out_dir = os.path.expanduser(session['user_id'])
        out_dem_stats = os.path.join(out_dir, 'Modis_LST_{}_{}.csv'.format(form.Statics.data,time_list[i]))

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        geemap.zonal_statistics(Modis_LST, states, out_dem_stats, statistics_type=form.Statics.data, scale=1000)
        data_temp = pd.read_csv(out_dem_stats)
        column_name_list = data_temp.columns.tolist()
        c = []
        d = []
        for k in zip(column_name_list[:]):
            c.append(k[0][0])
            d.append(k[0])
        data = []
        for j in range(0, len(column_name_list),len(form.Bands_Modis_LST.data)):            
            if all(m.isdigit() for m in c[j:j+len(form.Bands_Modis_LST.data)]) == True:
                    
                df = data_temp.loc[:,d[j:j+len(form.Bands_Modis_LST.data)]]
                df[form.Regional_category.data] = data_temp.loc[:,[form.Regional_category.data]]
                text = column_name_list[j][0:10]
                df.insert(0, 'Date', '')
                df['Date'] = trans_date_LST(text)
                df.insert(1, 'Doy', '')
                df['Doy'] = datetime.strptime(text, '%Y_%m_%d').strftime('%j')
                colnames=['Date','Doy']
                colnames.extend(list(form.Bands_Modis_LST.data))
                colnames.append(form.Regional_category.data)
                df.columns=[colnames]
                data.append(df)
            else:
                continue
                    
        appended_data = pd.concat(data, axis=0,ignore_index=True)
        #cols = appended_data.columns.to_list()
        #cols.insert(len(appended_data.columns), cols.pop(cols.index(file_name)))
        #appended_data = appended_data[cols]
            
        appended_data.to_csv(out_dem_stats,index=False)#Output the file with date and doy back
    cbind_Modis_LST(form.Statics.data)


def zonal_Modis_Nadir():

    ee.Initialize()


    mcd43a4 = ee.ImageCollection("MODIS/006/MCD43A4")\
            .select(['Nadir_Reflectance_Band1','Nadir_Reflectance_Band2','Nadir_Reflectance_Band3',
            'Nadir_Reflectance_Band4','Nadir_Reflectance_Band5','Nadir_Reflectance_Band6',
            'Nadir_Reflectance_Band7'],
            ['red', 'nir', 'blue', 'green', 'swir1', 'swir2', 'swir3'])


#Load a MODIS collection with quality data.
    mcd43a2 = ee.ImageCollection('MODIS/006/MCD43A2')\
            .select(['BRDF_Albedo_Band_Quality_Band1', 'BRDF_Albedo_Band_Quality_Band2', 'BRDF_Albedo_Band_Quality_Band3',
            'BRDF_Albedo_Band_Quality_Band4', 'BRDF_Albedo_Band_Quality_Band5', 'BRDF_Albedo_Band_Quality_Band6',
            'BRDF_Albedo_Band_Quality_Band7', 'BRDF_Albedo_LandWaterType'],
            ['qa1', 'qa2', 'qa3', 'qa4', 'qa5', 'qa6', 'qa7', 'water'])


    
    
    #Define an inner join.
    innerJoin = ee.Join.inner('NBAR', 'QA')

    #Specify an equals filter for image timestamps.
    filterTimeEq = ee.Filter.equals(
    leftField ='system:time_start',
    rightField ='system:time_start'
    )

    #Apply the join.
    innerJoinedMODIS = innerJoin.apply(mcd43a4, mcd43a2, filterTimeEq)

    #Merge two layers
    mergedCol = ee.ImageCollection(innerJoinedMODIS.map(addQABands))
    Modis_filter_vars = mergedCol.map(Modis_filter)

    # 先從表單中提取使用者給予的資料
    form = ProductForm(request.form)
    # star the google earth engine
    # shp file from the user
    states = geemap.shp_to_ee("".join(glob.glob(os.path.join(session['user_id'],'*.shp'))))
    # Time list
    time_list = monthlist(form.Star_Date.data, form.End_Date.data)
    
    crs = 'EPSG:4326'
    for i in range(0,len(time_list)):
        
        Modis_Nadir = ee.ImageCollection(Modis_filter_vars) \
            .filter(ee.Filter.date(time_list[i][0],datetime.strptime(time_list[i][1],"%Y-%m-%d")+ timedelta(days=1))) \
            .filterBounds(states) \
            .map(getNDVI) \
            .map(getEVI) \
            .map(getSAVI) \
            .map(getNDWI1) \
            .map(getNDWI2) \
            .map(getNDWI3) \
            .select(list(form.Bands_Modis_Nadir.data)) \
            .map(lambda image: image.clip(states)) \
            .map(lambda image: image.reproject(crs=crs))


        Modis_Nadir = Modis_Nadir.toBands()
        out_dir = os.path.expanduser(session['user_id'])
        out_dem_stats = os.path.join(out_dir, 'Modis_Nadir_{}_{}.csv'.format(form.Statics.data, time_list[i]))

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        geemap.zonal_statistics(Modis_Nadir, states, out_dem_stats, statistics_type=form.Statics.data, scale= 500)
        data_temp = pd.read_csv(out_dem_stats)
        column_name_list = data_temp.columns.tolist()
        c = []
        d = []
        for k in zip(column_name_list[:]):
            c.append(k[0][0])
            d.append(k[0])
        data = []
        for j in range(0, len(column_name_list),len(form.Bands_Modis_Nadir.data)):            
            if all(m.isdigit() for m in c[j:j+len(form.Bands_Modis_Nadir.data)]) == True:
                    
                df = data_temp.loc[:,d[j:j+len(form.Bands_Modis_Nadir.data)]]
                df[form.Regional_category.data] = data_temp.loc[:,[form.Regional_category.data]]
                text = column_name_list[j][0:10]
                df.insert(0, 'Date', '')
                df['Date'] = trans_date_Nadir(text)
                df.insert(1, 'Doy', '')
                df['Doy'] = datetime.strptime(text, '%Y_%m_%d').strftime('%j')
                colnames=['Date','Doy']
                colnames.extend(list(form.Bands_Modis_Nadir.data))
                colnames.append(form.Regional_category.data)
                df.columns=[colnames]
                data.append(df)
            else:
                continue
                    
        appended_data = pd.concat(data, axis=0,ignore_index=True)
        #cols = appended_data.columns.to_list()
        #cols.insert(len(appended_data.columns), cols.pop(cols.index(file_name)))
        #appended_data = appended_data[cols]
            
        appended_data.to_csv(out_dem_stats,index=False)#Output the file with date and doy back
    cbind_Modis_Nadir(form.Statics.data)
        