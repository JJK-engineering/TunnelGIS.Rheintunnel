
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random as ra
from matplotlib.lines import Line2D
import matplotlib.gridspec as gridspec

TunnelExcavationData = "/home/katharina/Desktop/TunnelGIS.Rheintunnel/WORK/Ostroehre.TunnelExcavationData.R2.csv"
TunnelExcavationData_df = pd.read_csv(TunnelExcavationData)
TunnelExcavationData_df_sel1 =  TunnelExcavationData_df.loc[:,["Elevation", "Station"]]
TunnelExcavationData_df_sel2 =  TunnelExcavationData_df.loc[:,["DTM","RockSurface"]]
TunnelExcavationData_df.columns

fig, axes = plt.subplots(nrows=2, ncols=1)
ax = TunnelExcavationData_df_sel1.plot(kind='line', x='Station', y='Elevation',ax=axes[0], color = "black", lw = 5);
TunnelExcavationData_df_sel2.plot(kind='area', stacked = False,ax=ax, color = ["green", "lightgrey"], alpha = 1)
ax.set_ylim(bottom=150)
ax.set_ylabel('masl.')
plt.setp( axes[0].xaxis.get_majorticklabels(), rotation=90 )
plt.tight_layout()
##########################################################################################################################################################
BC = TunnelExcavationData_df["BoreClass"]
TunnelExcavationData_df["BoreClass"].value_counts()
x = TunnelExcavationData_df["StationReal"]
y = [60]*len (BC) 

BC_points = {"BoreClass": BC, "x": x,"y":y}
BC_points_df = pd.DataFrame(BC_points)
BC_points_df.head()

BoreClass1 = BC_points_df[BC_points_df["BoreClass"] == 'BC1']
BoreClass2 = BC_points_df[BC_points_df["BoreClass"] == 'BC2']
BoreClass3 = BC_points_df[BC_points_df["BoreClass"] == 'BC3']

len(BoreClass1)
len(BoreClass2)
len(BoreClass3)

BoreClass1.plot(kind='scatter', x='x', y='y', s = 50, lw = 0, color='b',label='BC1',ax=axes[1])

axes[1].set_yticklabels([])
axes[1].set_xticklabels([])
axes[1].xaxis.label.set_visible(False)
axes[1].yaxis.label.set_visible(False)
plt.axis('off')

BoreClass2.plot(kind='scatter', x='x', y='y', s = 50, lw = 0, color='g',label='BC2',ax=axes[1])
BoreClass3.plot(kind='scatter', x='x', y='y', s = 50, lw = 0, color='r',label='BC2',ax=axes[1])

##########################################################################################################################################################

SC = TunnelExcavationData_df["SupportClass"]
TunnelExcavationData_df["SupportClass"].value_counts()

x = TunnelExcavationData_df["StationReal"]
y = [40]*len (SC)

SC_points = {"SupportClass": SC, "x": x,"y":y}
SC_points_df = pd.DataFrame(SC_points)
SC_points_df.head()

SupportClassT = SC_points_df[SC_points_df["SupportClass"] == 'SCT']
SupportClass5 = SC_points_df[SC_points_df["SupportClass"] == 'SC5']

len(SupportClassT)
len(SupportClass5)


SupportClassT.plot(kind='scatter', x='x', y='y', s = 50, lw = 0, color='k',label='SC1',ax=axes[1])
SupportClass5.plot(kind='scatter', x='x', y='y', s = 50, lw = 0, color='lightgrey',label='SC2',ax=axes[1])

##########################################################################################################################################################
DC = TunnelExcavationData_df["DisposalClass"]
TunnelExcavationData_df["DisposalClass"].value_counts()

x = TunnelExcavationData_df["StationReal"]
y = [20]*len (DC)

DC_points = {"DisposalClass": DC, "x": x,"y":y}
DC_points_df = pd.DataFrame(DC_points)
DC_points_df.head()

DisposalClass3 = DC_points_df[DC_points_df["DisposalClass"] == 'MC3']
DisposalClass5 = DC_points_df[DC_points_df["DisposalClass"] == 'MC5']
DisposalClass2 = DC_points_df[DC_points_df["DisposalClass"] == 'MC2']

len(DisposalClass3)
len(DisposalClass5)
len(DisposalClass2)

DisposalClass3.plot(kind='scatter', x='x', y='y', s = 50, lw = 0, color='c',label='MC3', ax=axes[1])
DisposalClass5.plot(kind='scatter', x='x', y='y', s = 50, lw = 0, color='m',label='MC5',ax=axes[1])
DisposalClass2.plot(kind='scatter', x='x', y='y', s = 50, lw = 0, color='y',label='MC2',ax=axes[1])

smb_bc1 = Line2D([0], [0], linestyle="none", marker="o", alpha=1,  markersize = 10, markeredgewidth = 0,  markerfacecolor="b") 
smb_bc2 = Line2D([0], [0], linestyle="none", marker="o", alpha=1,  markersize = 10, markeredgewidth = 0,  markerfacecolor="g") 
smb_bc3 = Line2D([0], [0], linestyle="none", marker="o", alpha=1,   markersize = 10, markeredgewidth = 0,  markerfacecolor="r") 

smb_sc1 = Line2D([0], [0], linestyle="none", marker="o", alpha=1,  markersize = 10, markeredgewidth = 0,  markerfacecolor="k") 
smb_sc2 = Line2D([0], [0], linestyle="none", marker="o", alpha=1,  markersize = 10, markeredgewidth = 0,  markerfacecolor="lightgrey") 


smb_mc3 = Line2D([0], [0], linestyle="none", marker="o", alpha=1,markersize = 10, markeredgewidth = 0,  markerfacecolor="c") 
smb_mc5 = Line2D([0], [0], linestyle="none", marker="o", alpha=1, markersize = 10, markeredgewidth = 0,  markerfacecolor="m") 
smb_mc2 = Line2D([0], [0], linestyle="none", marker="o", alpha=1, markersize = 10, markeredgewidth = 0,  markerfacecolor="y") 

first_legend = plt.legend((smb_bc1, smb_bc2, smb_bc3),( "BC1", "BC2", "BC3"), numpoints=1,loc="upper left")

ax = plt.gca().add_artist(first_legend)

second_legend = plt.legend((smb_sc1, smb_sc2),("SC1", "SC2"), numpoints=1,loc="center left")
ax = plt.gca().add_artist(second_legend)


plt.legend((smb_mc3, smb_mc5, smb_mc2),("MC1","MC2","MC2"), numpoints=1,loc=3)
plt.show()

