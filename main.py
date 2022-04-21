
import datetime
from icalendar import Calendar, Event, Alarm
import uuid
from datetime import timezone, timedelta


print("Please choose your language:")
print("请选择你的语言:")
print("1. English")
print("2. 中文")
print("请输入你的选择:")
# language = input("Please input your language:")
language = "2"

print("Please enter your medication cycle:")
print("请输入你的药物周期:")
# cycle_taking_pill = input()
cycle_taking_pill = 21

print("Please enter your withdrawal period:")
print("请输入你的停药周期:")
# cycle_stop_pill = input()
cycle_stop_pill = 7

reminderSetCN = {
    "calname": "短效小助手",
    "eventNameTakePill": "宝儿今天要吃药哦",
    "eventNameHaveARest": "宝儿今天得休息哦",
    "takingPillReminder": "该吃药了喔",
}

reminderSetEN = {
    "calname": "Short-term assistant",
    "eventNameTakePill": "Baby you need to take a pill today",
    "eventNameHaveARest": "Baby today is resting",
    "takingPillReminder": "Baby, It's time to take a pill",
}

reminderSet = reminderSetEN
if language == "2":
    reminderSet = reminderSetCN


def cread_event(eventName, start, end, createAlarm=False):
    # 创建事件/日程
    event = Event()
    event.add('summary', eventName)
    # datetime.datetime.now()
    dt_now = datetime.datetime.now(tz=tz_utc_8)
    event.add('dtstart', start)
    event.add('dtend', end)
    # 创建时间
    event.add('dtstamp', dt_now)
    # 重复
    event.add('rrule', {'freq': 'daily', 'interval': 28})
    # 提醒
    if createAlarm:
        alarm1 = Alarm()
        alarm1.add("action", "DISPLAY")
        alarm1.add("description", reminderSet["takingPillReminder"])
        alarm1.add("trigger", timedelta(minutes=0))
        event.add_component(alarm1)

        alarm2 = Alarm()
        alarm2.add("action", "DISPLAY")
        alarm2.add("description", reminderSet["takingPillReminder"])
        alarm2.add("trigger", timedelta(minutes=60))
        event.add_component(alarm2)

    # UID保证唯一
    event['uid'] = str(uuid.uuid1())

    return event


cal = Calendar()
cal.add('prodid', '-//Apple Inc.//Mac OS X 10.12//EN')
cal.add('version', '2.0')
cal.add('x-wr-calname', reminderSet["calname"])
cal.add('method', 'PUBLISH')
cal.add('x-apple-calendar-color', '#FC4208')
cal.add('class', 'PRIVATE')

tz_utc_8 = timezone(timedelta(hours=8))

startTime = datetime.datetime(2022, 4, 21, 18, 0, 0, 0, tzinfo=tz_utc_8)
# print(startTime)
for i in range(cycle_taking_pill):
    endTime = startTime + timedelta(minutes=1)
    eventName = reminderSet["eventNameTakePill"] + \
        "(" + str(i+1) + "/" + str(cycle_taking_pill) + ")"
    event = cread_event(eventName, startTime, endTime, 1)
    cal.add_component(event)
    startTime = endTime + timedelta(minutes=-1, days=1)

for i in range(cycle_stop_pill):
    endTime = startTime + timedelta(minutes=1)
    eventName = reminderSet["eventNameHaveARest"] + \
        "(" + str(i+1) + "/" + str(cycle_stop_pill) + ")"
    event = cread_event(eventName, startTime, endTime)
    cal.add_component(event)
    startTime = endTime + timedelta(minutes=-1, days=1)


# print(cal.to_ical())
with open("test.ics", "wb") as f:
    f.write(cal.to_ical())
