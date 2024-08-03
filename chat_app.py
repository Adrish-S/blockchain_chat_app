from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

messages = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    username = data['username']
    message = data['message']
    messages.append({'username': username, 'text': message})
    return jsonify({'status': 'success'})

@app.route('/get_messages')
def get_messages():
    return jsonify(messages)

if __name__ == '__main__':
    app.run(debug=True)
