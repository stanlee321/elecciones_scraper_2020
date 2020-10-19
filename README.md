# Elecciones Scraper

This bot download info from `http://atlaselectoral.oep.org.bo/`


## Setup


Hace el install dentro del python del sistema.

```console

pip install -r requirements

```

Setear la variable entorno

Setup project dir
```
export PROJ_DIR=$PWD

```

Permisos para cronjb


```
chmod 400 ./command.sh

```

COrrer el .sh

```command
./command.sh
```


```
sudo service cron reload


```

## How to run:



## TODOs

* Handle correct name matching for file downloaded in ./temp



## Refs

* https://medium.com/@gavinwiener/how-to-schedule-a-python-script-cron-job-dea6cbf69f4e