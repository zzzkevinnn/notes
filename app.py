from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'notes.json'

# Fungsi untuk membaca data dari file JSON
def read_notes():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

# Fungsi untuk menulis data ke file JSON
def write_notes(notes):
    with open(DATA_FILE, 'w') as f:
        json.dump(notes, f, indent=4)

# Halaman utama untuk menampilkan semua catatan
@app.route('/')
def index():
    notes = read_notes()
    return render_template('index.html', notes=notes)

# Menambah catatan baru
@app.route('/add', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        notes = read_notes()
        note = {
            "id": len(notes) + 1,
            "title": title,
            "content": content
        }
        notes.append(note)
        write_notes(notes)
        return redirect(url_for('index'))
    return render_template('add_note.html')


# Mengedit catatan
@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    notes = read_notes()
    note = next((note for note in notes if note['id'] == note_id), None)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if note:
            note['title'] = title
            note['content'] = content
            write_notes(notes)
        return redirect(url_for('index'))
    return render_template('edit_note.html', note=note)

# Menghapus catatan
@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    notes = read_notes()
    notes = [note for note in notes if note['id'] != note_id]
    write_notes(notes)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
