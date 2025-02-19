from flask import Flask, request, send_file, jsonify
import os
import json
import yaml
from werkzeug.utils import secure_filename
from datetime import datetime
from gpt_resume import GPTResume
from html_to_pdf import HTML_to_PDF  
import asyncio

app = Flask(__name__)
UPLOAD_FOLDER = './data'
RESUME_FOLDER = './resumes'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESUME_FOLDER, exist_ok=True)

@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    if 'yaml_file' not in request.files or 'jobDescription' not in request.form:
        return jsonify({'error': 'Missing YAML file or job description'}), 400
    
    yaml_file = request.files['yaml_file']
    job_description = request.form['jobDescription']
    
    yaml_filename = secure_filename(yaml_file.filename)
    yaml_path = os.path.join(UPLOAD_FOLDER, yaml_filename)
    yaml_file.save(yaml_path)
    
    with open(yaml_path, 'r') as file:
        resume_data = yaml.safe_load(file)
    print(resume_data)
     
    gpt_resume = GPTResume(job_description, resume_data)
    gpt_resume =  gpt_resume.generate_resume()
    
    timestamp_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pdf_filename = os.path.join(RESUME_FOLDER, f'resume_{timestamp_str}.pdf')
    os.makedirs("resumes", exist_ok=True)
    if(pdf_filename):
        pdf_filename = pdf_filename
    else:
        pdf_filename = f"resumes/resume.pdf"
    HTML_to_PDF(gpt_resume.get_text(), pdf_filename)
    
    return jsonify({'message': 'Resume generated successfully', 'file path': pdf_filename})

@app.route('/generate-resume-json', methods=['POST'])
def generate_resume_json():
    data = request.get_json()
    print(data)
    job_description = data['jobDescription']
    resume_data = json.loads(data['resumeData'])
    
    gpt_resume = GPTResume(job_description, resume_data)
    resume = asyncio.run(gpt_resume.generate_resume())

    timestamp_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pdf_filename = os.path.join(RESUME_FOLDER, f'resume_{timestamp_str}.pdf')
    os.makedirs("resumes", exist_ok=True)
    if(pdf_filename):
        pdf_filename = pdf_filename
    else:
        pdf_filename = f"resumes/resume.pdf"
    HTML_to_PDF(gpt_resume.get_text(), pdf_filename)
    
    return jsonify({'message': 'Resume generated successfully', 'file path': pdf_filename})

@app.route('/download_resume', methods=['GET'])
def download_resume():
    filename = request.args.get('filename', 'resume.pdf')  
    pdf_path = os.path.join(RESUME_FOLDER, filename)

    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True)
    else:
        return jsonify({'error': f'File {filename} not found'}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Railway's assigned port
    app.run(host="0.0.0.0", port=port, debug=False)