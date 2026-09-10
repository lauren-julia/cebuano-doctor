# 🩺 Cebuano Doctor
A locally running Cebuano healthcare chatbot using \*\*Google DeepMind Gemma 4\*\*, \*\*MedGemma\*\*, and \*\*Ollama\*\*.


## 📌 Project Overview
Cebuano Doctor is a local AI chatbot that allows users to ask healthcare questions in Cebuano.
The system uses **Gemma 4** to translate the Cebuano question into English, **MedGemma** to generate a medical response in English, and **Gemma 4** again to translate the response back into Cebuano.


## ✨ Features
* Ask healthcare questions in Cebuano
* Cebuano-to-English translation using Gemma 4
* Medical response using MedGemma
* English-to-Cebuano translation using Gemma 4
* Local graphical chat interface
* Chat history within the current session
* View the English translation and medical response
* Runs locally through Ollama


## 🛠️ Technologies
* **Python**
* **Ollama**
* **Gemma 4**
* **MedGemma**
* **Tkinter**


## 💻 Requirements
The following software must be installed:
1. Python
2. Ollama
3. Gemma 4
4. MedGemma


The project currently uses these Ollama models:
```text
gemma4:latest
medgemma:4b
```


## 📥 Installation
### 1. Install the Python Ollama library
```bash
python -m pip install ollama
```

### 2. Check your Ollama models
```bash
ollama list
```
Make sure `gemma4:latest` and `medgemma:4b` are installed.

### 3. Run the application
From the project folder:
```bash
python cebuano\_doctor\_gui.py
```

## 📂 Project Files
### `cebuano\_doctor.py`
Contains the main AI pipeline:

1. Translates Cebuano to English using Gemma 4.
2. Sends the English question to MedGemma.
3. Translates the medical response back to Cebuano using Gemma 4.

### `cebuano\_doctor\_gui.py`
Contains the graphical user interface for the Cebuano Doctor chatbot.


## ⚠️ Medical Disclaimer
This project is intended for **educational and informational purposes only**.
Cebuano Doctor is an AI system and does not replace a qualified healthcare professional. It should not be used as a substitute for professional medical advice, diagnosis, or treatment.
For emergencies or serious symptoms, users should seek appropriate medical care immediately.
