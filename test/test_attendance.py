import unittest

from random import shuffle
from random import randint
from uuid import uuid4

from dateutil.parser import parse
from datetime import timedelta

from task_manage.core import TaskDataFrame
from task_manage.core import Task
from task_manage.core import AttendanceDataFrame


def random_date(from_date, end_date):
    from_date = parse(from_date)
    end_date = parse(end_date)
    delta_time = end_date - from_date
    delta_time = int(delta_time.total_seconds())
    while True:
        rand = timedelta(seconds=randint(0, delta_time))
        yield from_date + rand


class FuzzyTaskDataFrame(TaskDataFrame):

    def created_normal_data(self, number):
        work_random_date = random_date('2021-12-25 07:00', '2021-12-25 08:00')
        over_random_date = random_date('2021-12-25 17:30', '2021-12-25 23:59')
        for i in range(number):
            self.create_data(work_random_date, over_random_date)

    def created_expect_work_data(self, number):
        over_random_date = random_date('2021-12-25 17:30', '2021-12-25 23:59')
        expect_work_time = random_date('2021-12-25 08:00', '2021-12-25 23:59')
        for i in range(number):
            self.create_data(expect_work_time, over_random_date)

    def created_expect_over_data(self, number):
        work_random_date = random_date('2021-12-25 07:00', '2021-12-25 08:00')
        expect_over_time = random_date('2021-12-25 08:00', '2021-12-25 17:30')
        for i in range(number):
            self.create_data(work_random_date, expect_over_time)

    def create_data(self, random_1, random_2):
        sender_name = uuid4().hex
        t = Task(sender_name=sender_name, subject='上班邮件', received_time=next(random_1).isoformat())
        self.data.append(t)
        t = Task(sender_name=sender_name, subject='下班邮件', received_time=next(random_2).isoformat())
        self.data.append(t)


class TestAttendance(unittest.TestCase):

    def random_date(self, from_date, end_date):
        from_date = parse(from_date)
        end_date = parse(end_date)
        delta_time = end_date - from_date
        delta_time = int(delta_time.total_seconds())
        while True:
            rand = timedelta(seconds=randint(0, delta_time))
            yield from_date + rand

    def setUp(self) -> None:
        task_df = FuzzyTaskDataFrame()
        self.normal_num = 10
        self.work_expect = 4
        self.over_expect = 12
        task_df.created_normal_data(self.normal_num)
        task_df.created_expect_work_data(self.work_expect)
        task_df.created_expect_over_data(self.over_expect)

        self.task_dataframe = task_df

    def test_expect_check(self):
        attendance_dataframe = AttendanceDataFrame.load_from_task(self.task_dataframe)
        normal_num = len(tuple(t for t in attendance_dataframe.data if t.work_expect == '正常' and t.over_expect == '正常'))
        self.assertEqual(self.normal_num, normal_num)

        work_expect_num = len(tuple(t for t in attendance_dataframe.data if t.work_expect == '异常'))
        self.assertEqual(self.work_expect, work_expect_num)

        over_expect_num = len(tuple(t for t in attendance_dataframe.data if t.over_expect == '异常'))
        self.assertEqual(self.over_expect, over_expect_num)


if __name__ == '__main__':
    unittest.main()
