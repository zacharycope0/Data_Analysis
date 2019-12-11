"""
Zachary Cope
Visualizing ACS PUMS Data
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

#Read in data
pums_df = pd.read_csv('ss13hil.csv')

#Set_up fig and subplots
fig = plt.figure(figsize = (12,7))

ax1 = fig.add_subplot(2,2,1) 
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)
ax4 = fig.add_subplot(2,2,4)

#Create pie chart with number of counts for HHL values.
labels = [r'English only', r'Spanish', r'Other Indo-European', r'Asian and Pacific Island languages', r'Other']
colors = ['blue', 'orange', 'green', 'red', 'purple']
patches, texts = ax1.pie(pums_df['HHL'].value_counts(), radius = 1,  colors=colors, counterclock=True, startangle=242)
ax1.legend(patches, labels, loc='upper left', fontsize = 'small')
ax1.axis('equal')
ax1.set_title('Household Languages', fontsize = 'medium')
ax1.set_ylabel('HHL', fontsize = 'small')

#Create histogram of household income with KDE superimposed
hincp = pums_df['HINCP']
hincp.plot(kind='kde',color='k',ls='dashed', ax=ax2)

#log scale on the x-axis with log-spaced bins
logspace = np.logspace(1,7,num=100,base=10.0) 
ax2.hist(hincp,bins=logspace,facecolor='g',alpha=0.5,histtype='bar', normed=True, range = (hincp.min(),hincp.max()))
ax2.set_title('Distribution of Household Income',fontsize = 'medium')
ax2.set_xlabel('Household Income($)- Log Scaled',fontsize = 'small')
ax2.set_ylabel('Density',fontsize = 'small')
ax2.set_xscale("log")
ax2.set_axisbelow(True)

#Create histogram with number of vehicle availble per household on axis 3
ax3.hist(pums_df[pums_df.VEH.notnull()]['VEH'], 
    weights = (pums_df[pums_df.VEH.notnull()]['WGTP']/1000), 
    color = 'r', bins=np.linspace(-0.5,6.5,8), rwidth = 0.80)

#Adjust axis 3 labels and tick
ax3.tick_params(labelsize = 'small')    
ax3.set_xticks(range(7))
plt.sca(ax3)
plt.xlim(-0.4,6.4)
ax3.set_yticks(range(250,1751,250))
ax3.set_title('Vehicles Availible in Households', fontsize = 'medium')
ax3.set_xlabel('# of Vehicles', fontsize = 'small')
ax3.set_ylabel('Thousands of Households', fontsize = 'small')

#Set up dictionary to convert property taxes catagories to lower bound interval
conv_TAXP = {1: np.NaN,2: 1.0,3: 50.0,4: 100.0,5: 150.0,6: 200.0,7: 250.0,8: 
 300.0,9: 350.0,10: 400.0,11: 450.0,12: 500.0,13: 550.0,14: 600.0,15: 650.0,16: 
 700.0,17: 750.0,18: 800.0,19: 850.0, 20: 900.0,21: 950.0,22: 1000.0,23: 1100.0,
 24: 1200.0,25: 1300.0,26: 1400.0,27: 1500.0,28: 1600.0,29: 1700.0,30: 1800.0,
 31: 1900.0,32: 2000.0,33: 2100.0,34: 2200.0,35: 2300.0,36: 2400.0,37: 2500.0,
 38: 2600.0,39: 2700.0,40: 2800.0,41: 2900.0,42: 3000.0,43: 3100.0,44: 3200.0,
 45: 3300.0,46: 3400.0,47: 3500.0,48: 3600.0,49: 3700.0,50: 3800.0,51: 3900.0,
 52: 4000.0,53: 4100.0,54: 4200.0,55: 4300.0,56: 4400.0,57: 4500.0,58: 4600.0,
 59: 4700.0,60: 4800.0,61: 4900.0,62: 5000.0,63: 5500.0,64: 6000.0,65: 7000.0,
 66: 8000.0,67: 9000.0,68: 10000.0}

#Apply convertion to TAXP 
pums_df['TAXP'] = pums_df.TAXP.map(conv_TAXP)

#Select data from dataframe that don't have null values for the property taxe or
#proberty value catagories
slct_df = pums_df[pums_df.TAXP.notnull() & pums_df.VALP.notnull()][['TAXP',
    'VALP','WGTP','MRGP']]

#Create scatter plot comparing property value against propertytaxes. Marker 
#color value set two first monthly mortgage payment and mark size set to housing
#weight 
plt.sca(ax4)
cm = plt.cm.get_cmap('bwr')
sc = ax4.scatter(slct_df['VALP'], slct_df['TAXP'], s=slct_df['WGTP'], 
    c=slct_df['MRGP'], cmap=cm, marker='o',alpha=0.40, edgecolors = 'none')

#Create and adjust colorbar
cbar = plt.colorbar(sc, use_gridspec=True)
cbar.set_label('First Mortgage Payment (Monthly $)', fontsize = 'small')
cbar.ax.tick_params(labelsize = 'small')
cbar.set_ticks(range(1250,5001,1250))

#Adjust axis 4 labels and tick
ax4.tick_params(labelsize = 'small')    
ax4.set_xticks(range(0,1200001,200000))
plt.xlim(0,1200000)
ax4.set_yticks(range(0,10001,2000))
plt.ylim(0,10500)
ax4.set_title('Property Taxes vs. Property Values', fontsize = 'medium')
ax4.set_xlabel('Property Value ($)', fontsize = 'small')
ax4.set_ylabel('Taxes ($)', fontsize = 'small')

#Show and save figure
fig.tight_layout()
plt.subplots_adjust(hspace=0.4)
fig.show()
plt.savefig('pums.png')
