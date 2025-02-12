import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import json
import sqlite3  # Added for chat memory
import requests  # Roboflow API for image classification

# Load environment variables
load_dotenv()

# API Keys
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY")
ROBOFLOW_MODEL_ID = os.getenv("ROBOFLOW_MODEL_ID")
ROBOFLOW_VERSION_NUMBER = os.getenv("ROBOFLOW_VERSION_NUMBER")

# Configure Google Gemini AI
genai.configure(api_key=GENAI_API_KEY)

app = Flask(__name__)

# Load the knowledge base
knowledge_base = {}
if os.path.exists("knowledge_base.json"):
    try:
        with open("knowledge_base.json", "r", encoding="utf-8") as f:
            knowledge_base = json.load(f)
    except json.JSONDecodeError:
        print("Error: Invalid knowledge_base.json format.")
else:
    print("Warning: No knowledge base found. Using AI for responses.")

# 🔹 Database Connection for Memory
def create_connection():
    """Creates a connection to the SQLite database."""
    conn = sqlite3.connect("chat_memory.db", check_same_thread=False)
    return conn

def create_table():
    """Creates a table for storing chatbot conversations."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS chats (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_message TEXT,
                        bot_response TEXT
                      )''')
    conn.commit()
    conn.close()

# Run this function to ensure the table exists
create_table()

# 🔹 Save and Retrieve Chat Memory
def save_chat(user_message, bot_response):
    """Saves user and bot messages to the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chats (user_message, bot_response) VALUES (?, ?)", (user_message, bot_response))
    conn.commit()
    conn.close()

def get_past_chats(limit=5):
    """Retrieves the last few chatbot interactions for context."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_message, bot_response FROM chats ORDER BY id DESC LIMIT ?", (limit,))
    chats = cursor.fetchall()
    conn.close()
    
    return "\n".join([f"User: {chat[0]}\nBot: {chat[1]}" for chat in reversed(chats)])

# 🔹 Function to check the knowledge base first
def get_knowledge_response(user_message):
    user_message = user_message.lower()
    for key, response in knowledge_base.items():
        if key.lower() in user_message:
            return response  # Return stored response
    return None  # No match, use AI response

# 🔹 Initialize Gemini Model
gemini_model = genai.GenerativeModel("gemini-pro")

def get_ai_response(user_message, past_chats=""):
    """Generates an AI response using Google Gemini with chat history."""
    try:
        full_prompt = f"{past_chats}\nUser: {user_message}\nBot:"
        response = gemini_model.generate_content(full_prompt, 
            generation_config={"temperature": 0.7, "max_output_tokens": 150})
        
        if hasattr(response, "text"):
            return response.text.strip()
        return "I'm not sure about that. Can you rephrase?"
    
    except Exception as e:
        print("Error in AI response:", str(e))
        return "Sorry, I couldn't process that request right now."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Chat API that retrieves past conversations for context-aware responses."""
    data = request.json
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Please enter a message."})

    # Retrieve past chats for context
    past_chats = get_past_chats()

    # Check knowledge base first
    knowledge_response = get_knowledge_response(user_message)
    if knowledge_response:
        save_chat(user_message, knowledge_response)  # Save response in memory
        return jsonify({"response": knowledge_response})

    # Get AI-generated response with context
    ai_response = get_ai_response(user_message, past_chats)

    # Save the conversation to the database
    save_chat(user_message, ai_response)

    return jsonify({"response": ai_response})

# 🚀 Waste Classification using Roboflow
def classify_waste(image_path):
    """Sends image to Roboflow API for classification."""
    url = f"https://detect.roboflow.com/{ROBOFLOW_MODEL_ID}/{ROBOFLOW_VERSION_NUMBER}"
    
    with open(image_path, "rb") as img:
        response = requests.post(
            url,
            files={"file": img},
            params={"api_key": ROBOFLOW_API_KEY}
        )
    
    if response.status_code == 200:
        data = response.json()

        if "predictions" in data and len(data["predictions"]) > 0:
            waste_type = data["predictions"][0]["class"]
            return waste_type
        else:
            return "Not Recognized"
    else:
        print("Error:", response.text)
        return None  # Handle API failure

# 🚀 Disposal Tips
def get_disposal_tips(waste_type):
    """Returns disposal instructions based on waste classification."""
    disposal_tips = {
        "plastic": "Rinse and dry before recycling. Avoid plastic bags in recycling bins.",
        "paper": "Flatten and keep dry. Avoid greasy or food-contaminated paper.",
        "metal": "Clean before recycling. Aluminum cans are highly recyclable!",
        "glass": "Rinse before recycling. Do not mix different colors of glass.",
        "organic": "Compost organic waste for better environmental impact.",
        "ewaste": "Dispose at e-waste collection centers to prevent pollution."
    }
    return disposal_tips.get(waste_type.lower(), "Dispose responsibly following local waste management guidelines.")

@app.route("/classify", methods=["POST"])
def classify():
    """API endpoint to classify waste from an image."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    image = request.files["file"]
    image_path = "temp_image.jpg"
    image.save(image_path)

    # Classify the waste
    waste_type = classify_waste(image_path)

    if waste_type is None:
        return jsonify({"error": "Failed to classify image"}), 500

    # Get disposal tips
    disposal_tip = get_disposal_tips(waste_type)

    return jsonify({
        "class": waste_type,
        "disposal_tip": disposal_tip
    })

# 🔹 Reset Memory API
@app.route("/reset_memory", methods=["POST"])
def reset_memory():
    """Clears all past chatbot conversations."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chats")
    conn.commit()
    conn.close()
    return jsonify({"response": "Chat memory has been cleared."})

if __name__ == "__main__":
    app.run(debug=False)  # Stable deployment setting
