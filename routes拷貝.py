from flask import render_template, request, redirect, url_for, session, Blueprint, send_file
from view_form import ProductForm
from models import str_random, zonal_Chirsp, zonal_era5, zonal_Modis_NDVI_EVI, zonal_Modis_LST, zonal_Modis_Nadir
from werkzeug.utils import secure_filename
import os
import shapefile
import glob
import shutil

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET','POST'])
def index():
    form = ProductForm()
    if request.method == 'POST':
        if str(form.Type.data) == str('Zonal Statistic (csv structured data)'):
            return redirect(url_for('routes.Zonal_Index', form=form))

        elif str(form.Type.data) == str('Raster(tiff structured data)'):
            return redirect(url_for('routes.Era5', form=form))

    return render_template('Index.html',form=form)

@routes.route('/Table', methods=['GET', 'POST'])
def Table():
    form = ProductForm()
    if request.method == 'POST':

        return render_template('Index.html', form=form)
    return render_template('Table.html', form=form)      



@routes.route('/Zonal_Index',methods=['GET','POST'])
def Zonal_Index():
    form = ProductForm()
    UPLOAD_FOLDER = str_random() 
    session['user_id'] = UPLOAD_FOLDER

    if form.validate_on_submit():

        return redirect(url_for('Zonal_All', form=form))

    return render_template('Zonal_Index.html',form=form)

@routes.route('/Zonal_All',methods=['GET','POST'])
def Zonal_All():
    form = ProductForm(request.form)
    if os.path.isdir(session['user_id']) == True:
        shutil.rmtree(session['user_id'], ignore_errors=True)
        os.makedirs(session['user_id'])
    else:
        os.makedirs(session['user_id'])

    files = request.files.getlist('file')
    for file in files:
        file.save(os.path.join(session['user_id'],secure_filename(file.filename)))
    if request.method == 'POST':

        if str(form.Product.data) == str('CHIRSP (Rainfall Estimates from Rain Gauge and Satellite Observations)'):
            return redirect(url_for('routes.Chirsp', form=form))
        elif str(form.Product.data) == str('EAR5'):
            return redirect(url_for('routes.Era5', form=form))
        elif str(form.Product.data) == str('MODIS NDVI/EVI (16-Days)'):
            return redirect(url_for('routes.Modis_NDVI_EVI', form=form))
        elif str(form.Product.data) == str('MODIS Land Surface Temperature'):
            return redirect(url_for('routes.Modis_LST', form=form))
        elif str(form.Product.data) == str('MODIS Vegetation/Water Index'):
            return redirect(url_for('routes.Modis_Nadir', form=form))    
        elif str(form.Product.data) == str('SRTM Elevation'):
            return redirect(url_for('routes.STRM_V4', form=form))
        elif str(form.Product.data) == str('World Cover'):
            return redirect(url_for('routes.World_Cover', form=form))

    return render_template('Zonal_All.html', form=form)


@routes.route('/Chirsp', methods=['GET', 'POST'])
def Chirsp():
    # read from table
    form = ProductForm(request.form)

    #read shpfile 
    shp = shapefile.Reader("".join(glob.glob(os.path.join(session['user_id'],'*.shp'))))
    # read shapfile label
    shp_filed = []

    for i in range(len(shp.fields)):
        label = shp.fields[i][0]
        shp_filed.append(label)

    form.Regional_category.choices = shp_filed

    #  flask_wtf類中提供判斷是否表單提交過來的method，不需要自行利用request.method來做判斷
    if form.validate_on_submit():

        return redirect(url_for('routes.Model_Chirsp', form=form))

    return render_template('Chirsp.html', form=form)


@routes.route('/Era5', methods=['GET', 'POST'])
def Era5():
    form = ProductForm(request.form)

    shp = shapefile.Reader("".join(glob.glob(os.path.join(session['user_id'],'*.shp'))))
    shp_filed = []
    for i in range(len(shp.fields)):
        label = shp.fields[i][0]
        shp_filed.append(label)

    form.Regional_category.choices = shp_filed

    #  flask_wtf類中提供判斷是否表單提交過來的method，不需要自行利用request.method來做判斷
    if form.validate_on_submit():

        return redirect(url_for('routes.Model_Era5', form=form))

    return render_template('Era5.html', form=form)


@routes.route('/Modis_NDVI_EVI', methods=['GET', 'POST'])
def Modis_NDVI_EVI():
    form = ProductForm()

    shp = shapefile.Reader(''.join(glob.glob(os.path.join(session['user_id'], '*.shp'))))
    shp_filed = []
    for i in range(len(shp.fields)):
        label = shp.fields[i][0]
        shp_filed.append(label)

    form.Regional_category.choices = shp_filed

    #  flask_wtf類中提供判斷是否表單提交過來的method，不需要自行利用request.method來做判斷
    if form.validate_on_submit():

        return redirect(url_for('routes.Model_Modis_NDVI_EVI', form=form))

    return render_template('Modis_NDVI_EVI.html', form=form)


@routes.route('/Modis_LST', methods=['GET', 'POST'])
def Modis_LST():
    form = ProductForm()

    shp = shapefile.Reader(''.join(glob.glob(os.path.join(session['user_id'], '*.shp'))))
    shp_filed = []
    for i in range(len(shp.fields)):
        label = shp.fields[i][0]
        shp_filed.append(label)

    form.Regional_category.choices = shp_filed

    #  flask_wtf類中提供判斷是否表單提交過來的method，不需要自行利用request.method來做判斷
    if form.validate_on_submit():

        return redirect(url_for('routes.Model_Modis_LST', form=form))

    return render_template('Modis_LST.html', form=form)

@routes.route('/Modis_Nadir', methods=['GET', 'POST'])
def Modis_Nadir():
    form = ProductForm()

    shp = shapefile.Reader(''.join(glob.glob(os.path.join(session['user_id'], '*.shp'))))
    # shp = shapefile.Reader(form.SHP.data)
    shp_filed = []
    for i in range(len(shp.fields)):
        label = shp.fields[i][0]
        shp_filed.append(label)

    form.Regional_category.choices = shp_filed

    #  flask_wtf類中提供判斷是否表單提交過來的method，不需要自行利用request.method來做判斷
    if form.validate_on_submit():

        return redirect(url_for('routes.Model_Modis_Nadir', form=form))

    return render_template('Modis_Nadir.html', form=form)


@routes.route('/Model_Chirsp', methods=['GET', 'POST'])
def Model_Chirsp():

    zonal_Chirsp()

    if os.path.isfile(session['user_id'] + '/final.csv') == True:
        return redirect(url_for('routes.download_file'))
    else:
        return('No file exist, Please retry again')


@routes.route('/Model_Era5', methods=['GET', 'POST'])
def Model_Era5():

    zonal_era5()

    if os.path.isfile(session['user_id'] + '/final.csv') == True:
        return redirect(url_for('routes.download_file'))
    else:
        return('No file exist, Please retry again')

@routes.route('/Model_Modis_NDVI_EVI', methods=['GET', 'POST'])
def Model_Modis_NDVI_EVI():

    zonal_Modis_NDVI_EVI()

    if os.path.isfile(session['user_id'] + '/final.csv') == True:
        return redirect(url_for('routes.download_file'))
    else:
        return('No file exist, Please retry again')


@routes.route('/Model_Modis_LST', methods=['GET', 'POST'])
def Model_Modis_LST():

    zonal_Modis_LST()

    if os.path.isfile(session['user_id'] + '/final.csv') == True:
        return redirect(url_for('routes.download_file'))
    
    else:
        return('No file exist, Please retry again')

@routes.route('/Model_Modis_Nadir', methods=['GET', 'POST'])
def Model_Modis_Nadir():

    zonal_Modis_Nadir()

    if os.path.isfile(session['user_id'] + '/final.csv') == True:
        return redirect(url_for('routes.download_file'))
    
    else:
        return('No file exist, Please retry again')


@routes.route('/download_file')
def download_file():
    # 取得下載檔案的路徑
    filepath = session['user_id'] + '/final.csv'
    
    # 設定下載檔案的資訊
    response = send_file(filepath, mimetype="text/csv", download_name="data.csv")
    
    response.set_cookie('fileDownload', 'true', max_age=20)
    # 刪除資料夾及其內容
    shutil.rmtree(session['user_id'])
    
    # 回傳下載檔案
    return response
