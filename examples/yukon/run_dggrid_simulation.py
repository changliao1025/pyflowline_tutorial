import os
import json
import shutil
from pathlib import Path
from os.path import realpath
import importlib.util
from shutil import copy2
from datetime import date
#import geopandas as gpd
import matplotlib.pyplot as plt
import logging

#%% setup logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time pyflowline simulation started.')

#%% Set the path to dggrid
sPath_dggrid_bin = "/qfs/people/liao313/bin/"
os.environ["PATH"] += os.pathsep + sPath_dggrid_bin

#%% Set workspace paths
sPath_parent = Path(__file__).resolve().parents[2]
print(f"Parent path: {sPath_parent}")

sWorkspace_data = os.path.join( sPath_parent, 'data', 'yukon')
if not os.path.exists(sWorkspace_data):
    print(sWorkspace_data)
    os.makedirs(sWorkspace_data)

sWorkspace_input = os.path.join( sWorkspace_data, 'input')
if not os.path.exists(sWorkspace_input):
    print(sWorkspace_input)
    os.makedirs(sWorkspace_input)

sWorkspace_output = os.path.join( sWorkspace_data, 'output')
if not os.path.exists(sWorkspace_output):
    print(sWorkspace_output)
    os.makedirs(sWorkspace_output)

#%% Setup temporary workspace for data
sPath_temp = os.path.join( sPath_parent, 'data', 'tmp' )
if not os.path.exists(sPath_temp):
    print(sPath_temp)
    os.makedirs(sPath_temp)
else:
    shutil.rmtree(sPath_temp)

# Specify the repository's URL
hexwatershed_data_repo = 'https://github.com/changliao1025/hexwatershed_data.git'

# Clone the repository
os.system(f'git clone {hexwatershed_data_repo} {sPath_temp}')
sPath_temp_data = os.path.join(sPath_parent, 'data', 'tmp', 'data', 'yukon', 'input')

# Check if the destination directory exists, if exists, remove it
if os.path.exists(sWorkspace_input):
    shutil.rmtree(sWorkspace_input)

# Copy all the files under the temp data folder using shutil
shutil.copytree(sPath_temp_data, sWorkspace_input)

shutil.rmtree(sPath_temp)

sFilename_configuration_in = os.path.join(sWorkspace_input, 'pyhexwatershed_yukon_dggrid.json')
sFilename_basins_in = os.path.join(sWorkspace_input, 'pyflowline_yukon_basins.json')
if os.path.isfile(sFilename_configuration_in):
    pass
else:
    print('The domain configuration file does not exist: ', sFilename_configuration_in)

print('Finished the data preparation step.')

#%% Define the case parameters
sRegion = 'yukon'
sMesh_type = 'dggrid'
sDggrid_type = 'ISEA3H'
iCase_index = 1
iResolution_index = 10 # dggrid resolution index

# Get today's year, month and day.
today = date.today()
iYear = today.year
iMonth = today.month
iDay = today.day
print("Today's date:", iYear, iMonth, iDay)
sDate = str(iYear) + str(iMonth).zfill(2) + str(iDay).zfill(2)

#%% Set the dggrid mesh resolution
from pyflowline.mesh.dggrid.create_dggrid_mesh import dggrid_find_resolution_by_index
dResolution = dggrid_find_resolution_by_index(sDggrid_type, iResolution_index)
print('Mesh resolution is: ', dResolution, 'm')

#%% Make copies of the configuration files
sFilename_configuration_copy = os.path.join(sWorkspace_output, 'pyflowline_configuration_copy.json')
copy2(sFilename_configuration_in, sFilename_configuration_copy)

# Also copy the basin configuration file to the output directory.
sFilename_basins_configuration_copy = os.path.join(sWorkspace_output, 'pyflowline_configuration_basins_copy.json')
copy2(sFilename_basins_in, sFilename_basins_configuration_copy)

#%% Change configuration parameters

# The json file will be overwritten, you may want to make a copy of it first.
sFilename_configuration = sFilename_configuration_copy
sFilename_basins = sFilename_basins_configuration_copy
from pyflowline.configuration.change_json_key_value import change_json_key_value

change_json_key_value(sFilename_configuration, 'sWorkspace_output', sWorkspace_output) # Output folder
change_json_key_value(sFilename_configuration, 'sFilename_basins', sFilename_basins) # Individual basin configuration file

# Set the domain boundary file, used to clip the mesh
sFilename_mesh_boundary = realpath(os.path.join(sWorkspace_input, 'boundary.geojson'))
change_json_key_value(sFilename_configuration, 'sFilename_mesh_boundary', sFilename_mesh_boundary)

#%% Read the configuration file
from pyflowline.configuration.read_configuration_file import pyflowline_read_configuration_file

oPyflowline = pyflowline_read_configuration_file(sFilename_configuration, iCase_index_in=iCase_index, sMesh_type_in=sMesh_type, iResolution_index_in=iResolution_index, sDate_in=sDate)

#%% Update some parameters

# Set the approximate outlet location
dLongitude_outlet_degree = -164.47594
dLatitude_outlet_degree = 63.04269
oPyflowline.aBasin[0].dThreshold_small_river = dResolution * 5

oPyflowline.pyflowline_change_model_parameter('dLongitude_outlet_degree', dLongitude_outlet_degree, iFlag_basin_in=1)
oPyflowline.pyflowline_change_model_parameter('dLatitude_outlet_degree', dLatitude_outlet_degree, iFlag_basin_in=1)

# Set the path to the user provided flowline
sFilename_flowline = realpath(os.path.join(sWorkspace_input, 'dggrid10/river_networks.geojson') )
oPyflowline.pyflowline_change_model_parameter('sFilename_flowline_filter', sFilename_flowline, iFlag_basin_in= 1)

# Turn debugging off
oPyflowline.pyflowline_change_model_parameter('iFlag_debug', 0, iFlag_basin_in=1)

# Set this flag false if the dggrid binary is on the system path, to let pyflowline find it. Set this flag true if the path to the binary file is set in the configuration file.
oPyflowline.iFlag_user_provided_binary = 0

#%% Setup the model

oPyflowline.pyflowline_setup()
oPyflowline.plot( sVariable_in = 'flowline_filter' )

#%% Flowline simplification
oPyflowline.pyflowline_flowline_simplification()
oPyflowline.plot( sVariable_in = 'flowline_simplified' )

#%% Mesh generation
oPyflowline.iFlag_mesh_boundary = 1
aCell = oPyflowline.pyflowline_mesh_generation()
oPyflowline.plot( sVariable_in = 'mesh')
oPyflowline.pyflowline_reconstruct_topological_relationship()

#%% Export the results
oPyflowline.pyflowline_export()
oPyflowline.plot( sVariable_in = 'flowline_conceptual')
oPyflowline.plot( sVariable_in = 'overlap')
oPyflowline.pyflowline_export_config_to_json()

# %%
print('Finished the simulation.')