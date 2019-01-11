import os
import fileinput
import datetime as dt
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from daterange_from_fico import ficodaterange

###Set up the environments###
workdir = os.getcwd()
swatdir = "SWAT_Project"
basedir = "Emb_SWAT_Mon_Base"
outdir = 'Outputs'
fobs = 'Camargo_Nitrate_monthly_kg.csv'
simulated_data = 'output.sub'
file_cio = 'file.cio'
fsim = os.path.join(workdir, swatdir, basedir, simulated_data)
fico = os.path.join(workdir, swatdir, basedir, file_cio)
outpath = os.path.join(workdir, outdir)

#Work on some general parameters
dateparse = lambda dates: [datetime.strptime(x,'%Y/%m') for x in dates]





def basin_precip(output_sub,dates):
    
    ####Read the simulated data and convert it to series
    columns = [(7,10), (20,24), (24,35), (36,45)]
    datasim = pd.read_fwf(output_sub, colspecs = columns, skiprows=8)
    outparam = list(datasim.columns.values)[3]
    nrows = datasim.shape[0]
    totalsubs = max(datasim['SUB'])
    
    datasim['Precip_X_Area'] = datasim.AREAkm2 * datasim.PRECIPmm
    datasim = datasim[(datasim['MON'] <=366)]
    if (dates.freqstr is not 'D'):
        datasim = datasim.loc[0:(nrows-totalsubs-1),:]
    
    #Get Basin Area
    k = 1
    area = iter((datasim.AREAkm2).tolist())
    Area = 0
    while k<=totalsubs:
        Area += next(area)
        k += 1    
    #for index
    
    #Sum up the basin precipitation
    precipsum = 0
    basinprecip = []
    for index, row in datasim.iterrows():
        precipsum += row.Precip_X_Area
        if row.SUB == totalsubs:
            basinprecip.append({'MON':row.MON, 'BasinPrecip':precipsum})
            precipsum = 0
    basinprecip = pd.DataFrame(basinprecip)
    basinprecip['BasinPrecip'] = basinprecip.BasinPrecip/Area   
    basinprecip_series = pd.Series(basinprecip.BasinPrecip.values, name = 'BasinPrecip',  index = dates)
    return basinprecip_series
    

