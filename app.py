import sqlite3
from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

# Configure SQLite database for storing chat history and threads
DATABASE = 'tracker.db'
RASA_SERVER_URL = 'http://localhost:5005/webhooks/rest/webhook'  # Update this URL based on your Rasa server


def deleteddb():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''DROP table events;''')
    c.execute('''DROP table threads;''')  # Table for threads
    conn.commit()
    conn.close()

deleteddb()
def create_db():
    """Create the SQLite database if it doesn't exist."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events 
                 (sender_id TEXT, event TEXT, text TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS threads
                 (thread_id INTEGER PRIMARY KEY AUTOINCREMENT, sender_id TEXT)''')  # Table for threads
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
        return jsonify([{'thread_id': thread[0], 'sender_id': thread[1]} for thread in threads])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/start_thread', methods=['POST'])
def start_thread():
    try:
        sender_id = request.json.get('sender_id')
        # Check if the sender_id already exists
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM threads WHERE sender_id=?", (sender_id,))
        existing_thread = cursor.fetchone()
        if existing_thread:
            return jsonify({'message': 'Thread already exists'})
        else:
            cursor.execute("INSERT INTO threads (sender_id) VALUES (?)", (sender_id,))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Thread started successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/end_thread', methods=['POST'])
def end_thread():
    try:
        sender_id = request.json.get('sender_id')
        print(sender_id)
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM threads WHERE sender_id=?", (sender_id,))
        # Optionally, you may want to delete messages associated with this sender_id from the events table
        cursor.execute("DELETE FROM events WHERE sender_id=?", (sender_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Thread ended successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/list_messages/<sender_id>', methods=['GET'])
def list_messages(sender_id):
    """List all messages for a specific sender_id (thread)."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events WHERE sender_id=?", (sender_id,))
        messages = cursor.fetchall()
        conn.close()
        print(messages)
        return jsonify([{'event': message[1], 'text': message[2]} for message in messages])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        sender_id = data['sender']
        message = data['message']
        print(message,sender_id)
        # Save user message to database
        save_message(sender_id, 'user', message)

        # Send the message to Rasa server
        response = requests.post(
            RASA_SERVER_URL,
            json={"sender": sender_id, "message": message}
        )
        response.raise_for_status()

        # Handle Rasa's response
        bot_responses = response.json()
        for bot_response in bot_responses:
            save_message(sender_id, 'bot', bot_response.get('text', ''))

        return jsonify(bot_responses)

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Rasa server error: ' + str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def save_message(sender_id, event, text):
    """Save a message to the SQLite database."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO events (sender_id, event, text) VALUES (?, ?, ?)",
            (sender_id, event, text)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error saving message: {e}")

if __name__ == '__main__':
    app.run(debug=True, port=5055)
