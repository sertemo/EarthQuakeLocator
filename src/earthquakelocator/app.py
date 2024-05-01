"""Módulo principal"""

import streamlit as st

def main() -> None:
    st.title("EarthQuake Locator")
    st.subheader("Muestra en un mapamundi todos los terremotos ocurridos\
                en los últimos 2 días")


if __name__ == '__main__':
    main()