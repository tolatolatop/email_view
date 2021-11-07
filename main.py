# -*- coding: UTF-8 -*-
import datetime
import logging
import threading
import uuid
from typing import List

from dateutil.parser import parse
from dateutil.tz import tzlocal
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from pydantic import BaseModel
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from task_manage.core import get_outlook_inbox_folders, get_task_dataframe, get_task_chart, task_query_record

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount('/static', StaticFiles(directory='static'), name='static')


class TaskQuery(BaseModel):
    from_date: str = None
    to_date: str = None
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

    task_dataframe = get_task_dataframe([])
    task_dataframe_headers = list(zip(task_dataframe.column_names, task_dataframe.column_ids))

    return templates.TemplateResponse('index.html', {'request': request, 'mail_folders': mail_folders,
                                                     'table_headers': task_dataframe_headers})


@app.get("/chart/{task_id}")
async def chart(request: Request, task_id: str):
    if task_id in task_query_record.keys():
        task_dataframe = task_query_record[task_id]
        task_chart = get_task_chart(task_dataframe)
        return templates.TemplateResponse('chart.html', {'request': request, 'task_chart': task_chart})
    else:
        raise HTTPException(status_code=404, detail="chart not found")


@app.post("/task_query/")
async def create_task_query(task_query: TaskQuery):
    tmp_id = uuid.uuid4().hex
    from_date = parse(task_query.from_date).replace(tzinfo=tzlocal())
    to_date = parse(task_query.to_date).replace(tzinfo=tzlocal())
    task_query_record[tmp_id] = get_task_dataframe(task_query.filters, from_date=from_date, to_date=to_date)
    return tmp_id


@app.get("/task/{task_id}")
async def get_task(task_id: str):
    if task_id in task_query_record.keys():
        task = task_query_record[task_id].data
        return task
    else:
        return []


@app.get('/file/{file_id}', response_class=FileResponse)
async def get_file(file_id: str):
    return file_id


if __name__ == '__main__':
    import uvicorn
    import webbrowser

    host_ip = '127.0.0.1'
    host_port = 8000
    url = f'http://{host_ip}:{host_port}'

    threading.Timer(2, webbrowser.open, args=(url,)).start()
    uvicorn.run(app, host=host_ip, port=host_port)
