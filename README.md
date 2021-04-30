# Elecciones Scraper

This bot download info from `https://computo.oep.org.bo/`

El bot corre en un loop infinito dentro del `main.py` para descargar los `csv`  de cada departamento.

El bot tarda alrededor de 1 minuto por departamento.

The info is downloaded into the folder `tmp/`

Si la descarga de `csv` se detiene por algun error, incrementar los tiempos de `time.sleep()` corredpondientes a cada proceso, la pagina puede empezar a volverce lenta y eso causara que se incremente los tiempos de espera para el bot.

## Setup

```console

pip install -r requirements

```

Setear la variable entorno

Setup project dir

```
export PROJ_DIR=$PWD

```


## How to run:

```
python main.py
```

## TODOS

* CI/CD with docker
* Setup cronjobs 
* Setup Airflow if is possible
