import os
import sys
import re
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

# Load environment variables from .env
load_dotenv(ENV_PATH)

app = Flask(__name__)

# Available Groq models on user account
AVAILABLE_MODELS = [
    {"id": "openai/gpt-oss-20b", "name": "GPT-OSS 20B (Ultra Fast)"},
    {"id": "openai/gpt-oss-120b", "name": "GPT-OSS 120B (High Intelligence)"},
    {"id": "qwen/qwen3.8-27b", "name": "Qwen 3.8 27B (Coding & Reasoning)"},
    {"id": "groq/compound", "name": "Groq Compound"},
]
DEFAULT_MODEL = "openai/gpt-oss-20b"

def get_groq_client():
    load_dotenv(ENV_PATH, override=True)
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key or api_key in ["your_groq_api_key_here", "gsk_your_groq_api_key_here"]:
        return None
    try:
        from groq import Groq
        return Groq(api_key=api_key)
    except Exception as e:
        print(f"Error initializing Groq client: {e}")
        return None

def build_system_prompt(mode, blazer_context=None, java_context=None):
    if mode == "blazer":
        prompt = (
            "You are 'Atelier Duke', an elite cartoon fashion tailor and blazer decoration stylist! 🎨🪡✨ "
            "You specialize in customizing, embellishing, and decorating blazers—from collegiate crests, "
            "vintage gold bullion wire embroidery, aesthetic anime/cartoon iron-on patches, and lapel pins, "
            "to velvet peak collars, pocket square folds, satin contrast piping, and engraved brass buttons. "
            "When users ask about blazer designs: "
            "1. Give rich visual descriptions and design concepts. "
            "2. Break down design components: Fabric & Color palette, Lapel & Collar accents, Embroidery & Patches placement, "
            "Buttons & Hardware, and Pocket Square & Trim. "
            "3. Offer DIY crafting steps (materials, needle/thread/ironing technique) and styling recommendations (event types, pant/shirt pairings). "
            "Keep your tone stylish, artistic, encouraging, and vibrant with tasteful emojis and markdown formatting."
        )
        if blazer_context:
            prompt += f"\nCurrent Active Blazer Customization State in Visualizer:\n{blazer_context}"
        return prompt

    elif mode == "java":
        prompt = (
            "You are 'Duke the Java Wizard' ☕⚡, an enthusiastic, friendly cartoon mentor dedicated to teaching Java programming "
            "to complete beginners and college freshers! "
            "Your golden rules: "
            "1. Explain concepts simply using everyday real-world analogies (e.g. Classes are cookie cutters, Objects are cookies). "
            "2. Provide clean, well-commented, beginner-friendly Java code snippets. "
            "3. Always highlight common fresher pitfalls (e.g. String comparison with .equals() vs ==, off-by-one loop errors, "
            "NullPointerException, forgetting 'new', class naming conventions). "
            "4. Break down code step-by-step ('Line-by-Line breakdown'). "
            "5. Maintain a super supportive, cheerful cartoon demeanor with encouraging feedback!"
        )
        if java_context:
            prompt += f"\nActive Java Context / Topic: {java_context}"
        return prompt

    else:
        # General cartoon companion
        return (
            "You are 'Sparky', an ultra-smart, animated cartoon AI companion! 🤖✨ "
            "You are cheerful, humorous, witty, and highly intelligent. You love animation, cartoon sound effects "
            "(*boing!*, *whoosh!*, *ding!*), and giving comprehensive, well-structured, clear answers with rich markdown. "
            "You are also knowledgeable in fashion customization (especially decorating blazers) and software development "
            "(especially Java for beginners). Help the user with any question with boundless cartoon energy and wisdom!"
        )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def status():
    load_dotenv(ENV_PATH, override=True)
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    has_key = bool(api_key and api_key not in ["your_groq_api_key_here", "gsk_your_groq_api_key_here"])
    masked = ""
    if has_key:
        masked = api_key[:6] + "..." + api_key[-4:] if len(api_key) > 10 else "configured"
    return jsonify({
        "has_key": has_key,
        "masked_key": masked,
        "available_models": AVAILABLE_MODELS,
        "default_model": DEFAULT_MODEL
    })

@app.route("/api/save-key", methods=["POST"])
def save_key():
    data = request.get_json() or {}
    api_key = data.get("api_key", "").strip()
    if not api_key:
        return jsonify({"success": False, "error": "API key cannot be empty"}), 400

    # Save to .env file
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    try:
        content = ""
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                content = f.read()

        if re.search(r"^GROQ_API_KEY=.*$", content, flags=re.MULTILINE):
            content = re.sub(r"^GROQ_API_KEY=.*$", f"GROQ_API_KEY={api_key}", content, flags=re.MULTILINE)
        else:
            content += f"\nGROQ_API_KEY={api_key}\n"

        with open(env_path, "w", encoding="utf-8") as f:
            f.write(content)

        # Update current process environment
        os.environ["GROQ_API_KEY"] = api_key

        return jsonify({
            "success": True,
            "message": "Groq API key saved successfully to .env!",
            "masked_key": api_key[:6] + "..." + api_key[-4:] if len(api_key) > 10 else "configured"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "").strip()
    history = data.get("history", [])
    mode = data.get("mode", "general") # 'general', 'blazer', or 'java'
    requested_model = data.get("model", DEFAULT_MODEL)
    blazer_context = data.get("blazer_context")
    java_context = data.get("java_context")

    if not user_message:
        return jsonify({"success": False, "error": "Message cannot be empty"}), 400

    client = get_groq_client()

    if not client:
        # Provide rich offline demo fallback response with instructions
        demo_reply = generate_offline_demo_response(user_message, mode, blazer_context, java_context)
        return jsonify({
            "success": True,
            "reply": demo_reply,
            "is_demo": True,
            "notice": "Offline preview mode. To unlock unlimited real-time Groq LLM generations, add your free GROQ_API_KEY in the Key Setup modal or .env file."
        })

    # Validate model
    valid_ids = [m["id"] for m in AVAILABLE_MODELS]
    model = requested_model if requested_model in valid_ids else DEFAULT_MODEL

    try:
        system_prompt = build_system_prompt(mode, blazer_context, java_context)
        messages = [{"role": "system", "content": system_prompt}]

        # Append recent history (up to last 10 messages)
        for h in history[-10:]:
            role = h.get("role")
            content = h.get("content")
            if role in ["user", "assistant"] and content:
                messages.append({"role": role, "content": content})

        messages.append({"role": "user", "content": user_message})

        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=2048,
            )
        except Exception as model_err:
            # If the specific model errored, attempt default model fallback
            print(f"Model {model} failed, falling back to {DEFAULT_MODEL}: {model_err}")
            response = client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=2048,
            )
            model = DEFAULT_MODEL

        reply_content = response.choices[0].message.content
        return jsonify({
            "success": True,
            "reply": reply_content,
            "is_demo": False,
            "model_used": model
        })
    except Exception as e:
        error_msg = str(e)
        print(f"Groq API Error: {error_msg}")
        return jsonify({
            "success": False,
            "error": f"Groq API Error: {error_msg}",
            "hint": "Please verify your GROQ_API_KEY in .env or via the Key Settings button."
        }), 500

def generate_offline_demo_response(query, mode, blazer_context=None, java_context=None):
    """Smart offline generator to demonstrate features before user provides API key"""
    q_lower = query.lower()

    if mode == "blazer":
        return (
            "### 🎨 Atelier Duke's Blazer Decoration Design Blueprint!\n\n"
            "*Snip snip, stitch stitch!* Here is a custom decoration design concept tailored for your blazer:\n\n"
            "#### 1. 🪡 Lapel & Crest Embroidery\n"
            "- **Left Chest Pocket**: A handcrafted monogram crest with gold bullion wire & navy silk threads.\n"
            "- **Lapel Embellishment**: Dual enamel pins—a minimal geometric brass pin paired with an artistic cartoon motif.\n\n"
            "#### 2. ✨ Sleeve & Collar Accents\n"
            "- **Elbow Patches**: Charcoal suede or velvet diamond-stitched elbow patches for subtle vintage elegance.\n"
            "- **Collar**: Under-collar contrast red felt or royal blue velvet with hidden embroidered motto.\n\n"
            "#### 3. 🔘 Hardware & Details\n"
            "- **Buttons**: Heavyweight embossed antique brass anchor or crest buttons.\n"
            "- **Pocket Square**: Silk puff fold featuring a vibrant pattern peek.\n\n"
            "💡 **DIY Pro-Tip**: When applying iron-on embroidery patches, use a pressing cloth and apply firm heat at 150°C for 25 seconds, then reinforce edges with a hidden catch-stitch!\n\n"
            "> *To generate infinite bespoke blazer designs, simply enter your free GROQ_API_KEY!*"
        )

    elif mode == "java":
        return (
            "### ☕ Duke's Java Fresher Quick Guide!\n\n"
            "*Hey fresher! Welcome to Java!* Let's break down your question with simple analogies:\n\n"
            "```java\n"
            "public class FresherGuide {\n"
            "    public static void main(String[] args) {\n"
            "        // 1. Variables: Think of them as labeled storage boxes!\n"
            "        String studentName = \"Alex\";\n"
            "        int codingScore = 95;\n"
            "        \n"
            "        // 2. Output to console:\n"
            "        System.out.println(\"Welcome \" + studentName + \"! Score: \" + codingScore);\n"
            "    }\n"
            "}\n"
            "```\n\n"
            "#### 🔍 Line-by-Line Breakdown for Beginners:\n"
            "1. `public class FresherGuide`: In Java, all code lives inside a class (a blueprint).\n"
            "2. `public static void main(...)`: The gateway! Java always starts executing here.\n"
            "3. `System.out.println()`: The voice of your program to print text to the screen.\n\n"
            "⚠️ **Top Fresher Trap**: Always remember Java is case-sensitive! `String` starts with uppercase 'S', while `int` is lowercase.\n\n"
            "> *Connect your free GROQ_API_KEY to ask any Java question, debug compiler errors, and practice live!*"
        )

    else:
        return (
            "### 🤖 Sparky the Cartoon Assistant Reporting for Duty!\n\n"
            "*WHOOSH!* I heard you say: **\"" + query + "\"**\n\n"
            "I am your animated AI sidekick! Here is what we can do together:\n"
            "- 🧥 **Blazer Studio**: Switch to Blazer mode to create embroidery, lapel pin layouts, and stylish trims.\n"
            "- ☕ **Java for Freshers**: Switch to Java mode for zero-stress coding lessons, bug fixing, and OOP walkthroughs.\n"
            "- ⚡ **Generative AI**: Plug in your Groq API key in the top right to unleash ultra-fast Llama 3.3 responses!\n\n"
            "What would you like to explore next? Click any suggested card or ask away!"
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    print(f">> Cartoon Groq Chatbot running on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
