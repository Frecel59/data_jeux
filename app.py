# Importation des bibliothèques nécessaires
import streamlit as st
from dotenv import load_dotenv
import os

# Utilisation de toute la largeur de l'écran
st.set_page_config(
    page_title="Pasino / MAS & JT",
    page_icon="img/logo_pasino.png",
    layout="wide"
)


# Pages avec leurs icônes respectives
pages = {
    "Informations": "📋",
    "Exports": "📤",

}

def display_app_content():
    # Logo du Pasnio
    st.sidebar.image('img/logo_pasino.png')

    # Utiliser une variable de session pour stocker la dernière page
    # Par défaut, aucune page sélectionnée
    selected_page = st.session_state.get("selected_page", "Informations")

    # Afficher le menu
    st.sidebar.title("Restauration")
    selected_page = st.sidebar.radio(
        "Sélectionnez une page",
        list(pages.keys()),
        format_func=lambda page: f"{pages[page]} {page}"
    )

    # Mettre à jour la variable de session
    st.session_state.selected_page = selected_page

    # Afficher la page sélectionnée
    if selected_page == "Informations":
        import infos
        infos.main()
    elif selected_page == "Exports":
        import exports
        exports.main()



    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    st.sidebar.markdown("<br>", unsafe_allow_html=True)


    # Logo du Partouche
    st.sidebar.image('img/logo_p_partouche.png', width=30)

def main():
    # Charger le contenu du fichier CSS
    with open('style.css', 'r') as css_file:
        css = css_file.read()

    # Afficher le contenu CSS dans la page Streamlit
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    # # Vérifiez si l'utilisateur est déjà authentifié
    # if st.session_state.get("authenticated", False):
    #     display_app_content()
    # else:
    #     # Logo de l'entreprise
    #     st.sidebar.image('img/logo_pasino.png')
    #     st.title("Authentification")
    #     st.write("Veuillez entrer le mot de passe pour accéder à l'application.")

    #     col_pass1, col_pass2, col_pass3 = st.columns([0.2, 0.4, 0.4])
    #     with col_pass1:
    #         # Demander le mot de passe à l'utilisateur
    #         pwd = st.text_input("Entrez le mot de passe :", type="password")
    #         if st.button("Se connecter"):
    #             stored_pwd = st.secrets["PASSWORD"]
    #             if pwd == stored_pwd:
    #                 st.session_state.authenticated = True
    #                 # Rafraîchir la page après authentification réussie
    #                 st.rerun()
    #             else:
    #                 st.error("Mot de passe incorrect.")

    # Charger les variables d'environnement depuis le fichier .env
    load_dotenv()

    # Vérifiez si l'utilisateur est déjà authentifié
    if st.session_state.get("authenticated", False):
        display_app_content()
    else:
        # Logo de l'entreprise
        st.sidebar.image('img/logo_pasino.png')
        st.title("Authentification")
        st.write("Veuillez entrer le mot de passe pour accéder à l'application.")

        col_pass1, col_pass2, col_pass3 = st.columns([0.2, 0.4, 0.4])
        with col_pass1:
            # Demander le mot de passe à l'utilisateur
            pwd = st.text_input("Entrez le mot de passe :", type="password")
            if st.button("Se connecter"):
                stored_pwd = os.getenv('PASSWORD')
                if pwd == stored_pwd:
                    st.session_state.authenticated = True
                    # Rafraîchir la page après authentification réussie
                    st.rerun()
                else:
                    st.error("Mot de passe incorrect.")

if __name__ == "__main__":
    main()
