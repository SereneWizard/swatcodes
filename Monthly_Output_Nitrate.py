import os
import fileinput
import datetime as dt
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

###Import the user defined functions
from daterange_from_fico import ficodaterange
from basin_precip import basin_precip

###Set up the environments###
workdir = os.getcwd()
swatdir = "SWAT_Project"
basedir = "Emb_SWAT_Mon_Base"
outdir = 'Outputs'
fobs = 'Camargo_Nitrate_monthly_kg.csv'
output_rch = 'output.rch'
file_cio = 'file.cio'
fsim = os.path.join(workdir, swatdir, basedir, output_rch)
output_sub = os.path.join(workdir,swatdir,basedir,'output.sub')
fico = os.path.join(workdir, swatdir, basedir, file_cio)
outpath = os.path.join(workdir, outdir)

#Work on some general parameters
dateparse = lambda dates: [datetime.strptime(x,'%Y/%m') for x in dates]

###Get the daterange
dates = ficodaterange(fico,'MS')
startdate = dates[0]
enddate = dates [(len(dates)-1)]
startyear = startdate.year
endyear = enddate.year

###Import the basin precipitation data
precip = basin_precip(output_sub,dates)
                      
####Read the simulated data and convert it to series
columns = [(7,10), (21,25), (50,61), (182,193)]
datasim = pd.read_fwf(fsim, colspecs = columns, skiprows=8)
outparam = list(datasim.columns.values)[3]
nrows = datasim.shape[0]
outlet = max(datasim['RCH'])
datasim = datasim[(datasim['RCH'] == outlet) & (datasim['MON'] <=12)]
nrows = datasim.shape[0]
datasim.drop(datasim.index[nrows-1:,], inplace=True)
tseriessim = pd.Series(datasim[outparam].values, name = outparam,  index = dates)


#Read in the observed data and convert it to the series
dataobs = pd.read_csv(fobs, parse_dates = ['Date'], date_parser = dateparse)
tseriesobs = pd.Series(dataobs['NO3_obs'].values*30, index = dataobs['Date'])
tseriesobs = tseriesobs[startdate:enddate]

####Calculate Performance Statistics####
obs = np.array(tseriesobs)
sim = np.array(tseriessim)
nse = 1 -np.sum((obs-sim)**2)/np.sum((obs-np.mean(obs))**2)
correlation = tseriesobs.corr(tseriessim)
r2 = correlation**2

maxval = max(obs)
if max(sim) > maxval:
    maxval = max(sim)

textr2 = (r"$R^2 = {0:.2f}$".format(r2))
textnse = (r"$NSE = {0:.2f}$".format(nse))


#Plot and plot properties
filename = "_".join([outparam, str(startyear), str(endyear)])
fig = plt.figure(1, figsize=(11,5))
ax = fig.add_subplot(111)
plot1 = ax.plot(dates, tseriesobs, linewidth=1.2, 
                label="Observed", color='darkblue', markersize=20)
plot2 = ax.plot(dates, tseriessim, '--*', linewidth=1.0, 
                label = "Simulated", color='red', markersize=7)
ax.set_ylabel(r"Nitrate Load $(kg/month)$")
ax.set_xlabel(r"$Date$")
ax.set_aspect('auto')
ax.set_ylim([0,maxval*1.35])
ax.text(0.06, 0.66, textr2,
     horizontalalignment='center', verticalalignment='center',
     transform = ax.transAxes, color='darkred', weight='bold')
ax.text(0.06, 0.62, textnse,
     horizontalalignment='center', verticalalignment='center',
     transform = ax.transAxes, color='darkred', weight='bold')

###Plot precipitation in inverted axis
ax2 = ax.twinx()
plot3 = ax2.bar(dates,precip.values, color='darkgreen', 
                alpha=0.5, width=27, label='Precipitation')
ax2.set_ylim([0,max(precip.values)*4])
ax2.set_ylabel (r"Precipitation $(mm)$")
ax2.set_ylim(ax2.get_ylim()[::-1])

####Overall plot properties
handle1, label1 = ax.get_legend_handles_labels()
handle2, label2 = ax2.get_legend_handles_labels()
handles = handle1 + handle2
labels = label1 + label2
plt.legend(handles, labels, loc=7, prop={'size':10})
plt.gca().xaxis.grid(True)
plt.title(filename)
outfig = os.path.join(outdir, (filename+ '.png'))
plt.savefig(outfig, format = 'png')
