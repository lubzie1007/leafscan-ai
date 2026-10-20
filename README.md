# 🌿 Crop Doctor AI

**An End-to-End Deep Learning and LLM Solution for Plant Disease Diagnosis.**

Crop Doctor AI is a Progressive Web App (PWA) that allows farmers and gardeners to instantly diagnose plant diseases by simply uploading a photograph of a leaf. It combines a robust computer vision ensemble with Google's Gemini LLM to provide not just a diagnosis, but a full treatment plan.

---

## 📌 The Problem

Traditional plant disease diagnosis relies on visual inspection by agricultural experts, which is slow, expensive, and often inaccessible. While existing AI models exist, they suffer from the **"Lab-to-Field Gap"**: models trained on clean, laboratory-style images fail drastically when deployed in the real world where photos have messy backgrounds, varying lighting, and complex plant structures. Furthermore, they only provide a label, not an actionable cure.

## 💡 Our Solution

1. **Bridging the Gap:** We engineered a custom dataset by merging 54,000 lab-condition images (PlantVillage) with 2,600 real-world field images (PlantDoc). This domain adaptation ensures the AI works in the real world.
2. **Ensemble Vision:** We use a dual-model architecture (ResNet50 + DenseNet121) that averages their predictions to maximize accuracy.
3. **Generative Advice:** We integrated Google's Gemini LLM to translate the AI's technical label into a simple, human-readable diagnosis, treatment plan, and prevention strategy.

---

## 🚀 Tech Stack

**Machine Learning & AI**
*   **TensorFlow / Keras:** For training and running the vision models.
*   **ResNet50 & DenseNet121:** Pre-trained architectures used for transfer learning.
*   **Google Gemini API:** For natural language generation (symptoms, treatment, prevention, and chatbot).

**Backend**
*   **Python 3.11**
*   **FastAPI:** High-performance API for serving the models.
*   **Uvicorn:** ASGI web server.

**Frontend**
*   **React (Vite):** For a fast, component-based UI.
*   **Vite PWA:** For installable, native-app-like behavior on mobile devices.
*   **Axios:** For API communication.
*   **Vanilla CSS:** Custom responsive layout (Sidebar on desktop, Bottom Nav on mobile).

---

## ✨ Key Features

*   📸 **Real-time Diagnosis:** Upload or take a photo of a leaf.
*   🧠 **Dual-Model Ensemble:** Combines ResNet50 and DenseNet for higher confidence.
*   💬 **AI Follow-up Chat:** Ask Crop Doctor AI questions about the disease.
*   📄 **Export to PDF:** Save the diagnosis and treatment plan as a clean PDF report.
*   📱 **Mobile-First PWA:** Installable on iOS and Android home screens.

---

## 📂 Project Structure

```text
leafscan-ai/
├── api.py                  # FastAPI backend server
├── requirements.txt        # Python dependencies
├── .env                    # (Ignored in git) Gemini API Key
├── src/                    # Backend source code
│   ├── ensemble_predict.py # Combines ResNet and DenseNet
│   ├── llm_advisor.py      # Gemini LLM integration
│   └── data_loader.py      # Dataset preprocessing
├── models/                 # (Ignored in git) Trained .h5 models
├── data/                   # (Ignored in git) PlantVillage & PlantDoc data
└── frontend/               # React PWA frontend
    ├── src/
    │   ├── pages/          # Dashboard, Analyse, Result, History
    │   ├── components/     # Sidebar, Floating Chatbot
    │   └── api.js          # Axios configuration
    └── vite.config.js      # Vite + Proxy configuration
