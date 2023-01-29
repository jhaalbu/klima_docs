Datanedlasting
--------------------------------------------
Forklaring på dei enkelte funksjoner som genererer klimadata fra NVI sitt api.


.. py:function:: klima_dataframe(x: str, y: str, startdato: str, sluttdato: str, parametere: list) -> pd.DataFrame:
    
    Lager dataframe basert på klimadata fra NVE api.

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



.. py:function:: nve_api(x: str, y: str, startdato: str, sluttdato: str, para: str) -> list
    
    Henter data frå NVE api GridTimeSeries.
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

.. py:function:: hent_data_klima_dogn(x: str, y: str, startdato: str, sluttdato: str, parametere: list) -> dict

    Henter ned klimadata basert på liste av parametere

    Henter data frå NVE api GridTimeSeries.
    Funksjonen henter ned data frå eit gitt punkt, med gitt start og slutt dato.
    Denne funksjonen tar i mot ei liste av parametere, og gir tilbake ein
    dict med parameternavn som key, og values som verdiene.

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



.. py:function:: stedsnavn(x: str, y: str) -> list

    Henter stedsnavn fra geonorge api for stedsnavnsøk
    
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

.. py:function:: maxdf(df: pd.DataFrame) -> pd.DataFrame:
    
    Tar in klimadataframe, og returnerer ny dataframe med årlige maksimalverdier
    
    Parameters
    ----------
        df
            Pandas dataframe med klimadata
        
    Returns
    ----------
        maxdf
            Pandas dataframe med årlige maksimalverdier


.. py:function:: vind_nedbor(df: pd.DataFrame) -> pd.DataFrame:
    
    Tar in vinddataframe, og returnerer ny dataframe med der nedbør (rr) under 0.2mm blir fjerna
    
    Parameters
    ----------
        df
            Pandas dataframe med klimadata

    Returns
    ----------
        df
            Pandas dataframe der dager med nedbør (rr) under 0.2mm blir fjerna
    



.. py:function:: vind_regn(df: pd.DataFrame) -> pd.DataFrame:
    
    Tar in vinddataframe, og returnerer ny dataframe med der regn (rrl) under 0.2mm blir fjerna
    
    Bruker rrl istedenfor rr, da rr er nedbør, mens rrl er regn fra NVE Grid Times Series API

    Parameters
    ----------
        df
            Pandas dataframe med klimadata

    Returns
    ----------
        df
            Pandas dataframe der dager med regn (rrl) under 0.2mm blir fjerna
    



.. py:function:: vind_sno_fsw(df: pd.DataFrame) -> pd.DataFrame:
    
    Tar in vinddataframe, og returnerer ny dataframe med der nysnø under 0.2mm blir fjerna
    
    Parameters
    ----------
        df
            Pandas dataframe med klimadata
        
    Returns
    ----------
        df
            Pandas dataframe der dager med nysnø under 0.2mm blir fjerna


.. py:function:: vind_sno_rr_tm(df: pd.DataFrame) -> pd.DataFrame:
   
   Tar in vinddataframe, og returnerer ny dataframe med der nedbør under 0.2mm og temperatur under 1 grad blir fjerna
    
    Parameters
    ----------
        df
            Pandas dataframe med klimadata
        
    Returns
    ----------
        df
            Pandas dataframe der dager med nedbør under 0.2mm og temperatur blir fjerna




.. py:function:: rullande_3dogn_nedbor(dataframe: pd.DataFrame) -> pd.DataFrame:
    
    Tar in klimadataframe og returnerer med ny kollonne med utrekna 3 døgs nedbør basert på døgnnedbør
    
    Parameters
    ----------
        dataframe
            Pandas dataframe med klimadata
        
    Returns
    ----------
        df
            Pandas dataframe med ny kollonne med utrekna 3 døgs nedbør basert på døgnnedbør
    



.. py:function:: plot_ekstremverdier_3dsno(df: pd.DataFrame, ax1=None):
    
    Tilpasset funksjon for utrekning av klimadata
    
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
