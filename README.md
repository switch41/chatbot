# Chatbot Project

## Overview

This chatbot leverages AI to provide intelligent responses by combining a knowledge base with the **Gemini API** for enhanced conversational abilities. It first checks a structured **JSON knowledge base**, and if no relevant response is found, it falls back to AI-generated replies. Additionally, it integrates an **image classification model from Roboflow** for analyzing and understanding images.

## Features

✅ AI-powered responses using the **Gemini API**\
✅ Knowledge-based replies from a structured **JSON file**\
✅ **Image classification support** via **Roboflow**\
✅ Smart fallback mechanism for enhanced accuracy\
✅ Supports both **text and image-based queries**\
✅ **SQLite database** for storing chat history

## Technologies Used

- **Backend**: Python (Flask/FastAPI)
- **AI Model**: Gemini API for natural language processing
- **Database**: JSON-based knowledge storage & SQLite (chat history)
- **Image Classification**: Roboflow model
- **Environment Management**: `.env` file for API keys

## Installation & Setup

### Prerequisites

Ensure you have the following installed:

- [Python](https://www.python.org/)
- Virtual environment (recommended)

### Clone the Repository

```bash
git clone https://github.com/switch41/chatbot.git
cd chatbot
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root directory and add your API keys:

```
GEMINI_API_KEY=your_gemini_api_key
ROBOFLOW_API_KEY=your_roboflow_api_key
ROBOFLOW_MODEL_ID=your_model_id
ROBOFLOW_VERSION_NUMBER=your_version_number
```

Replace `your_gemini_api_key`, `your_roboflow_api_key`, `your_model_id`, and `your_version_number` with your actual credentials.

### Running the Application

```bash
python chatbot.py
```

## Usage

- The chatbot first checks the knowledge base (`knowledge_base.json`) for responses.
- If no matching response is found, it queries the Gemini API.
- The chatbot can also classify images using the Roboflow model.
- Chat history is stored in **SQLite (chat\_memory.db)**.

## Output Preview
![image](https://github.com/user-attachments/assets/7b40def6-32af-4779-b6cb-83842b11a8e3)


![Chatbot Interface](image.png)

## Folder Structure

```
├── env/                     # Environment configuration
├── node_modules/            # Node.js dependencies (if applicable)
├── templates/               # HTML templates (if frontend is included)
├── .env                     # API keys and environment variables
├── .gitignore               # Git ignore file
├── chatbot.py               # Main chatbot implementation
├── chat_memory.db           # SQLite database for chat history
├── knowledge_base.json      # JSON file storing predefined responses
├── package-lock.json        # Node.js lock file (if applicable)
├── package.json             # Node.js metadata and scripts (if applicable)
├── temp_image.jpg           # Temporary image storage
├── test.py                  # Test script for chatbot functionality
└── README.md                # Project documentation
```

## Contributing

Contributions are welcome! Please submit pull requests for improvements and additional features.

## Copyright

This project is developed and maintained by **switch41**. All rights reserved.

## Contact

For questions or suggestions, feel free to reach out via GitHub.

