# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 17:46:08 2020

@author: pepeb
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.dates as mdates
from types import SimpleNamespace
import io
import requests
import pandas as pd


def cod_ine(NomCom):

    Comunidades = {
    "ANDA":   1,
    "ARAG":   2,
    "ASTUR":  3,
    "BALE":   4,
    "CANA":   5 ,
    'CANTA':  6,
    'MANCHA':  8,
    'LEON':    7,
    "CATALU":  9,
    "CEUT":  18,
    "VALEN":  10,
    "EXTRE":  11,
    "GALI" :  12,
    "MADRI":  13,
    "MELI":   19,
    "MURC":   14, 
    "NAVARR": 15,
    "VASC":   16,
    "EUSK":   16,
    "RIOJ":   17,
    "ESP":     0

    }
    for key in Comunidades:
    
        if NomCom.upper().find(key)>-1:
            return Comunidades[key]
    
    return -1
   
def ploteame(txt, Comunidad, tipo):

    count = -1
    plt.figure()
    fig, ax = plt.subplots()
    dfOld = GetStat(txt)
    tipo = diarioortotal(tipo)
    for i in Comunidad:
        count = count +1
        print(count)
        
        df = dfOld.set_index('cod_ine')
        NombreComunidad = df['CCAA'].loc[i]
        df = df.loc[i][1:np.shape(dfOld)[1]]
        df.index = pd.to_datetime(df.index)    
        if tipo.upper().find('DIA')>-1:
            #df.diff().plot.bar(label = NombreComunidad, color = cm.tab20(count), ax = ax)
            ax.bar(df.index, df.diff(), color = cm.tab10(count), label = NombreComunidad)
        
     
        elif tipo.upper().find('TOT')>-1:
            #df.plot(label = NombreComunidad,  color = cm.tab20(count), ax = ax)
            ax.plot(df.index, df, label = NombreComunidad,  color = cm.tab10(count), linewidth=4)
    #set ticks every week
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    fig.autofmt_xdate()
    #set major ticks format
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.tick_params(labelsize=13)
    ylab = txt+' '+ diarioortotal(tipo) 
    ax.set_ylabel(ylab, fontsize = 13)
    plt.legend(loc=2, fontsize = 13)       
    plt.savefig('Ploteo.png')
    
def tipo(txt):
    x = txt.split() 
    for i in x:
        if i.upper().find('MUE')>-1 or i.upper().find('FALLE')>-1:
            return 'FALLECIDOS'
        if i.upper().find('CONTAG')>-1 or i.upper().find('INFEC')>-1:
            return 'INFECTADOS'

def diarioortotal(txt):
    x = txt.split() 
    for i in x:
        if i.upper().find('TOT')>-1 or i.upper().find('ACUM')>-1:
            return 'TOTALES'
        if i.upper().find('DIA')>-1:
            return 'DIARIOS'

def comunidad(txt):
    x = txt.split() 
    a = []
    for i in x:
        
        if cod_ine(i)>-1:
            
            a.append(cod_ine(i))
        
    return a



def GetStat(txt):
    if txt == 'FALLECIDOS':
        url ="https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_fallecidos.csv"

    if txt == 'INFECTADOS':
        url ="https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_casos.csv"
        
    s = requests.get(url).content
    Stat = pd.read_csv(io.StringIO(s.decode('utf-8')))
    return Stat