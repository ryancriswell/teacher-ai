from flask import Flask, request, send_file, jsonify
from pyngrok import ngrok
from worksheet.templates.word_bubbles import WordBubbles
from flask_cors import CORS
from dotenv import load_dotenv
import logging

logging.basicConfig(level = logging.INFO)
# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Allow requests from local and deployed frontends
CORS(app, origins=['http://192.168.0.7:3000', 'https://www.ryancriswell.com'])

@app.route('/generate-word-bubbles', methods=['POST'])
def generate_word_bubbles():
    data = request.json
    if data is None:
        return jsonify({"error": "A theme must be provided"}), 400
    
    theme = data['theme']  # Provide a default if not specified

    wordBubbles = WordBubbles.builder() \
        .set_image_theme(theme) \
        .build()
    file_name = 'test_worksheet.pdf'
    byte_stream = wordBubbles.create_pdf(file_name)

    # Send the in-memory file
    return send_file(byte_stream, as_attachment=True, download_name='worksheet.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    # Start a new ngrok tunnel pointing to your local server
    public_url = ngrok.connect(name='default')
    print(f'Ngrok tunnel is live at: {public_url}')

    # Start the Flask development server
    app.run(port=5000)