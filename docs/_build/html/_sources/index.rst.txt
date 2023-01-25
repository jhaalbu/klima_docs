.. AV-Klima documentation master file, created by
   sphinx-quickstart on Tue Jan 17 11:17:19 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Dokumentasjon av AV-Klima tjenesten
====================================
.. toctree::
   :maxdepth: 2
   :caption: Contents:

Skildring av tjenesten
----------------------
Test

Tjenesten er ein web applikasjon for å forenkle uthenting av klimadata. Den nyttar
seg av eit gridda datasett, dvs eit datasett der det finnes data for kvar 1x1 km rute
av landet.

Fra NVE sin skredfareveileder (https://veileder-skredfareutredning-bratt-terreng.nve.no/)
er det åpna for at gridda data kan vere aktuelle å bruke, særleg der det er langt fra stajonsdata.
Ofte mangler nærliggande stasjonar også f.eks vind, snømengde eller andre aktuelle parametere.

Tjenesten gjer ein spørring til eit NVE API for å hente ut data for ein gitt koordinat. Den 
lager så automatisk til plot med data som er aktuelle i ei skredfarevurdering. Eller andre 
klimanalaysar.

Lenke til NVE api:

http://api.nve.no/doc/gridtimeseries-data-gts/

Lenke til forklaring for generering av datasett:

https://senorge.no/Models

Der er det vidare henvisning til vitenskaplige artiklar som skildrar metodane i detalj


Bruksanvisning
--------------
Appen på web med lenke: https://app-avtools-klima-dev.azurewebsites.net/

Den har enkelt input med trykk i kart, eller innskriving av koordinat.

Videre gir den moglegheit for å velje forskjellige type sampleplot

Klimaoversikt:

- Gjennomsnittleg månedstemperatur og nedbør

- Fordeling av snømengde gjennom året, med snitt, max og min sammen med temperatur

- Åresnedbør tilbake i tid

- Årleg maksimal snødjupne tilbake i tid


Klimaoversikt med 3 døgn snø og returverdi:

Dette gir dei samme plotta som for klimaoversikt me i tilleg

- 3 døgns snø mengde

- Returverdi for 3 døgns snø basert på gumbelfordeling


Dersom ein ynskjer å få verdier plotta ut på plot for gjennomsnittleg måndestemperatur og nedøbr er det mulig å huka av for å vise tall på normalplott


Dersom ein ynskjer ei vindanalyse for klimapunktet kan ein huke av for å køyre klimanalayse. 

Det blir da lasta ned datasett for vind og følgande plott blir generert:
- Vindretning for alle 


Modul for plotting av klimadata
-------------------------------
.. automodule:: klimadata.plot
    :members:


Nedhenting og bearbeiding av klimadata modul
--------------------------------------------
.. automodule:: klimadata.klimadata
    :members:


