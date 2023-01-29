Plotfunksjoner
-------------------------------
Forklaring på dei forskjellige funksjoner som genererer plot.



.. py:function:: plot_normaler(klima: pd.DataFrame, ax1=None) -> plt.Axes:
    
    Tar imot klimadataframe, og returnerer ax plotteobjekt fra matplotlib. 
    Funksjonen plotter normalverdier for nedbør og temperatur for perioden 1991-2020.


    Kan kombineres i samleplot, eller stå aleine. 
    Finnes ein søsterfunksjon som skriver ut tall på plottet. 

    Parameters
    ----------
        klima
            Klimadataframe fra klimadata.py
        
    Returns
    ----------
        ax1
            Plotteobjekt fra matplotlib

    


.. py:function:: normaler_annotert(klima: pd.DataFrame, ax1=None) -> plt.Axes:
    
    Tar imot klimadataframe, og returnerer ax plotteobjekt fra matplotlib. 
    Funksjonen plotter normalverdier for nedbør og temperatur for perioden 1991-2020.
    Kan kombineres i samleplot, eller stå aleine. 
    Finnes ein søsterfunksjon uten tall på plottet.
    
    Parameters
    ----------
        klima
            Klimadataframe fra klimadata.py
        
    Returns
    ----------
        ax1
            Plotteobjekt fra matplotlib

    
    TODO: Kan samkøyrast med generell normalplot
    

.. py:function::  plot_aarsnedbor(df: pd.DataFrame, ax1=None) -> plt.Axes:
    
    Tar inn klimadataframe og returnerer plot for snødjupne
    Plottet bruker parameteren rr - Døgnnedbør v2.0 - mm frå NVE api
    Denne returnerer døgnnedbør i mm
    Se https://senorge.no/Models for mer informasjon om måten data er generert

    Plottet tar ut snittverdier for normalperiode 1961-1990 og 1991-2020 samt for heile perioden.
    Det blir også rekna ut ein trend for heile datasettet.
    
    Parameters
    ----------
        df
            pandas dataframe med klimadata

    Returns
    -------
        ax1
            Matplotlib axes objekt med døgnnedbør plot
    
    


.. py:function::  snodjupne(df: pd.DataFrame, ax1=None) -> plt.Axes:
    
    Tar inn klimadataframe og returnerer plot for snødjupne
    
    Plottet bruker parameteren sd - Snødybde v2.0.1 frå NVE api.
    Denne returnerer snødybde i cm.

    Se https://senorge.no/Models for meir informasjon om måten data er generert

    Plottet tar ut snittverdier for normalperiode 1961-1990 og 1991-2020 samt for heile perioden.
    Det blir også rekna ut ein trend for heile datasettet.
    
    Parameters
    ----------
        df
            pandas dataframe med klimadata

    Returns
    -------
        ax1
            Matplotlib axes objekt med snødjupne plot
    
    


.. py:function::  nysnodjupne_3d(df: pd.DataFrame, ax1=None) -> plt.Axes:
    
    Tar inn klimadataframe og returnerer plot for 3 døgns nysnødjupne

    Plottet bruker parameteren sdfsw3d - Nynsødybde 3 døgn frå NVE api

    Se https://senorge.no/Models for mer informasjon om måten data er generert
    Det anbefales å sette seg inn i måten datasettet regner om frå mm vann til cm snø.

    Plottet tar ut snittverdier for normalperiode 1961-1990 og 1991-2020 samt for heile perioden.
    Det blir også rekna ut ein trend for heile datasettet.
    
    Parameters
    ----------
        df
            pandas dataframe med klimadata

    Returns
    -------
        ax1
            Matplotlib axes objekt med snødjupne plot
    
    


.. py:function::  snomengde(df: pd.DataFrame, ax1=None) -> plt.Axes:
    Funksjon for å plotte snomengde i løpet av året for normalperiode 1991-2020
    
    Funksjonen filtrerer ut data for normalperiode 1991-2020.
    Funksjonen glatter ut plottet ved å bruke 7-dagers glidende snitt.
    Deretter beregnes snitt, max og min verdier for kvar dag i året, og legges til i en ny dataframe.

    Parameters
    ----------
        df
            Klimadataframe
        ax1
            Plott-objekt
    
    Returns
    -------
        ax1
            Plott-objekt med snødager
        ax2
            Plott-objekt med temperatur

   


.. py:function::  vind(vind_df: pd.DataFrame) -> plt.Axes:
    Funksjon for å plotte vind mot nedbør og snø

    Plottet lager 3 subplots:
        1. Vindrose for vindretning uansett nedbør eller ikkje, delt inn i vindstyrker
        2. Vindrose for vindretning med regn, delt inn i mm regn 
        3. Vindrose for vindretning med nynsø siste døgn (fsw), delt inn i cm snø

    Ved tolking av vindrose må ein både sjå på % antall dager, men også på kva mengde som kjem ved kvar vindretning
    det kan f.eks være flest dager frå vest, men dagene med virkelig snøfall kan komme fra andre retninger

    Parameters
    ----------
        vind_df
            Dataframe med vinddata fra mars 2018 til mars 2022
        
    Returns
    -------
        fig
            Plott-objekt med 3 subplot
    

    


.. py:function::  klimaoversikt(df: pd.DataFrame, lokalitet: str, annotert: bool) -> plt.Figure:
    Funksjonen lager sampleplot
    
    Parameters
    ----------
        df
            Dataframe med klimadata
        
        lokalitet
            Navn på klimapunktet
        
        annotert
            Boolsk verdi som avgjør om det skal lages annotert plot eller ikkje
        
        Returns
        -------
            fig
                Plott-objekt med 4 subplot
     


.. py:function::  klima_sno_oversikt(df, lokalitet, annotert):
    Funksjonen lager sampleplot

    Parameters
    ----------
        df
            Dataframe med klimadata

        lokalitet
            Navn på klimapunktet

        annotert
            Boolsk verdi som avgjør om det skal lages annotert plot eller ikkje

    Returns
     -------
        fig
            Plott-objekt med 6 subplot
    


.. py:function::  plot_ekstremverdier_3dsno(df, ax1=None):
    maximal = maxdf(df)
    liste = maximal["sdfsw3d"].tolist()
    array = np.array(liste)
    model = e.Gumbel(array, fit_method="mle", ci=0.05, ci_method="delta")

    if ax1 is None:
        ax1 = plt.gca()

    return model.plot_return_values("3ds")


.. py:function::  ekstrem_3d_sno_oversikt(df):
    fig = plt.figure(figsize=(20, 8))

    ax1 = fig.add_subplot(121)
    ax1, ax2 = nysnodjupne_3d(df)

    ax3 = fig.add_subplot(122)
    ax3 = plot_ekstremverdier_3dsno(df)

    return fig
