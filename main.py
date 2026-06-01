import tkinter as tk

from gui import TextEncryptionApp


def main() -> None:
    """Start the Text Encryption Tool desktop application."""
    root = tk.Tk()
    TextEncryptionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
