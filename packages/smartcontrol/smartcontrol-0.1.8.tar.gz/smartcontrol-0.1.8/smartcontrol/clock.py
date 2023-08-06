"""
    
    Module contains tools to deal with the process related to time and scheduling 

    
"""
from enum import Enum
import typing
import time, datetime
import asyncio
import re
from typing import Coroutine


class Language(Enum):
    FR = 1
    EN = 2


def delta_time_from_now(hour: str, date: (datetime.datetime or str) = None) -> float:
    def add_date_to_hour(hour: str, date: datetime.datetime) -> datetime.datetime:
        hour = datetime.datetime.strptime(hour, "%H:%M:%S.%f")
        target = hour.replace(year=date.year, month=date.month, day=date.day)

        return target

    def format_in_milisec(format: str) -> str:
        if len(re.findall(r"\d{1,2}:\d{1,2}:\d{1,2}", format)) < 1:
            return format + ":00.00"
        if len(re.findall(r"\.[0-9]+$", format)) < 1:
            return format + ".00"
        return format

    def is_contain_hour(format: str) -> bool:
        return len(re.findall(r"[0-9]{1,2}:[0-9]{1,2}(:\d{1,2}(\.\d+)?)?", format)) > 0

    def is_contain_date(format: str) -> bool:
        return len(re.findall(r"[0-9]{1,2}/[0-9]{1,2}/[0-9]+", format)) > 0

    now = time.time()
    hour = format_in_milisec(hour)
    if is_contain_date(hour):

        date_time_obj = datetime.datetime.strptime(hour, "%d/%m/%Y %H:%M:%S.%f")
        target = date_time_obj.timestamp()

    else:
        if type(date) == str:
            date = datetime.datetime.strptime(date, "%d/%m/%Y")

        date_time_obj = add_date_to_hour(hour, date)

        target = date_time_obj.timestamp()

    return target - now


class Calender:
    @staticmethod
    def date_range_day(
        start_date: datetime.datetime, end_date: datetime.datetime, step: int = 1
    ) -> Coroutine:
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
                - Calender.numbers_days_between(start, end, 5)
                - Calender.numbers_days_between(start, end, 6)
            )
        else:
            end = start + datetime.timedelta(amount)
            end = end + datetime.timedelta(
                Calender.numbers_days_between(start, end, 5)
                + Calender.numbers_days_between(start, end, 6)
            )
            for date in Calender.date_range_day(start, end):
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

    async def __to_do_after(self, fnc: typing.Coroutine, delay: float or int):
        if delay != 0:
            await asyncio.sleep(delay)
        await fnc

    def add_event(
        self,
        task: typing.Coroutine,
        hour: str = None,
        date: datetime.datetime = None,
        delay: float or int = None,
    ):
        if hour:
            if not date:
                date = datetime.datetime.now()
            delay = delta_time_from_now(hour, date)
        else:
            if not delay:
                delay = 0
        self.tasks.append(self.__to_do_after(task, delay))

    def start(self) -> None:
        async def main():
            concurrent_tasks = []
            for task in self.tasks:
                concurrent_tasks.append(asyncio.create_task(task))
            await asyncio.gather(*concurrent_tasks)

        asyncio.run(main())


async def say(what, d):
    global badr
    for i in range(10):
        badr += d
    print(badr)


async def say_after(what):
    global badr
    for i in range(10):
        await say(badr)
    print(badr)


if __name__ == "__main__":
    schedule = Schedule()
    global badr
    badr = 0
    schedule.add_event(task=say(badr, 3), delay=1)
    schedule.add_event(task=say(badr, 3))
    schedule.add_event(task=say(badr, 1))
    schedule.add_event(task=say(badr, 7))
    schedule.add_event(task=say(badr, 8))
    schedule.add_event(task=say(badr, 1))

    schedule.start()
    print(badr, badr)
