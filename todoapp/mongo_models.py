from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId   
def get_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['todoapi_db']
    return db
class TodoManager:
    def __init__(self, db=get_db()):
        self.db = db
        self.collection = self.db['tasks']

    def add_task(self, task_name, category, priority, created_at=None, due_date=None, status='Pending'):
        # Define created_at with actual date
        created_at = created_at or datetime.now()

        if due_date and isinstance(due_date, str):
            try:
                due_date = datetime.strptime(due_date, '%d/%m/%Y')
            except ValueError:
                raise ValueError('Formato de data inválido')

        task = {
            'task_name': task_name,
            'category': category,
            'priority': priority,
            'created_at': created_at,
            'due_date': due_date,
            'status': status,
        }
        self.collection.insert_one(task)
        print(f'{task_name} success')

    def remove_task(self, task_name):
        try:
            result = self.collection.delete_one({'task_name':task_name})
            if result.deleted_count > 0:
                print(f'{task_name} removed from tasks')
            else:
                print(f'No task found with the name {task_name}')
        except Exception as e:
            print(f'Error removing task: {str(e)}')
        
    def finish_task(self, task_id):
        try:
            self.collection.update_one(
                {'_id':ObjectId(task_id)},
                {'$set':{'status':'Finished'}}
            )
            print('Task finished with success')
        except Exception as e:
            print(f'Error updating task {str(e)}')

    def tasks_list(self):
        tasks = list(self.collection.find({}, {"_id": 1, "task_name": 1, "category": 1,'priority':1 , "created_at": 1 , 'due_date':1, "status": 1,}))
        for task in tasks:
            task['id'] = str(task.pop('_id'))
        tasks_formatted = self.format_tasks_list(tasks)
        return tasks_formatted
    
    def format_tasks_list(self, tasks: list):
        formatted_tasks = []
        for task in tasks:
            # Formatating created_at
            if isinstance(task.get('created_at'), datetime):
                task['created_at'] = task['created_at'].strftime('%d/%m/%Y - %H:%M:%S')

            # Formating date in case ISO
            if 'due_date' in task:
                if isinstance(task['due_date'], datetime):
                    task['due_date'] = task['due_date'].strftime('%d/%m/%Y')
                elif isinstance(task['due_date'], str):
                    try:
                        task['due_date'] = datetime.strptime(task['due_date'], '%Y-%m-%d').strftime('%d/%m/%Y')
                    except ValueError:
                        task['due_date'] = 'Date not specified'
                else:
                    task['due_date'] = 'Date not specified'
            
            formatted_tasks.append({
                'id': task['id'],
                'task_name': task['task_name'],
                'category': task['category'],
                'priority': task['priority'],
                'created_at': task['created_at'],
                'due_date': task['due_date'],
                'status': task['status']
            })
        
        return formatted_tasks
    
    def check_len_db(self):
        return self.collection.count_documents({})

    def task_exists(self, task_name):
        task = self.collection.find_one({'task_name': task_name})
        return task is not None  # Return true if task exists else false
# Tests
if __name__ == '__main__':
    todoapp = TodoManager()
    tasks = todoapp.tasks_list()
    print(todoapp.check_len_db())
    todoapp.remove_task('Reuniao Ciranda')
    print(todoapp.check_len_db())

    

        
    