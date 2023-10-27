import os
import io
import pandas as pd
import streamlit as st
from gcp import get_storage_client
from google.cloud.exceptions import NotFound
from google.cloud import storage


import footer
from utils import display_icon

def main():
    # Charger le contenu du fichier CSS
    with open('style.css', 'r') as css_file:
        css = css_file.read()

    # Afficher le contenu CSS dans la page Streamlit
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    # Afficher l'icône pour la page avec le titre personnalisé
    display_icon("Exports", "Exportations des fichiers")


    # Utiliser le séparateur horizontal avec la classe CSS personnalisée
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    st.markdown(f'<p class="period-text">Merci de ne pas utiliser pour le moment les pages où il est noté : </p>' , unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align:center;">
            <h2 style="color:red;">🚧 Développement en cours 🚧</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    #########################################################################
    ############################## EN COURS #################################
    #########################################################################
    footer.display()

if __name__ == "__main__":
    main()
