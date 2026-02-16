from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route("/add", methods=["POST"])
def add_note():
    data = request.json
    text = data.get("text")

    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (text) VALUES (?)", (text,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Note saved"})

@app.route("/notes", methods=["GET"])
def get_notes():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, text FROM notes")
    notes = cursor.fetchall()
    conn.close()

    return jsonify([
        {"id": n[0], "text": n[1]} for n in notes
    ])

@app.route("/delete/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Note deleted"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
