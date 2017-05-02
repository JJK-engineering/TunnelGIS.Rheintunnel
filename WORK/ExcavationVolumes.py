# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 15:37:00 2017

@author: kzq653
"""

from numpy import *
import pandas as pd
import matplotlib.pyplot as plt

texv_data = pd.read_csv('Ostroehre.TunnelBoQdata.R2.csv',index_col=0)

mc5_vol = texv_data.loc[texv_data['PayItem'] == 'MC5', 'Quantity'].sum()
mc3_vol = texv_data.loc[texv_data['PayItem'] == 'MC3', 'Quantity'].sum()
mc2_vol = texv_data.loc[texv_data['PayItem'] == 'MC2', 'Quantity'].sum()
all_vol = mc2_vol + mc3_vol + mc5_vol

title_font = {'fontname':'Arial', 'size':'16', 'color':'black', 'weight':'normal',
              'verticalalignment':'bottom'} # Bottom vertical alignment for more space
axis_font = {'fontname':'Arial', 'size':'14'}

fig=plt.figure()
objects = ('All', 'MC2', 'MC3', 'MC5')
y_pos = arange(0.0,2.0,0.5)
width=0.35

p1 = plt.bar(0+width, all_vol/1000, 
                 width, color='b')
p2 = plt.bar(0.5+width, mc2_vol/1000,
                 width, color='g')
p3 = plt.bar(1.0+width, mc3_vol/1000,
                 width, color='r')        
p4 = plt.bar(1.5+width, mc5_vol/1000,
                 width, color='c')                   
                 
plt.xticks(y_pos+0.5, objects, **axis_font)
plt.yticks( **axis_font)
plt.ylabel('Excavated Volume $[\cdot 10^3 m^3]$', **axis_font)
titleA=('Excavated Volume ')
plt.title(titleA, **title_font)
#plt.legend()
plt.show()
fig.savefig('C:\Users\kzq653\Documents\geopython\_' + str(titleA) +'.png', dpi=300)

from numpy import *
import pandas as pd
import matplotlib.pyplot as plt
# import the DataFrame with calculated Results from GIS
tv_df = pd.read_csv('Ostroehre.TunnelExcavationData.R2.csv',index_col=0)

bc1_sum=tv_df.loc[tv_df['BoreClass'] == 'BC1'].count()
bc2_sum=tv_df.loc[tv_df['BoreClass'] == 'BC2'].count()
bc3_sum=tv_df.loc[tv_df['BoreClass'] == 'BC3'].count()


fig=plt.figure()
objects = ('BC1', 'BC2', 'BC3')
y_pos = arange(len(objects))
width=0.35

p1 = plt.bar(y_pos[0]+width, bc1_sum[0]*3, 
                 width, color='b')
p2 = plt.bar(y_pos[1]+width, bc2_sum[0]*3,
                 width, color='g')
p3 = plt.bar(y_pos[2]+width, bc3_sum[0]*3,
                 width, color='r')                         
                 
plt.xticks(y_pos+0.5, objects,  **axis_font)
plt.yticks( **axis_font)
plt.ylabel('Tunnelmeter $[m]$',  **axis_font)
titleA=('Frequency of Bore Classes ')
plt.title(titleA, **title_font)
#plt.legend()
plt.show()
fig.savefig('C:\Users\kzq653\Documents\geopython\_' + str(titleA) +'.png', dpi=300)


'''
fig=plt.figure()
objects = ('Gesamtmasse', 'Molasse', u'Tüllinger Schicht', 'MixedFace', 'Lockergestein')
y_pos = np.arange(len(objects))
width = 0.5

p1 = plt.bar(y_pos+width/2, massen_fch, 
             width, color='b', 
             label='F-CH')
p2 = plt.bar(y_pos+width/2, massen_chf, 
             width, color='g', bottom=massen_fch, 
             label='CH-F')
p3 = plt.bar(y_pos+width/2, massen_dch, 
             width, color='r', bottom=np.add(massen_fch, massen_chf), 
             label='D-CH')
             
plt.xticks(y_pos+width, objects)
plt.ylim((0,110))
plt.ylabel('Ausbruchsmassen  $[\%]$')
titleA=('Gesamt-Ausbruchsmaterial Rheintunnel in Prozent')
plt.title(titleA)
plt.legend()
plt.show()
fig.savefig('C:\Users\kzq653\Documents\geopython_' + str(titleA) +'.png', dpi=300)

'''




'''
DF_all = pd.DataFrame()

texv_data = pd.read_csv('Ostroehre.TunnelExcavationData.R2.csv',index_col=0)


import glob
from dominate import document
from dominate.tags import *
from dominate.util import raw

plots = glob.glob('C:\Users\kzq653\Documents\geopython\*.png')

with document(title='plots') as doc:
    h1('Results')
    raw('izgutfztf')
    raw(texv_data .to_html())
    h1('Plots')
    with table().add(tbody()):
        l = tr()
        for path in plots:
            l += td(div(img(src=path), _class='plots'))
    
            


with open('gallery.html', 'w') as f:
    f.write(doc.render())
    
    
html_test = texv_data .to_html()
f=open('html_test.html', 'w')
f.write(html_test)
f.close()

tbm_vol=texv_data.loc[texv_data['ExcavationType'] == 'TBM', 'ExcavationVolume'].sum()
mul_vol=texv_data.loc[texv_data['ExcavationType'] == 'MUL', 'ExcavationVolume'].sum()



len_df = len(texv_data.index)

res=chatattay(())


 dc=chararray((len(S)),itemsize=3)
    dc[ (abs(beta)<1./500.) | (abs(S*1000)<10)] = 'DC1'
    dc[ ((1./500.<abs(beta)) & (abs(beta)<1./250.)) | ((10<abs(S*1000)) & (abs(S*1000)<30))] = 'DC2'
    dc[ (abs(beta)>1./250.) | (abs(S*1000)>30)] = 'DC3'
    
'''