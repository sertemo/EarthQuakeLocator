"""Módulo principal"""

from datetime import datetime
from datetime import timedelta
from typing import Any

import plotly.express as pe
import requests
import streamlit as st
from streamlit_plotly_events import plotly_events

starttime = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
endtime = datetime.strftime(datetime.today(), "%Y-%m-%d")
URL_BASE = "https://earthquake.usgs.gov/fdsnws/event/1/"
query = f"query?format=geojson&starttime={starttime}&endtime={endtime}"
URL = URL_BASE + query


@st.cache_data(show_spinner=False)
def make_request(url: str) -> Any | None:
    """Lanza la request y devuelve una respuesta
    en formato json

    Parameters
    ----------
    url : str
        _description_

    Returns
    -------
    requests.Response
        _description_
    """
    response = requests.get(url)

    if response.status_code != 200:
        print(response)
        print(response.status_code)
        return None

    return response.json()


def main() -> None:
    # Configuración de la app
    st.set_page_config(
        page_title="EarthQuake Locator",
        page_icon="🌎",
        layout="wide",
        initial_sidebar_state="auto",
    )
    st.title("EarthQuake Locator")
    st.subheader(
        "Muestra en un mapamundi todos los terremotos ocurridos\
                en los últimos 2 días"
    )

    data = make_request(URL)
    if data is None:
        st.error("Se ha producido un error al lanzar la petición.")
        st.stop()

    terremotos_dict = data["features"]
    terremotos_cantidad = len(terremotos_dict)
    terremotos_title = [d["properties"]["title"] for d in terremotos_dict]
    terremotos_mag = [max(0, d["properties"]["mag"]) for d in terremotos_dict]
    terremotos_long = [d["geometry"]["coordinates"][0] for d in terremotos_dict]
    terremotos_lat = [d["geometry"]["coordinates"][1] for d in terremotos_dict]

    fig = pe.scatter_geo(
        lat=terremotos_lat,
        lon=terremotos_long,
        # text=terremotos_title,
        hover_name=terremotos_title,
        size=terremotos_mag,
        size_max=10,
        opacity=0.7,
        projection="natural earth",
        color_continuous_scale="ylorrd",  # TODO queda aplicar este color a los puntos
        title=f"{terremotos_cantidad} Terremotos mundiales entre {starttime} y {endtime}",
    )

    plotly_events(fig, click_event=True)


if __name__ == "__main__":
    main()
