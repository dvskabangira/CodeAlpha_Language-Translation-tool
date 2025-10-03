
import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator, LANGUAGES
import pyttsx3
import pyperclip
import tkinter.font as tkFont


class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Translation Tool")
        self.root.geometry("800x600")   # Bigger window
        self.translator = Translator()

        # Define bigger font
        self.text_font = tkFont.Font(family="Arial", size=14)

        # Input Frame 
        input_frame = tk.Frame(root, padx=20, pady=20)
        input_frame.pack(fill="both", expand=True)

        tk.Label(input_frame, text="Enter Text:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.input_text = tk.Text(input_frame, height=10, wrap="word", font=self.text_font)
        self.input_text.pack(fill="both", expand=True)

        # Language Selection
        lang_frame = tk.Frame(root, padx=10, pady=10)
        lang_frame.pack(fill="x")

        tk.Label(lang_frame, text="Source Language:", font=("Arial", 11)).grid(row=0, column=0, sticky="w")
        self.src_lang = ttk.Combobox(lang_frame, values=list(LANGUAGES.values()), width=25)
        self.src_lang.set("english")
        self.src_lang.grid(row=0, column=1, padx=5)

        tk.Label(lang_frame, text="Target Language:", font=("Arial", 11)).grid(row=0, column=2, sticky="w")
        self.dest_lang = ttk.Combobox(lang_frame, values=list(LANGUAGES.values()), width=25)
        self.dest_lang.set("french")
        self.dest_lang.grid(row=0, column=3, padx=5)

        # Buttons 
        btn_frame = tk.Frame(root, pady=10)
        btn_frame.pack()

        tk.Button(btn_frame, text="Translate", font=("Arial", 11), command=self.translate_text).grid(row=0, column=0, padx=15)
        tk.Button(btn_frame, text="Copy", font=("Arial", 11), command=self.copy_text).grid(row=0, column=1, padx=15)
        tk.Button(btn_frame, text="Speak", font=("Arial", 11), command=self.speak_text).grid(row=0, column=2, padx=15)

        # Output Frame 
        output_frame = tk.Frame(root, padx=20, pady=20)
        output_frame.pack(fill="both", expand=True)

        tk.Label(output_frame, text="Translated Text:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.output_text = tk.Text(output_frame, height=10, wrap="word", font=self.text_font)
        self.output_text.pack(fill="both", expand=True)

        # Make translated text blue
        self.output_text.tag_configure("blue_text", foreground="blue")

    def translate_text(self):
        try:
            src = self.src_lang.get().lower()
            dest = self.dest_lang.get().lower()
            text = self.input_text.get("1.0", tk.END).strip()
            if not text:
                messagebox.showwarning("Input Required", "Please enter text to translate.")
                return
            # Get ISO code from language name
            src_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(src)]
            dest_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(dest)]
            translation = self.translator.translate(text, src=src_code, dest=dest_code)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, translation.text, "blue_text")  # Insert in blue
        except Exception as e:
            messagebox.showerror("Error", f"Translation failed:\n{str(e)}")

    def copy_text(self):
        text = self.output_text.get("1.0", tk.END).strip()
        if text:
            pyperclip.copy(text)
            messagebox.showinfo("Copied", "Translated text copied to clipboard!")

    def speak_text(self):
        text = self.output_text.get("1.0", tk.END).strip()
        if text:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()


if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()
