import logging

from py_mapi.core import get_outlook, get_accounts, MailFolder


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
        inbox = outlook.Folders(display_name)
        root_mail_box = MailFolder('/收件箱', inbox)
        for mail_folders, mails in root_mail_box.walk():
            for folder in mail_folders:
                folders.append({'name': folder.path, 'owner': display_name})
    return folders


def get_task_from_outlook(folder_path):
    outlook = get_outlook()
    accounts = get_accounts()
    result = []
    for account in accounts:
        display_name = account.DeliveryStore.DisplayName
        inbox = outlook.Folders(display_name)
        mail_box = MailFolder(folder_path, inbox)
        try:
            for mail in mail_box.list_mail():
                result.append([mail.sender_address, mail.subject, mail.received_time.strftime('%Y/%m/%d')])
        except FileNotFoundError as e:
            logging.exception(e)
    return result


def get_task_dataframe():
    all_tasks_data = []
    all_folder_path = ['/收件箱/阿里云', '/收件箱/信用卡']
    for folder_path in all_folder_path:
        tasks_data = get_task_from_outlook(folder_path)
        all_tasks_data.extend(tasks_data)

    task_dataframe = {
        'headers': ['发送人', '标题', '接收日期'],
        'data': all_tasks_data
    }
    return task_dataframe


def get_task_chart():
    task_chart = {
        'labels': ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        'data': [12, 19, 3, 5, 2, 3],
        'backgroundColor': [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
        ],
        'borderColor': [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
        ]
    }
    return task_chart
