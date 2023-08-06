"""
    
    Module contains tools to deal with the process related to time and scheduling 

    
"""
from enum import Enum
import typing
import time, datetime
import asyncio
import re
from typing import Coroutine, Generator


class Language(Enum):
    FR = 1
    EN = 2


def delta_time_from_now(hour, date=None):
    def add_date_to_hour(hour, date):
        hour = datetime.strptime(hour, "%H:%M:%S.%f")
        target = hour.replace(year=date.year, month=date.month, day=date.day)

        return target

    def format_in_milisec(format):
        if len(re.findall(r"\d{1,2}:\d{1,2}:\d{1,2}", format)) < 1:
            return format + ":00.00"
        if len(re.findall(r"\.[0-9]+$", format)) < 1:
            return format + ".00"
        return format

    def is_contain_date(format):
        return len(re.findall(r"[0-9]{1,2}/[0-9]{1,2}/[0-9]+", format)) > 0

    now = time.time()
    hour = format_in_milisec(hour)
    if is_contain_date(hour):

        date_time_obj = datetime.strptime(hour, "%d/%m/%Y %H:%M:%S.%f")
        target = date_time_obj.timestamp()

    else:
        if type(date) == str:
            date = datetime.strptime(date, "%d/%m/%Y")

        date_time_obj = add_date_to_hour(hour, date)

        target = date_time_obj.timestamp()

    return target - now


class Calendar:
    @staticmethod
    def date_range_day(
        start_date: datetime.datetime, end_date: datetime.datetime, step: int = 1
    ) -> Generator:
        for n in range(int((end_date - start_date).days)):
            yield start_date + datetime.timedelta(n)

    @staticmethod
    def numbers_days_between(
        start: datetime.datetime, end: datetime.datetime, week_day: int
    ) -> int:
        num_weeks, remainder = divmod((end - start).days, 7)
        if (week_day - start.weekday()) % 7 <= remainder:
            return num_weeks + 1
        else:
            return num_weeks

    @staticmethod
    def get_slots(
        amount: int,
        step: int = 1,
        start: datetime.datetime
        or typing.List[datetime.datetime] = datetime.datetime.now()
        + datetime.timedelta(1),
        end: datetime.datetime or typing.List[datetime.datetime] = None,
        language: Language = Language.FR,
    ) -> str:

        days = []
        if end:
            functional_days = (
                (end - start).days
                - Calendar.numbers_days_between(start, end, 5)
                - Calendar.numbers_days_between(start, end, 6)
            )
        else:
            end = start + datetime.timedelta(amount)
            end = end + datetime.timedelta(
                Calendar.numbers_days_between(start, end, 5)
                + Calendar.numbers_days_between(start, end, 6)
            )
            for date in Calendar.date_range_day(start, end):
                if date.weekday() not in (5, 6):
                    days.append(date)

        slots = "Le " + days[0].strftime("%d/%m")
        for i in range(1, len(days) - 1):
            slots += ", le " + days[i].strftime("%d/%m")
        if (n := len(days)) > 1:
            slots += ", et le " + days[n - 1].strftime("%d/%m")
        return slots


class Schedule:
    def __init__(self):
        self.tasks = []

    async def __to_do_after(self, fnc, delay):
        await asyncio.sleep(delay)
        await fnc

    def add_event(self, task, hour, date=None, name=None):
        delay = delta_time_from_now(hour, date)
        self.tasks.append(self.__to_do_after(task, delay))

    def start(self):
        async def main():
            concurrent_tasks = []
            for task in self.tasks:
                concurrent_tasks.append(asyncio.create_task(task))
            for task in concurrent_tasks:
                await task

        asyncio.run(main())


async def say_after(what):
    print(what)


if __name__ == "__main__":
    schedule = Schedule()
    schedule.add_event(task=say_after("badr"), hour="12:17", date=datetime.now())
    schedule.add_event(task=say_after("badr2"), hour="12:17:05", date="17/07/2021")
    schedule.start()
