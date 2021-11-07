import logging
from pydantic import BaseModel
from typing import List

from py_mapi.core import get_outlook, get_accounts, MailFolder

# 此处使用uuid缓存 会概率性引发BUG
task_query_record = {}


class Task(BaseModel):
    sender_name: str = ''
    subject: str = ''
    received_time: str = ''


class TaskDataFrame(BaseModel):
    column_names: List[str] = ['发送者', '标题', '发送时间']
    column_ids: List[str] = ['sender_name', 'subject', 'received_time']
    data: List[Task] = []

    def write_to_excel(self):
        print(self.data)


class TasksChart(BaseModel):
    labels: List[str] = []
    data: List[int] = []
    backgroundColor: List[str] = []
    borderColor: List[str] = []

    @staticmethod
    def background_color(index):
        if index % 2 == 0:
            return 'rgba(255, 99, 132, 0.2)'
        else:
            return 'rgba(54, 162, 235, 0.2)'

    @staticmethod
    def border_color(index):
        if index % 2 == 0:
            return 'rgba(255, 99, 132, 1)'
        else:
            return 'rgba(54, 162, 235, 1)'


def html_to_csv():
    pass


def csv_to_excel():
    pass


def get_outlook_inbox_folders():
    outlook = get_outlook()
    accounts = get_accounts()
    folders = []
    for account in accounts:
        display_name = account.DeliveryStore.DisplayName
        folders.append({'name': '/收件箱', 'owner': display_name})
        inbox = outlook.Folders(display_name)
        root_mail_box = MailFolder('/收件箱', inbox)
        for mail_folders, mails in root_mail_box.walk():
            for folder in mail_folders:
                folders.append({'name': folder.path, 'owner': display_name})
    return folders


def get_task_from_outlook(folder_path, from_date=None, to_date=None):
    outlook = get_outlook()
    accounts = get_accounts()
    result = []
    for account in accounts:
        display_name = account.DeliveryStore.DisplayName
        inbox = outlook.Folders(display_name)
        mail_box = MailFolder(folder_path, inbox)
        try:
            for mail in mail_box.list_mail(from_date=from_date, to_date=to_date):
                task = Task()
                task.sender_name = mail.sender_address
                task.subject = mail.subject
                task.received_time = mail.received_time.strftime('%Y/%m/%d')
                result.append(task)
        except FileNotFoundError as e:
            logging.exception(e)
    return result


def get_task_dataframe(all_folder_path, from_date=None, to_date=None):
    all_tasks_data = []
    for folder_path in all_folder_path:
        tasks_data = get_task_from_outlook(folder_path, from_date=from_date, to_date=to_date)
        all_tasks_data.extend(tasks_data)

    task_dataframe = TaskDataFrame()
    task_dataframe.data = all_tasks_data
    return task_dataframe


def get_task_chart(task_dataframe: TaskDataFrame):
    task_chart = TasksChart()
    chart_data = {}
    for data in task_dataframe.data:
        if data.sender_name in chart_data.keys():
            chart_data[data.sender_name] += 1
        else:
            chart_data[data.sender_name] = 1

    task_chart.labels = list(chart_data.keys())
    task_chart.data = [chart_data[label] for label in task_chart.labels]
    task_chart.borderColor = [task_chart.border_color(i) for i in range(len(task_chart.labels))]
    task_chart.backgroundColor = [task_chart.background_color(i) for i in range(len(task_chart.labels))]
    return task_chart
