[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/changliao1025/pyflowline_tutorial/HEAD) (right click to open in a new window)

# Introduction

This is a short course for the PyFlowline model.

PyFlowline: a mesh independent river network generator for hydrologic models.

For full details of the model, please refer to our [papers](#references) and the PyFlowline [documentation](https://pyflowline.readthedocs.io/).

Note that PyFlowline works hand in hand with Hexwatershed. Users interested in the full end-to-end watershed processing workflow enabled by Hexwatershed may wish to visit the [hexwatershed_tutorial](https://github.com/changliao1025/hexwatershed_tutorial).

# Getting Started

If you're just getting started, here's what we recommend:

- Right click on the `launch|binder` link at the top of this page.
- Open the link in a new window or tab.
- Grab a coffee while the Binder environment starts up.
- Run the interactive notebook from within the Binder environment.
  - `notebooks/yukon/dggrid_example.ipynb`.
- If the Binder environment fails to load, please open the notebook in your local Jupyter notebook environment.
  - To run the notebook locally, refer to the [requirements](#requirements).
  - Otherwise, read the notebook at your liesure to learn about PyFlowline.

_**Please note**_: This repository is specifically designed to host the interactive Binder notebook linked at the top of this page. Binder provides a self-contained environment with all software dependencies installed. Once loaded, use the Binder environment to run the `dggrid_example.ipynb` Jupyter notebook. This interactive tutorial demonstrates how to use the Pyflowline software to generate flow networks on a dggrid (Discrete Global Grid) system mesh for hydrologic modeling, with no coding or software installation required.

To run the example notebooks locally, familiarity with the Python coding ecosystem is required. Please read the instructions below.

# Requirements

You need an internet connection to install the Pyflowline package and its dependencies using Python Pip or Conda. We recommended Conda.

You can use Visual Studio Code to run the Python examples.

You can use QGIS to visualize some of the model results.

# Step-by-step instruction

- Download this tutorial.

   ```bash
   git clone https://github.com/changliao1025/pyflowline_tutorial.git
   cd pyflowline_tutorial
   ```

- Create a conda environment named `pyflowline_tutorial`, and install the `pyflowline` package.

   ```bash
   # Recommended: use the provided environment.yml file:
   conda env create -f environment.yml
   conda activate pyflowline_tutorial

   # By hand:
   conda create --name pyflowline_tutorial -c conda-forge python pyflowline
   conda activate pyflowline_tutorial
   conda install -c conda-forge jupyterlab cmake make numpy gdal netCDF4 mscorefonts matplotlib cartopy geopandas libgdal-arrow-parquet python-dotenv pyearth
   ```

- Optional: copy the `.env.example` file to `.env` and update it with paths specific to your local environment.

   ```bash
   cp .env.example .env
   ```

- Run the examples within the `example` folder.
  - Edit the template `configuration` json files to match with your data set paths.
  - Trial and error may be required.

- View and visualize model output files.
  - View normal json files using any text editor such as VS Code.
  - Visualize `geojson` files using `QGIS`.

# Building dggrid

To run the tutorial locally you need to install [dggrid](https://github.com/sahrk/DGGRID). To install dggrid, follow the instructions [here](https://github.com/sahrk/DGGRID/blob/master/INSTALL.md).

When building dggrid, it will be linked to gdal. If dggrid is installed while the `pyflowline_tutorial` conda environment is activated, then (unless configured otherwise) cmake will find and link dggrid against the gdal version installed into this environment by conda. If the `pyflowline_tutorial` environment is later removed, or for any reason gdal is uninstalled from this environment, dggrid will break. So we recommend to deactivate the `pyflowline_tutorial` environment and link dggrid against a stable gdal installation on your local machine. This could be a gdal installed with `brew`, or `pipx`, or in a general purpose environment managed by `pyenv-virtualenv` or `conda`. Depending on your choice, this will also ensure dggrid is available for use outside of this tutorial. To run the examples, reactivate your `pyflowline_tutorial` environment.

# Advanced use

Users who plan to use the software in their own work may wish to create a conda environment named `pyflowline` (rather than `pyflowline_tutorial`). Better yet, since `pyflowline` users will almost certainly also use [hexwatershed](https://github.com/changliao1025/pyhexwatershed), users may wish to create a single conda environment named `hexwatershed` using the `environment.yml` file over at the [hexwatershed_tutorial](https://github.com/changliao1025/hexwatershed_tutorial), which contains all of the dependencies required by `pyflowline` plus the `hexwatershed` ones. This `hexwatershed` environment can then be used for both `pyflowline` and `hexwatershed` related workflows.

# FAQ

1. Why did `import GDAL` fail?

   - Consider using the `conda-forge` channel to install `GDAL`.
   - Ensure the `GDAL` bindings installed with conda are properly linked against the gdal library installed on your local machine. See the instructions [here](https://pypi.org/project/GDAL/).

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

- Liao, Chang, Zhou, T., Xu, D., Cooper, M. G., Engwirda, D., Li, H.-Y., Leung, L. R. (2023). Topological relationship-based flow direction modeling: Mesh-independent river networks representation. Journal of Advances in Modeling Earth Systems, 15, e2022MS003089. https://doi.org/10.1029/2022MS003089

- Liao and Cooper, (2023). pyflowline: a mesh-independent river network generator for hydrologic models. Journal of Open Source Software, 8(91), 5446, https://doi.org/10.21105/joss.05446

- Liao. C. (2022). Pyflowline: a mesh independent river network generator for hydrologic models. Zenodo. https://doi.org/10.5281/zenodo.6407299
