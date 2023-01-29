import pandas as pd
import datetime
import requests
import klimadata.extreme as e
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

'''Funksjonar for å hente ned data frå NVE api GridTimeSeries og enkel bearbeiding før plotting
Modulen tek i bruk streamlit cache for å redusere antall kall til api
'''

@st.cache
def nve_api(x: str, y: str, startdato: str, sluttdato: str, para: str) -> list:
    """Henter data frå NVE api GridTimeSeries

    Funksjonen henter ned data frå eit gitt punkt, med gitt start og slutt dato.
    Denne funksjonen henter kunn ned ein parameter.

    Parameters
    ----------
        x 
            øst koordinat (i UTM33)
        y  
            nord koordinat (i UTM33)
        startdato
            startdato for dataserien som hentes ned
        sluttdato 
            sluttdato for dataserien som hentes ned
        para
            kva parameter som skal hentes ned f.eks rr for nedbør

    Returns
    ----------
        verdier
            returnerer ei liste med klimaverdier

    """
    api = "http://h-web02.nve.no:8080/api/"
    url = (
        api
        + "/GridTimeSeries/"
        + str(x)
        + "/"
        + str(y)
        + "/"
        + str(startdato)
        + "/"
        + str(sluttdato)
        + "/"
        + para
        + ".json"
    )
    r = requests.get(url)

    verdier = r.json()
    return verdier

@st.cache
def stedsnavn(x: str, y: str) -> list:
    """Henter stedsnavn fra geonorge api for stedsnavnsøk
    
    Koordinatsystem er hardcoda inn i request streng sammen med søkeradius
    Radius er satt til 500m

    Parameters
    ----------
        x
            nord koordinat i UTM33
        y
            øst koordinat i UTM33

    Returns
    ----------
        verier
            Liste med stedsnavn innanfor radius på 500m

    """
    url = f"https://ws.geonorge.no/stedsnavn/v1/punkt?nord={y}&ost={x}&koordsys=5973&radius=500&utkoordsys=4258&treffPerSide=1&side=1"
    r = requests.get(url)
    verdier = r.json()
    # for verdi in
    return verdier


def hent_data_klima_dogn(x: str, y: str, startdato: str, sluttdato: str, parametere: list) -> dict:
    """Henter ned klimadata basert på liste av parametere

    Parameters
    ----------
        x
            øst-vest koordinat (i UTM33)
        y
            nord-sør koordinat (i UTM33)
        startdato
            startdato for dataserien som hentes ned
        sluttdato 
            sluttdato for dataserien som hentes ned
        parametere
            liste med parametere som skal hentes ned f.eks rr for nedbør

    Returns
    ----------
        parameterdict
            dict med parameternavn til key, og liste med verdier som value

    """
    parameterdict = {}
    for parameter in parametere:

        parameterdict[parameter] = nve_api(x, y, startdato, sluttdato, parameter)[
            "Data"
        ]
    return parameterdict


def klima_dataframe(x: str, y: str, startdato: str, sluttdato: str, parametere: list) -> pd.DataFrame:
    """Lager dataframe basert på klimadata fra NVE api.

    Bruker programpakken pandas for å samle klimadata i ein dataframe.
    Dette forenkler videre behandling av data og plotting.
    Bruker start og sluttdato for å generere index i pandas dataframe.

    Parameters
    ----------
        x
            øst-vest koordinat (i UTM33)
        y
            nord-sør koordinat (i UTM33)
        startdato
            startdato for dataserien som hentes ned
        sluttdato
            sluttdato for dataserien som hentes ned
        parametere
            liste med parametere som skal hentes ned f.eks rr for nedbør

    Returns
    ----------
        df
            Pandas dataframe med klimadata

    """
    parameterdict = {}
    for parameter in parametere:

        parameterdict[parameter] = nve_api(x, y, startdato, sluttdato, parameter)[
            "Data"
        ]

    df = pd.DataFrame(parameterdict)
    df = df.set_index(
        #Setter index til å være dato, basert på start og sluttdato
        pd.date_range(
            datetime.datetime(
                int(startdato[0:4]), int(startdato[5:7]), int(startdato[8:10])
            ),
            datetime.datetime(
                int(sluttdato[0:4]), int(sluttdato[5:7]), int(sluttdato[8:10])
            ),
        )
    )
    df[df > 1000] = 0 #Kutter ut verdier som er større enn 1000, opprydding
    df = rullande_3dogn_nedbor(df)
    return df

@st.cache
def hent_hogde(x: str, y: str) -> str:
    """Henter ned høgdeverdi for koordinat fra NVE api

    Parameters
    ----------
        x
            øst-vest koordinat (i UTM33)
        y
            nord-sør koordinat (i UTM33)

    Returns
    ----------
        høgde
            høgdeverdi for koordinat

    """

    return str(nve_api(x, y, '01-01-2022', '01-01-2022', 'rr') ['Altitude'])

 

def maxdf(df: pd.DataFrame) -> pd.DataFrame:
    """Tar in klimadataframe, og returnerer ny dataframe med årlige maksimalverdier
    
    Parameters
    ----------
        df
            Pandas dataframe med klimadata
        
    Returns
    ----------
        maxdf
            Pandas dataframe med årlige maksimalverdier
    """
    maxdf = pd.DataFrame(df["sdfsw3d"].groupby(pd.Grouper(freq="Y")).max()).assign(
        rr=df["rr"].groupby(pd.Grouper(freq="Y")).max(),
        rr3=df["rr3"].groupby(pd.Grouper(freq="Y")).max(),
        sd=df["sd"].groupby(pd.Grouper(freq="Y")).max(),
    )
    return maxdf


def vind_nedbor(df: pd.DataFrame) -> pd.DataFrame:
    """Tar in vinddataframe, og returnerer ny dataframe med der nedbør (rr) under 0.2mm blir fjerna
    
    Parameters
    ----------
        df
            Pandas dataframe med klimadata

    Returns
    ----------
        df
            Pandas dataframe der dager med nedbør (rr) under 0.2mm blir fjerna
    
    """
    return df.where(df.rr > 0.2).dropna()


def vind_regn(df: pd.DataFrame) -> pd.DataFrame:
    """Tar in vinddataframe, og returnerer ny dataframe med der regn (rrl) under 0.2mm blir fjerna
    
    Bruker rrl istedenfor rr, da rr er nedbør, mens rrl er regn fra NVE Grid Times Series API

    Parameters
    ----------
        df
            Pandas dataframe med klimadata

    Returns
    ----------
        df
            Pandas dataframe der dager med regn (rrl) under 0.2mm blir fjerna
    
    """
    return df.where(df.rrl > 0.2).dropna()


def vind_sno_fsw(df: pd.DataFrame) -> pd.DataFrame:
    """Tar in vinddataframe, og returnerer ny dataframe med der nysnø under 0.2mm blir fjerna
    
    Parameters
    ----------
        df
            Pandas dataframe med klimadata
        
    Returns
    ----------
        df
            Pandas dataframe der dager med nysnø under 0.2mm blir fjerna
    """
    filter1 = df["fsw"] > 0.2 #Fjerner dager med nysnø under 0.2 cm (lite relevante)
    filter2 = df["fsw"] < 200 #Håndterer feil i data
    return df.where(filter1 & filter2).dropna()


def vind_sno_rr_tm(df: pd.DataFrame) -> pd.DataFrame:
    """Tar in vinddataframe, og returnerer ny dataframe med der nedbør under 0.2mm og temperatur under 1 grad blir fjerna
    
    Parameters
    ----------
        df
            Pandas dataframe med klimadata
        
    Returns
    ----------
        df
            Pandas dataframe der dager med nedbør under 0.2mm og temperatur blir fjerna

    """
    return df.where(df.rr > 0.2).dropna().where(df.tm < 1).dropna()


def rullande_3dogn_nedbor(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Tar in klimadataframe og returnerer med ny kollonne med utrekna 3 døgs nedbør basert på døgnnedbør
    
    Parameters
    ----------
        dataframe
            Pandas dataframe med klimadata
        
    Returns
    ----------
        df
            Pandas dataframe med ny kollonne med utrekna 3 døgs nedbør basert på døgnnedbør
    
    """
    df = dataframe.assign(rr3=dataframe["rr"].rolling(3).sum().round(2)).fillna(0)
    return df


def plot_ekstremverdier_3dsno(df: pd.DataFrame, ax1=None):
    """Gammel funksjon for å jobbe med eldre tilpassing av ekstremverdiutrekning
    
    Parameters
    ----------
        df
            Pandas dataframe med klimadata
        ax1
            Matplotlib axis
    
    Returns
    ----------
        model
            Ekstremverdiutrekning basert på Gumbel distribusjon
    """
    maximal = maxdf(df)
    liste = maximal["sdfsw3d"].tolist()
    array = np.array(liste)
    model = e.Gumbel(array, fit_method="mle", ci=0.05, ci_method="delta")

    if ax1 is None:
        ax1 = plt.gca()

    return model.plot_return_values("3ds")
