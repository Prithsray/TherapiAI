import sqlite3
from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

# Configure SQLite database for storing chat history and threads
DATABASE = 'tracker.db'
RASA_SERVER_URL = 'https://therapiai.onrender.com/webhooks/rest/webhook'  # Update this URL based on your Rasa server

def deleteddb():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''DROP table events;''')
    c.execute('''DROP table threads;''')  # Table for threads
    conn.commit()
    conn.close()

#deleteddb()


def create_db():
    """Create the SQLite database if it doesn't exist."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, thread_id INTEGER, event TEXT, text TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS threads
                 (thread_id INTEGER PRIMARY KEY AUTOINCREMENT, thread_name TEXT)''')
    conn.commit()
    conn.close()

create_db()

@app.route('/')
def index():
    """Serve the main chat interface."""
    return render_template('index.html')

@app.route('/list_threads', methods=['GET'])
def list_threads():
    """List all active threads (sessions)."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM threads")
        threads = cursor.fetchall()
        conn.close()
        return jsonify([{'thread_id': thread[0], 'thread_name': thread[1]} for thread in threads])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/start_thread', methods=['POST'])
def start_thread():
    try:
        thread_name = request.json.get('thread_name')
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO threads (thread_name) VALUES (?)", (thread_name,))
        conn.commit()
        thread_id = cursor.lastrowid  # Get the last inserted thread_id
        conn.close()
        return jsonify({'message': 'Thread started successfully', 'thread_id': thread_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/end_thread', methods=['POST'])
def end_thread():
    try:
        thread_id = request.json.get('thread_id')
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM threads WHERE thread_id=?", (thread_id,))
        cursor.execute("DELETE FROM events WHERE thread_id=?", (thread_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Thread ended successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/list_messages/<int:thread_id>', methods=['GET'])
def list_messages(thread_id):
    """List all messages for a specific thread_id."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events WHERE thread_id=?", (thread_id,))
        messages = cursor.fetchall()
        conn.close()
        return jsonify([{'event': message[2], 'text': message[3]} for message in messages])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        thread_id = data['thread_id']
        message = data['message']
        print(thread_id,message)
        save_message(thread_id, 'user', message)

        response = requests.post(
            RASA_SERVER_URL,
            json={"sender": thread_id, "message": message}
        )
        response.raise_for_status()

        bot_responses = response.json()
        for bot_response in bot_responses:
            save_message(thread_id, 'bot', bot_response.get('text', ''))

        return jsonify(bot_responses)

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Rasa server error: ' + str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def save_message(thread_id, event, text):
    """Save a message to the SQLite database."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO events (thread_id, event, text) VALUES (?, ?, ?)",
            (thread_id, event, text)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error saving message: {e}")

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8000)
