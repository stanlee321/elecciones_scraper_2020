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
Opciones de voto
http://atlaselectoral.oep.org.bo/descarga/52/opcion_voto.csv
                               sigla|nombre|colorRGB
0           PUB|PARTIDO DE LA UNIÓN BOLIVIANA|0000FF
1  MNR(ALIANZA)|ALIANZA DEL MOVIMIENTO NACIONALIS...
2                                     ADN|ADN|FF0000
3            UDP|UNIDAD DEMOCRÁTICA Y POPULAR|FF530D
4         MITKA|MOVIMIENTO INDIO TUPAC KATARI|654321
Candidatos
http://atlaselectoral.oep.org.bo/descarga/52/candidatos.csv
  NOMBRE|CARGO|OPCION O SIGLA|CODIGO GEOGRAFIA|CANDIDATO O GANADORJULIO TUMIRI APAZA|DIPUTADO|undefined|undefined|ELECTO
0  JOSÉ ZEGARRA CERRUTO|DIPUTADO|undefined|undefi...                                                                    
1  JOSÉ MARÍA PALACIOS LÓPEZ|DIPUTADO|undefined|u...                                                                    
2  FERNANDO BAPTISTA GUMUCIO|SENADOR|undefined|un...                                                                    
3  GUALBERTO CLAURE ORTUÑO|SENADOR|undefined|unde...                                                                    
4  CARLOS CARRASCO FERNÁNDEZ|DIPUTADO|undefined|u...                                                                    
Votos Totales
http://atlaselectoral.oep.org.bo/descarga/52/votos_totales.csv
  Codigo PAIS|Nombre PAIS|Codigo DEPARTAMENTO|Nombre DEPARTAMENTO|ADN|APIN|MITKA|MNR(ALIANZA)|PS-1|PUB|UDP|VO|BLANCOS|EMITIDOS|NULOS|VALIDOS
0  BO|BOLIVIA|01|CHUQUISACA|10032|2185|1343|34609...                                                                                        
1  BO|BOLIVIA|02|LA PAZ|77614|8454|16557|78023|24...                                                                                        
2  BO|BOLIVIA|03|COCHABAMBA|42983|16449|3744|6464...                                                                                        
3  BO|BOLIVIA|04|ORURO|10633|10819|2707|46232|646...                                                                                        
4  BO|BOLIVIA|05|POTOSI|16090|2789|2677|105782|39...  
```


## TODOs

* Perform click and continue pipeline for each one of the dropdown elements in the `Elecciones Generales` menu button.



