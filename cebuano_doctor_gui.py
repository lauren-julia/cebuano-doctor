
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import re

from cebuano_doctor import (
    translate_to_english,
    get_medical_response,
    translate_to_cebuano
)


BACKGROUND = "#F4F8FB"
BLUE = "#1976D2"
DARK_BLUE = "#0D47A1"
WHITE = "#FFFFFF"
GRAY = "#666666"
GREEN = "#2E7D32"
LIGHT_GREEN = "#E8F5E9"
DARK_GRAY = "#333333"
WARNING_BG = "#FFF8E1"
WARNING_TEXT = "#795548"


last_english_question = ""
last_english_response = ""


def insert_formatted_text(text_widget, text):
    """
    Display basic Markdown formatting in a Tkinter Text widget.

    Supports:
    **bold**
    *italic*
    # headings
    - bullet points
    * bullet points
    """

    lines = text.splitlines()

    for line in lines:

        # --------------------------------------
        # HEADINGS
        # --------------------------------------

        if line.startswith("### "):
            insert_inline_markdown(
                text_widget,
                line[4:],
                "heading3"
            )
            text_widget.insert(tk.END, "\n")
            continue

        if line.startswith("## "):
            insert_inline_markdown(
                text_widget,
                line[3:],
                "heading2"
            )
            text_widget.insert(tk.END, "\n")
            continue

        if line.startswith("# "):
            insert_inline_markdown(
                text_widget,
                line[2:],
                "heading1"
            )
            text_widget.insert(tk.END, "\n")
            continue

        # --------------------------------------
        # BULLET POINTS
        # --------------------------------------

        if line.startswith("- "):
            text_widget.insert(
                tk.END,
                "• ",
                "bullet"
            )

            insert_inline_markdown(
                text_widget,
                line[2:]
            )

            text_widget.insert(
                tk.END,
                "\n"
            )

            continue

        if line.startswith("* ") and not line.startswith("**"):
            text_widget.insert(
                tk.END,
                "• ",
                "bullet"
            )

            insert_inline_markdown(
                text_widget,
                line[2:]
            )

            text_widget.insert(
                tk.END,
                "\n"
            )

            continue

        # --------------------------------------
        # NORMAL TEXT
        # --------------------------------------

        insert_inline_markdown(
            text_widget,
            line
        )

        text_widget.insert(
            tk.END,
            "\n"
        )


def insert_inline_markdown(text_widget, text, default_tag=None):
    """
    Handle inline Markdown such as **bold** and *italic*.
    """

    # Find **bold** and *italic*
    pattern = r"(\*\*(.*?)\*\*|\*(.*?)\*)"

    position = 0

    for match in re.finditer(pattern, text):

        # Insert normal text before formatting
        if match.start() > position:
            text_widget.insert(
                tk.END,
                text[position:match.start()],
                default_tag
            )

        # Bold
        if match.group(2) is not None:
            text_widget.insert(
                tk.END,
                match.group(2),
                "bold"
            )

        # Italic
        elif match.group(3) is not None:
            text_widget.insert(
                tk.END,
                match.group(3),
                "italic"
            )

        position = match.end()

    # Insert remaining text
    if position < len(text):
        text_widget.insert(
            tk.END,
            text[position:],
            default_tag
        )


def ask_doctor():

    question = question_box.get(
        "1.0",
        tk.END
    ).strip()

    if not question:
        messagebox.showwarning(
            "No question",
            "Please enter a Cebuano healthcare question."
        )
        return

    # Clear input
    question_box.delete(
        "1.0",
        tk.END
    )

    # Add user message
    add_user_message(question)

    # Disable button
    ask_button.config(
        state=tk.DISABLED
    )

    status_label.config(
        text="Doctor is thinking..."
    )

    thread = threading.Thread(
        target=process_question,
        args=(question,),
        daemon=True
    )

    thread.start()


def process_question(question):

    try:

        # --------------------------------------
        # STEP 1. Cebuano -> English
        # --------------------------------------

        english_question = translate_to_english(
            question
        )

        # --------------------------------------
        # STEP 2. MedGemma medical response
        # --------------------------------------

        english_response = get_medical_response(
            english_question
        )

        # --------------------------------------
        # STEP 3. English -> Cebuano
        # --------------------------------------

        cebuano_response = translate_to_cebuano(
            english_response
        )

        # Send to GUI
        window.after(
            0,
            lambda: show_doctor_response(
                cebuano_response,
                english_question,
                english_response
            )
        )

    except Exception as error:

        window.after(
            0,
            lambda: show_error(error)
        )


# ==========================================
# CHAT DISPLAY
# ==========================================

def add_user_message(message):

    chat_box.config(
        state=tk.NORMAL
    )

    chat_box.insert(
        tk.END,
        "\nYou\n",
        "user_name"
    )

    insert_formatted_text(
        chat_box,
        message
    )

    chat_box.insert(
        tk.END,
        "\n"
    )

    chat_box.config(
        state=tk.DISABLED
    )

    chat_box.see(
        tk.END
    )


def show_doctor_response(
    cebuano_response,
    english_question,
    english_response
):

    global last_english_question
    global last_english_response

    # Save English information
    last_english_question = english_question
    last_english_response = english_response

    chat_box.config(
        state=tk.NORMAL
    )

    chat_box.insert(
        tk.END,
        "\nCebuano Doctor\n",
        "doctor_name"
    )

    insert_formatted_text(
        chat_box,
        cebuano_response
    )

    chat_box.insert(
        tk.END,
        "\n"
    )

    chat_box.config(
        state=tk.DISABLED
    )

    chat_box.see(
        tk.END
    )

    # Enable translation button
    english_button.config(
        state=tk.NORMAL
    )

    # Enable Ask button
    ask_button.config(
        state=tk.NORMAL
    )

    status_label.config(
        text="Ready"
    )


def show_error(error):

    messagebox.showerror(
        "Error",
        f"Something went wrong:\n\n{error}"
    )

    ask_button.config(
        state=tk.NORMAL
    )

    status_label.config(
        text="Ready"
    )


# ==========================================
# SHOW ENGLISH TRANSLATION
# ==========================================

def show_english():

    if not last_english_question:

        messagebox.showinfo(
            "No translation",
            "Ask the doctor a question first."
        )

        return

    english_window = tk.Toplevel(
        window
    )

    english_window.title(
        "English Translation"
    )

    english_window.geometry(
        "700x550"
    )

    english_window.configure(
        bg=BACKGROUND
    )

    # --------------------------------------
    # TITLE
    # --------------------------------------

    title = tk.Label(
        english_window,
        text="English Translation",
        font=("Arial", 20, "bold"),
        bg=BACKGROUND,
        fg=DARK_BLUE
    )

    title.pack(
        pady=(20, 10)
    )

    # --------------------------------------
    # ENGLISH QUESTION
    # --------------------------------------

    question_label = tk.Label(
        english_window,
        text="English question sent to MedGemma:",
        font=("Arial", 12, "bold"),
        bg=BACKGROUND
    )

    question_label.pack(
        anchor="w",
        padx=25
    )

    question_text = scrolledtext.ScrolledText(
        english_window,
        height=5,
        font=("Arial", 11),
        wrap=tk.WORD,
        bg=WHITE
    )

    question_text.pack(
        fill="x",
        padx=25,
        pady=(5, 20)
    )

    insert_formatted_text(
        question_text,
        last_english_question
    )

    question_text.config(
        state=tk.DISABLED
    )

    # --------------------------------------
    # MEDICAL RESPONSE
    # --------------------------------------

    response_label = tk.Label(
        english_window,
        text="English medical response from MedGemma:",
        font=("Arial", 12, "bold"),
        bg=BACKGROUND
    )

    response_label.pack(
        anchor="w",
        padx=25
    )

    response_text = scrolledtext.ScrolledText(
        english_window,
        height=15,
        font=("Arial", 11),
        wrap=tk.WORD,
        bg=WHITE
    )

    response_text.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=(5, 20)
    )

    insert_formatted_text(
        response_text,
        last_english_response
    )

    response_text.config(
        state=tk.DISABLED
    )


# ==========================================
# NEW CHAT
# ==========================================

def clear_chat():

    global last_english_question
    global last_english_response

    chat_box.config(
        state=tk.NORMAL
    )

    chat_box.delete(
        "1.0",
        tk.END
    )

    chat_box.config(
        state=tk.DISABLED
    )

    last_english_question = ""
    last_english_response = ""

    english_button.config(
        state=tk.DISABLED
    )

    status_label.config(
        text="Ready"
    )


# ==========================================
# MAIN WINDOW
# ==========================================

window = tk.Tk()

window.title(
    "Cebuano Doctor"
)

window.geometry(
    "800x750"
)

window.minsize(
    650,
    600
)

window.configure(
    bg=BACKGROUND
)


# ==========================================
# TITLE
# ==========================================

title = tk.Label(
    window,
    text="🩺 Cebuano Doctor",
    font=("Arial", 24, "bold"),
    bg=BACKGROUND,
    fg=DARK_BLUE
)

title.pack(
    pady=(20, 2)
)


subtitle = tk.Label(
    window,
    text="Local AI healthcare assistant",
    font=("Arial", 11),
    bg=BACKGROUND,
    fg=GRAY
)

subtitle.pack(
    pady=(0, 15)
)


# ==========================================
# CHAT AREA
# ==========================================

chat_box = scrolledtext.ScrolledText(
    window,
    font=("Arial", 12),
    wrap=tk.WORD,
    bg=WHITE,
    padx=15,
    pady=10
)

chat_box.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=(0, 10)
)


# ==========================================
# TEXT STYLES
# ==========================================

chat_box.tag_config(
    "user_name",
    foreground=BLUE,
    font=("Arial", 11, "bold")
)

chat_box.tag_config(
    "user_message",
    foreground=DARK_GRAY,
    font=("Arial", 12)
)

chat_box.tag_config(
    "doctor_name",
    foreground=GREEN,
    font=("Arial", 11, "bold")
)

chat_box.tag_config(
    "doctor_message",
    foreground=DARK_GRAY,
    font=("Arial", 12)
)

chat_box.tag_config(
    "bold",
    font=("Arial", 12, "bold")
)

chat_box.tag_config(
    "italic",
    font=("Arial", 12, "italic")
)

chat_box.tag_config(
    "heading1",
    font=("Arial", 17, "bold"),
    foreground=DARK_BLUE
)

chat_box.tag_config(
    "heading2",
    font=("Arial", 15, "bold"),
    foreground=DARK_BLUE
)

chat_box.tag_config(
    "heading3",
    font=("Arial", 13, "bold"),
    foreground=DARK_BLUE
)

chat_box.tag_config(
    "bullet",
    font=("Arial", 12, "bold"),
    foreground=BLUE
)

chat_box.config(
    state=tk.DISABLED
)


# ==========================================
# STATUS
# ==========================================

status_label = tk.Label(
    window,
    text="Ready",
    font=("Arial", 10),
    bg=BACKGROUND,
    fg=GRAY
)

status_label.pack(
    pady=(0, 5)
)


# ==========================================
# QUESTION INPUT
# ==========================================

input_frame = tk.Frame(
    window,
    bg=BACKGROUND
)

input_frame.pack(
    fill="x",
    padx=25
)


question_box = tk.Text(
    input_frame,
    height=3,
    font=("Arial", 12),
    wrap=tk.WORD
)

question_box.pack(
    side=tk.LEFT,
    fill="both",
    expand=True
)


ask_button = tk.Button(
    input_frame,
    text="Ask\nDoctor",
    font=("Arial", 11, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground=DARK_BLUE,
    activeforeground=WHITE,
    padx=15,
    pady=8,
    cursor="hand2",
    command=ask_doctor
)

ask_button.pack(
    side=tk.RIGHT,
    padx=(10, 0)
)


# ==========================================
# BUTTONS
# ==========================================

button_frame = tk.Frame(
    window,
    bg=BACKGROUND
)

button_frame.pack(
    pady=12
)


english_button = tk.Button(
    button_frame,
    text="Show English Translation",
    font=("Arial", 10),
    command=show_english,
    state=tk.DISABLED,
    padx=10
)

english_button.pack(
    side=tk.LEFT,
    padx=5
)


clear_button = tk.Button(
    button_frame,
    text="New Chat",
    font=("Arial", 10),
    command=clear_chat,
    padx=10
)

clear_button.pack(
    side=tk.LEFT,
    padx=5
)


# ==========================================
# MEDICAL DISCLAIMER
# ==========================================

disclaimer = tk.Label(
    window,
    text=(
        "⚠️ Medical disclaimer: This is for educational and informational "
        "purposes only and does not replace a qualified healthcare professional. "
        "For emergencies or serious symptoms, seek medical care immediately."
    ),
    font=("Arial", 9),
    bg=WARNING_BG,
    fg=WARNING_TEXT,
    wraplength=720,
    justify=tk.CENTER,
    padx=10,
    pady=8
)

disclaimer.pack(
    fill="x",
    padx=25,
    pady=(0, 15)
)


# ==========================================
# START APPLICATION
# ==========================================

window.mainloop()
