import tkinter as tk
from tkinter import ttk
from googletrans import Translator, LANGUAGES

# Create the main app window
root = tk.Tk()
root.title("Language Translator")
root.geometry("500x400")
root.configure(bg='white')

# Translator object
translator = Translator()

# Get languages list
language_choices = list(LANGUAGES.values())
lang_to_code = {v: k for k, v in LANGUAGES.items()}

# Heading
tk.Label(root, text="Language Translator", font=("Arial", 18, "bold"), bg='white').pack(pady=10)

# Input text
input_label = tk.Label(root, text="Enter text:", bg='white')
input_label.pack()
input_text = tk.Text(root, height=5, width=50)
input_text.pack(pady=5)

# Source language
src_lang_label = tk.Label(root, text="From:", bg='white')
src_lang_label.pack()
src_lang = ttk.Combobox(root, values=language_choices)
src_lang.set("english")
src_lang.pack(pady=2)

# Target language
dest_lang_label = tk.Label(root, text="To:", bg='white')
dest_lang_label.pack()
dest_lang = ttk.Combobox(root, values=language_choices)
dest_lang.set("french")
dest_lang.pack(pady=2)

# Output
output_label = tk.Label(root, text="Translated text:", bg='white')
output_label.pack()
output_text = tk.Text(root, height=5, width=50, state='disabled')
output_text.pack(pady=5)

# Translate function
def translate_text():
    src = lang_to_code.get(src_lang.get(), 'en')
    dest = lang_to_code.get(dest_lang.get(), 'fr')
    text = input_text.get("1.0", tk.END).strip()
    
    try:
        translated = translator.translate(text, src=src, dest=dest)
        output_text.configure(state='normal')
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated.text)
        output_text.configure(state='disabled')
    except Exception as e:
        output_text.configure(state='normal')
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Error: {e}")
        output_text.configure(state='disabled')

# Translate button
translate_btn = tk.Button(root, text="Translate", command=translate_text, bg='#0078D4', fg='white', font=('Arial', 12, 'bold'))
translate_btn.pack(pady=10)

root.mainloop()
