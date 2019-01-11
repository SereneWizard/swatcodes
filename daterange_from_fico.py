# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 20:43:46 2016

@author: serenewizard
"""

""""
This file generates 
Parameters: file_cio, frequency

(1) file_cio    :   Full path of the file.cio file should be provided
(2) frequency   :   The temporal frequency of the date series to be generated

######################################################
The following alias are available for time frequency:
Alias	      Description
-----       -----------
B	      Business day
D	      Calendar day
W	      Weekly
M	      Month end
Q	      Quarter end
A	      Year end
BA	      Business year end
AS	      Year start
H	      Hourly frequency
T, min	      Minutely frequency
S	      Secondly frequency
L, ms	      Millisecond frequency
U, us	      Microsecond frequency
N, ns	      Nanosecond frequency
#######################################################

"""

# Requried Python Package Imports: 
import os
import numpy as np
import pandas as pd 
import datetime as dt
from datetime import datetime, timedelta




def ficodaterange(file_cio, frequency):
    import os
    import numpy as np
    import pandas as pd 
    import datetime as dt
    from datetime import datetime, timedelta
    ###Read the 'file.cio' file for information
    lines = []
    linenums = [7,8,9,10, 59]
    with open (file_cio, 'rt') as stdfile:
        for linenum, line in enumerate (stdfile):
            if linenum in linenums: 
                lines.append(line)
                
    timeparams = np.array([lines[i][12:16] for i in range(5)]).astype(np.int)
    startyear = timeparams[1] + timeparams[4]
    duration = timeparams[0]-timeparams[4]
    endyear = startyear + duration - 1
    startdate = pd.datetime(startyear,1,1)
    enddate = pd.datetime(endyear,1,1) + timedelta(days=int(timeparams[3])-1)
    dates = pd.date_range(startdate, enddate, freq=frequency)
    return dates



if __name__ == "__main__":
    ficopath = None
    