import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from dotenv import load_dotenv
from google import genai

load_dotenv()
API_KEY = os.getenv("AQ.AbRN6JG5Pdkl26vatzlGzOrhpOu1mj1qu8fK0RttlqjJK4_ow", "").strip()

class JarvisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JARVIS • Personal AI Assistant")
        self.root.geometry("900x680")
        self.root.minsize(650, 500)
        self.root.configure(bg="#07111f")
        self.client = None
        self.history = []
        self.busy = False

        if API_KEY:
            try:
                self.client = genai.Client(api_key=API_KEY)
            except Exception as exc:
                self.after_status(f"Could not initialize Gemini: {exc}")

        self.build_ui()
        self.add_message("JARVIS", "Hello! I'm JARVIS. Type a message below to begin.")
        if not API_KEY:
            self.after_status("API key missing. Add GEMINI_API_KEY to your .env file and restart.")

    def build_ui(self):
        header = tk.Frame(self.root, bg="#0b1b2e", padx=22, pady=16)
        header.pack(fill="x")
        tk.Label(header, text="J A R V I S", font=("Segoe UI", 22, "bold"),
                 fg="#53dcff", bg="#0b1b2e").pack(anchor="w")
        tk.Label(header, text="PERSONAL AI ASSISTANT  •  GEMINI POWERED",
                 font=("Segoe UI", 9), fg="#9ab7cc", bg="#0b1b2e").pack(anchor="w", pady=(3, 0))

        self.status = tk.Label(self.root, text="● Ready", anchor="w",
                               bg="#07111f", fg="#79e6b1", padx=22, pady=8,
                               font=("Segoe UI", 9))
        self.status.pack(fill="x")

        self.chat = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state="disabled", bg="#0a1726",
            fg="#e5f4ff", insertbackground="white", relief="flat",
            font=("Segoe UI", 11), padx=16, pady=14
        )
        self.chat.pack(fill="both", expand=True, padx=18, pady=(0, 12))
        self.chat.tag_config("name", foreground="#53dcff", font=("Segoe UI", 10, "bold"))
        self.chat.tag_config("body", foreground="#e5f4ff")

        bottom = tk.Frame(self.root, bg="#07111f", padx=18, pady=12)
        bottom.pack(fill="x")
        self.entry = tk.Text(bottom, height=3, wrap="word", bg="#102338", fg="#f3f9ff",
                             insertbackground="white", relief="flat", font=("Segoe UI", 11),
                             padx=10, pady=9)
        self.entry.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.entry.bind("<Control-Return>", lambda _event: self.send_message())
        self.send_btn = tk.Button(bottom, text="SEND  ➤", command=self.send_message,
                                  bg="#087da5", fg="white", activebackground="#0b9bc9",
                                  activeforeground="white", relief="flat", padx=18,
                                  font=("Segoe UI", 10, "bold"), cursor="hand2")
        self.send_btn.pack(side="right", fill="y")

        footer = tk.Frame(self.root, bg="#07111f", padx=22, pady=(0, 10))
        footer.pack(fill="x")
        tk.Label(footer, text="Ctrl + Enter to send  •  Do not share your API key",
                 bg="#07111f", fg="#6d8ba3", font=("Segoe UI", 8)).pack(anchor="w")

    def after_status(self, text):
        if hasattr(self, "status"):
            self.root.after(0, lambda: self.status.config(text="● " + text, fg="#ffcc80"))
        else:
            print(text)

    def add_message(self, speaker, text):
        self.chat.configure(state="normal")
        self.chat.insert("end", f"{speaker}\n", "name")
        self.chat.insert("end", text + "\n\n", "body")
        self.chat.configure(state="disabled")
        self.chat.see("end")

    def send_message(self):
        prompt = self.entry.get("1.0", "end").strip()
        if not prompt or self.busy:
            return
        self.entry.delete("1.0", "end")
        self.add_message("YOU", prompt)

        if not self.client:
            self.add_message("JARVIS", "Gemini is not configured. Add your API key to the .env file, then restart.")
            return

        self.busy = True
        self.send_btn.configure(state="disabled", text="THINKING…")
        self.status.configure(text="● Thinking…", fg="#53dcff")
        threading.Thread(target=self.ask_gemini, args=(prompt,), daemon=True).start()

    def ask_gemini(self, prompt):
        try:
            self.history.append({"role": "user", "parts": [{"text": prompt}]})
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=self.history,
                config={"system_instruction": (
                    "You are JARVIS, a helpful, polite personal AI assistant. "
                    "Be clear and practical. Do not claim to have performed actions "
                    "outside this chat unless they were actually performed."
                )}
            )
            answer = response.text or "I couldn't generate a text response. Please try again."
            self.history.append({"role": "model", "parts": [{"text": answer}]})
            self.root.after(0, lambda: self.add_message("JARVIS", answer))
            self.root.after(0, lambda: self.status.configure(text="● Connected", fg="#79e6b1"))
        except Exception as exc:
            # Remove the user turn if the API request failed, so history stays usable.
            if self.history and self.history[-1].get("role") == "user":
                self.history.pop()
            msg = f"Sorry, the request failed.\n{exc}\n\nCheck your API key, internet connection, model access, and quota."
            self.root.after(0, lambda: self.add_message("JARVIS", msg))
            self.root.after(0, lambda: self.status.configure(text="● Request failed", fg="#ff9d9d"))
        finally:
            self.busy = False
            self.root.after(0, lambda: self.send_btn.configure(state="normal", text="SEND  ➤"))

def main():
    root = tk.Tk()
    JarvisApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
