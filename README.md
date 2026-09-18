# 🤖 ToonGroq AI Studio

An interactive, responsive full-stack chatbot built with **Flask**, **Groq LLM API**, and a modern web frontend featuring **animated cartoon characters**, an **interactive blazer decoration studio**, and a **Java fresher coding launchpad**.

---

## ✨ Features

### 1. 🎭 Animation of Cartoons
- **Animated Cartoon Mascot ("Sparky / Duke")**:
  - Expressive vector character with floating, breathing, and eye-blinking keyframe animations.
  - Synchronized mouth-flap animations while generating responses.
  - Interactive emote buttons (`👋 Wave`, `🎉 Cheer`, `🤔 Think`, `🕺 Dance`).
  - Dynamic speech bubbles reacting to modes and user actions.
  - Synthesized Web Audio cartoon sound effects (boing, blip, chime).

### 2. 🧥 Designs I Wish for Decorate Blazer
- **Interactive Visual Blazer Customizer Canvas**:
  - Live SVG blazer preview that changes in real-time.
  - Fabric color swatches: *Midnight Navy*, *Onyx Black*, *Emerald Green*, *Burgundy Velvet*, and *Ivory Cream*.
  - Layer toggles:
    - 👑 **Chest Pocket Monogram Crest**: Gold bullion wire embroidery.
    - ⚜️ **Lapel Brooch & Pin**: Metallic vintage crest pins.
    - 🧣 **Pocket Square**: Silk puff folds with contrasting patterns.
    - ✨ **Gold Contrast Piping**: Satin peak lapel trim.
    - 🛡️ **Suede Elbow Patches**: Diamond stitched heritage patches.
    - ⚡ **Anime / Pop Patch**: Vibrant sleeve embroidery motifs.
  - **Atelier Duke Stylist AI**: Generates custom bespoke blazer decoration blueprints, DIY embroidery guides, fabric pairing tips, and event recommendations.

### 3. ⚡ Getting Generative Answers (Groq API)
- Ultra-fast AI completions using Groq's open-source LLM fleet:
  - `llama-3.3-70b-versatile` (Default, flagship high-intelligence model)
  - `llama-3.1-8b-instant` (Ultra-low latency responses)
  - `mixtral-8x7b-32768` (High context capacity)
- Markdown rendering for headings, lists, tables, bold styling, and blockquotes.
- Code blocks with syntax formatting and one-click "Copy" buttons.
- Chat history export to Markdown file.
- Clean offline preview mode in case the API key is not yet configured.

### 4. ☕ Easy Use of Coding in Java for Freshers
- **Duke the Java Wizard Mentor**:
  - Zero-stress beginner tutorials with real-world analogies (e.g., Classes are cookie cutters, Objects are cookies).
  - Starter interactive code playground with live topic switcher:
    - 🔰 *Hello World & Syntax*
    - 📦 *Variables & Data Types*
    - 🔄 *For & While Loops*
    - 🧱 *Classes & Objects (OOP)*
    - ⚠️ *Top 5 Fresher Traps (`==` vs `.equals()`, NullPointerException)*
  - One-click **"💡 Explain Line-by-Line"** button.
  - Quick beginner prompt pills for instant answers.

---

## 🚀 Quick Start Guide

### 1. Configure your Groq API Key in `.env`
Edit the `.env` file in the project folder:
```env
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
PORT=5000
FLASK_DEBUG=True
```
> **Tip**: You can get a free key anytime from [Groq Console](https://console.groq.com/keys). Alternatively, you can enter your key directly inside the app using the **Groq API Key** button in the top-right header!

### 2. Run the Application
Double-click `run.bat` or open PowerShell and run:
```powershell
& "C:\Users\ise\anaconda3\python.exe" app.py
```
Or with standard Python:
```powershell
python app.py
```

### 3. Open in Browser
Visit **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your web browser.

---

## 📁 Project Architecture
```
generative ai/
├── .env                  # Environment config with GROQ_API_KEY
├── .env.example          # Template configuration
├── requirements.txt      # Python dependencies (flask, groq, python-dotenv)
├── app.py                # Flask server, Groq client & persona endpoints
├── run.bat               # 1-click Windows runner
├── README.md             # Project documentation
├── templates/
│   └── index.html        # Modern single-page app layout
└── static/
    ├── css/
    │   └── styles.css    # Cartoon keyframes, glassmorphism, responsive design
    └── js/
        └── app.js        # Cartoon animation controller, blazer customizer, Java hub & chat
```
