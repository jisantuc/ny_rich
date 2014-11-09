import requests
from zipfile import ZipFile
from StringIO import StringIO
from states import states

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
sns.reset_orig()

#lists of PUMAs in NYC and SF
nyc_PUMA = [3701,3702,3703,3704,3705,3706,3707,3708,3709,
            3710,3801,3802,3803,3804,3805,3806,3807,3808,
            3809,3810,3901,3902,3903,4001,4002,4003,4004,
            4005,4006,4007,4008,4009,4010,4011,4012,4013,
            4014,4015,4016,4017,4018,4101,4102,4103,4104,
            4105,4106,4107,4108,4109,4110,4111,4112,4113,
            4114]

sf_PUMA = [7503,7504,7505,7506,7507]

keep_cols = ['SERIALNO','PUMA','HINCP']

def state_ACS_data(state):
    url = 'http://www2.census.gov/acs2012_1yr/pums/csv_h{0}.zip'.format(state.lower())
    r = requests.get(url)
    z = ZipFile(StringIO(r.content))
    csv = z.extract('ss12h{0}.csv'.format(state.lower()))
    out = pd.read_csv(csv)
    
    return out[keep_cols]

def combine_ACS(states = states.keys()):
    inf_list = [state_ACS_data(s) for s in states]
    out_df = pd.concat(inf_list)
    print 'Data read in losslessly for {0} states: '.format(len(states)), len(out_df) == np.array([len(x) for x in inf_list]).sum()
    return out_df

def split_city(data, PUMAs, city):
    tp = [data[data['PUMA'] == p] for p in PUMAs]
    out = pd.concat([chunk for chunk in tp])
    out['city'] = city
    return out

df = combine_ACS()
df_nyc = split_city(df, nyc_PUMA, 'NYC')
df_sf = split_city(df, sf_PUMA, 'SF')

#Graph things!
fig, ax = plt.subplots(figsize = (10,10))
for d, l in zip([df_nyc, df_sf, df], ['NYC', 'SF', 'US']):
    sns.kdeplot(d['HINCP'],shade = True, **{'label':l})

plt.xlabel('Household Income')
plt.ylabel('Density Estimate')
plt.title('Kernel Density Estimate of Income Distribution,\nNYC and SF')
plt.xlim((min(min(df_nyc['HINCP']),min(df_sf['HINCP']),min(df['HINCP'])) - 10000,
          max(max(df_nyc['HINCP']),max(df_sf['HINCP']),max(df['HINCP'])) + 10000))
plt.ylim((0,0.000012))
plt.legend()

#plt.show()
plt.savefig('plot.png', bbox_inches = 'tight', pad_inches = 0.2)
