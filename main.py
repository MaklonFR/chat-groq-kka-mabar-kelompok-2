from flask import Flask, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

# Ganti dengan API Key Groq Anda
GROQ_API_KEY = ""  # Paste API Key di sini

client = Groq(api_key=GROQ_API_KEY)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        # Panggil API Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
            model="meta-llama/llama-4-maverick-17b-128e-instruct",  # Model Llama-3.1-8B
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False
        )
        response = chat_completion.choices[0].message.content
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
