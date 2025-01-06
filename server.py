from flask import Flask, request, jsonify, send_from_directory
from pyngrok import ngrok
from worksheet.templates.word_bubbles import WordBubbles
from flask_cors import CORS
from dotenv import load_dotenv
from pyngrok import ngrok
import logging
import threading
import uuid
import os

logging.basicConfig(level = logging.INFO)
# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Allow requests from local and deployed frontends
CORS(app, origins=['http://192.168.0.7:3000', 'https://www.ryancriswell.com'])

# Dictionary to keep track of progress for each request, not thread-safe
generation_status = {}

@app.route('/teacher-ai/generate-word-bubbles', methods=['POST'])
def generate_word_bubbles():
    theme = request.args.get('theme')
    if theme is None:
        return jsonify({"error": "A taskId must be provided"}), 400
    
    task_id = str(uuid.uuid4())  # Use a unique identifier for each task
    generation_status[task_id] = {'status': 'Running'}

    # A separate function that does the actual work in a thread.
    def create_pdf_in_background(task_id, theme):
        try:
            wordBubbles = WordBubbles.builder() \
                .set_image_theme(theme) \
                .build()
            file_name = f'{task_id}.pdf'
            # Create the PDF and save it to the file system
            wordBubbles.create_pdf(file_name)
        except Exception as e:
            # Log error and mark task as failed
            generation_status[task_id]['status'] = 'Failed'
            logging.error(f"Error processing task {task_id}: {e}")

    # Start the PDF creation process in a new thread.
    thread = threading.Thread(target=create_pdf_in_background, args=(task_id, theme))
    thread.start()

    return jsonify({"taskId": task_id})

@app.route('/teacher-ai/status', methods=['GET'])
def check_status():
    task_id = request.args.get('taskId')
    if task_id is None:
        return jsonify({"error": "A taskId must be provided"}), 400
    
    # Check if the file exists to determine if it is complete
    if os.path.exists(f'worksheet/generated_sheets/{task_id}.pdf'):
        generation_status[task_id]['status'] = 'Complete'
        
    return jsonify({'status': generation_status[task_id]['status']})

@app.route('/teacher-ai/worksheet', methods=['GET'])
def get_worksheet():
    task_id = request.args.get('taskId')
    if task_id is None:
        return jsonify({"error": "A taskId must be provided"}), 400
    
    # Send the file
    return send_from_directory(directory='worksheet/generated_sheets/', path=f'{task_id}.pdf', as_attachment=True, download_name='worksheet.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    # Start a new ngrok tunnel pointing to your local server with the config
    public_url = ngrok.connect(name='default', addr='http://127.0.0.1:5000')
    print(f'Ngrok tunnel is live at: {public_url}')

    # Start the Flask development server
    # Do not run debug=True, it will cause the server to fail to start due to multiple ngrok agent sessions
    app.run(port=5000)