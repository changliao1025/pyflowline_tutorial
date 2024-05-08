[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/changliao1025/pyflowline_tutorial/HEAD) (right click to open in a new window)

# Introduction

This is a short course for the PyFlowline model.

PyFlowline: a mesh independent river network generator for hydrologic models.

For full details of the model, please refer to our papers and the PyFlowline [documentation](https://pyflowline.readthedocs.io/).

# Requirements

You need an internet connection to install the package using Python Pip or Conda (recommended).

You can use Visual Studio Code to run the Python examples.

You can use QGIS to visualize some of the model results.

# Step-by-step instruction

1. Create a conda environment named `pyflowline`, and install the `pyflowline` package.

  ```bash
  conda create --name pyflowline -c conda-forge python pyflowline
  conda activate pyflowline
  conda install -c conda-forge numpy gdal matplotlib cartopy geopandas netCDF4
  ```

2. Download this tutorial.

   ```bash
   git clone https://github.com/changliao1025/pyflowline_tutorial.git
   ```

3. Run the examples within the `example` folder.

   - Edit the template `configuration` json file to match with your data set paths.
   - View and visualize model output files.
   - View normal json file using any text editor such as VS Code.
   - Visualize `geojson` files using `QGIS`.

# FAQ

1. Why import `GDAL` failed?

   Consider using the `conda-forge` channel.

2. `proj` related issue https://github.com/OSGeo/gdal/issues/1546

   Make sure you correctly set up the `PROJ_LIB`

   Because the `GDAL` library is used by this project and the `proj` library is often not configured correctly automatically.
   On Linux or Mac, you can set it up using the `.bash_profile` such as:

   Anaconda:

   `export PROJ_LIB=/people/user/.conda/envs/pyflowline/share/proj`

   Miniconda:

   `export PROJ_LIB=/opt/miniconda3/envs/pyflowline/share/proj`

3. What if my model doesn't produce the correct or expected answer?

   Answer: There are several hidden assumptions within the workflow. For example, if you provide the DEM and river network for two different regions, the program won't be able to tell you that. A visual inspection of your data is important.

   Optionally, you can turn on the `iFlag_debug` option in the configuration file to output the `intermediate files`.

# References

* Liao, Chang, Zhou, T., Xu, D., Cooper, M. G., Engwirda, D., Li, H.-Y., Leung, L. R. (2023). Topological relationship-based flow direction modeling: Mesh-independent river networks representation. Journal of Advances in Modeling Earth Systems, 15, e2022MS003089. https://doi.org/10.1029/2022MS003089

* Liao et al., (2023). pyflowline: a mesh-independent river network generator for hydrologic models. Journal of Open Source Software, 8(91), 5446, https://doi.org/10.21105/joss.05446

* Liao. C. (2022). Pyflowline: a mesh independent river network generator for hydrologic models. Zenodo. https://doi.org/10.5281/zenodo.6407299

