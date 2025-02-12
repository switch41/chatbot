import google.generativeai as genai

genai.configure(api_key="AIzaSyBPPkiLDWkdHb0aYuqJ3hKADQoqkg7TCAI")  # Replace manually

gemini_model = genai.GenerativeModel("gemini-pro")
response = gemini_model.generate_content("Hello, how are you?")

print("Response from Gemini:", response.text)
