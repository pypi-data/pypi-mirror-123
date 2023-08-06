# Dataplay: The Data Handling Handbook and Python Library
> Our one stop shop to learn about data intake, processing, and visualization.


<img src="https://raw.githubusercontent.com/bniajfi/bniajfi/main/bnia_logo_new.png" height="160px" width="auto" style="max-width: autopx">

<h2 align="left"><img src="https://raw.githubusercontent.com/sidbelbase/sidbelbase/master/wave.gif" width="30px">Hi! We are <a href="https://bniajfi.org/">BNIA-JFI</a>.</h2>

This package was made to help with data handling

__Included__
- Functions built and used by BNIA for day to day tasks.
- Made to be shared via IPYNB/ Google Colab notebooks with in-built examples using 100% publicly accessible data & links.
- Online [documentation](https://bniajfi.org/dataplay/)  and [PyPi](https://pypi.org/project/dataplay/) libraries created from the notebooks.

[TOC](https://github.com/bniajfi)

[Dataplay](https://bniajfi.org/dataplay/) uses functions found in our [VitalSigns](https://bniajfi.org/VitalSigns/) Module and vice-versa.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/bnia/dataplay/main?filepath=%2Fnotebooks%2Findex.ipynb)
[![Binder](https://pete88b.github.io/fastpages/assets/badges/colab.svg)](https://colab.research.google.com/github/bnia/dataplay/blob/main/notebooks/index.ipynb)
[![Binder](https://pete88b.github.io/fastpages/assets/badges/github.svg)](https://github.com/bnia/dataplay/tree/main/notebooks/index.ipynb)
[![Open Source Love svg3](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

[![NPM License](https://img.shields.io/npm/l/all-contributors.svg?style=flat)](https://github.com/bnia/dataplay/blob/main/LICENSE)
[![Active](http://img.shields.io/badge/Status-Active-green.svg)](https://bnia.github.io) 
[![Python Versions](https://img.shields.io/pypi/pyversions/dataplay.svg)](https://pypi.python.org/pypi/dataplay/)
[![GitHub last commit](https://img.shields.io/github/last-commit/bnia/dataplay.svg?style=flat)]()  

[![GitHub stars](https://img.shields.io/github/stars/bnia/dataplay.svg?style=social&label=Star)](https://github.com/bnia/dataplay) 
[![GitHub watchers](https://img.shields.io/github/watchers/bnia/dataplay.svg?style=social&label=Watch)](https://github.com/bnia/dataplay) 
[![GitHub forks](https://img.shields.io/github/forks/bnia/dataplay.svg?style=social&label=Fork)](https://github.com/bnia/dataplay) 
[![GitHub followers](https://img.shields.io/github/followers/bnia.svg?style=social&label=Follow)](https://github.com/bnia/dataplay) 

[![Tweet](https://img.shields.io/twitter/url/https/github.com/bnia/dataplay.svg?style=social)](https://twitter.com/intent/tweet?text=Check%20out%20this%20%E2%9C%A8%20colab%20by%20@bniajfi%20https://github.com/bnia/dataplay%20%F0%9F%A4%97) 
[![Twitter Follow](https://img.shields.io/twitter/follow/bniajfi.svg?style=social)](https://twitter.com/bniajfi)

<h2 align="left">Create maps, networks graphs, and gifs!</h2>
<img src="https://bniajfi.org/images/mermaid/vitalSignsCorrelations.png" width="500px" style="max-width: 500pxpx">
<img src="https://bniajfi.org/images/mermaid/vitalSignsGif.gif" width="500px" style="max-width: 500pxpx">

## About this Tutorial: 

### Whats inside?

#### __The Tutorial__

You use can use these docs to learn from or as documentation when using the attached library.

#### __TIPS__
 
- Content covered in previous tutorials will be used in later tutorials. 

- __New code and or  information *should* have explanations and or descriptions__ attached. 

- Concepts or code covered in previous tutorials will be used without being explaining in entirety.

- __If content can not be found in the current tutorial and is not covered in previous tutorials, please let me know.__

- This notebook has been optimized for Google Colabs ran on a Chrome Browser. 

- Statements found in the index page on view expressed, responsibility, errors and ommissions, use at risk, and licensing  extend throughout the tutorial.

#### __Objectives__
 
By the end of this tutorial users should have an understanding of:
- Importing data with pandas and geopandas
- Querying data from Esri
- Retrieveing data programmatically
- This module assumes the data needs no handling prior to intake
- Loading data in a variety of formats
- Visualizing said data

## Usage Instructions

### Install the Package

The code is on <a href="https://pypi.org/project/test-template/">PyPI</a> so you can install the scripts as a python library using the command:

`!pip install dataplay geopandas`

{% include important.html content='Contributers should follow the maintanance instructions and will not need to run this step. ' %}>
> Their modules will be retrieved from the VitalSigns-GDrive repo they have mounted into their Colabs Enviornment. 

Then...

### Import Modules

1) Import the installed module into your code:
``` 
from VitalSigns.acsDownload import retrieve_acs_data 
```
2) use it
```
retrieve_acs_data(state, county, tract, tableId, year, saveAcs)
```
Now you could do something like merge it to another dataset! 
```
from dataplay.merge import mergeDatasets
mergeDatasets(left_ds=False, right_ds=False, crosswalk_ds=False,  use_crosswalk = True, left_col=False, right_col=False, crosswalk_left_col = False, crosswalk_right_col = False, merge_how=False, interactive=True)
```

### Getting Help

You can get information on the package, modules, and methods by using the help command.

Here we look at the package's modules:

```
import dataplay
help(dataplay)
```

    Help on package dataplay:
    
    NAME
        dataplay
    
    PACKAGE CONTENTS
        _nbdev
        corr
        geoms
        gifmap
        html
        intaker
        merge
    
    VERSION
        0.0.28
    
    FILE
        /usr/local/lib/python3.7/dist-packages/dataplay/__init__.py
    
    


Lets take a look at what functions the geoms module provides:

```
import dataplay.geoms
help(dataplay.geoms)
```

    /usr/local/lib/python3.7/dist-packages/psycopg2/__init__.py:144: UserWarning: The psycopg2 wheel package will be renamed from release 2.8; in order to keep installing from binary please use "pip install psycopg2-binary" instead. For details see: <http://initd.org/psycopg/docs/install.html#binary-install-from-pypi>.
      """)
    /usr/local/lib/python3.7/dist-packages/VitalSigns/acsDownload.py:27: FutureWarning: Passing a negative integer is deprecated in version 1.0 and will not be supported in future version. Instead, use None to not limit the column width.
      pd.set_option('display.max_colwidth', -1)


    Help on module dataplay.geoms in dataplay:
    
    NAME
        dataplay.geoms - # AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/03_Map_Basics_Intake_and_Operations.ipynb (unless otherwise specified).
    
    FUNCTIONS
        map_points(data, lat_col='POINT_Y', lon_col='POINT_X', zoom_start=11, plot_points=True, cluster_points=False, pt_radius=15, draw_heatmap=False, heat_map_weights_col=None, heat_map_weights_normalize=True, heat_map_radius=15, popup=False)
            Creates a map given a dataframe of points. Can also produce a heatmap overlay
            
            Arg:
                df: dataframe containing points to maps
                lat_col: Column containing latitude (string)
                lon_col: Column containing longitude (string)
                zoom_start: Integer representing the initial zoom of the map
                plot_points: Add points to map (boolean)
                pt_radius: Size of each point
                draw_heatmap: Add heatmap to map (boolean)
                heat_map_weights_col: Column containing heatmap weights
                heat_map_weights_normalize: Normalize heatmap weights (boolean)
                heat_map_radius: Size of heatmap point
            
            Returns:
                folium map object
        
        readInGeometryData(url=False, porg=False, geom=False, lat=False, lng=False, revgeocode=False, save=False, in_crs=4326, out_crs=False)
            # reverseGeoCode, readFile, getGeoParams, main
        
        workWithGeometryData(method=False, df=False, polys=False, ptsCoordCol=False, polygonsCoordCol=False, polyColorCol=False, polygonsLabel='polyOnPoint', pntsClr='red', polysClr='white', interactive=False)
            # Cell
            #
            # Work With Geometry Data
            # Description: geomSummary, getPointsInPolygons, getPolygonOnPoints, mapPointsInPolygons, getCentroids
    
    DATA
        __all__ = ['workWithGeometryData', 'map_points', 'readInGeometryData']
    
    FILE
        /usr/local/lib/python3.7/dist-packages/dataplay/geoms.py
    
    


And here we can look at an individual function and what it expects:

```
import VitalSigns.acsDownload
help(VitalSigns.acsDownload.retrieve_acs_data)
```

    Help on function retrieve_acs_data in module VitalSigns.acsDownload:
    
    retrieve_acs_data(state, county, tract, tableId, year, save)
    


## Examples

#### Examples

So heres an example:


Import your modules

```
%%capture 
import pandas as pd
from VitalSigns.acsDownload import retrieve_acs_data 
from dataplay.geoms import workWithGeometryData
from dataplay.geoms import map_points
from dataplay.intaker import Intake
```

Read in some data

Define our download parameters.

More information on these parameters can be found in the tutorials!

```
tract = '*'
county = '510'
state = '24'
tableId = 'B19001'
year = '17'
saveAcs = False
```

And download the Baltimore City ACS data using the imported VitalSigns library.

```
df = retrieve_acs_data(state, county, tract, tableId, year, saveAcs)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>B19001_001E_Total</th>
      <th>B19001_002E_Total_Less_than_$10,000</th>
      <th>B19001_003E_Total_$10,000_to_$14,999</th>
      <th>...</th>
      <th>state</th>
      <th>county</th>
      <th>tract</th>
    </tr>
    <tr>
      <th>NAME</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Census Tract 2710.02</th>
      <td>1510</td>
      <td>209</td>
      <td>73</td>
      <td>...</td>
      <td>24</td>
      <td>510</td>
      <td>271002</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 20 columns</p>
</div>



Here we can import and display a geospatial dataset with special intake requirements.

Here we pull a list of Baltimore Cities CSA's

```
help(csa_gdf.plot)
```

Now in this example we will load in a bunch of coorinates

```
geoloom_gdf_url = "https://services1.arcgis.com/mVFRs7NF4iFitgbY/ArcGIS/rest/services/Geoloom_Crowd/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=true&f=pgeojson"
geoloom_gdf = dataplay.geoms.readInGeometryData(url=geoloom_gdf_url, porg=False, geom='geometry', lat=False, lng=False, revgeocode=False,  save=False, in_crs=4326, out_crs=False)
geoloom_gdf = geoloom_gdf.dropna(subset=['geometry'])
# geoloom_gdf = geoloom_gdf.drop(columns=['POINT_X','POINT_Y'])
geoloom_gdf.head(1)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>OBJECTID</th>
      <th>Data_type</th>
      <th>Attach</th>
      <th>...</th>
      <th>POINT_Y</th>
      <th>GlobalID</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Artists &amp; Resources</td>
      <td>None</td>
      <td>...</td>
      <td>4.762932e+06</td>
      <td>e59b4931-e0c8-4d...</td>
      <td>POINT (-76.60661...</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 14 columns</p>
</div>



And here we get the number of **points** **in** each of our corresponding CSAs (**polygons**)

```
geoloom_w_csas = dataplay.geoms.workWithGeometryData(method='pinp', df=geoloom_gdf, polys=csa_gdf, ptsCoordCol='geometry', polygonsCoordCol='geometry', polyColorCol='hhchpov18', polygonsLabel='CSA2010', pntsClr='red', polysClr='white')
```

And we plot it with a legend

```
geoloom_w_csas.plot( column='pointsinpolygon', legend=True)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7f05723a05d0>




![png](index_files/output_44_1.png)


What were to happen if I wanted to create a interactive click map with the label of each csa (**polygon**) **on** each **point**?

Well we just run the reverse operation!

```
geoloom_w_csas = workWithGeometryData(method='ponp', df=geoloom_gdf, polys=csa_gdf, ptsCoordCol='geometry', polygonsCoordCol='geometry', polyColorCol='hhchpov18', polygonsLabel='CSA2010', pntsClr='red', polysClr='white')
```

And then we can visualize it like:

```
outp = map_points(geoloom_w_csas, lat_col='POINT_Y', lon_col='POINT_X', zoom_start=12, plot_points=True, cluster_points=False,
               pt_radius=1, draw_heatmap=True, heat_map_weights_col=None, heat_map_weights_normalize=True,
               heat_map_radius=15, popup='CSA2010')
```




<div style="width:100%;"><div style="position:relative;width:100%;height:0;padding-bottom:60%;"><span style="color:#565656">Make this Notebook Trusted to load map: File -> Trust Notebook</span><iframe src="about:blank" style="position:absolute;width:100%;height:100%;left:0;top:0;border:none !important;" data-html=%3C%21DOCTYPE%20html%3E%0A%3Chead%3E%20%20%20%20%0A%20%20%20%20%3Cmeta%20http-equiv%3D%22content-type%22%20content%3D%22text/html%3B%20charset%3DUTF-8%22%20/%3E%0A%20%20%20%20%3Cscript%3EL_PREFER_CANVAS%3Dfalse%3B%20L_NO_TOUCH%3Dfalse%3B%20L_DISABLE_3D%3Dfalse%3B%3C/script%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//cdn.jsdelivr.net/npm/leaflet%401.4.0/dist/leaflet.js%22%3E%3C/script%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//code.jquery.com/jquery-1.12.4.min.js%22%3E%3C/script%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js%22%3E%3C/script%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js%22%3E%3C/script%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//cdn.jsdelivr.net/npm/leaflet%401.4.0/dist/leaflet.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//rawcdn.githack.com/python-visualization/folium/master/folium/templates/leaflet.awesome.rotate.css%22/%3E%0A%20%20%20%20%3Cstyle%3Ehtml%2C%20body%20%7Bwidth%3A%20100%25%3Bheight%3A%20100%25%3Bmargin%3A%200%3Bpadding%3A%200%3B%7D%3C/style%3E%0A%20%20%20%20%3Cstyle%3E%23map%20%7Bposition%3Aabsolute%3Btop%3A0%3Bbottom%3A0%3Bright%3A0%3Bleft%3A0%3B%7D%3C/style%3E%0A%20%20%20%20%0A%20%20%20%20%3Cmeta%20name%3D%22viewport%22%20content%3D%22width%3Ddevice-width%2C%0A%20%20%20%20%20%20%20%20initial-scale%3D1.0%2C%20maximum-scale%3D1.0%2C%20user-scalable%3Dno%22%20/%3E%0A%20%20%20%20%3Cstyle%3E%23map_a4c4074d9e604661a9486f822e03ab64%20%7B%0A%20%20%20%20%20%20%20%20position%3A%20relative%3B%0A%20%20%20%20%20%20%20%20width%3A%20100.0%25%3B%0A%20%20%20%20%20%20%20%20height%3A%20100.0%25%3B%0A%20%20%20%20%20%20%20%20left%3A%200.0%25%3B%0A%20%20%20%20%20%20%20%20top%3A%200.0%25%3B%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%3C/style%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//leaflet.github.io/Leaflet.heat/dist/leaflet-heat.js%22%3E%3C/script%3E%0A%3C/head%3E%0A%3Cbody%3E%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%3Cdiv%20class%3D%22folium-map%22%20id%3D%22map_a4c4074d9e604661a9486f822e03ab64%22%20%3E%3C/div%3E%0A%3C/body%3E%0A%3Cscript%3E%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20bounds%20%3D%20null%3B%0A%20%20%20%20%0A%0A%20%20%20%20var%20map_a4c4074d9e604661a9486f822e03ab64%20%3D%20L.map%28%0A%20%20%20%20%20%20%20%20%27map_a4c4074d9e604661a9486f822e03ab64%27%2C%20%7B%0A%20%20%20%20%20%20%20%20center%3A%20%5B39.3136523276475%2C%20-76.61656956522424%5D%2C%0A%20%20%20%20%20%20%20%20zoom%3A%2012%2C%0A%20%20%20%20%20%20%20%20maxBounds%3A%20bounds%2C%0A%20%20%20%20%20%20%20%20layers%3A%20%5B%5D%2C%0A%20%20%20%20%20%20%20%20worldCopyJump%3A%20false%2C%0A%20%20%20%20%20%20%20%20crs%3A%20L.CRS.EPSG3857%2C%0A%20%20%20%20%20%20%20%20zoomControl%3A%20true%2C%0A%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%0A%20%20%20%20%0A%20%20%20%20var%20tile_layer_119450040eb24eb2838fb60225f7c4d0%20%3D%20L.tileLayer%28%0A%20%20%20%20%20%20%20%20%27https%3A//%7Bs%7D.tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png%27%2C%0A%20%20%20%20%20%20%20%20%7B%0A%20%20%20%20%20%20%20%20%22attribution%22%3A%20null%2C%0A%20%20%20%20%20%20%20%20%22detectRetina%22%3A%20false%2C%0A%20%20%20%20%20%20%20%20%22maxNativeZoom%22%3A%2018%2C%0A%20%20%20%20%20%20%20%20%22maxZoom%22%3A%2018%2C%0A%20%20%20%20%20%20%20%20%22minZoom%22%3A%200%2C%0A%20%20%20%20%20%20%20%20%22noWrap%22%3A%20false%2C%0A%20%20%20%20%20%20%20%20%22opacity%22%3A%201%2C%0A%20%20%20%20%20%20%20%20%22subdomains%22%3A%20%22abc%22%2C%0A%20%20%20%20%20%20%20%20%22tms%22%3A%20false%0A%7D%29.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_79f6771631364288b55ee85c84303c68%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3059284576752%2C%20-76.6084962613261%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_2a26de0959224b3a9066124a1811f815%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_17863e437f2a47878916286091ed672e%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_17863e437f2a47878916286091ed672e%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMidtown%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_2a26de0959224b3a9066124a1811f815.setContent%28html_17863e437f2a47878916286091ed672e%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_79f6771631364288b55ee85c84303c68.bindPopup%28popup_2a26de0959224b3a9066124a1811f815%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_7fa34d4fe5864ed8b8049e289593fba1%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.354049947202%2C%20-76.594919959319%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_32e61fcdccbe4ea18a7f9aef0f36124d%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_9e244bb1537541428df4d552ac41178b%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_9e244bb1537541428df4d552ac41178b%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ENorthwood%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_32e61fcdccbe4ea18a7f9aef0f36124d.setContent%28html_9e244bb1537541428df4d552ac41178b%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_7fa34d4fe5864ed8b8049e289593fba1.bindPopup%28popup_32e61fcdccbe4ea18a7f9aef0f36124d%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_db76698000ff4b34ad70ad47184e60fc%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3053725867077%2C%20-76.6165491304473%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_f3e14e4b8203413290bf766b9de7525f%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_499ce218ba7340a781569922f3e276c8%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_499ce218ba7340a781569922f3e276c8%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMidtown%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_f3e14e4b8203413290bf766b9de7525f.setContent%28html_499ce218ba7340a781569922f3e276c8%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_db76698000ff4b34ad70ad47184e60fc.bindPopup%28popup_f3e14e4b8203413290bf766b9de7525f%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_d0c18cc03208489c84f5af0be27d6d2c%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3053725867077%2C%20-76.6165491304473%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_f3e65ab1a8554283b6b96c8ecab5b2a5%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_f829e55550bc4c019c7c080919972266%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_f829e55550bc4c019c7c080919972266%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMidtown%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_f3e65ab1a8554283b6b96c8ecab5b2a5.setContent%28html_f829e55550bc4c019c7c080919972266%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_d0c18cc03208489c84f5af0be27d6d2c.bindPopup%28popup_f3e65ab1a8554283b6b96c8ecab5b2a5%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_b1eaaea9d05a4a75879a5eeeaae02fa5%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3053725867077%2C%20-76.6165491304473%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_403e2fb2ea764dfc86349ecf54deda25%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_98c7dfb823394c719a8678ee2569d088%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_98c7dfb823394c719a8678ee2569d088%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMidtown%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_403e2fb2ea764dfc86349ecf54deda25.setContent%28html_98c7dfb823394c719a8678ee2569d088%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_b1eaaea9d05a4a75879a5eeeaae02fa5.bindPopup%28popup_403e2fb2ea764dfc86349ecf54deda25%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_509dcbb00cf24f1db02912a42143ea15%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3205305004358%2C%20-76.62029445046%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_2d9b58fef8064789abaab3dd6f257cec%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_45161cf3a1c24d2e83d539201ed6fb40%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_45161cf3a1c24d2e83d539201ed6fb40%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMedfield/Hampden/Woodberry/Remington%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_2d9b58fef8064789abaab3dd6f257cec.setContent%28html_45161cf3a1c24d2e83d539201ed6fb40%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_509dcbb00cf24f1db02912a42143ea15.bindPopup%28popup_2d9b58fef8064789abaab3dd6f257cec%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_7fff1c83b8924fe1b31cf5b482591895%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3132344995704%2C%20-76.6156319686376%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_4d0b17dde29f41b9aface796dc1ec324%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_6d524a05a5d048f48b7f6f22f6dbe194%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_6d524a05a5d048f48b7f6f22f6dbe194%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EGreater%20Charles%20Village/Barclay%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_4d0b17dde29f41b9aface796dc1ec324.setContent%28html_6d524a05a5d048f48b7f6f22f6dbe194%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_7fff1c83b8924fe1b31cf5b482591895.bindPopup%28popup_4d0b17dde29f41b9aface796dc1ec324%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_157e30c17c3048f2bc8d06f6a52128ef%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3025382004351%2C%20-76.6123550083559%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_43d93923f23b4706ba48fc412c87446f%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_6c4e9f0c4cb44de4b0a824e4c7e39939%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_6c4e9f0c4cb44de4b0a824e4c7e39939%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMidtown%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_43d93923f23b4706ba48fc412c87446f.setContent%28html_6c4e9f0c4cb44de4b0a824e4c7e39939%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_157e30c17c3048f2bc8d06f6a52128ef.bindPopup%28popup_43d93923f23b4706ba48fc412c87446f%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_65cbf44e9f814b9aa3924a31a8a41242%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.330960442152%2C%20-76.6097324686376%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_8b524ee7c63347879db9374717e453dc%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_281049c7e159498c9f3ef4e613e4b6ac%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_281049c7e159498c9f3ef4e613e4b6ac%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ENorth%20Baltimore/Guilford/Homeland%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_8b524ee7c63347879db9374717e453dc.setContent%28html_281049c7e159498c9f3ef4e613e4b6ac%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_65cbf44e9f814b9aa3924a31a8a41242.bindPopup%28popup_8b524ee7c63347879db9374717e453dc%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_e3f911f6ffad4f39a9ea4794e9c7becc%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3394246352966%2C%20-76.5728076182136%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_b4f83a7d6c90410498c0480aa6db521d%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_852584fbcacd4614af9de3d9deff48d4%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_852584fbcacd4614af9de3d9deff48d4%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ELauraville%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_b4f83a7d6c90410498c0480aa6db521d.setContent%28html_852584fbcacd4614af9de3d9deff48d4%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_e3f911f6ffad4f39a9ea4794e9c7becc.bindPopup%28popup_b4f83a7d6c90410498c0480aa6db521d%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_9889f05057f0416294ad42aab7056a9c%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3663642396761%2C%20-76.5807452381971%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_a47608940d034b018757e13fc6c810d6%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_0385cdb6dd9144b586cefaeb7cf129d4%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_0385cdb6dd9144b586cefaeb7cf129d4%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ELoch%20Raven%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_a47608940d034b018757e13fc6c810d6.setContent%28html_0385cdb6dd9144b586cefaeb7cf129d4%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_9889f05057f0416294ad42aab7056a9c.bindPopup%28popup_a47608940d034b018757e13fc6c810d6%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_a981ca97c54a4978a89356d1ea0c5857%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3112287786895%2C%20-76.6169870308888%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_bdf7b546ee7d4c45b6fe2f3059ac5a59%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_bfffaf3047dd413682d17d95d27492af%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_bfffaf3047dd413682d17d95d27492af%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EGreater%20Charles%20Village/Barclay%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_bdf7b546ee7d4c45b6fe2f3059ac5a59.setContent%28html_bfffaf3047dd413682d17d95d27492af%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_a981ca97c54a4978a89356d1ea0c5857.bindPopup%28popup_bdf7b546ee7d4c45b6fe2f3059ac5a59%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_d5b71dfeb251436f87bcffd532f22aa3%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3313095000031%2C%20-76.6273815000012%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_266675acb26c4a649804e9ca87ab6ae0%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_c5529e0803884bd98feb2b1f67760c0d%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_c5529e0803884bd98feb2b1f67760c0d%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMedfield/Hampden/Woodberry/Remington%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_266675acb26c4a649804e9ca87ab6ae0.setContent%28html_c5529e0803884bd98feb2b1f67760c0d%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_d5b71dfeb251436f87bcffd532f22aa3.bindPopup%28popup_266675acb26c4a649804e9ca87ab6ae0%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_7b56434679484718b8162db92c2b754a%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3111954460472%2C%20-76.6168148083572%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_eba3b97810334945846534c8cb616a29%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_cb80c86e494f4f558f986de8b12ec256%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_cb80c86e494f4f558f986de8b12ec256%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EGreater%20Charles%20Village/Barclay%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_eba3b97810334945846534c8cb616a29.setContent%28html_cb80c86e494f4f558f986de8b12ec256%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_7b56434679484718b8162db92c2b754a.bindPopup%28popup_eba3b97810334945846534c8cb616a29%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_3a3b966168da44c7b80a03da8037008d%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3097800000032%2C%20-76.6165900000012%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_6adb9d3494914485a1763e1149751656%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_c86c89ed3d6f46779e61aaa2d80f1991%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_c86c89ed3d6f46779e61aaa2d80f1991%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMidtown%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_6adb9d3494914485a1763e1149751656.setContent%28html_c86c89ed3d6f46779e61aaa2d80f1991%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_3a3b966168da44c7b80a03da8037008d.bindPopup%28popup_6adb9d3494914485a1763e1149751656%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_d909a92ce6a74df592d7ee48c95244ec%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3053725867077%2C%20-76.6165491304473%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_88285e79e1f24c95b03d3bc2f0a6f413%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_be4b532a4ae14164a4c52dcac52b8205%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_be4b532a4ae14164a4c52dcac52b8205%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMidtown%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_88285e79e1f24c95b03d3bc2f0a6f413.setContent%28html_be4b532a4ae14164a4c52dcac52b8205%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_d909a92ce6a74df592d7ee48c95244ec.bindPopup%28popup_88285e79e1f24c95b03d3bc2f0a6f413%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_e0900c0ed5de4d308df41b911cb834a9%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3140701557246%2C%20-76.6357692877849%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_234bb5a91036410b8d82ffe3c21a18e5%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_bd26a52aa1f84e60a8ecec3fcf48f7c3%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_bd26a52aa1f84e60a8ecec3fcf48f7c3%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EPenn%20North/Reservoir%20Hill%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_234bb5a91036410b8d82ffe3c21a18e5.setContent%28html_bd26a52aa1f84e60a8ecec3fcf48f7c3%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_e0900c0ed5de4d308df41b911cb834a9.bindPopup%28popup_234bb5a91036410b8d82ffe3c21a18e5%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_32dccd3865a54eee8051fc2a2299cd4a%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3140701557246%2C%20-76.6357692877849%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_dc289f4675e642ee9171b09c012f82f1%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_e244d4ee93264d04b228d8b8060cdcf1%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_e244d4ee93264d04b228d8b8060cdcf1%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EPenn%20North/Reservoir%20Hill%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_dc289f4675e642ee9171b09c012f82f1.setContent%28html_e244d4ee93264d04b228d8b8060cdcf1%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_32dccd3865a54eee8051fc2a2299cd4a.bindPopup%28popup_dc289f4675e642ee9171b09c012f82f1%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_69615fc956ac41619525280702d80df6%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3061130466302%2C%20-76.6162883877901%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_bdabae97394a45a4a07fb8d56982425a%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_9fe50613d1404626884668eebe0f51fd%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_9fe50613d1404626884668eebe0f51fd%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMidtown%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_bdabae97394a45a4a07fb8d56982425a.setContent%28html_9fe50613d1404626884668eebe0f51fd%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_69615fc956ac41619525280702d80df6.bindPopup%28popup_bdabae97394a45a4a07fb8d56982425a%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_e75acefea4e0433e88b50a93fe3f86f2%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3017150000032%2C%20-76.6202300000012%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_b5646a3efbfa45f5ab18dc0329013dba%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_4282708a682647e1a4de1859a2ad30ae%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_4282708a682647e1a4de1859a2ad30ae%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMidtown%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_b5646a3efbfa45f5ab18dc0329013dba.setContent%28html_4282708a682647e1a4de1859a2ad30ae%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_e75acefea4e0433e88b50a93fe3f86f2.bindPopup%28popup_b5646a3efbfa45f5ab18dc0329013dba%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_c9d4b9501bff42259b042edad67d2fe6%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3017150000032%2C%20-76.6202300000012%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_0497f07069e040e9a0238a0f812f0fab%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_54d8323ec57a4274aac11ba95a41ca1d%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_54d8323ec57a4274aac11ba95a41ca1d%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMidtown%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_0497f07069e040e9a0238a0f812f0fab.setContent%28html_54d8323ec57a4274aac11ba95a41ca1d%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_c9d4b9501bff42259b042edad67d2fe6.bindPopup%28popup_0497f07069e040e9a0238a0f812f0fab%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_62834990399940d580437e98f4bfba29%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3159400000032%2C%20-76.6096900000012%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_429bab6668da4cacbd844a59495cd765%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_f231aefd161647929eb01fa44138fb10%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_f231aefd161647929eb01fa44138fb10%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EGreater%20Charles%20Village/Barclay%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_429bab6668da4cacbd844a59495cd765.setContent%28html_f231aefd161647929eb01fa44138fb10%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_62834990399940d580437e98f4bfba29.bindPopup%28popup_429bab6668da4cacbd844a59495cd765%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_6161362c64f04e6e98766c6267a02edf%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3243857282909%2C%20-76.6294667363678%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_7f5168e082994d13b8476d2a9f556bbe%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_7f564fe0d44840e683fc5e676ffa542c%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_7f564fe0d44840e683fc5e676ffa542c%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMedfield/Hampden/Woodberry/Remington%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_7f5168e082994d13b8476d2a9f556bbe.setContent%28html_7f564fe0d44840e683fc5e676ffa542c%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_6161362c64f04e6e98766c6267a02edf.bindPopup%28popup_7f5168e082994d13b8476d2a9f556bbe%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_c59d7c0ab163492c9eeb430f2635d68d%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3518547124792%2C%20-76.5618773076933%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_46ca9d14b4c449eea254bc8ac87b2355%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_bab9180884404d48b7025e72467df3ae%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_bab9180884404d48b7025e72467df3ae%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EHarford/Echodale%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_46ca9d14b4c449eea254bc8ac87b2355.setContent%28html_bab9180884404d48b7025e72467df3ae%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_c59d7c0ab163492c9eeb430f2635d68d.bindPopup%28popup_46ca9d14b4c449eea254bc8ac87b2355%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_b1fb9b9b82fb4ae5a3b9ddb0939c46f6%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3540395711272%2C%20-76.5949191991194%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_8d5d8c22bd78421992f4a1b65a2a18e7%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_9dece41e79384e9b843d491345c9972e%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_9dece41e79384e9b843d491345c9972e%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ENorthwood%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_8d5d8c22bd78421992f4a1b65a2a18e7.setContent%28html_9dece41e79384e9b843d491345c9972e%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_b1fb9b9b82fb4ae5a3b9ddb0939c46f6.bindPopup%28popup_8d5d8c22bd78421992f4a1b65a2a18e7%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_196a12870d554437bba8dbf00401630d%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3454084293701%2C%20-76.6310377077168%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_a1cebd07858b4055862caf82b3ef09f7%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_5b9cc47225b74a95b1b0f6549d80fb33%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_5b9cc47225b74a95b1b0f6549d80fb33%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EGreater%20Roland%20Park/Poplar%20Hill%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_a1cebd07858b4055862caf82b3ef09f7.setContent%28html_5b9cc47225b74a95b1b0f6549d80fb33%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_196a12870d554437bba8dbf00401630d.bindPopup%28popup_a1cebd07858b4055862caf82b3ef09f7%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_9154b6cf1d2043e88eead367e2258737%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3054254932224%2C%20-76.6429111990029%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_c4a9733f6f5c4cc79a581b68ad36eca5%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_2a4f1a849f8e4192b80f06e1136aa7d2%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_2a4f1a849f8e4192b80f06e1136aa7d2%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ESandtown-Winchester/Harlem%20Park%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_c4a9733f6f5c4cc79a581b68ad36eca5.setContent%28html_2a4f1a849f8e4192b80f06e1136aa7d2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_9154b6cf1d2043e88eead367e2258737.bindPopup%28popup_c4a9733f6f5c4cc79a581b68ad36eca5%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_1eb7969cd0394a9c8a6205fcdb52841c%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3053725867077%2C%20-76.6165491304473%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_38d5c98c4f6440a3a141db7ebb4f2e19%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_164686c2b0f44ce98f25f805d5182423%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_164686c2b0f44ce98f25f805d5182423%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMidtown%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_38d5c98c4f6440a3a141db7ebb4f2e19.setContent%28html_164686c2b0f44ce98f25f805d5182423%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_1eb7969cd0394a9c8a6205fcdb52841c.bindPopup%28popup_38d5c98c4f6440a3a141db7ebb4f2e19%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_8cf15c0d4f194085be4fcb8abe7eb9c4%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3053735782905%2C%20-76.6166029730092%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_e553e9901e4045a9afe538d8a8388702%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_287d4834fb654365b89edb94e25629f0%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_287d4834fb654365b89edb94e25629f0%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMidtown%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_e553e9901e4045a9afe538d8a8388702.setContent%28html_287d4834fb654365b89edb94e25629f0%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_8cf15c0d4f194085be4fcb8abe7eb9c4.bindPopup%28popup_e553e9901e4045a9afe538d8a8388702%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_500946693e2a48ec8d9e720c7fea286c%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3098540513334%2C%20-76.6422915487344%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_1180bb440060478b939e37219d036d69%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_d7359b1a7e0a41ba904b4533c92fa6ec%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_d7359b1a7e0a41ba904b4533c92fa6ec%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ESandtown-Winchester/Harlem%20Park%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_1180bb440060478b939e37219d036d69.setContent%28html_d7359b1a7e0a41ba904b4533c92fa6ec%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_500946693e2a48ec8d9e720c7fea286c.bindPopup%28popup_1180bb440060478b939e37219d036d69%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_c4dc1c3faacd4ef18a7b36e44e6f5be8%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.331329442152%2C%20-76.6275211151839%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_d4d6bde85e6648d7b4b40568e4d4e3db%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_cbecf47d0f1747db94d952a4855708bf%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_cbecf47d0f1747db94d952a4855708bf%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMedfield/Hampden/Woodberry/Remington%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_d4d6bde85e6648d7b4b40568e4d4e3db.setContent%28html_cbecf47d0f1747db94d952a4855708bf%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_c4dc1c3faacd4ef18a7b36e44e6f5be8.bindPopup%28popup_d4d6bde85e6648d7b4b40568e4d4e3db%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_d8a01314596f434a88cd3dffd4c169ec%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.331329442152%2C%20-76.6275211151839%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_2d376e25323545b1a4a14519f9a14e21%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_b2740c579b7646bc9b20f003a8c28943%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_b2740c579b7646bc9b20f003a8c28943%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMedfield/Hampden/Woodberry/Remington%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_2d376e25323545b1a4a14519f9a14e21.setContent%28html_b2740c579b7646bc9b20f003a8c28943%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_d8a01314596f434a88cd3dffd4c169ec.bindPopup%28popup_2d376e25323545b1a4a14519f9a14e21%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_cc3a8a03e96b4225bc2c629c4c4f52fb%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3061685720253%2C%20-76.6163105668306%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_b2ca172f97144132974c9c5e54fc8c20%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_ad31aa818e8f4319af0cc2cbb768e2bd%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_ad31aa818e8f4319af0cc2cbb768e2bd%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMidtown%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_b2ca172f97144132974c9c5e54fc8c20.setContent%28html_ad31aa818e8f4319af0cc2cbb768e2bd%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_cc3a8a03e96b4225bc2c629c4c4f52fb.bindPopup%28popup_b2ca172f97144132974c9c5e54fc8c20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_a61b0544bf734065b6ad42a12abf4759%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3557085114907%2C%20-76.6325299272257%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_b0f5a7428bd9420b9b32c9b8e13361cf%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_63cf9bdda69f40c9a8d5a69db710ee11%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_63cf9bdda69f40c9a8d5a69db710ee11%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EGreater%20Roland%20Park/Poplar%20Hill%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_b0f5a7428bd9420b9b32c9b8e13361cf.setContent%28html_63cf9bdda69f40c9a8d5a69db710ee11%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_a61b0544bf734065b6ad42a12abf4759.bindPopup%28popup_b0f5a7428bd9420b9b32c9b8e13361cf%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_0b148b58a620457e8080c809a04f4b81%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3557085114907%2C%20-76.6325299272257%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_d7b0de352c5344ce889c30833eed6185%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_9ec771a32198404ebce4894635e9a8af%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_9ec771a32198404ebce4894635e9a8af%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EGreater%20Roland%20Park/Poplar%20Hill%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_d7b0de352c5344ce889c30833eed6185.setContent%28html_9ec771a32198404ebce4894635e9a8af%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_0b148b58a620457e8080c809a04f4b81.bindPopup%28popup_d7b0de352c5344ce889c30833eed6185%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_80f030b5fa8c4ccfabb00f86f7459925%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.3320899965888%2C%20-76.5492359719015%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22%233388ff%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22%233db7e4%22%2C%0A%20%20%22fillOpacity%22%3A%200.2%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%201%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_5108f7e7ab5c438b8b131c12af32ef52%20%3D%20L.popup%28%7BmaxWidth%3A%20%27100%25%27%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_9d1793dac158402ab8bae6f7a81b0587%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_9d1793dac158402ab8bae6f7a81b0587%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ECedonia/Frankford%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_5108f7e7ab5c438b8b131c12af32ef52.setContent%28html_9d1793dac158402ab8bae6f7a81b0587%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_80f030b5fa8c4ccfabb00f86f7459925.bindPopup%28popup_5108f7e7ab5c438b8b131c12af32ef52%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20heat_map_c3d6a730c4564d6b9001d24da3432f1d%20%3D%20L.heatLayer%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B%5B39.3059284576752%2C%20-76.6084962613261%5D%2C%20%5B39.354049947202%2C%20-76.594919959319%5D%2C%20%5B39.3053725867077%2C%20-76.6165491304473%5D%2C%20%5B39.3053725867077%2C%20-76.6165491304473%5D%2C%20%5B39.3053725867077%2C%20-76.6165491304473%5D%2C%20%5B39.3205305004358%2C%20-76.62029445046%5D%2C%20%5B39.3132344995704%2C%20-76.6156319686376%5D%2C%20%5B39.3025382004351%2C%20-76.6123550083559%5D%2C%20%5B39.330960442152%2C%20-76.6097324686376%5D%2C%20%5B39.3394246352966%2C%20-76.5728076182136%5D%2C%20%5B39.3663642396761%2C%20-76.5807452381971%5D%2C%20%5B39.3112287786895%2C%20-76.6169870308888%5D%2C%20%5B39.3313095000031%2C%20-76.6273815000012%5D%2C%20%5B39.3111954460472%2C%20-76.6168148083572%5D%2C%20%5B39.3097800000032%2C%20-76.6165900000012%5D%2C%20%5B39.3053725867077%2C%20-76.6165491304473%5D%2C%20%5B39.3140701557246%2C%20-76.6357692877849%5D%2C%20%5B39.3140701557246%2C%20-76.6357692877849%5D%2C%20%5B39.3061130466302%2C%20-76.6162883877901%5D%2C%20%5B39.3017150000032%2C%20-76.6202300000012%5D%2C%20%5B39.3017150000032%2C%20-76.6202300000012%5D%2C%20%5B39.3159400000032%2C%20-76.6096900000012%5D%2C%20%5B39.3243857282909%2C%20-76.6294667363678%5D%2C%20%5B39.3518547124792%2C%20-76.5618773076933%5D%2C%20%5B39.3540395711272%2C%20-76.5949191991194%5D%2C%20%5B39.3454084293701%2C%20-76.6310377077168%5D%2C%20%5B39.3054254932224%2C%20-76.6429111990029%5D%2C%20%5B39.3053725867077%2C%20-76.6165491304473%5D%2C%20%5B39.3053735782905%2C%20-76.6166029730092%5D%2C%20%5B39.3098540513334%2C%20-76.6422915487344%5D%2C%20%5B39.331329442152%2C%20-76.6275211151839%5D%2C%20%5B39.331329442152%2C%20-76.6275211151839%5D%2C%20%5B39.3061685720253%2C%20-76.6163105668306%5D%2C%20%5B39.3557085114907%2C%20-76.6325299272257%5D%2C%20%5B39.3557085114907%2C%20-76.6325299272257%5D%2C%20%5B39.3320899965888%2C%20-76.5492359719015%5D%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20minOpacity%3A%200.5%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20maxZoom%3A%2018%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20max%3A%201.0%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20radius%3A%2015%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20blur%3A%2015%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20gradient%3A%20null%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20.addTo%28map_a4c4074d9e604661a9486f822e03ab64%29%3B%0A%20%20%20%20%20%20%20%20%0A%3C/script%3E onload="this.contentDocument.open();this.contentDocument.write(    decodeURIComponent(this.getAttribute('data-html')));this.contentDocument.close();" allowfullscreen webkitallowfullscreen mozallowfullscreen></iframe></div></div>



These interactive visualizations can be exported to html using a tool found later in this document. 

Its how I made this page!

If you like what you see, there is more in the package you will just have to explore. 

<h2 align="left">Have Fun!</h2>
<img src="https://bniajfi.org/images/mermaid/vitalSignsCorrelations.png" width="500px" style="max-width: 500pxpx">
<img src="https://bniajfi.org/images/mermaid/vitalSignsGif.gif" width="500px" style="max-width: 500pxpx">

## Disclaimer

__Disclaimer__

**Views Expressed**:
All views expressed in this tutorial are the authors own and do not represent the opinions of any entity whatsover with which they have been, are now, or will be affiliated.

**Responsibility, Errors and Ommissions**: 
The author makes no assurance about the reliability of the information. The author makes takes no responsibility for updating the tutorial nor maintaining it porformant status. Under no circumstances shall the Author or its affiliates be liable for any indirect incedental, consequential, or special and or exemplary damages arising out of or in connection with this tutorial. Information is provided 'as is' with distinct plausability of errors and ommitions. Information found within the contents is attached with an **MIT license**. Please refer to the License for more information. 

**Use at Risk**:
Any action you take upon the information on this Tutorial is strictly at your own risk, and the author will not be liable for any losses and damages in connection with the use of this tutorial and subsequent products.

**Fair Use**
this site contains copyrighted material the use of which has not always been specifically authorized by the copyright owner. While no intention is made to unlawfully use copyrighted work, circumstanes may arise in which such material is made available in effort to advance scientific literacy. We believe this constitutes a 'fair use' of any such copyrighted material as provided for in section 107 of the US Copyright Law. In accordance with Titile 17 U.S.C. Section 108, the material on this tutorial is distributed without profit to those who have expressed a prior interest in receiving the included information for research and education purposes. 

for more information go to: http://www.law.cornell.edu/uscode/17/107.shtml. If you wish to use copyrighted material from this site for purposes of your own that go beyond 'fair use', you must obtain permission from the copyright owner.

__License__

Copyright © 2019 BNIA-JFI

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


## FOR CONTRIBUTERS

### Dev Instructions

From a local copy of the git repo:
0. __Clone__ the repo local onto GDrive 
  - Via Direct-DL&Drive-Upload or Colab/Terminal/Git
  - `git clone https://github.com/BNIA/dataplay.git`
1. __Update__ the the IPYNB 
  - From the GDrive dataplay folder via Colabs
2. __Build__ the new libraries from these NBs 
  - Using this *index.ipynb*
  - - Mount the Colabs Enviornment (and navigate to) the GDrive dataplay folder
  - - run `!nbdev_build_lib` to build .py modules.
3. __Test__ the Library/ Modules
  - Using the same runtime as step 2's *index.ipynb*.
  - - Do not install the module from PyPi (if published) and then...
  - - Import your module (
  from your dataplay/dataplay)
  - - If everything runs properly, go to step 5.
4. __Edit__ modules directly
  - Within the same runtime as step 2/3's *index.ipynb*...
  - - Locate the dataplay/dataplay using the colab file nav
  - - double-click the .py modules in the file nav to open them in an in-browser editor
  - Make changes and return to step 3 with the following caveat:
  - - Use the hot module reloading to ensure updates are auto-re-imported 
  - - `%load_ext autoreload %autoreload 2`
  - Then when finished, persist the changes from the .py modules back to the .ipynb docs 
  - - via `!nbdev_update_lib` and `!relimport2name`
5. **Create** Docs, **Push** to Github, and **Publish** to PyPI
  - All done via [nbdev](https://nbdev.fast.ai/) 
  - Find more notes I made on that here: [dataplay](https://github.com/bnia/dataplay) > nbdev [notes](https://bnia.github.io/datalabs/nbdev/index.html) 
  - `!nbdev_build_docs --force_all True --mk_readme True `
  - `!git commit -m ...`
  - `%%capture ! pip install twine`
  - `!nbdev_bump_version`
  - `! make pypi`

```
# https://nbdev.fast.ai/tutorial.html#Set-up-prerequisites
# settings.ini > requirements = fastcore>=1.0.5 torchvision<0.7
# https://nbdev.fast.ai/tutorial.html#View-docs-locally
# console_scripts = nbdev_build_lib=nbdev.cli:nbdev_build_lib
# https://nbdev.fast.ai/search
```

### Dev Scripts

Not shown.

```
!nbdev_build_lib
```

    Converted 01_Download_and_Load.ipynb.
    Converted 02_Merge_Data.ipynb.
    Converted 03_Map_Basics_Intake_and_Operations.ipynb.
    Converted 04_nb_2_html.ipynb.
    Converted 05_Map_Correlation_Networks.ipynb.
    Converted 06_Timelapse_Data_Gifs.ipynb.
    Converted index.ipynb.


```
!pip install geopandas
```

```
!pip install VitalSigns
```

```
!pip install marko
```

```
!nbdev_build_docs --force_all True --mk_readme True
```

```
!nbdev_nb2md 'notebooks/index.ipynb' > README.md
```
