# Elecciones Scraper

This bot download info from `http://atlaselectoral.oep.org.bo/`


## Setup

```console

pip install -r requirements

```

## How to run:

```
python main.py

```

**Output**
```
full_path_to_file:  /home/stanlee321/Desktop/2020/ELECCIONES/scraper/tmp/ELECCIONES GENERALES 2014 (1).csv

   Codigo Departamento   MAS-IPSP MAS-IPSP%  ...  Blancos   Nulos   Emitidos Inscritos Habilitados
0       1   CHUQUISACA    165.785     63,38  ...    9.308  13.348    284.218               323.129
1       2       LA PAZ  1.006.433     68,92  ...   22.690  50.817  1.533.812             1.678.769
2       3   COCHABAMBA    637.125     66,67  ...   19.021  41.237  1.015.890             1.128.351
3       4        ORURO    166.360     66,42  ...    5.700  10.725    266.873               293.576
4       5       POTOSI    224.215     69,49  ...   14.091  20.932    357.695               409.144

[5 rows x 17 columns]
 
```


## TODOs

* Handle correct name matching for file downloaded in ./temp


