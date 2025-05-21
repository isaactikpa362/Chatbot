import os
import streamlit as st
import google.generativeai as genai

# Récupérer la clé API depuis la variable d'environnement
api_key = os.getenv("AIzaSyDjYySZqgpDZElWKLKP_lGFptqEGpO_e1E")

if api_key is None:
    st.error("Erreur : La clé API Gemini n'est pas définie dans la variable d'environnement GEMINI_API_KEY.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Fonction d'appel à Gemini
def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Erreur Gemini : {str(e)}"

# Fonction principale (directement Gemini)
def chatbot(query):
    return ask_gemini(query)

# Interface Streamlit
def main():
    st.title("🤖 Mon Chatbot Intelligent (Gemini uniquement)")
    st.write("Pose ta question, Gemini répond directement.")

    user_input = st.text_input("Vous :")

    if st.button("Envoyer"):
        if user_input.strip() == "":
            st.warning("Veuillez écrire une question.")
        else:
            with st.spinner("Réflexion en cours..."):
                reponse = chatbot(user_input)
                st.markdown(f"**Chatbot :** {reponse}")

if __name__ == "__main__":
    main()

