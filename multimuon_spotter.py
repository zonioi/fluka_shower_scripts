def multimuons_spotter_new (df):
    
    'Number of muons detected in a 16x4 m for shower'

    variables = ['counter','id', 'ltrack','ekin','ptrack','x','y','z_creation','cx','cy','cz',
                                    'id_anc','ekin_anc', 'x_anc','y_anc','z_anc']
    
    mu1, mu2, mu3 = ([] for i in range(3))
    ls1, ls2, ls3 = ([] for i in range(3))


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
                

                multimuons = {'counter':counter, 'id':id_mu, 'ltrack':ltrack, 'x':x, 'y':y, 'cx':cx, 'cy':cy,
                              'cz':cz, 'ekin':ekin,'ptrack':ptrack,'id_anc':id_anc, 'ekin_anc':ekin_anc,
                              'x_anc':x_anc,'y_anc':y_anc,'multiplicity':len_df, 'icode': icode}
        
                multi_df = pd.DataFrame(multimuons)
                
                
                ls1.append(multi_df['counter'].values[0])
                
                        
                z_creation = df[(df['counter'].isin(ls1)) & (df['icode'] ==200)]['z'].values[0]
                z_anc = df[(df['counter'].isin(ls1)) & (df['icode'] ==200)]['z_anc'].values[0]
                
                multi_df['z_creation'] = z_creation
                multi_df['z_anc'] = z_anc
                    
                multi_df = multi_df[variables]
               
                
                mu1.append(multi_df.values)

            if len_df == 2:
                
                counter2 = var('counter', det)
                id_mu2 = var('id', det)
                x2 = var('x', det)
                y2 = var('y', det)
                cx2 = var('cx', det)
                cy2 = var('cy', det)
                cz2 = var('cz', det)
                ekin2 = var('ekin', det)
                ptrack2 = var('ptrack', det)
                ltrack2 = var('ltrack', det)
                icode2 = var('icode', det)
                
                id_anc2 = var('id_anc', det)
                ekin_anc2 = var('ekin_anc', det)
                x_anc2 = var('x_anc', det)
                y_anc2 = var('y_anc', det)
                z_anc2 = var('z_anc', det)            
                

                multimuons2 = {'counter':counter2, 'id':id_mu2, 'ltrack':ltrack2, 'x':x2, 'y':y2, 'cx':cx2, 'cy':cy2, 
                              'cz':cz2, 'ekin':ekin2,'ptrack':ptrack2,'id_anc':id_anc2, 'ekin_anc':ekin_anc2,
                              'x_anc':x_anc2,'y_anc':y_anc2,'multiplicity':len_df, 'icode': icode2}
        
                multi_df2 = pd.DataFrame(multimuons2)
                
                
                ls2.append(multi_df2['counter'].values[0:2])
                
                z_creation2 = [] 
                z_anc2 = []
                for i in range(2):                 
                    z_creation2.append(df[(df['counter'].isin(ls2[0])) & (df['icode'] ==200)]['z'].values[i])
                    z_anc2.append(df[(df['counter'].isin(ls2[0])) & (df['icode'] ==200)]['z_anc'].values[i])
                
                multi_df2['z_creation'] = z_creation2
                multi_df2['z_anc'] = z_anc2
                    
                multi_df2 = multi_df2[variables]
                
                mu2.append(multi_df2.values)

            
                
                
    return mu1, mu2, ls2
