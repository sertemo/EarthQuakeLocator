"""Módulo principal"""

from datetime import datetime
from datetime import timedelta

import pandas as pd
import plotly.express as pe
import streamlit as st

from src.earthquakelocator.request import make_request


class EarthquakeApp:
    def __init__(self) -> None:
        self.starttime = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
        self.starttime_title = (datetime.now() - timedelta(days=2)).strftime("%d/%m/%Y")
        self.endtime = datetime.strftime(datetime.today(), "%Y-%m-%d")
        self.endtime_title = datetime.strftime(datetime.today(), "%d/%m/%Y")
        self.URL_BASE = "https://earthquake.usgs.gov/fdsnws/event/1/"
        self.query = (
            f"query?format=geojson&starttime={self.starttime}&endtime={self.endtime}"
        )
        self.URL = self.URL_BASE + self.query

    def main(self) -> None:
        # Configuración de la app
        st.set_page_config(
            page_title="EarthQuake Locator",
            page_icon="🌎",
            layout="centered",
            initial_sidebar_state="auto",
        )
        st.title("EarthQuake Locator")
        st.subheader(
            "Muestra un mapa interactivo con todos los terremotos ocurridos\
                    en los últimos 2 días"
        )

        self.data = make_request(self.URL)
        if self.data is None:
            st.error("Se ha producido un error al lanzar la petición.")
            st.stop()

        terremotos_dict = self.data["features"]
        terremotos_cantidad = len(terremotos_dict)
        self.df = pd.DataFrame(
            {
                "title": [d["properties"]["title"] for d in terremotos_dict],
                "magnitude": [max(0, d["properties"]["mag"]) for d in terremotos_dict],
                "longitude": [d["geometry"]["coordinates"][0] for d in terremotos_dict],
                "latitude": [d["geometry"]["coordinates"][1] for d in terremotos_dict],
                "depth": [d["geometry"]["coordinates"][2] for d in terremotos_dict],
            }
        )

        self.fig = pe.scatter_geo(
            self.df,
            lat="latitude",
            lon="longitude",
            hover_name="title",
            size="magnitude",
            size_max=10,
            opacity=0.7,
            projection="natural earth",
            color="magnitude",
            color_continuous_scale="ylorrd",
            title=f"{terremotos_cantidad} Terremotos producidos entre {self.starttime_title} y {self.endtime_title}",
            hover_data={"magnitude": ":.2f", "depth": ":.2f km"},
        )
        self.fig.update_layout(
            width=1000,  # Ancho del gráfico en píxeles
            height=600,
            hoverlabel=dict(
                bgcolor="#fee691",
                font_size=16,
                font_family="Rockwell",
                font_color="black",
            ),
        )

        st.plotly_chart(self.fig, use_container_width=True)


if __name__ == "__main__":
    app = EarthquakeApp()
    app.main()
