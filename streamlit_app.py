'''Enkel webapp for uthenting av klimaanalyser i samband med skredfarevurderinger
Bruker streamlit pakken for å lage webapp fra python script
'''

import streamlit as st
from pyproj import Transformer
from klimadata import klimadata
from klimadata import plot
import folium
from streamlit_folium import st_folium


st.header("AV-Klima")

# Setter liste med parametere brukt i analyse, tenkt å kunne utvides
parameterliste = ["rr", "tm", "sd", "fsw", "sdfsw", "sdfsw3d"]

# For kartbruk må koordinater transformerer mellom lat/lon og UTM
transformer = Transformer.from_crs(4326, 5973)

# Setter opp kartobjekt, med midtpunkt og zoom nivå
m = folium.Map(location=[62.14497, 9.404296], zoom_start=5)
folium.raster_layers.WmsTileLayer(
    url="https://opencache.statkart.no/gatekeeper/gk/gk.open_gmaps?layers=topo4&zoom={z}&x={x}&y={y}",
    name="Norgeskart",
    fmt="image/png",
    layers="topo4",
    attr='<a href="http://www.kartverket.no/">Kartverket</a>',
    transparent=True,
    overlay=True,
    control=True,
).add_to(m)

# Litt knotete måte å hente ut koordinater fra Streamlit, kanskje bedre i nye versjoner av streamlit? Ev. litt bedre måte i rein javascript?
m.add_child(folium.ClickForMarker(popup="Waypoint"))
output = st_folium(m, width=700, height=500)

utm_lat = 0
utm_lon = 0
st.write("Trykk i kartet, eller skriv inn koordinater for å velge klimapunkt.")
st.write(
    "Finn automatisk nærmaste stadnavn dersom det er eit navn innafor 500m radius."
)

# Enkel måte å vente på klikk i kartet
try:
    kart_kord_lat = output["last_clicked"]["lat"]
    kart_kord_lng = output["last_clicked"]["lng"]
    utm_ost, utm_nord = transformer.transform(kart_kord_lat, kart_kord_lng)
    utm_nord = round(utm_nord, 2)
    utm_ost = round(utm_ost, 2)

except TypeError:
    utm_nord = "Trykk i kart, eller skriv inn koordinat"
    utm_ost = "Trykk i kart, eller skriv inn koordinat"

# Lat, lon begrep henger igjen etter gamle versjon av script, trenger opprydding
lat = st.text_input("NORD(UTM 33)", utm_nord)
lon = st.text_input("ØST  (UTM 33)", utm_ost)

# Venter på klikk, og prøver å finne stedsnavn
try:
    navn = klimadata.stedsnavn(utm_nord, utm_ost)["navn"][0]["stedsnavn"][0][
        "skrivemåte"
    ]
except (IndexError, KeyError):
    navn = "Skriv inn navn"

lokalitet = st.text_input("Gi navn til lokalitet", navn)

# Hardkoda start og sluttdato, det er mulig å utvide dette til å la bruker velge, 
# men funksjoner for plotting er ikke utvikla for å håndtere dette
startdato = "1958-01-01"
sluttdato = "2022-12-31"

#Lar brukere velge plotversjoner
plottype = st.radio(
    "Velg plottype", ("Klimaoversikt", "Klimaoversikt med 3 døgn snø og returverdi")
)

#Lar bruker velge om de vil ha annotert normalplot
annotert = st.checkbox("Vis tall på normalplot")

#Lar bruker velge om de vil ha vindanalyse
vind = st.checkbox("Vindanalyse")

#Enkel knapp for å vente med kjøre resten av scriptet før input er registert
knapp = st.button("Vis plott")

if knapp:
    lon = int(float(lon.strip()))
    lat = int(float(lat.strip()))
    df = klimadata.klima_dataframe(lon, lat, startdato, sluttdato, parameterliste)
    st.write(f'Modellhøgden frå punktet er {klimadata.hent_hogde(lon, lat)} moh. Denne kan avvike fra faktisk terrenghøgde.')
    if plottype == "Klimaoversikt":
        st.write("Trykk på pil oppe i høgre hjørne for å utvide plot")
        st.pyplot(plot.klimaoversikt(df, lokalitet, annotert))
        st.download_button(
            "Last ned klimadata",
            df.to_csv().encode("utf-8"),
            "klimadata.csv",
            "text/csv",
            key="download-csv",
        )
    if plottype == "Klimaoversikt med 3 døgn snø og returverdi":
        st.write("Trykk på pil oppe i høgre hjørne for å utvide plot")
        st.pyplot(plot.klima_sno_oversikt(df, lokalitet, annotert))
        st.download_button(
            "Last ned klimadata",
            df.to_csv().encode("utf-8"),
            "klimadata.csv",
            "text/csv",
            key="download-csv",
        )
    if vind:
        st.write("Trykk på pil oppe i høgre hjørne for å utvide plot")
        vind_para = [
            "windDirection10m24h06",
            "windSpeed10m24h06",
            "rr",
            "tm",
            "fsw",
            "rrl",
        ]
        vindslutt = "2022-03-01"
        vindstart = "2018-03-01"
        vind_df = klimadata.klima_dataframe(lon, lat, vindstart, vindslutt, vind_para)
        st.pyplot(plot.vind(vind_df))
        st.download_button(
            "Last ned vinddata",
            vind_df.to_csv().encode("utf-8"),
            "vinddata.csv",
            "text/csv",
            key="download-csv-vind",
        )
        st.write(
            "Vinddata må brukast med forsiktigheit. Vinddata finnes kunn fra mars 2018 - mars 2022. Vinddata bør hentes fra høgaste punkt i området, og ikkje nede i fjord/dalstrøk."
        )
        st.write(
            "Vær særleg obs på at det i områder er få dager med snø for å få fram snøførende vindretning."
        )
st.write(
    "Scriptet henter ned data frå NVE sitt Grid Time Series API, som er visualisert på xgeo.no"
)
st.write("Parametere som er brukt er: ")

#hardcoda inn kva parameter som er brukt
parametere = {
    "rr": "Døgnnedbør v2.0 - mm",
    "tm": "Døgntemperatur v2.0	 - Celcius",
    "sd": "Snødybde v2.0.1 - cm",
    "fsw": "Nysnø siste døgn	 - mm",
    "sdfsw3d": "Nysnødybde 3 døgn - cm",
    "rrl": "Regn - mm",
    "windDirection10m24h06": "Vindretning 10m døgn",
    "windSpeed10m24h06": "Vindhastighet 10m døgn -  m/s",
}
st.json(parametere)
link = "[SeNorge - Snøkart](https://www.nve.no/media/11700/hvordan-lages-sn%C3%B8kartene-i-senorge-og-xgeo.pdf)"
st.write(
    "Sjå link under for forklaring på snødybdeparametere som er brukt i plot for snødybder"
)
st.markdown(link, unsafe_allow_html=True)
st.write("Ved spørsmål eller feil ta kontakt på jan.aalbu@asplanviak.no")
