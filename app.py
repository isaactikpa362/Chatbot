import streamlit as st
import google.generativeai as genai

# 🔽 Configuration de l'API Gemini (Google)
genai.configure(api_key="AIzaSyDjYySZqgpDZElWKLKP_lGFptqEGpO_e1E")  # ⚠️ Pense à sécuriser ta clé

model = genai.GenerativeModel("gemini-1.5-flash")  # ou "gemini-pro"

# 🔽 Fonction d'appel à Gemini
def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Erreur Gemini : {str(e)}"

# 🔽 Fonction principale du chatbot hybride
def chatbot(query):
    best_sentence, similarity = get_most_relevant_sentence(query)
    if similarity < 0.2:
        return ask_gemini(query)
    else:
        return best_sentence

# 🔽 Interface Streamlit
def main():
    st.title("🤖 Mon Chatbot Intelligent (texte + Gemini)")
    st.write("Pose une question sur le texte fourni. Gemini prend le relais si besoin.")

    user_input = st.text_input("Vous :")

    if st.button("Envoyer"):
        if user_input.strip() == "":
            st.warning("Veuillez écrire une question.")
        else:
            with st.spinner("Réflexion en cours..."):
                reponse = chatbot(user_input)
                st.markdown(f"**Chatbot :** {reponse}")

# 🔽 Point d'entrée du script
if __name__ == "__main__":
    main()
