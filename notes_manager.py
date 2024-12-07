import csv
from models.note import Note
from data_handler import load_data, save_data
from datetime import datetime


class NotesManager:
    def __init__(self):
        self.notes = []
        self.load_notes()

    def create_note(self, title, content):
        id = self.notes[-1].id + 1 if self.notes else 1
        timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        note = Note(id, title, content, timestamp)
        self.notes.append(note)
        self.save_notes()

    def edit_note(self, note_id, title=None, content=None):
        note = next((n for n in self.notes if n.id == note_id), None)
        if note:
            if title: note.title = title
            if content: note.content = content
            note.timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            self.save_notes()
        else:
            print("Заметка не найдена.")

    def delete_note(self, note_id):
        self.notes = [n for n in self.notes if n.id != note_id]
        self.save_notes()

    def view_notes(self):
        if not self.notes:
            print("Заметок нет.")
            return

        for note in self.notes:
            print(f"ID: {note.id}, Заголовок: {note.title}, Дата: {note.timestamp}")

    def view_note_details(self, note_id):
        note = next((n for n in self.notes if n.id == note_id), None)
        if note:
            print(f"Заголовок: {note.title}\nСодержание: {note.content}\nДата: {note.timestamp}")
        else:
            print("Заметка не найдена.")

    def export_notes_to_csv(self, filename="notes_export.csv"):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Title', 'Content', 'Timestamp'])
            for note in self.notes:
                writer.writerow([note.id, note.title, note.content, note.timestamp])

        print(f"Заметки экспортированы в файл {filename}")

    def import_notes_from_csv(self, filename="notes_export.csv"):
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.create_note(row['Title'], row['Content'])

        print("Заметки успешно импортированы.")

    def load_notes(self):
        data = load_data('notes.json')
        self.notes = [Note(**note) for note in data]

    def save_notes(self):
        data = [note.to_dict() for note in self.notes]
        save_data('notes.json', data)