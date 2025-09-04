# 🌐 Social Media Wellness Analyzer

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)
![Contributions](https://img.shields.io/badge/Contributions-Welcome-orange)

---

## 📌 Overview

The **Social Media Wellness Analyzer** is a mental health companion platform that helps users **track mood, analyze journal entries, and access wellness tools**. It uses **machine learning** to analyze text for signs of depression and provides **self-care features** like motivational thoughts, stress tips, and breathing exercises.

⚠️ **Disclaimer**: This platform is an **awareness & self-care tool only** — not a medical device. If you are in crisis, contact local emergency services or a mental health helpline immediately.

---

## 🚀 Features

✅ **Text Analysis** – Detect depressive language using ML models trained on Reddit data.
✅ **Mood Tracker** – Log your daily mood (1–5 scale) and track patterns.
✅ **Journal** – Write and reflect on your daily experiences.
✅ **Wellness Tools** – Get motivational thoughts, stress tips, and a 5-min breathing coach.
✅ **Export Data** – Download mood and journal data as CSV/TXT reports.
✅ **Helpline Support** – Quick access to helpline numbers and mental health resources.

---


<img width="1920" height="1080" alt="Screenshot (264)" src="https://github.com/user-attachments/assets/6aa6bc57-658c-448d-9c4c-9af9b2626010" />

### 📝 Journal – Write & Reflect

<img width="1920" height="1080" alt="Screenshot (267)" src="https://github.com/user-attachments/assets/03b69a8d-6cd9-4545-93c6-c099312126b4" />


### 🧘 Wellness Tools

<img width="1920" height="1080" alt="Screenshot (268)" src="https://github.com/user-attachments/assets/51d726a0-3f82-4e18-8b2a-075d659d8ed1" />


### 📊 Export Data & Summary

<img width="1920" height="1080" alt="Screenshot (269)" src="https://github.com/user-attachments/assets/d4930ae6-7ec8-4891-bef9-8f397490da66" />


---

## 🛠️ Tech Stack

* **Frontend**: Streamlit (Python)
* **Backend**: Machine Learning (Logistic Regression + TF-IDF)
* **Libraries Used**:

  * `pandas` → dataset handling
  * `scikit-learn` → ML model & text vectorization
  * `streamlit` → Web UI framework
  * `matplotlib` → graphs/visualizations

---

## ⚙️ How It Works

1. **Input** – User writes journal text or provides posts.
2. **Preprocessing** – Text is cleaned & converted to TF-IDF vectors.
3. **ML Model** – Logistic Regression predicts if text shows depressive traits.
4. **Output** – User sees result + confidence score.
5. **Wellness Tools** – Provides tips & activities to improve mental wellbeing.
6. **Data Export** – Users can download mood/journal history in CSV/TXT format.

---

## ▶️ Installation & Usage

```bash
# Clone repository
git clone https://github.com/yourusername/social-media-wellness-analyzer.git
cd social-media-wellness-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 📊 Example

```text
User Input: "I feel very hopeless and tired of everything."
Prediction: Depressed 😔 (Confidence: 92%)

User Input: "I’m so happy today, I achieved my goals!"
Prediction: Not Depressed 🙂 (Confidence: 95%)
```

---

## 📂 Export Options

* **CSV** → moods.csv, journal.csv
* **TXT** → summary.txt with average mood & streaks

---

## 📞 Emergency Support

* 🇮🇳 India — KIRAN Helpline: 1800-599-0019
* Vandrevla Foundation: +91 9152987821
* [Befrienders Worldwide](https://www.befrienders.org/)
* [WHO Mental Health](https://www.who.int/health-topics/mental-health)

---

## ⚠️ Disclaimer

This app is for **awareness and self-care purposes only**.
It is **not a medical device** and should not replace professional help.


👉 Do you also want me to make a **requirements.txt** file (with libraries like `streamlit`, `pandas`, `scikit-learn`, etc.) so anyone can install and run your project easily?
