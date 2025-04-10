from flask import Flask, request, send_file, jsonify
import os
import json
from datetime import datetime
from gpt_resume import GPTResume
from gpt_cover_letter import GPTCoverLetter
from html_to_pdf import HTML_to_PDF  

app = Flask(__name__)
RESUME_FOLDER = './resumes'
COVER_LETTER_FOLDER = './cover_letters'
os.makedirs(RESUME_FOLDER, exist_ok=True)
os.makedirs(COVER_LETTER_FOLDER, exist_ok=True)


@app.route('/generate_resume', methods=['POST'])
def generate_resume_json():
    data = request.get_json()
    
    job_description = data['jobDescription']
    resume_data = json.loads(data['resumeData'])
    
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


@app.route('/download_resume', methods=['GET'])
def download_resume():
    filename = request.args.get('filename', 'resume.pdf')  
    pdf_path = os.path.join(RESUME_FOLDER, filename)

    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True)
    else:
        return jsonify({'error': f'File {filename} not found'}), 404


@app.route('/delete_resume', methods=['DELETE'])
def delete_resume():
    filename = request.args.get('filename', 'resume.pdf')
    pdf_path = os.path.join(RESUME_FOLDER, filename)

    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        return jsonify({'message': f'File {filename} deleted successfully'})
    else:
        return jsonify({'error': f'File {filename} not found'}), 404


    

@app.route('/generate_cover_letter', methods=['POST'])
def generate_cover_letter_json():
    data = request.get_json()

    job_description = data['jobDescription']
    resume_data = json.loads(data['resumeData'])
    
    gpt_cover_letter = GPTCoverLetter(job_description, resume_data)
    gpt_cover_letter = gpt_cover_letter.generate_cover_letter()
    
    
    timestamp_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pdf_filename = os.path.join(COVER_LETTER_FOLDER, f'cover_letter_{timestamp_str}.pdf')
    os.makedirs("cover_letters", exist_ok=True)
    if(pdf_filename):
        pdf_filename = pdf_filename
    else:
        pdf_filename = f"cover_letters/cover_letter.pdf"
    HTML_to_PDF(gpt_cover_letter.get_text(), pdf_filename)
    
    return jsonify({'message': 'Cover Letter generated successfully', 'file path': pdf_filename})


@app.route('/download_cover_letter', methods=['GET'])
def download_cover_letter():
    filename = request.args.get('filename', 'cover_letter.pdf')  
    pdf_path = os.path.join(COVER_LETTER_FOLDER, filename)

    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True)
    else:
        return jsonify({'error': f'File {filename} not found'}), 404


@app.route('/delete_cover_letter', methods=['DELETE'])
def delete_cover_letter():
    filename = request.args.get('filename', 'cover_letter.pdf')  
    pdf_path = os.path.join(COVER_LETTER_FOLDER, filename)

    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        return jsonify({'message': f'File {filename} deleted successfully'})
    else:
        return jsonify({'error': f'File {filename} not found'}), 404





if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port, debug=False)