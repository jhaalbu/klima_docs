Datanedlasting
--------------------------------------------
Forklaring på dei enkelte funksjoner som genererer klimadata fra NVI sitt api.

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

