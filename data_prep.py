# Script to read data from fluka. Three new columns will be calculated and added: Unique_id, icode_cr and line_cr.
# These three new columns will help to separate the creation and dead point (unique_id) and to find three pions decayment from Kaons (icode_cr and line_cr)

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
from tqdm.notebook import trange
import uproot

file_name = 'shower001_decay_acc' # Fluka output

df = pd.read_csv(file_name, sep='\s+',comment='#', index_col=False,
                 names=('icode','id','ekin','ptrack', 'atrack', 'ltrack', 'x', 'y', 'z',
                        'cx', 'cy', 'cz', 'id_anc','lt_anc','etot_anc', 'x_anc', 'y_anc', 'z_anc', 'ptrack_anc', 'cx_anc', 'cy_anc', 'cz_anc',
                        'icode_anc', 'line_anc'))



#  Creation and addition of unique id to the df
unique_id = []
n = 0
for i in trange(len(df)-1):
    if (df['id'][i] == df['id'][i+1]) and \
    (df['ekin'][i] > df['ekin'][i+1]) and \
    (df['atrack'][i] <= df['atrack'][i+1]) and \
    (df['ltrack'][i] == df['ltrack'][i+1]):
        n = n
    else:
        n +=1
    unique_id.append(n)

unique_id.insert(0, 0)
df['unique_id'] = unique_id


df.insert(25, "unique_id_anc", np.zeros(len(df)))  # add column to store unique_id_anc icode

# Generating the data frame First and Last which are the creation point of the particle and the end point of the same particle.

df_first = df.drop_duplicates(subset=['unique_id'], keep='first')
df_last = df.drop_duplicates(subset=['unique_id'], keep='last')

# When the Fluka Monte Carlo code generates a particle, the icode tells us which process has suffered this particle. Thinking this way, the icode which is of our interest is the last one of the particle transport, this is the one in the df_last data frame.
# Because of that, the icode in the df_first is substitued by the icode from the data_last.

# Change icode data first for last.
extracted_column = df_last['icode']
extracted_column = np.array(extracted_column)
df_first['icode'] = extracted_column

# df_first is used instead of df because it is much smaller making the loop below much faster and with the same output.
# Generating data for the icode_anc and creation_line

table = np.array(df_first)

# icode 0

# id 1
# ltrack 5

# idanc 12
# ltrackanc 13

# prod icode 22

# unique_id 24
# unique_id_anc 25



# forward loop
for i in range(len(table)):

    line_i = table[i]
    anc_id, anc_ltrack = line_i[12], line_i[13]
    curr_id, curr_ltrack = line_i[1], line_i[5]
    unique_id = line_i[24]

    # reverse loop
    for i_reverse in range(i-1, -1, -1):

        line_ir = table[i_reverse]
        id, ltrack = line_ir[1], line_ir[5]
        unique_id_r = line_ir[24]


        # skip propagation / delta ray production
        #if id == curr_id and ltrack == curr_ltrack and unique_id_r == unique_id:
        #    break

        if anc_id == id and anc_ltrack == ltrack:

            table[i, 22] = line_ir[0]
            table[i, 23] = i_reverse
            table[i, 25] = line_ir[24]

            break  # stop after ancestor is found
df_first = pd.DataFrame(table)
df_first.columns = ['icode','id','ekin','ptrack', 'atrack', 'ltrack', 'x', 'y', 'z','cx', 'cy', 'cz', 'id_anc','lt_anc','etot_anc', 'x_anc', 'y_anc', 'z_anc',
                     'ptrack_anc', 'cx_anc', 'cy_anc', 'cz_anc','icode_anc', 'line_anc', 'unique_id', 'unique_id_anc']

# Copy icode_cr, line_cr to data_last and unique_id_anc
extracted_column2 = df_first['icode_anc']
extracted_column2 = np.array(extracted_column2)
df_last['icode_anc'] = extracted_column2

extracted_column3 = df_first['line_anc']
extracted_column3 = np.array(extracted_column3)
df_last['line_anc'] = extracted_column3

extracted_column4 = df_first['unique_id_anc']
extracted_column4 = np.array(extracted_column4)
df_last['unique_id_anc'] = extracted_column4


# Set the unique id label as an index for all df
df = df.set_index('unique_id')
df_first = df_first.set_index('unique_id')
df_last = df_last.set_index('unique_id')

# Write the df_first and last into a csv file reorganizing columns to match.

#df_first[['icode','id','ltrack','ekin','ptrack', 'atrack', 'x', 'y', 'z','cx', 'cy', 'cz',
                      #'id_anc','lt_anc','etot_anc', 'ptrack_anc', 'x_anc', 'y_anc', 'z_anc',
                      #'cx_anc', 'cy_anc', 'cz_anc','icode_anc', 'line_anc','unique_id_anc']].to_csv('First.csv')

#df_last[['icode','id','ltrack','ekin','ptrack', 'atrack', 'x', 'y', 'z','cx', 'cy', 'cz',
                      #'id_anc','lt_anc','etot_anc', 'ptrack_anc', 'x_anc', 'y_anc', 'z_anc',
                      #'cx_anc', 'cy_anc', 'cz_anc','icode_anc', 'line_anc','unique_id_anc']].to_csv('Last.csv')


#df[['icode','id','ltrack','ekin','ptrack', 'atrack', 'x', 'y', 'z','cx', 'cy', 'cz',
                      #'id_anc','lt_anc','etot_anc', 'ptrack_anc', 'x_anc', 'y_anc', 'z_anc',
                      #'cx_anc', 'cy_anc', 'cz_anc']].to_csv('Main.csv')

# Write df, df_first and last into a root file reorganizing columns to match. The single root file will have three trees> main, first and last.

df_first = df_first[['icode','id','ltrack','ekin','ptrack', 'atrack', 'x', 'y', 'z','cx', 'cy', 'cz',
                      'id_anc','lt_anc','etot_anc', 'ptrack_anc', 'x_anc', 'y_anc', 'z_anc',
                      'cx_anc', 'cy_anc', 'cz_anc','icode_anc', 'line_anc','unique_id_anc']]

df_last = df_last[['icode','id','ltrack','ekin','ptrack', 'atrack', 'x', 'y', 'z','cx', 'cy', 'cz',
                      'id_anc','lt_anc','etot_anc', 'ptrack_anc', 'x_anc', 'y_anc', 'z_anc',
                      'cx_anc', 'cy_anc', 'cz_anc','icode_anc', 'line_anc','unique_id_anc']]

df = df[['icode','id','ltrack','ekin','ptrack', 'atrack', 'x', 'y', 'z','cx', 'cy', 'cz',
                      'id_anc','lt_anc','etot_anc', 'ptrack_anc', 'x_anc', 'y_anc', 'z_anc',
                      'cx_anc', 'cy_anc', 'cz_anc']]

fs = uproot.recreate('fs_1_100_0.root')
fs["main"] = df
fs["first"] = df_first
fs["last"] = df_last
