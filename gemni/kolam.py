import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY_HERE")

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Say hello Gemini!")
print(response.text)
