import csv
from models.task import Task
from data_handler import load_data , save_data

class TasksManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def create_task(self, title, description, priority, due_date):
        id = self.tasks[-1].id + 1 if self.tasks else 1
        task = Task(id, title, description, done=False, priority=priority, due_date=due_date)
        self.tasks.append(task)
        self.save_tasks()

    def edit_task(self, task_id, title=None, description=None, priority=None, due_date=None):
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task:
            if title: task.title = title
            if description: task.description = description
            if priority: task.priority = priority
            if due_date: task.due_date = due_date
            self.save_tasks()
        else:
            print("Задача не найдена.")

    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t.id != task_id]
        self.save_tasks()

    def mark_task_as_done(self, task_id):
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task:
            task.done = True
            self.save_tasks()
        else:
            print("Задача не найдена.")

    def view_tasks(self):
        if not self.tasks:
            print("Задач нет.")
            return
        for task in self.tasks:
            status = "Выполнена" if task.done else "Не выполнена"
            print(f"ID: {task.id}, Заголовок: {task.title}, Приоритет: {task.priority}, Срок: {task.due_date}, Статус: {status}")

    def export_tasks_to_csv(self, filename="tasks_export.csv"):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Title', 'Description', 'Done', 'Priority', 'Due Date'])
            for task in self.tasks:
                writer.writerow([task.id, task.title, task.description, task.done, task.priority, task.due_date])
        print(f"Задачи экспортированы в файл {filename}")

    def import_tasks_from_csv(self, filename="tasks_export.csv"):
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.create_task(row['Title'], row['Description'], row['Priority'], row['Due Date'])
        print("Задачи успешно импортированы.")

    def load_tasks(self):
        data = load_data('tasks.json')
        self.tasks = [Task(**task) for task in data]

    def save_tasks(self):
        data = [task.to_dict() for task in self.tasks]
        save_data('tasks.json', data)
