from todoist import TodoistAPI
from Apis.config_loader import load_config
from datetime import datetime
from dateutil.tz import tzlocal


class Task:
    def __init__(self, name, date, project_name, project_color):
        self.name = name
        self.date = date
        self.project_name = project_name
        self.project_color = project_color

    def __str__(self):
        return self.name + "  " + str(self.date) + " " + self.project_name + "  " + str(self.project_color)

class TodoistApi:

    def __init__(self):
        self.config = load_config()
        api_token = self.config['todoist']['token']
        self.todoist = TodoistAPI(token=api_token)
        self.todoist.sync()
        self.projects = self.get_projects()

    def get_projects(self):
        projects = {}
        all_projects = self.todoist.projects.all()
        for project in all_projects:
            projects[project['id']] = {
                "color": project['color'],
                "name": project['name']
            }
        return projects

    def get_active_task(self):
        tasks = []
        all_tasks = self.todoist.items.all()
        for task in all_tasks:
            name = task['content']
            project_id = task['project_id']
            project_name = self.projects[project_id]["name"]
            project_color = self.projects[project_id]["color"]
            date = datetime.strptime(task['due_date_utc'],"%a %d %b %Y %H:%M:%S %z").astimezone(tzlocal())
            tasks.append(Task(name, date, project_name, project_color))
        tasks.sort(key=lambda r: r.date)
        return tasks


if __name__ == '__main__':
    api = TodoistApi()
    for t in api.get_active_task():
        print(t)
