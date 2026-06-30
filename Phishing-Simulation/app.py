import base64
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def generate_employee_links():
    base_url = "http://127.0.0.1:5000/auth/verify-identity"
    employees = [
        "employee1@company.com",
        "employee2@company.com"
    ]
    
    print("\n" + "="*60)
    for email in employees:
        encoded_id = base64.b64encode(email.encode()).decode().strip("=")
        print(f"{email} -> {base_url}?emp_id={encoded_id}")
    print("="*60 + "\n")

@app.route('/auth/verify-identity', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/log', methods=['POST'])
def log_click():
    data = request.get_json()
    emp_id = data.get('id')
    
    if emp_id:
        try:
            padded_id = emp_id + '=' * (-len(emp_id) % 4)
            decoded_email = base64.b64decode(padded_id.encode()).decode()
            
            with open("clicks.txt", "a", encoding="utf-8") as f:
                f.write(f"{decoded_email}\n")
                
            return jsonify({"status": "success"}), 200
        except Exception as e:
            return jsonify({"status": "error"}), 400

    return jsonify({"status": "failed"}), 400

if __name__ == '__main__':
    generate_employee_links()
    app.run(debug=True, port=5000)