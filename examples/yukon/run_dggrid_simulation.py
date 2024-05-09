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
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time pyflowline simulation started.')


os.environ["PATH"] += os.pathsep + "/qfs/people/liao313/bin/"
from pyflowline.configuration.change_json_key_value import change_json_key_value
from pyflowline.configuration.read_configuration_file import pyflowline_read_configuration_file

sPath_parent = Path().resolve()

print(sPath_parent)

sWorkspace_data = os.path.join( sPath_parent, 'data', 'yukon' )
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

sFilename_configuration_in = os.path.join(sWorkspace_input , 'pyhexwatershed_yukon_dggrid.json')
sFilename_basins_in = os.path.join( sWorkspace_input , 'pyflowline_yukon_basins.json')
if os.path.isfile(sFilename_configuration_in):
    pass
else:
    print('The domain configuration file does not exist: ', sFilename_configuration_in)

print('Finished the data preparation step.')


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


from pyflowline.mesh.dggrid.create_dggrid_mesh import dggrid_find_resolution_by_index
dResolution = dggrid_find_resolution_by_index(sDggrid_type,
                                              iResolution_index)
print('Mesh resolution is: ', dResolution, 'm')

sFilename_configuration_copy = os.path.join(
    sWorkspace_output, 'pyflowline_configuration_copy.json')
copy2(sFilename_configuration_in, sFilename_configuration_copy)

# Also copy the basin configuration file to the output directory.
sFilename_basins_configuration_copy = os.path.join(
    sWorkspace_output, 'pyflowline_configuration_basins_copy.json')
copy2(sFilename_basins_in, sFilename_basins_configuration_copy)


# The json file will be overwritten, you may want to make a copy of it first.
sFilename_configuration = sFilename_configuration_copy
sFilename_basins = sFilename_basins_configuration_copy
# Output folder
change_json_key_value(sFilename_configuration,
                                 'sWorkspace_output', sWorkspace_output)
# Individual basin configuration file
change_json_key_value(sFilename_configuration,
                                 'sFilename_basins', sFilename_basins)

# Boundary to clip mesh
sFilename_mesh_boundary = realpath(os.path.join(
    sWorkspace_input, 'boundary.geojson'))
change_json_key_value(sFilename_configuration,
                                 'sFilename_mesh_boundary', sFilename_mesh_boundary)


# User provided flowline
oPyflowline = pyflowline_read_configuration_file(sFilename_configuration,
                                                 iCase_index_in=iCase_index,
                                                 sMesh_type_in=sMesh_type,
                                                 iResolution_index_in=iResolution_index,
                                                 sDate_in=sDate)

dLongitude_outlet_degree = -164.47594
dLatitude_outlet_degree = 63.04269
oPyflowline.aBasin[0].dThreshold_small_river = dResolution * 5

oPyflowline.pyflowline_change_model_parameter('dLongitude_outlet_degree',
                                              dLongitude_outlet_degree,
                                              iFlag_basin_in=1)

oPyflowline.pyflowline_change_model_parameter('dLatitude_outlet_degree',
                                              dLatitude_outlet_degree,
                                              iFlag_basin_in=1)
sFilename_flowline = realpath(os.path.join(sWorkspace_input, 'dggrid10/river_networks.geojson') )
oPyflowline.pyflowline_change_model_parameter('sFilename_flowline_filter', sFilename_flowline, iFlag_basin_in= 1)
oPyflowline.pyflowline_change_model_parameter('iFlag_debug', 0, iFlag_basin_in= 1)

#setup the model
oPyflowline.iFlag_user_provided_binary = 0
oPyflowline.pyflowline_setup()
#oPyflowline.plot( sVariable_in = 'flowline_filter' )
oPyflowline.pyflowline_flowline_simplification()
#oPyflowline.plot( sVariable_in = 'flowline_simplified' )
oPyflowline.iFlag_mesh_boundary = 1
aCell = oPyflowline.pyflowline_mesh_generation()
#oPyflowline.plot( sVariable_in = 'mesh')
oPyflowline.pyflowline_reconstruct_topological_relationship()
oPyflowline.pyflowline_export()
#oPyflowline.plot( sVariable_in = 'flowline_conceptual')
oPyflowline.plot( sVariable_in = 'overlap')
oPyflowline.pyflowline_export_config_to_json()
print('Finished the simulation.')
