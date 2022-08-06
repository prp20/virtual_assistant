from __future__ import print_function

import datetime
import os.path
import utils
import pytz, json


# SCOPES = ['https://www.googleapis.com/auth/tasks']

# service = utils.get_authenticated_google_service('tasks', 'v1', ['https://www.googleapis.com/auth/tasks'])

def create_new_tasklist(tasklistname):
    service = utils.get_authenticated_google_service('tasks', 'v1', ['https://www.googleapis.com/auth/tasks'])
    # Call the Tasks API
    tasklist = service.tasklists().insert(body={"title":tasklistname}).execute()
    return tasklist

def list_tasklists():
    service = utils.get_authenticated_google_service('tasks', 'v1', ['https://www.googleapis.com/auth/tasks'])
    tasklists = service.tasklists().list().execute()
    print(tasklists['items'][0]['id']) 


def create_new_tasks(textdata):
    tasklist_id = "MDg2OTc1NjU4NDk3Mzk1NjAwMzY6MDow"
    
    base_title = textdata.split("about")[1]
    task_title, base_time = base_title.split("on")
    due_date, due_time = base_time.split("at")
    print(due_date, due_time)
    utils.get_date(due_date, due_time)
    # global service
    # title = task_title
    # notes = ''
    # due = utils.convert_to_RFC_datetime(datetime.datetime.combine(utils.get_date(due_time), datetime.datetime.max.time()))
    # status = 'needsAction'
    # deleted = False

    # request_body = {
    #     'title': title,
    #     'notes': notes,
    #     'due': due,
    #     'deleted': deleted,
    #     'status': status
    # }
    # try:
    #     response = service.tasks().insert(tasklist=tasklist_id,body=request_body).execute()
    #     print(response)
    #     utils.respond("Task created successfully.")
    # except response.error != 0:
    #     utils.respond("Sorry that was unsuccessful. Please try again.")

def list_all_tasks(due=None, showCompleted=None):
    global service
    tasklist_id = "MDg2OTc1NjU4NDk3Mzk1NjAwMzY6MDow"
    print(due)
    due = utils.convert_to_RFC_datetime(due) if due else None

    showCompleted = True if showCompleted else False
    tasks_list = service.tasks().list(tasklist=tasklist_id,dueMax=due, showCompleted=showCompleted).execute()
    lstitems = tasks_list.get('items')
    lstitems = format_tasks(lstitems)
    return lstitems

def format_tasks(tasklists):
    result = []
    for task in tasklists:
        new_task = {}
        new_task['title'] = task['title']
        new_task['datetime'] = [utils.convert_to_local_time(task['due']).strftime("%d-%b-%Y:%H:%M") if 'due' in task else None][0]
        new_task['dateandtime'] = [utils.convert_to_local_time(task['due']).strftime("%A, %-d %B %Y, %-I:%M %p") if 'due' in task else None][0]
        result.append(new_task)
    return result

def tasks_asst(textdata):
    if "create" in textdata or "add" in textdata:
        print("calling create")
        create_new_tasks(textdata)
    elif "list" in textdata:
        reqdate = utils.get_date(textdata)
        end = datetime.datetime.combine(reqdate, datetime.datetime.max.time())
        isodate = utils.convert_to_RFC_datetime(end)
        list_of_tasks = list_all_tasks(due=end)
        utils.respond(f"You have a total of {len(list_of_tasks)} pending tasks.")
        for task in list_of_tasks:
            utils.respond(f"{task['title']} on {task['dateandtime']}")   


def main():
    list_all_tasks()

if __name__ == '__main__':
    main()