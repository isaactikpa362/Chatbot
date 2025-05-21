import streamlit as st
import nltk
import string
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import google.generativeai as genai

# 🔽 Initialisation et téléchargements NLTK
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')

# 🔽 Lecture du texte source
with open("/home/isaac-tikpa/Bureau/Chatbot/corpus.txt", 'r', encoding='utf-8') as f:
    data = f.read().replace('\n', ' ')

# 🔽 Tokenisation en phrases
sentences = sent_tokenize(data)

# 🔽 Préparation outils NLTK
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('french'))

# 🔽 Prétraitement d'une phrase
def preprocess(sentence):
    words = word_tokenize(sentence)
    words = [word.lower() for word in words if word.lower() not in stop_words and word not in string.punctuation]
    words = [lemmatizer.lemmatize(word) for word in words]
    return words

# 🔽 Corpus prétraité
corpus = [preprocess(sentence) for sentence in sentences]

# 🔽 Fonction de similarité de Jaccard
def get_most_relevant_sentence(query):
    query_processed = preprocess(query)
    max_similarity = 0
    best_sentence = ""
    for i, sentence in enumerate(corpus):
        similarity = len(set(query_processed).intersection(sentence)) / float(len(set(query_processed).union(sentence)))
        if similarity > max_similarity:
            max_similarity = similarity
            best_sentence = sentences[i]
    return best_sentence, max_similarity

# 🔽 Configuration de l'API Gemini (Google)
genai.configure(api_key="AIzaSyDjYySZqgpDZElWKLKP_lGFptqEGpO_e1E")

model = genai.GenerativeModel("gemini-1.5-flash")  # ou gemini-pro

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
                st.markdown(f"*Chatbot :* {reponse}")

if __name__ == "__main__":

    main()
