import csv
from models.contact import Contact
from data_handler import load_data, save_data

class ContactsManager:
    def __init__(self):
        self.contacts = []
        self.load_contacts()

    def create_contact(self, name, phone, email):
        id = self.contacts[-1].id + 1 if self.contacts else 1
        contact = Contact(id, name, phone, email)
        self.contacts.append(contact)
        self.save_contacts()

    def edit_contact(self, contact_id, name=None, phone=None, email=None):
        contact = next((c for c in self.contacts if c.id == contact_id), None)
        if contact:
            if name: contact.name = name
            if phone: contact.phone = phone
            if email: contact.email = email
            self.save_contacts()
        else:
            print("Контакт не найден.")

    def delete_contact(self, contact_id):
        self.contacts = [c for c in self.contacts if c.id != contact_id]
        self.save_contacts()

    def search_contact(self, search_term):
        found_contacts = [c for c in self.contacts if search_term.lower() in c.name.lower() or search_term in c.phone]
        if not found_contacts:
            print("Контакты не найдены.")
        else:
            for contact in found_contacts:
                print(f"ID: {contact.id}, Имя: {contact.name}, Телефон: {contact.phone}, Email: {contact.email}")

    def view_contacts(self):
        if not self.contacts:
            print("Контакты не найдены.")
            return
        for contact in self.contacts:
            print(f"ID: {contact.id}, Имя: {contact.name}, Телефон: {contact.phone}, Email: {contact.email}")

    def export_contacts_to_csv(self, filename="contacts_export.csv"):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Name', 'Phone', 'Email'])
            for contact in self.contacts:
                writer.writerow([contact.id, contact.name, contact.phone, contact.email])
        print(f"Контакты экспортированы в файл {filename}")

    def import_contacts_from_csv(self, filename="contacts_export.csv"):
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.create_contact(row['Name'], row['Phone'], row['Email'])
        print("Контакты успешно импортированы.")

    def load_contacts(self):
        data = load_data('contacts.json')
        self.contacts = [Contact(**contact) for contact in data]

    def save_contacts(self):
        data = [contact.to_dict() for contact in self.contacts]
        save_data('contacts.json', data)
