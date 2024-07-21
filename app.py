from flask import Flask, request, jsonify
import pdfplumber

app = Flask(__name__)

def extract_table_from_pdf(pdf_path):
    result = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for table in tables:
                table_data = []
                for row in table:
                    table_data.append(row)
                result.append({
                    'page': page_number + 1,
                    'table': table_data
                })
    return result

@app.route('/pdf/extract', methods=['POST'])
def extract():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        file_path = f"/tmp/{file.filename}"
        file.save(file_path)
        extracted_data = extract_table_from_pdf(file_path)
        return jsonify(extracted_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
