def get_text(widget) -> str:
    """Return all text from a Tkinter Text widget without the trailing newline."""
    return widget.get("1.0", "end-1c")


def set_text(widget, value: str) -> None:
    """Replace all text in a Tkinter Text widget."""
    widget.delete("1.0", "end")
    widget.insert("1.0", value)


def clear_text(widget) -> None:
    """Clear all text in a Tkinter Text widget."""
    widget.delete("1.0", "end")
