# -*- coding: UTF-8 -*-
import datetime
import logging
import threading
from typing import List

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from pydantic import BaseModel
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from task_manage.core import get_outlook_inbox_folders, get_task_dataframe, get_task_chart

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount('/static', StaticFiles(directory='static'), name='static')


class TaskQuery(BaseModel):
    start_date: str = None
    end_date: str = None
    filters: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/")
async def main(request: Request):
    try:
        mail_folders = get_outlook_inbox_folders()
    except Exception as e:
        logging.exception(e)
        mail_folders = ['获取邮件信息失败']

    task_dataframe = get_task_dataframe()

    return templates.TemplateResponse('index.html', {'request': request, 'mail_folders': mail_folders,
                                                     'task_dataframe': task_dataframe})


@app.get("/chart")
async def chart(request: Request):
    task_chart = get_task_chart()
    return templates.TemplateResponse('chart.html', {'request': request, 'task_chart': task_chart})


@app.post("/task_query/")
async def create_task_query(task_query: TaskQuery):
    logging.info(task_query)
    return get_task_dataframe()


@app.get('/file/{file_id}', response_class=FileResponse)
async def create_task_query(file_id: str):
    return file_id


if __name__ == '__main__':
    import uvicorn
    import webbrowser

    host_ip = '127.0.0.1'
    host_port = 8000
    url = f'http://{host_ip}:{host_port}'

    threading.Timer(2, webbrowser.open, args=(url,)).start()
    uvicorn.run(app, host=host_ip, port=host_port)
