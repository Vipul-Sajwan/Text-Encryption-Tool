import tkinter as tk
from tkinter import messagebox, ttk

import aes_encrypt
import des_encrypt
import rsa_encrypt
from utils import clear_text, get_text, set_text


class TextEncryptionApp:
    """Tkinter GUI for AES, DES, and RSA text encryption."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Text Encryption Tool")
        self.root.geometry("780x620")
        self.root.minsize(720, 560)
        self.root.configure(bg="#15191f")

        self.algorithm_var = tk.StringVar(value="AES")

        self._configure_styles()
        self._build_layout()

    def _configure_styles(self) -> None:
        """Apply a compact dark theme to common Tkinter widgets."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#15191f", foreground="#f2f5f8", font=("Segoe UI", 10))
        style.configure("TButton", background="#2f80ed", foreground="#ffffff", padding=7, font=("Segoe UI", 10))
        style.map("TButton", background=[("active", "#1f6fd1")])
        style.configure("TCombobox", fieldbackground="#222833", background="#222833", foreground="#111111")

    def _build_layout(self) -> None:
        """Create and arrange all GUI widgets."""
        main_frame = tk.Frame(self.root, bg="#15191f", padx=16, pady=14)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Text Encryption Tool", font=("Segoe UI", 18, "bold")).grid(
            row=0, column=0, columnspan=4, sticky="w", pady=(0, 12)
        )

        ttk.Label(main_frame, text="Algorithm").grid(row=1, column=0, sticky="w")
        algorithm_menu = ttk.Combobox(
            main_frame,
            textvariable=self.algorithm_var,
            values=("AES", "DES", "RSA"),
            state="readonly",
            width=18,
        )
        algorithm_menu.grid(row=1, column=1, sticky="w", padx=(8, 18))

        ttk.Label(
            main_frame,
            text="Secret Key / RSA Public or Private Key (AES: 16, 24, or 32 characters)",
        ).grid(row=2, column=0, columnspan=4, sticky="w", pady=(12, 0))
        self.key_text = tk.Text(
            main_frame,
            height=4,
            bg="#222833",
            fg="#f8fafc",
            insertbackground="#ffffff",
            relief="flat",
            wrap="word",
            font=("Consolas", 9),
        )
        self.key_text.grid(row=3, column=0, columnspan=4, sticky="ew", pady=(6, 8))

        ttk.Button(main_frame, text="Generate RSA Keys", command=self.generate_rsa_keys).grid(
            row=4, column=0, sticky="ew", pady=(4, 8)
        )
        ttk.Button(main_frame, text="Encrypt", command=self.encrypt).grid(row=4, column=1, sticky="ew", padx=8, pady=(4, 8))
        ttk.Button(main_frame, text="Decrypt", command=self.decrypt).grid(row=4, column=2, sticky="ew", padx=8, pady=(4, 8))
        ttk.Button(main_frame, text="Clear", command=self.clear_all).grid(row=4, column=3, sticky="ew", pady=(4, 8))

        ttk.Label(main_frame, text="Input Text").grid(row=5, column=0, columnspan=4, sticky="w")
        self.input_text = tk.Text(
            main_frame,
            height=9,
            bg="#222833",
            fg="#f8fafc",
            insertbackground="#ffffff",
            relief="flat",
            wrap="word",
            font=("Consolas", 10),
        )
        self.input_text.grid(row=6, column=0, columnspan=4, sticky="nsew", pady=(6, 12))

        ttk.Label(main_frame, text="Output Text").grid(row=7, column=0, columnspan=4, sticky="w")
        self.output_text = tk.Text(
            main_frame,
            height=9,
            bg="#222833",
            fg="#dbeafe",
            insertbackground="#ffffff",
            relief="flat",
            wrap="word",
            font=("Consolas", 10),
        )
        self.output_text.grid(row=8, column=0, columnspan=4, sticky="nsew", pady=(6, 12))

        ttk.Button(main_frame, text="Copy Output", command=self.copy_output).grid(row=9, column=3, sticky="ew")

        for i in range(4):
            main_frame.columnconfigure(i, weight=1)
        main_frame.rowconfigure(6, weight=1)
        main_frame.rowconfigure(8, weight=1)

    def _run_crypto_action(self, action: str) -> None:
        """Run the selected encryption or decryption function and show errors cleanly."""
        algorithm = self.algorithm_var.get()
        source_text = get_text(self.input_text)
        key = get_text(self.key_text)

        try:
            if algorithm == "AES":
                result = aes_encrypt.encrypt_text(source_text, key) if action == "encrypt" else aes_encrypt.decrypt_text(source_text, key)
            elif algorithm == "DES":
                result = des_encrypt.encrypt_text(source_text, key) if action == "encrypt" else des_encrypt.decrypt_text(source_text, key)
            else:
                result = rsa_encrypt.encrypt_text(source_text, key) if action == "encrypt" else rsa_encrypt.decrypt_text(source_text, key)

            set_text(self.output_text, result)
        except ValueError as exc:
            messagebox.showerror("Crypto Error", str(exc))
        except Exception as exc:
            messagebox.showerror("Unexpected Error", f"Something went wrong: {exc}")

    def encrypt(self) -> None:
        """Encrypt input text using the selected algorithm."""
        self._run_crypto_action("encrypt")

    def decrypt(self) -> None:
        """Decrypt input text using the selected algorithm."""
        self._run_crypto_action("decrypt")

    def generate_rsa_keys(self) -> None:
        """Generate RSA keys and place them in the output area for copying."""
        public_key, private_key = rsa_encrypt.generate_key_pair()
        self.algorithm_var.set("RSA")
        set_text(self.key_text, public_key)
        set_text(self.output_text, f"PUBLIC KEY:\n{public_key}\n\nPRIVATE KEY:\n{private_key}")
        messagebox.showinfo("RSA Keys Generated", "Public key was placed in the key field. Save the private key from the output area.")

    def clear_all(self) -> None:
        """Clear input, output, and key fields."""
        clear_text(self.input_text)
        clear_text(self.key_text)
        clear_text(self.output_text)

    def copy_output(self) -> None:
        """Copy the output text to the system clipboard."""
        output = get_text(self.output_text)
        if not output:
            messagebox.showwarning("Copy Output", "There is no output to copy.")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(output)
        messagebox.showinfo("Copy Output", "Output copied to clipboard.")
