from flask import Flask, render_template, jsonify, request
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/get', methods=['POST'])
def get_response():
    user_message = request.form.get("msg")

    try:
        # Execute bitsgpt.py with the user message and capture the output
        result = subprocess.run(['python', 'bitsgpt.py', user_message], capture_output=True, text=True, check=True)
        bot_response = result.stdout
    except subprocess.CalledProcessError as e:
        bot_response = f"Error: {e.stderr}"

    return jsonify(bot_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
