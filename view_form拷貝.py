from wsgiref.validate import validator
from numpy import str0
from wtforms import MultipleFileField ,StringField, BooleanField, DateField, RadioField, SelectField, TextAreaField,SubmitField, SelectMultipleField, FileField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired

#  從繼承FlaskForm開始
class ProductForm(FlaskForm):

  Product = RadioField('', choices=['CHIRSP (Rainfall Estimates from Rain Gauge and Satellite Observations)', 
                                          'EAR5', 
                                          'MODIS NDVI/EVI (16-Days)', 
                                          'MODIS Land Surface Temperature', 
                                          'MODIS Vegetation/Water Index', 
                                          'SRTM Elevation', 
                                          'World Cover'],validators=[DataRequired(message='Be sure to choose one')])

  Type = RadioField('Select output format', 
                  choices=['Zonal Statistic (csv structured data)', 'Raster(tiff structured data)'], 
                  validators=[DataRequired(message='Be sure to choose one')])

  Star_Date = DateField('Start Date',validators=[DataRequired(message='Be sure to choose one')] )
  End_Date = DateField('End Date',validators=[DataRequired(message='Be sure to choose one')] )
  Bands_Chirps = SelectMultipleField('Environmental Parameters', choices=['precipitation'] ,validators=[DataRequired(message='Be sure to choose one')])
  Bands_Era5 = SelectMultipleField('Environmental Parameters', choices=['Air_2m_T_C_mean', 'Air_2m_T_C_min', 'Air_2m_T_C_max', 'dewpoint_2m_C','RH','mean_2m_air_temperature','minimum_2m_air_temperature',
        'maximum_2m_air_temperature','dewpoint_2m_temperature','total_precipitation','surface_pressure','mean_sea_level_pressure',
        'u_component_of_wind_10m','v_component_of_wind_10m'], validators=[DataRequired(message='Be sure to choose one')])
  Bands_Modis_NDVI_EVI = SelectMultipleField('Environmental Parameters',choices=['NDVI', 'EVI'], validators=[DataRequired(message='Be sure to choose one')])
  Bands_Modis_LST = SelectMultipleField('Environmental Parameters',choices=['LST_Day','LST_Night','LST_Mean'], validators=[DataRequired(message='Be sure to choose one')])
  Bands_Modis_Nadir = SelectMultipleField('Environmental Parameters', choices=['NDVI','EVI','SAVI','NDWI_Gao', 'NDWI_Mc', 'MNDWI'], validators=[DataRequired(message='Be sure to choose one')])
  SHP = MultipleFileField('Shp file', validators=[DataRequired()])
  Regional_category = SelectField('Location ID',coerce=str0)
  Statics = SelectField('Statistics',choices=['MEAN','MAXIMUM', 'MINIMUM', 'MEDIAN', 'STD', 'VARIANCE', 'SUM'],validators=[DataRequired(message='Be sure to choose one')])
  Statics_World_Cover = SelectField('Statics',choices=['SUM', 'PERCENTAGE'],validators=[DataRequired(message='Be sure to choose one')])
  submit = SubmitField('Submit')