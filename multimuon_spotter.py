#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import glob
from natsort import natsorted
import os 

import uproot

from collections import Counter


# Read the local files. All files in a directory terminated in detections
def files(path = '' ):
    files = natsorted(glob.glob(path + "/*detections"))
    return files

# Read Fluka outputs (all files defined above) with pandas
def write_data(file_):
    df = pd.read_csv(file_, skiprows=1,sep='\s+',comment='#', index_col=False,
                     names=('counter','icode','id','ltrack','ekin','ptrack', 'atrack', 'x', 'y', 'z','cx','cy','cz','id_anc','lt_anc', 'ekin_anc','ptrack_anc','x_anc', 'y_anc', 'z_anc'))

    return df

# Separate muons at the detection plane and at surface plane
def detections1 (df):
    '''Detections df'''
    det=df[(df['icode'] == 20)]
    return det

def detections2 (df):
    '''Detections df'''
    det=df[(df['icode'] == 21)]
    return det


def surface (df):
    '''Muons at surface df'''
    surf=(df[df['icode'] == 19])
    return surf

#get the proton height, energy and director cosines of the primary
def proton_features(df):
    '''First proton inelastic interaction'''
    height = df[df['icode']==101]['z']
    energy = df[df['icode']==101]['ekin']
    cx = df[df['icode']==101]['cx']
    cy = df[df['icode']==101]['cy']
    cz = df[df['icode']==101]['cz']
    features = [height, energy, cx, cy, cz]
    return features



# The cather
def multimuons_spotter_new (df):

    'Number of muons detected in a 16x4 m for shower'

    variables = ['counter','id', 'ltrack','ekin','ptrack','x','y','z_creation','cx','cy','cz',
                                    'id_anc','ekin_anc', 'x_anc','y_anc','z_anc']

    mu1, mu2, mu3, mu4, mu5, mu6, mu7, mu8, mu9, mu10, mu11, mu12 = ([] for i in range(12))

    det = detections2(df)

    def var (varname, det):

        vari = det[(det['x'] >= a) &
        (det['x'] <= a+1600) &
        (det['y'] >= b) &
        (det['y'] <= b+400)][varname]

        return vari


    for a in range(-100000,100000, 1600):
        for b in range(-100000,100000, 400):
            len_df = len(det[(det['x'] >= a ) & (det['x'] <= a+1600) &
            (det['y'] >= b) & (det['y'] <= b+400)])


            if len_df == 1:

                counter = var('counter', det)
                id_mu = var('id', det)
                x = var('x', det)
                y = var('y', det)
                cx = var('cx', det)
                cy = var('cy', det)
                cz = var('cz', det)
                ekin = var('ekin', det)
                ptrack = var('ptrack', det)
                ltrack = var('ltrack', det)
                icode = var('icode', det)

                id_anc = var('id_anc', det)
                ekin_anc = var('ekin_anc', det)
                x_anc = var('x_anc', det)
                y_anc = var('y_anc', det)
                z_anc = var('z_anc', det)

                z_creation = df[(df['counter'] == counter.values[0]) & (df['icode'] == 200)]['z'].values[0]
                z_anc = df[(df['counter'] == counter.values[0]) & (df['icode'] == 200)]['z_anc'].values[0]

                multimuons = {'counter':counter, 'id':id_mu, 'ltrack':ltrack, 'x':x, 'y':y,
                              'z_creation':z_creation,'cx':cx, 'cy':cy,'cz':cz, 'ekin':ekin,'ptrack':ptrack,
                              'id_anc':id_anc,'ekin_anc':ekin_anc, 'x_anc':x_anc,'y_anc':y_anc, 'z_anc':z_anc}

                multi_df = pd.DataFrame(multimuons)

                multi_df = multi_df[variables]

                mu1.append(multi_df.values)

            if len_df == 2:

                n = 2
                counter = var('counter', det)
                id_mu = var('id', det)
                x = var('x', det)
                y = var('y', det)
                cx = var('cx', det)
                cy = var('cy', det)
                cz = var('cz', det)
                ekin = var('ekin', det)
                ptrack = var('ptrack', det)
                ltrack = var('ltrack', det)
                icode = var('icode', det)

                id_anc = var('id_anc', det)
                ekin_anc = var('ekin_anc', det)
                x_anc = var('x_anc', det)
                y_anc = var('y_anc', det)
                z_anc = var('z_anc', det)

                z_creation = []
                z_anc = []

                for i in range(n):
                    z_creation.append(df[(df['counter'] == counter.values[i]) & (df['icode'] == 200)]['z'].values[0])
                    z_anc.append(df[(df['counter'] == counter.values[i]) & (df['icode'] == 200)]['z_anc'].values[0])

                multimuons = {'counter':counter, 'id':id_mu, 'ltrack':ltrack, 'x':x, 'y':y,'cx':cx, 'cy':cy,
                              'cz':cz, 'ekin':ekin,'ptrack':ptrack,'id_anc':id_anc, 'ekin_anc':ekin_anc,
                              'x_anc':x_anc, 'y_anc':y_anc}

                multi_df = pd.DataFrame(multimuons)

                multi_df['z_creation'] = z_creation
                multi_df['z_anc'] = z_anc

                multi_df = multi_df[variables]

                mu2.append(multi_df.values)

            if len_df == 3:

                n = 3
                counter = var('counter', det)
                id_mu = var('id', det)
                x = var('x', det)
                y = var('y', det)
                cx = var('cx', det)
                cy = var('cy', det)
                cz = var('cz', det)
                ekin = var('ekin', det)
                ptrack = var('ptrack', det)
                ltrack = var('ltrack', det)
                icode = var('icode', det)

                id_anc = var('id_anc', det)
                ekin_anc = var('ekin_anc', det)
                x_anc = var('x_anc', det)
                y_anc = var('y_anc', det)
                z_anc = var('z_anc', det)

                z_creation = []
                z_anc = []

                for i in range(n):
                    z_creation.append(df[(df['counter'] == counter.values[i]) & (df['icode'] == 200)]['z'].values[0])
                    z_anc.append(df[(df['counter'] == counter.values[i]) & (df['icode'] == 200)]['z_anc'].values[0])

                multimuons = {'counter':counter, 'id':id_mu, 'ltrack':ltrack, 'x':x, 'y':y,'cx':cx, 'cy':cy,
                              'cz':cz, 'ekin':ekin,'ptrack':ptrack,'id_anc':id_anc, 'ekin_anc':ekin_anc,
                              'x_anc':x_anc, 'y_anc':y_anc}

                multi_df = pd.DataFrame(multimuons)

                multi_df['z_creation'] = z_creation
                multi_df['z_anc'] = z_anc

                multi_df = multi_df[variables]

                mu3.append(multi_df.values)


            if len_df == 4:

                n = 4
                counter = var('counter', det)
                id_mu = var('id', det)
                x = var('x', det)
                y = var('y', det)
                cx = var('cx', det)
                cy = var('cy', det)
                cz = var('cz', det)
                ekin = var('ekin', det)
                ptrack = var('ptrack', det)
                ltrack = var('ltrack', det)
                icode = var('icode', det)

                id_anc = var('id_anc', det)
                ekin_anc = var('ekin_anc', det)
                x_anc = var('x_anc', det)
                y_anc = var('y_anc', det)
                z_anc = var('z_anc', det)

                z_creation = []
                z_anc = []

                for i in range(n):
                    z_creation.append(df[(df['counter'] == counter.values[i]) & (df['icode'] == 200)]['z'].values[0])
                    z_anc.append(df[(df['counter'] == counter.values[i]) & (df['icode'] == 200)]['z_anc'].values[0])

                multimuons = {'counter':counter, 'id':id_mu, 'ltrack':ltrack, 'x':x, 'y':y,'cx':cx, 'cy':cy,
                              'cz':cz, 'ekin':ekin,'ptrack':ptrack,'id_anc':id_anc, 'ekin_anc':ekin_anc,
                              'x_anc':x_anc, 'y_anc':y_anc}

                multi_df = pd.DataFrame(multimuons)

                multi_df['z_creation'] = z_creation
                multi_df['z_anc'] = z_anc

                multi_df = multi_df[variables]

                mu4.append(multi_df.values)

            if len_df == 5:

                n = 5
                counter = var('counter', det)
                id_mu = var('id', det)
                x = var('x', det)
                y = var('y', det)
                cx = var('cx', det)
                cy = var('cy', det)
                cz = var('cz', det)
                ekin = var('ekin', det)
                ptrack = var('ptrack', det)
                ltrack = var('ltrack', det)
                icode = var('icode', det)

                id_anc = var('id_anc', det)
                ekin_anc = var('ekin_anc', det)
                x_anc = var('x_anc', det)
                y_anc = var('y_anc', det)
                z_anc = var('z_anc', det)

                z_creation = []
                z_anc = []

                for i in range(n):
                    z_creation.append(df[(df['counter'] == counter.values[i]) & (df['icode'] == 200)]['z'].values[0])
                    z_anc.append(df[(df['counter'] == counter.values[i]) & (df['icode'] == 200)]['z_anc'].values[0])

                multimuons = {'counter':counter, 'id':id_mu, 'ltrack':ltrack, 'x':x, 'y':y,'cx':cx, 'cy':cy,
                              'cz':cz, 'ekin':ekin,'ptrack':ptrack,'id_anc':id_anc, 'ekin_anc':ekin_anc,
                              'x_anc':x_anc, 'y_anc':y_anc}

                multi_df = pd.DataFrame(multimuons)

                multi_df['z_creation'] = z_creation
                multi_df['z_anc'] = z_anc

                multi_df = multi_df[variables]

                mu5.append(multi_df.values)

            if len_df == 6:

                n = 6
                counter = var('counter', det)
                id_mu = var('id', det)
                x = var('x', det)
                y = var('y', det)
                cx = var('cx', det)
                cy = var('cy', det)
                cz = var('cz', det)
                ekin = var('ekin', det)
                ptrack = var('ptrack', det)
                ltrack = var('ltrack', det)
                icode = var('icode', det)

                id_anc = var('id_anc', det)
                ekin_anc = var('ekin_anc', det)
                x_anc = var('x_anc', det)
                y_anc = var('y_anc', det)
                z_anc = var('z_anc', det)

                z_creation = []
                z_anc = []

                for i in range(n):
                    z_creation.append(df[(df['counter'] == counter.values[i]) & (df['icode'] == 200)]['z'].values[0])
                    z_anc.append(df[(df['counter'] == counter.values[i]) & (df['icode'] == 200)]['z_anc'].values[0])

                multimuons = {'counter':counter, 'id':id_mu, 'ltrack':ltrack, 'x':x, 'y':y,'cx':cx, 'cy':cy,
                              'cz':cz, 'ekin':ekin,'ptrack':ptrack,'id_anc':id_anc, 'ekin_anc':ekin_anc,
                              'x_anc':x_anc, 'y_anc':y_anc}

                multi_df = pd.DataFrame(multimuons)

                multi_df['z_creation'] = z_creation
                multi_df['z_anc'] = z_anc

                multi_df = multi_df[variables]

                mu6.append(multi_df.values)

            if len_df == 7:

                n = 7
                counter = var('counter', det)
                id_mu = var('id', det)
                x = var('x', det)
                y = var('y', det)
                cx = var('cx', det)
                cy = var('cy', det)
                cz = var('cz', det)
                ekin = var('ekin', det)
                ptrack = var('ptrack', det)
                ltrack = var('ltrack', det)
                icode = var('icode', det)

                id_anc = var('id_anc', det)
                ekin_anc = var('ekin_anc', det)
                x_anc = var('x_anc', det)
                y_anc = var('y_anc', det)
                z_anc = var('z_anc', det)

                z_creation = []
                z_anc = []

                for i in range(n):
                    z_creation.append(df[(df['counter'] == counter.values[i]) & (df['icode'] == 200)]['z'].values[0])
                    z_anc.append(df[(df['counter'] == counter.values[i]) & (df['icode'] == 200)]['z_anc'].values[0])

                multimuons = {'counter':counter, 'id':id_mu, 'ltrack':ltrack, 'x':x, 'y':y,'cx':cx, 'cy':cy,
                              'cz':cz, 'ekin':ekin,'ptrack':ptrack,'id_anc':id_anc, 'ekin_anc':ekin_anc,
                              'x_anc':x_anc, 'y_anc':y_anc}

                multi_df = pd.DataFrame(multimuons)

                multi_df['z_creation'] = z_creation
                multi_df['z_anc'] = z_anc

                multi_df = multi_df[variables]

                mu7.append(multi_df.values)

            if len_df == 8:

                n = 8
                counter = var('counter', det)
                id_mu = var('id', det)
                x = var('x', det)
                y = var('y', det)
                cx = var('cx', det)
                cy = var('cy', det)
                cz = var('cz', det)
                ekin = var('ekin', det)
                ptrack = var('ptrack', det)
                ltrack = var('ltrack', det)
                icode = var('icode', det)

                id_anc = var('id_anc', det)
                ekin_anc = var('ekin_anc', det)
                x_anc = var('x_anc', det)
                y_anc = var('y_anc', det)
                z_anc = var('z_anc', det)

                z_creation = []
                z_anc = []

                for i in range(n):
                    z_creation.append(df[(df['counter'] == counter.values[i]) & (df['icode'] == 200)]['z'].values[0])
                    z_anc.append(df[(df['counter'] == counter.values[i]) & (df['icode'] == 200)]['z_anc'].values[0])

                multimuons = {'counter':counter, 'id':id_mu, 'ltrack':ltrack, 'x':x, 'y':y,'cx':cx, 'cy':cy,
                              'cz':cz, 'ekin':ekin,'ptrack':ptrack,'id_anc':id_anc, 'ekin_anc':ekin_anc,
                              'x_anc':x_anc, 'y_anc':y_anc}

                multi_df = pd.DataFrame(multimuons)

                multi_df['z_creation'] = z_creation
                multi_df['z_anc'] = z_anc

                multi_df = multi_df[variables]

                mu8.append(multi_df.values)

            if len_df == 9:

                n = 9
                counter = var('counter', det)
                id_mu = var('id', det)
                x = var('x', det)
                y = var('y', det)
                cx = var('cx', det)
                cy = var('cy', det)
                cz = var('cz', det)
                ekin = var('ekin', det)
                ptrack = var('ptrack', det)
                ltrack = var('ltrack', det)
                icode = var('icode', det)

                id_anc = var('id_anc', det)
                ekin_anc = var('ekin_anc', det)
                x_anc = var('x_anc', det)
                y_anc = var('y_anc', det)
                z_anc = var('z_anc', det)

                z_creation = []
                z_anc = []

                for i in range(n):
                    z_creation.append(df[(df['counter'] == counter.values[i]) & (df['icode'] == 200)]['z'].values[0])
                    z_anc.append(df[(df['counter'] == counter.values[i]) & (df['icode'] == 200)]['z_anc'].values[0])

                multimuons = {'counter':counter, 'id':id_mu, 'ltrack':ltrack, 'x':x, 'y':y,'cx':cx, 'cy':cy,
                              'cz':cz, 'ekin':ekin,'ptrack':ptrack,'id_anc':id_anc, 'ekin_anc':ekin_anc,
                              'x_anc':x_anc, 'y_anc':y_anc}

                multi_df = pd.DataFrame(multimuons)

                multi_df['z_creation'] = z_creation
                multi_df['z_anc'] = z_anc

                multi_df = multi_df[variables]

                mu9.append(multi_df.values)

            if len_df == 10:

                n = 10
                counter = var('counter', det)
                id_mu = var('id', det)
                x = var('x', det)
                y = var('y', det)
                cx = var('cx', det)
                cy = var('cy', det)
                cz = var('cz', det)
                ekin = var('ekin', det)
                ptrack = var('ptrack', det)
                ltrack = var('ltrack', det)
                icode = var('icode', det)

                id_anc = var('id_anc', det)
                ekin_anc = var('ekin_anc', det)
                x_anc = var('x_anc', det)
                y_anc = var('y_anc', det)
                z_anc = var('z_anc', det)

                z_creation = []
                z_anc = []

                for i in range(n):
                    z_creation.append(df[(df['counter'] == counter.values[i]) & (df['icode'] == 200)]['z'].values[0])
                    z_anc.append(df[(df['counter'] == counter.values[i]) & (df['icode'] == 200)]['z_anc'].values[0])

                multimuons = {'counter':counter, 'id':id_mu, 'ltrack':ltrack, 'x':x, 'y':y,'cx':cx, 'cy':cy,
                              'cz':cz, 'ekin':ekin,'ptrack':ptrack,'id_anc':id_anc, 'ekin_anc':ekin_anc,
                              'x_anc':x_anc, 'y_anc':y_anc}

                multi_df = pd.DataFrame(multimuons)

                multi_df['z_creation'] = z_creation
                multi_df['z_anc'] = z_anc

                multi_df = multi_df[variables]

                mu10.append(multi_df.values)

            if len_df == 11:

                n = 11
                counter = var('counter', det)
                id_mu = var('id', det)
                x = var('x', det)
                y = var('y', det)
                cx = var('cx', det)
                cy = var('cy', det)
                cz = var('cz', det)
                ekin = var('ekin', det)
                ptrack = var('ptrack', det)
                ltrack = var('ltrack', det)
                icode = var('icode', det)

                id_anc = var('id_anc', det)
                ekin_anc = var('ekin_anc', det)
                x_anc = var('x_anc', det)
                y_anc = var('y_anc', det)
                z_anc = var('z_anc', det)

                z_creation = []
                z_anc = []

                for i in range(n):
                    z_creation.append(df[(df['counter'] == counter.values[i]) & (df['icode'] == 200)]['z'].values[0])
                    z_anc.append(df[(df['counter'] == counter.values[i]) & (df['icode'] == 200)]['z_anc'].values[0])

                multimuons = {'counter':counter, 'id':id_mu, 'ltrack':ltrack, 'x':x, 'y':y,'cx':cx, 'cy':cy,
                              'cz':cz, 'ekin':ekin,'ptrack':ptrack,'id_anc':id_anc, 'ekin_anc':ekin_anc,
                              'x_anc':x_anc, 'y_anc':y_anc}

                multi_df = pd.DataFrame(multimuons)

                multi_df['z_creation'] = z_creation
                multi_df['z_anc'] = z_anc

                multi_df = multi_df[variables]

                mu11.append(multi_df.values)

            if len_df == 12:

                n = 12
                counter = var('counter', det)
                id_mu = var('id', det)
                x = var('x', det)
                y = var('y', det)
                cx = var('cx', det)
                cy = var('cy', det)
                cz = var('cz', det)
                ekin = var('ekin', det)
                ptrack = var('ptrack', det)
                ltrack = var('ltrack', det)
                icode = var('icode', det)

                id_anc = var('id_anc', det)
                ekin_anc = var('ekin_anc', det)
                x_anc = var('x_anc', det)
                y_anc = var('y_anc', det)
                z_anc = var('z_anc', det)

                z_creation = []
                z_anc = []

                for i in range(n):
                    z_creation.append(df[(df['counter'] == counter.values[i]) & (df['icode'] == 200)]['z'].values[0])
                    z_anc.append(df[(df['counter'] == counter.values[i]) & (df['icode'] == 200)]['z_anc'].values[0])

                multimuons = {'counter':counter, 'id':id_mu, 'ltrack':ltrack, 'x':x, 'y':y,'cx':cx, 'cy':cy,
                              'cz':cz, 'ekin':ekin,'ptrack':ptrack,'id_anc':id_anc, 'ekin_anc':ekin_anc,
                              'x_anc':x_anc, 'y_anc':y_anc}

                multi_df = pd.DataFrame(multimuons)

                multi_df['z_creation'] = z_creation
                multi_df['z_anc'] = z_anc

                multi_df = multi_df[variables]

                mu12.append(multi_df.values)

    return mu1, mu2, mu3, mu4, mu5, mu6, mu7, mu8, mu9, mu10, mu11, mu12


def multimuons_to_savez (df, file_):

    mu_out = multimuons_spotter_new(df)
    features = proton_features(df)

    m1out = np.array(mu_out[0])
    m2out = np.array(mu_out[1])
    m3out = np.array(mu_out[2])
    m4out = np.array(mu_out[3])
    m5out = np.array(mu_out[4])
    m6out = np.array(mu_out[5])
    m7out = np.array(mu_out[6])
    m8out = np.array(mu_out[7])
    m9out = np.array(mu_out[8])
    m10out = np.array(mu_out[9])
    m11out = np.array(mu_out[10])
    m12out = np.array(mu_out[11])

    np.savez(os.path.basename(file_) + '.npz',shower_features = features,m1out=m1out, m2out=m2out, m3out=m3out, m4out=m4out, m5out=m5out, m6out=m6out, m7out=m7out, m8out=m8out, m9out=m9out, m10out=m10out, m11out=m11out, m12out=m12out)
