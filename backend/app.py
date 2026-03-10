import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import groq
import anthropic

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'ogg', 'flac'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/process-lesson', methods=['POST'])
def process_lesson():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    student_name = request.form.get('student_name', 'Student')

    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # 1. Transcription with Groq
            groq_client = groq.Groq(api_key=os.environ.get("GROQ_API_KEY"))
            with open(filepath, "rb") as file_stream:
                transcription = groq_client.audio.transcriptions.create(
                    file=(filename, file_stream.read()),
                    model="whisper-large-v3",
                    response_format="text"
                )

            # 2. Summarization with Anthropic
            anthropic_client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

            # Read style guide
            try:
                # Use absolute path to ensure it works regardless of CWD
                current_dir = os.path.dirname(os.path.abspath(__file__))
                style_guide_path = os.path.join(current_dir, '..', 'templates', 'Master_EmailStyle_Guide.md')
                with open(style_guide_path, 'r') as f:
                    style_guide = f.read()
            except FileNotFoundError:
                style_guide = "Write a professional summary email."

            prompt = f"""
            You are a helpful teaching assistant. using the following style guide:
            {style_guide}

            Please write a summary email for student: {student_name}
            Based on the following transcript:
            {transcription}
            """

            message = anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                temperature=0,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            email_content = message.content[0].text

            # Clean up uploaded file
            os.remove(filepath)

            return jsonify({
                'success': True,
                'email': email_content,
                'transcript_preview': transcription[:500] + "..." if len(transcription) > 500 else transcription
            })

        except Exception as e:
            # Clean up uploaded file in case of error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
