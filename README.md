# Feature Tracking Cookbook

<img src="thumbnails/readmethumb.png" alt="thumbnail" width="500"/>

[![nightly-build](https://github.com/ProjectPythia/feature-tracking-cookbook/actions/workflows/nightly-build.yaml/badge.svg)](https://github.com/ProjectPythia/feature-tracking-cookbook/actions/workflows/nightly-build.yaml)
[![Binder](https://binder.projectpythia.org/badge_logo.svg)](https://binder.projectpythia.org/v2/gh/ProjectPythia/feature-tracking-cookbook/main?labpath=notebooks)
[![DOI](https://zenodo.org/badge/1270409068.svg)](https://zenodo.org/badge/latestdoi/1270409068)

_See the [Cookbook Contributor's Guide](https://projectpythia.org/cookbook-guide) for step-by-step instructions on how to create your new Cookbook and get it hosted on the [Pythia Cookbook Gallery](https://cookbooks.projectpythia.org)!_

This Project Pythia Cookbook covers how to identify and track meteorological features across space and time using **three methods**: `Matplotlib, SciPy, and Scikit.`


## Motivation

Atmospheric phenomena of interest are almost always dynamically evolving and rapidly changing. Examples include `thunderstorm complexes, tropical/extratropical cyclones, or precipitation shields.` **Students or researchers** studying these features must first be able to **identify and track** them through concurrent time steps before any further analysis.  

Listed below is the workflow for identifying and **tracking 2D geophysical features** in gridded data.

More specifically, it is aimed at users who have fields such as *sea-level pressure, precipitation, CWV, temperature, vorticity, or reflectivity*, and want to:

 - **Identify** spatial objects from a thresholded field
 - **Compare** different object-identification methods
 - **Extract** simple object properties such as area, centroid, and mask
 - **Track** those objects through time using frame-to-frame overlap


## Authors

Matthew Lynne, Brian Rose, Sarah Ravellette, Snigdha Samantaray, Jacob Vile, Christine Deng, Reda Algendy 

### Contributors

<a href="https://github.com/ProjectPythia/feature-tracking-cookbook/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ProjectPythia/feature-tracking-cookbook" />
</a>

## Structure

This cookbook is broken up into six main sections: *Preamble, Foundations, Precipitation Tracking, Sea Level Pressure Tracking, Combined Tracking, and Appendix.*

### Section 1 Preamble

How to cite the cookbook.

### Section 2 Foundations

 - Foundational material about Matplotlib, SciPy, and Scikit.
 - Where to apply these tools.

### Section 3 Precipitation Tracking

How to track precipitation over time.

### Section 4 Sea Level Pressure Tracking

How to track sea level pressure over time.

### Section 5 Combined Tracking

How to track sea level pressure *and* precipitation over time.

### Section 6 Appendix

Exploring data sources for ERA5.

## Running the Notebooks

You can either run the notebooks in the Cookbook using [Binder](https://binder.projectpythia.org/) or on your local machine.

### Running on Binder

The simplest way to interact with a Jupyter Notebook is through
[Binder](https://binder.projectpythia.org/), which enables "one click"
execution in the cloud. Simply navigate your mouse to
the top right corner of the book chapter you are viewing and click
on the rocket ship icon (see screenshots [here](https://foundations.projectpythia.org/preamble/how-to-use/#running-pythia-foundations-examples)),
and a text box will appear. Type or paste the Pythia Binder link
(`https://binder.projectpythia.org`) and click "Launch".
After a few moments you should be presented with a
notebook that you can interact with. You’ll be able to execute code
and even change the example programs. At first the code cells
have no output, until you execute them by pressing
{kbd}`Shift`\+{kbd}`Enter`. Complete details on how to interact with
a live Jupyter notebook are described in the Pythia Foundations chapter [Getting Started with
Jupyter](https://foundations.projectpythia.org/foundations/getting-started-jupyter).

Note, not all Cookbook chapters are executable. If you do not see
the rocket ship icon, such as on this page, you are not viewing an
executable book chapter.


### Running on Your Own Machine

If you are interested in running this material locally on your computer, you will need to follow this workflow:

(Replace "cookbook-example" with the title of your cookbooks)

1. Clone the `https://github.com/ProjectPythia/cookbook-example` repository:

   ```bash
    git clone https://github.com/ProjectPythia/cookbook-example.git
   ```

1. Move into the `cookbook-example` directory
   ```bash
   cd cookbook-example
   ```
1. Create and activate your conda environment from the `environment.yml` file
   ```bash
   conda env create -f environment.yml
   conda activate cookbook-example
   ```
1. Move into the `notebooks` directory and start up Jupyterlab
   ```bash
   cd notebooks/
   jupyter lab
   ```
