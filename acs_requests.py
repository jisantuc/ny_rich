import requests
from zipfile import ZipFile
from StringIO import StringIO
from states import states

import pandas as pd
import numpy as np

def state_ACS_data(state):
    url = 'http://www2.census.gov/acs2012_1yr/pums/csv_h{0}.zip'.format(state.lower())
    r = requests.get(url)
    z = ZipFile(StringIO(r.content))
    csv = z.extract('ss12h{0}.csv'.format(state.lower()))
    out = pd.read_csv(csv)
    
    return out[out.columns[:5]]

def combine_ACS(states = states.keys()):
    inf_list = [state_ACS_data(s) for s in states]
    out_df = pd.concat(inf_list)
    print 'Data read in losslessly for {0} states:'.format(len(states)), len(out_df) == np.array([len(x) for x in inf_list]).sum()
    return out_df

df = combine_ACS(states = ['NY','CA'])
