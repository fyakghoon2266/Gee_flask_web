import ee

def getC_air_mean(image):
    
    Air_2m_T_C_mean = image.expression(
      'T - 273.15',{
      'T' : image.select('mean_2m_air_temperature')}).rename('Air_2m_T_C_mean')
    
    return image.addBands(Air_2m_T_C_mean)

def getC_air_min(image):
    
    Air_2m_T_C_min = image.expression(
      'T - 273.15',{
      'T' : image.select('minimum_2m_air_temperature')}).rename('Air_2m_T_C_min')
    
    return image.addBands(Air_2m_T_C_min)

def getC_air_max(image):
    
    Air_2m_T_C_max = image.expression(
      'T - 273.15',{
      'T' : image.select('maximum_2m_air_temperature')}).rename('Air_2m_T_C_max')
    
    return image.addBands(Air_2m_T_C_max)


def getC_dewpoint(image):
    
    dewpoint_2m_temperature_C = image.expression(
      'T - 273.15',{
      'T' : image.select('dewpoint_2m_temperature')}).rename('dewpoint_2m_C')
    
    return image.addBands(dewpoint_2m_temperature_C)

def getRH(image):
    
    RH = image.expression(
      '100 * (exp((17.625 * Td)/(243.04 + Td))/exp((17.625*T)/(243.04 + T)))',{
      'Td' : image.select('dewpoint_2m_temperature').add(-273.15),
      'T' : image.select('mean_2m_air_temperature').add(-273.15)}).rename('RH')
    
    return image.addBands(RH)

def lst_day(image):
    
    lst_day = image.select('LST_Day_1km').multiply(0.02).subtract(273.15).rename("LST_Day")
    image = image.addBands(lst_day)

    return(image)

def lst_night(image):
    
    lst_night = image.select('LST_Night_1km').multiply(0.02).subtract(273.15).rename("LST_Night")
    image = image.addBands(lst_night)

    return(image)

def lst_mean(image):
    lst_mean = image.expression(
    '(day + night) / 2', {
    'day': image.select('LST_Day'),
    'night': image.select('LST_Night')}).rename('LST_Mean');

    return image.addBands(lst_mean)

def lst_filter(image):
    
    qaday = image.select(['QC_Day'])
    qanight = image.select(['QC_Night'])
    dayshift = qaday.rightShift(6)
    nightshift = qanight.rightShift(6)
    daymask = dayshift.lte(2)
    nightmask = nightshift.lte(2)
    #dayshift1 = qaday.leftShift(6)
    #dayshift2 = qaday.rightShift(6)
    #daymask = dayshift2.eq(0)
    #nightshift1 = qanight.leftShift(6)
    #nightshift2 = qanight.rightShift(6)
    #nightmask = nightshift2.eq(0)
    outimage = ee.Image(image.select(['LST_Day_1km', 'LST_Night_1km']))
    outmask = ee.Image([daymask, nightmask])
    return outimage.updateMask(outmask)




def maskModisQA(image):
    qa = image.select('SummaryQA')
    MODLAND_QA_Bits = 1<<1
    mask = qa.bitwiseAnd(MODLAND_QA_Bits).eq(0)
    return image.updateMask(mask).divide(10000)


# Modis_Nadir

# get indexes NDVI
def getNDVI(image):
    
    # Normalized difference vegetation index (NDVI)
    ndvi = image.normalizedDifference(['nir','red']).rename("NDVI")
    image = image.addBands(ndvi)

    return(image)

def getEVI(image):
    evi = image.expression(
      '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))', {
      'NIR' : image.select('nir'),
      'RED' : image.select('red'),
      'BLUE': image.select('blue')}).rename('EVI')
    return image.addBands(evi)
    

def getSAVI(image):
    savi = image.expression(
     '1.5 * (nir - red) / (nir + red + 0.5)', {
      'nir': image.select('nir'),
      'red': image.select('red')}).rename('SAVI')
    return image.addBands(savi)


# get indexes NDWI1
def getNDWI1(image):
    
    # Normalized difference vegetation index (NDWI1) (Xnir - Xswir1)/(Xnir + Xswir1)
    ndwi1 = image.normalizedDifference(['nir','swir2']).rename("NDWI_Gao")
    image = image.addBands(ndwi1)

    return(image)

# get indexes NDWI2
def getNDWI2(image):
    
    # Normalized difference vegetation index (NDWI2) (Xnir - Xswir2)/(Xnir + Xswir2)
    ndwi2 = image.normalizedDifference(['green','nir']).rename("NDWI_Mc")
    image = image.addBands(ndwi2)

    return(image)

# get indexes NDWI3
def getNDWI3(image):
    
    # Normalized difference vegetation index (NDWI3) (Xgreen - Xnir)/(Xgreen + Xnir)
    ndwi3 = image.normalizedDifference(['green','swir2']).rename("MNDWI")
    image = image.addBands(ndwi3)

    return(image)


def addQABands(image):
    nbar = ee.Image(image.get('NBAR'))
    qa = ee.Image(image.get('QA')).select(['qa2'])
    water = ee.Image(image.get('QA')).select(['water'])
    return(nbar.addBands([qa, water]))

def Modis_filter(image):
        qaband = image.select(['qa2']); #Right now, only using QA info for the NIR band
        wband = image.select(['water'])
        qamask = qaband.lte(2) and (wband.eq(1))
        nir_r = image.select('nir').multiply(0.0001).rename('nir')
        red_r = image.select('red').multiply(0.0001).rename('red')
        swir1_r = image.select('swir1').multiply(0.0001).rename('swir1')
        swir2_r = image.select('swir2').multiply(0.0001).rename('swir2')
        blue_r = image.select('blue').multiply(0.0001).rename('blue')
        return image.addBands(nir_r).addBands(red_r).addBands(swir1_r).addBands(swir2_r).addBands(blue_r).updateMask(qamask)
