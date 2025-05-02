import nltk
import random
import string
import tkinter as tk
from tkinter import scrolledtext
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

#NLTK Setup
nltk.download('punkt')
nltk.download('wordnet')


lemmatizer = WordNetLemmatizer()

def preprocess(sentence):
    sentence = sentence.lower()
    words = word_tokenize(sentence)
    words = [lemmatizer.lemmatize(w) for w in words if w not in string.punctuation]
    return words

#FAQ Questions and Answers
faq_data = {
    "what is your return policy": "Our return policy allows returns within 30 days of purchase with a valid receipt.",
    "how can i contact customer support": "You can contact customer support via email at support@example.com or call 123-456-7890.",
    "what payment methods do you accept": "We accept Visa, MasterCard, PayPal, and Apple Pay.",
    "do you ship internationally": "Yes, we ship to most countries worldwide. Shipping fees may apply.",
    "how do i track my order": "After your order is shipped, you'll receive a tracking number via email.",
    "can i change my order": "You can change your order within 24 hours of placing it. Please contact customer support.",
    "what is the warranty period": "Our products come with a one-year warranty against manufacturing defects.",
    "do you offer gift cards": "Yes, we offer gift cards in various denominations. You can purchase them on our website.",
    "how do i reset my password": "To reset your password, go to the login page and click on 'Forgot Password'.",
    "where can i find size charts": "Size charts are available on each product page under the 'Size Guide' section.",
    "what is your privacy policy": "Our privacy policy outlines how we collect, use, and protect your personal information.",
    "how do i unsubscribe from emails": "To unsubscribe, click the 'Unsubscribe' link at the bottom of our emails.",
}

def get_response(user_input):
    user_words = preprocess(user_input)
    best_match = None
    highest_score = 0
    for question, answer in faq_data.items():
        question_words = preprocess(question)
        score = len(set(user_words) & set(question_words))
        if score > highest_score:
            highest_score = score
            best_match = answer
    if highest_score == 0:
        return "Sorry, I couldn't understand your question."
    else:
        return best_match


def send_message():
    user_input = entry.get()
    if user_input.strip() != "":
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, "You: " + user_input + "\n")
        response = get_response(user_input)
        chat_window.insert(tk.END, "Bot: " + response + "\n\n")
        chat_window.config(state=tk.DISABLED)
        entry.delete(0, tk.END)

root = tk.Tk()
root.title("FAQ Chatbot")

chat_window = scrolledtext.ScrolledText(root, width=60, height=20, state=tk.DISABLED)
chat_window.pack(padx=10, pady=10)

entry = tk.Entry(root, width=50)
entry.pack(padx=10, pady=5)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

root.mainloop()
