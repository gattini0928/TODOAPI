from datetime import datetime
from pymongo import MongoClient
def get_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['todoapi_db']
    return db
class TodoManager:
    def __init__(self, db=get_db()):
        self.db = db

    def add_task(self, task_name, category, priority, created_at=None, due_date=None, status='Pending', subcategory=None):
        collection = self.db['tasks']
        # Define created_at with actual date
        created_at = created_at or datetime.now()

        task = {
            'task_name': task_name,
            'category': {'name': category, 'subcategories': subcategory},
            'priority': priority,
            'created_at': created_at,
            'due_date': due_date,
            'status': status,
        }
        collection.insert_one(task)
        print(f'{task_name} success')
# Tests
if __name__ == '__main__':
    todoapp = TodoManager()
    todoapp.add_task('Learn Python', 'Programming', 10, due_date='28/08/2025')

    

        
    