#! /usr/bin/env python
##########################################################################################
#Program to identify precipitation regions associated with an ETC
##########################################################################################
import sys
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import numpy.ma as ma
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import math 
from scipy.ndimage.filters import minimum_filter
from scipy.ndimage import label, generate_binary_structure
import time
from joblib import Parallel, delayed
from numba import njit
from datetime import datetime, timedelta
from matplotlib.axes import Axes
from matplotlib.path import Path
from cartopy.mpl.geoaxes import GeoAxes
GeoAxes._pcolormesh_patched = Axes.pcolormesh	

def crosses_dateline(labeled_arr):
	#Shift 180 degrees
	shifted_arr = np.roll(labeled_arr, 180*4, axis = 1)

	#Examine a 3x3 region centered at the dateline
	for lat in range(0, len(shifted_arr) - 1):
		sample_arr = shifted_arr[lat:lat+2, 719:721]
		#print('Sample arr', sample_arr)

		top_left = sample_arr[0, 0]
		top_right = sample_arr[0, 1]
		bottom_right = sample_arr[1, 1]
		bottom_left = sample_arr[1, 0]
		
		#Compare top left with position next to it
		if(top_left != 0 and top_right != 0):
			if(top_left != top_right):
				num_to_change = top_left
				shifted_arr = np.where(shifted_arr != num_to_change, shifted_arr, top_right)
				sample_arr = shifted_arr[lat:lat+2, 719:721]
				#print('Changed arr', sample_arr)

		#Compare top left with position diagonal to it
		if(top_left != 0 and bottom_right != 0):
			if(top_left != bottom_right):
				num_to_change = top_left
				shifted_arr = np.where(shifted_arr != num_to_change, shifted_arr, bottom_right)
				sample_arr = shifted_arr[lat:lat+2, 719:721]
				#print('Changed arr', sample_arr)
		
		#Compate bottom left with position next to it
		if(bottom_left != 0 and bottom_right != 0):
			if(bottom_left != bottom_right):
				num_to_change = bottom_left
				shifted_arr = np.where(shifted_arr != num_to_change, shifted_arr, bottom_right)
				sample_arr = shifted_arr[lat:lat+2, 719:721]
				#print('Changed arr bot left, bot right', sample_arr)
		
		#Compare bottom left with position diagonal to it
		if(bottom_left != 0 and top_right != 0):
			if(bottom_left != top_right):
				num_to_change = bottom_left
				shifted_arr = np.where(shifted_arr != num_to_change, shifted_arr, top_right)
				sample_arr = shifted_arr[lat:lat+2, 719:721]
				#print('Changed arr bot left, top right', sample_arr)

	#return np.roll(shifted_arr, 180, axis = 1)
	return shifted_arr

##################################
#Read in all files
##################################
print('Opening files')
char = 'tp'
full_char = 'total_precipitation'
#df = pd.read_csv('/project/wcp/mlynne/Project2_historical_precip/files/ETC_data/mc_tracks_clean_0150_to_0424', dtype = 'float', usecols = [0,1,2,3,4,5,8,12,13,14,15,17], header = 0)
#vf = open('/project/wcp/mlynne/Project2_historical_precip/files/ETC_data/mc_clean_verts_01.txt', 'r')
#vfs = vf.readlines()

#start_years = [2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022]
#end_years = [2005, 2007, 2009, 2011, 2013, 2015, 2017, 2019, 2021, 2023]
#start_years = [2004]
#end_years = [2005]

#start_years = np.arange(2004, 2024, 2)
#start_years = np.arange(1996, 20, 2)
#end_years = np.arange(2005, 2025, 2)
#end_years = np.arange(1951, 2005, 2)

start_date = datetime(2000, 2, 29, 0)
end_date = datetime(2022, 4, 30, 23)

dates = pd.date_range(start = start_date, end = end_date, freq = 'D')
dates = dates[np.logical_or(dates.month < 5, dates.month > 9)]
dates = dates[~np.logical_and(dates.month == 2, dates.day == 29)]

#ETC_occ = xr.open_dataset('../../../Project2_historical_precip/files/ETC_netCDF/' + ETC_start + '-' + ETC_end + '_Occurrence.nc')

#nc_start = '2000'
#nc_end = '2009'
#p_netCDF = xr.open_dataset('/aspen1/era5/hourly/surface/' + char + '_era5_' + nc_start + '-' + nc_end + '.nc')

for date in dates:
	print(date)
	###############################################
	#Initialize the grid to add precip data 
	###############################################
	#start_date = datetime(start_year, 10, 1, 0, 0, 0)
	#end_date = datetime(end_year + 1, 4, 30, 23, 0, 0)
	#end_date = datetime(start_year, 10, 15, 0, 0, 0)
	#print('Opening')
	p_netCDF = xr.open_dataset('/ama3/adai/wrf-conus404/CTL/hourly/wrf2d_d01_15vars_' + str(date.year) + '-' + str(f"{date.month:02}") + '-' + str(f"{date.day:02}") + '.nc')
	
	xlat = p_netCDF['XLAT'].values
	xlon = p_netCDF['XLONG'].values


	#ETC_occ = xr.open_dataset('../../../Project2_historical_precip/files/ETC_netCDF/' + str(start_year) + '-' + str(end_year) + '_Occurrence.nc')
	ETC_occ = xr.open_dataset('/ama3/adai/wrf-conus404/CTL/hourly/ETC_freq_namer_' + str(date.year) + '-' + str(f"{date.month:02}") + '-' + str(f"{date.day:02}") + '.nc')
	#print('Done opening')
	#times = pd.date_range(start = start_date, end = end_date, freq = 'H')
	#times = times[np.logical_or(times.month < 5, times.month > 9)]
	#print(times)
	#lats = np.arange(80, 21.75, -0.25)
	#lons = np.arange(0, 360, 0.25)

	#df = df[(df['Year'] != 1950) | (df['Month'] >= 10)] #Exclude everything prior to 1950-10-01
 
	grid = np.zeros((24, 1015, 1367), dtype = 'float32')
	tmp_grid = np.zeros((24, 1015, 1367), dtype = 'float32')
	###############################################
	#Now loop through each time step
	###############################################
	date_index = 0
	for h in pd.date_range(start = datetime(date.year, date.month, date.day, 0), end = datetime(date.year, date.month, date.day, 23), freq = 'h'):
		#if(date.year == start_year + 2 and date.month == 1 and date.day == 1 and date.hour == 0 and date.year != start_years[-1] + 2):
		#if(date.year == start_year + 2 and date.month == 1 and date.day == 1 and date.hour == 0):
		#	p_netCDF.close()
		#	p_netCDF = xr.open_dataset('/aspen1/era5/hourly/surface/' + char + '_era5_' + str(start_year + 2) + '-' + str(end_year + 2) + '.nc')
		#elif(date.year == start_year + 2 and date.month == 1 and date.day == 1 and date.hour == 0 and date.year == start_years[-1] + 2):
		#	p_netCDF.close()
		#	p_netCDF = xr.open_dataset('/aspen1/era5/hourly/surface/' + char + '_era5_' + str(start_year + 2) + '-' + str(start_year + 2) + '.nc')
		#if(date.hour == 0):
		#print(date)	
		
		ETC_field = ETC_occ["ETC_freq"].sel(Time = datetime(date.year, date.month, date.day, h.hour, 0, 0))
	
		precip_field = p_netCDF["PREC_ACC_NC"].sel(Time = datetime(date.year, date.month, date.day, h.hour))
		precip_field = precip_field.where(precip_field > 0.25, 0)
		precip_field = precip_field.where(precip_field.notnull(), 0)

		#First thing to do is set the grid equal to the precip field at the same time. 
		#The precip field will be trimmed down later.
		tmp_grid[date_index] = precip_field
		#tmp_grid[date_index] = np.roll(tmp_grid[date_index], 180*4, axis = 1)
	
		#print('Labeling precip objects')
		s = generate_binary_structure(2,2)
		labeled_pfield, num_features = label(precip_field, structure = s)
		#print(labeled_pfield)
		
		#Correct the labeled field for objects that cross the dateline
		#corrected_labeled_pfield = crosses_dateline(labeled_pfield)
		corrected_labeled_pfield = labeled_pfield
		#plt.pcolormesh(precip_field["longitude"][:], precip_field["latitude"][36:39], corrected_labeled_pfield[36:39, :])
		#plt.colorbar()
		#plt.show()
	
		#############################################################
		#Loop thruogh each precip label and get its coordinates
		#############################################################
		ETC_vals = ETC_field
		#arr_lats = ((80 - lats) * 4).astype(int)
		#arr_lons = (lons * 4).astype(int)

		#precip_vals = corrected_labeled_pfield[arr_lats[:, None], arr_lons]
		precip_vals = corrected_labeled_pfield
		mask = (np.flipud(ETC_vals.values) > 0) & (precip_vals > 0)
		
		masked_lbl_pfield = corrected_labeled_pfield[mask]
		#print(masked_lbl_pfield)
		final_labels = np.unique(masked_lbl_pfield)
		#print(final_labels)
		final_mask = np.isin(corrected_labeled_pfield, final_labels)
		
		final_pfield = tmp_grid[date_index]
		final_pfield[~final_mask] = 0
		
		#final_pfield = final_pfield * 1000000
		
		#pfield_to_save = final_pfield.astype('int16')
		#grid[date_index] = pfield_to_save
		grid[date_index] = np.flipud(final_pfield)
		#print(grid[date_index].dtype)
		date_index = date_index + 1

	times_to_save = pd.date_range(start = datetime(date.year, date.month, date.day, 0), end = datetime(date.year, date.month, date.day, 23), freq = 'h')

	#grid = grid * 1000
	data_min = float(np.min(grid))
	data_max = float(np.max(grid))

	scale_factor = (data_max - data_min) / (2**16 - 1)
	add_offset = data_min + scale_factor * ((2**16 - 1) / 2)
	#grid = grid.astype('float32')
	
	final_ds = xr.Dataset(data_vars = {
		'ETC_' + char: (
			['Time', 'south_north', 'west_east'],
			grid,
			{
				'units': 'None',
				'long_name':'ETC_' + char,
				'cell_methods':'Time: mean'
			}
		)
	},
	coords={
		'Time': times_to_save,
		'lat': (
			['south_north', 'west_east'],
			np.flipud(xlat).astype(float),
			{
				'long_name': 'latitude',
				'standard_name': 'latitude',
				'units': 'degrees_north'
			}
		),
		'lon': (
			['south_north', 'west_east'],
			np.flipud(xlon).astype(float),
			{
				'long_name': 'longitude',
				'standard_name': 'longitude',
				'units': 'degrees_east'
			}
		)
	})

	encoding = {
		'ETC_' + char: {
			'dtype': 'int16',
			'scale_factor': scale_factor,
			'add_offset': add_offset,
			'_FillValue': -9999,
			}
	}

	

	'''
	final_ds=xr.Dataset({'ETC_' + char:(['time','lat','lon'],grid,
				{'units':'mm of LWE h^-1',
				'long_name':'ETC_Associated_' + full_char,
				#'add_offset':add_offset,
				#'scale_factor':scale_factor,
				#'_FillValue':-9999,
				'cell_methods':'time: mean'
				})
			},
			coords = {
				'time':('time',times),
				'lat':('lat',lats.astype(float),
					{'long_name':"Latitudes, y-coordinate in Cartesian system",
					'standard_name':"latitude",
					'units':"degrees_north"}),
				'lon':('lon',lons.astype(float),
					{'long_name':"Longitudes, x-coordinate in Cartesian system",
					'standard_name':"longitude",
					'units':"degrees_east"})
				}
			)
	encoding = {
		'ETC_' + char: {
			'dtype': 'int16',
			#'zlib': True,
			'scale_factor': scale_factor,
			'add_offset': add_offset,
			'_FillValue': -9999,
			}
		}
	'''     
	#print(final_ds)
	#final_ds = final_ds * 1000000
	#final_ds = final_ds.round(0)
	#final_final_ds = final_ds.astype('int16')
	#print('Saving')
	final_ds.to_netcdf('/ama3/adai/wrf-conus404/CTL/hourly/ETC_precip_namer_' + str(date.year) + '-' + str(f"{date.month:02}") + '-' + str(f"{date.day:02}") + '.nc', encoding = encoding, format = 'NETCDF4')
	#print('Done saving')
	ETC_occ.close()
	p_netCDF.close()
'''
#Weight the DataArray
weights = np.cos(np.deg2rad(genesis_da.latitude))
'''
