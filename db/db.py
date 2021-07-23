
# async def main():
#     async with asqlite.connect('example.db') as conn:
#         async with conn.cursor() as cursor:
#             # Create table
#             await cursor.execute('''CREATE TABLE stocks
#                                     (date text, trans text, symbol text, qty real, price real)''')
#
#             # Insert a row of data
#             await cursor.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
#
#             # Save (commit) the changes
#             await conn.commit()
#
# asyncio.run(main())


from os.path import isfile
from apscheduler.triggers.cron import CronTrigger
import asyncio
import asqlite

DB_PATH = "./data/database.db"
BUILD_PATH = "./db/build.sql"

def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()

    return inner

@with_commit
async def build():
    if isfile(BUILD_PATH):
        await scriptexec(BUILD_PATH)


async def scriptexec(path):
     async with asqlite.connect('example.db') as conn:
        async with conn.cursor() as cursor:
            with open(path, "r", encoding="utf-8") as script:
                cursor.executescript(script.read())


# from os.path import isfile
# from apscheduler.triggers.cron import CronTrigger
# import asyncio
# import asqlite
#
# DB_PATH = "./data/database.db"
# BUILD_PATH = "./db/build.sql"
#
# connection = connect(DB_PATH, check_same_thread=False)
# cursor = connection.cursor()
#
# def with_commit(func):
#     def inner(*args, **kwargs):
#         func(*args, **kwargs)
#         commit()
#
#     return inner
#
# @with_commit
# def build():
#     if isfile(BUILD_PATH):
#         scriptexec(BUILD_PATH)
#
# def commit():
#     connection.commit()
#
# def autosave(sched):
#     sched.add_job(commit, CronTrigger(second=0))
#
# def close():
#     connection.close()
#
# def field(command, *values):
#     cursor.execute(command, tuple(values))
#
#     if (fetch := cursor.fetchone()) is not None:
#         return fetch[0]
#
# def record(command, *values):
#     cursor.execute(command, tuple(values))
#
#     return cursor.fetchone()
#
# def records(command, *values):
#     cursor.execute(command, tuple(values))
#
#     return cursor.fetchall()
#
# def column(command, *values):
#     cursor.execute(command, tuple(values))
#
#     return [item[0] for item in cursor.fetchall()]
#
# def execute(command, *values):
#     cursor.execute(command, tuple(values))
#
# def multiexec(command, valueset):
#     cursor.executemany(command, valueset)
#
# def scriptexec(path):
#     with open(path, "r", encoding="utf-8") as script:
#         cursor.executescript(script.read())
