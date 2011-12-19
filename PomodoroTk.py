#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
PomodoroTk is a simple timer based on The Pomodoro Technique
( www.pomodorotechnique.com ), written in Python 3 and Tkinter.
author:  Felix Lu
email:   lugh82@gmail.com
version: 0.6
date:    2011-10-20
license: GNU GPL
'''

import os
import time
import sqlite3
from tkinter import Tk, Entry, Label, Button, Frame, StringVar
from tkinter.messagebox import showinfo, showerror, askokcancel

from multilistbox import MultiListbox

from dlgCalendar import tkCalendar


class PomodoroTk(Frame):

    def __init__(self, parent, con, cur):
        super().__init__(parent)
        self.parent = parent
        self.con = con
        self.cur = cur
        self.grid(row=0, column=0)

        # UI Constants
        self.START = 'Start'
        self.CANCEL = 'Cancel'

        self.COLOR_IDLE = 'red'
        self.COLOR_WORKING = 'green'
        self.COLOR_RESTING = 'yellow'

        self.IDLE = 'Idle'
        self.WORKING = 'Working'
        self.RESTING = 'Resting'

        self.STATUS_LEFT_TIME_FORMAT = '{0:<10}{1:>8}'
        self.DATE_FORMAT_YMD = '%Y-%m-%d'
        self.TIME_FORMAT_HMS = '%H:%M:%S'

        self.IDLE_REMINDER = 10     # in Minutes

        # Data initialize
        self.this_year = time.localtime()[0]
        self.this_month = time.localtime()[1]
        self.today = time.localtime()[2]

        self.pomodoro_time = 0
        self.rest_time = 0
        self.left_time = 0
        self.after_id = 0              # for canceling .after
        self.status = self.IDLE         # indicator of pomodoro status
        self.cycle_count = 0
        self.continue_cycle = False
        self.idle_time = 0
        self.idle_id = 0

        # Task data
        self.TASK_STATUS = ['Cancelled', 'Finished']
        self.task_content = None
        self.task_start_time = None
        self.task_end_time = None
        self.task_is_cancelled = False
        self.editing_task_id = -1
        self.number_to_id = []

        # Widgets init
        self.create_widgets()
        self.update_widgets()
        self.cmd_search()
        self.idle_check()

    def create_widgets(self):
        # Pomodoro label and input field
        self.lbl_pomodoro = Label(self.parent, text='Pomodoro:')
        self.lbl_pomodoro.grid(row=0, column=0, sticky='E')

        self.pomodoro_time_var = StringVar()
        self.entry_pomodoro_time = Entry(self.parent, justify='right',
            textvariable=self.pomodoro_time_var)
        self.entry_pomodoro_time.grid(row=0, column=1)

        self.lbl_pomodoro_min = Label(self.parent, text='minutes')
        self.lbl_pomodoro_min.grid(row=0, column=2, sticky='W')

        # Rest Time label and input field
        self.lbl_rest_time = Label(self.parent, text='Rest Time:')
        self.lbl_rest_time.grid(row=1, column=0, sticky='E')

        self.rest_time_var = StringVar()
        self.entry_rest_time = Entry(self.parent, justify='right',
            textvariable=self.rest_time_var)
        self.entry_rest_time.grid(row=1, column=1)

        self.lbl_rest_time_min = Label(self.parent, text='minutes')
        self.lbl_rest_time_min.grid(row=1, column=2, sticky='W')

        # Cycle label and input field
        self.lbl_cycle = Label(self.parent, text='Cycle:')
        self.lbl_cycle.grid(row=2, column=0, sticky='E')

        self.cycle_var = StringVar()
        self.entry_cycle = Entry(self.parent, justify='right',
            textvariable=self.cycle_var)
        self.entry_cycle.grid(row=2, column=1)

        # Start button
        self.btn_start = Button(self.parent, command=self.cmd_start)
        self.btn_start.grid(row=2, column=2)

        # Task input field and Edit/Save button
        self.task_var = StringVar()
        self.lbl_task = Label(self.parent, text='Task:')
        self.lbl_task.grid(row=3, column=0, sticky='E')

        self.entry_task = Entry(self.parent, textvariable=self.task_var)
        self.entry_task.grid(row=3, column=1)

        self.btn_edit = Button(self.parent, text='Edit', command=self.cmd_edit)
        self.btn_edit.grid(row=3, column=2)

        self.btn_save = Button(self.parent, text='Save', command=self.cmd_save)
        self.btn_save.grid(row=3, column=3)

        # Date field and Search button
        self.date_var = StringVar()
        self.lbl_date = Label(self.parent, text='Date:')
        self.lbl_date.grid(row=4, column=0, sticky='E')

        self.entry_date = Entry(self.parent, textvariable=self.date_var)
        self.entry_date.grid(row=4, column=1)

        self.btn_get_date = Button(self.parent, text='Get Date',
            command=self.cmd_get_date)
        self.btn_get_date.grid(row=4, column=2)

        self.btn_search = Button(self.parent, text='Search',
            command=self.cmd_search)
        self.btn_search.grid(row=4, column=3)

        # Pomodoro list
        self.mlb_pomodoro = MultiListbox(self.parent,
            (('No.', 3), ('Task', 30), ('Status', 10), ('Date', 11),
            ('Start', 9), ('Minutes', 5)))
        self.mlb_pomodoro.grid(row=5, column=0, columnspan=4)

        # Left time and status
        self.left_time_var = StringVar()
        self.lbl_left_time = Label(self.parent,
            textvariable=self.left_time_var, font=('monospace', 12, 'bold'))
        self.lbl_left_time.grid(row=6, column=0, columnspan=4, sticky='EWNS')

        # Data initialize
        self.pomodoro_time_var.set(25)
        self.rest_time_var.set(5)
        self.cycle_var.set(4)
        self.date_var.set(time.strftime(self.DATE_FORMAT_YMD, time.localtime()))
        self.left_time_var.set(self.STATUS_LEFT_TIME_FORMAT.format(
            self.IDLE, '00:00'))

    def update_widgets(self):
        self.left_time_var.set(self.STATUS_LEFT_TIME_FORMAT.format(self.status,
            time_format(self.left_time)))
        if self.status == self.IDLE:
            self.btn_start.configure(text=self.START)
            self.lbl_left_time.configure(bg=self.COLOR_IDLE)
        elif self.status == self.WORKING:
            self.btn_start.configure(text=self.CANCEL)
            self.lbl_left_time.configure(bg=self.COLOR_WORKING)
        elif self.status == self.RESTING:
            self.lbl_left_time.configure(bg=self.COLOR_RESTING)
        else:
            pass

    def cmd_start(self):
        # start from Idle
        if self.status == self.IDLE:
            self.idle_time = 0
            self.lbl_left_time.after_cancel(self.idle_id)
            if not self.continue_cycle:
                # get verified input
                self.pomodoro_time = get_int(self.pomodoro_time_var.get()) * 60
                self.rest_time = get_int(self.rest_time_var.get()) * 60
                self.cycle_count = get_int(self.cycle_var.get())

            if self.pomodoro_time > 0:
                if self.rest_time > 0:
                    # reset status and indicator
                    self.task_is_cancelled = False
                    self.status = self.WORKING
                    self.left_time = self.pomodoro_time
                    self.update_widgets()
                    # get start time
                    self.task_start_time = time.time()
                    # start count down for Pomodoro
                    self.count_down()
                else:
                    self.invalid_input_msg_of('Rest Time')
            else:
                self.invalid_input_msg_of('Pomodoro')

        # cancel work or rest
        elif self.status == self.WORKING or self.status == self.RESTING:
            self.cmd_cancel()

        else:
            pass

    def cmd_cancel(self):
        self.lbl_left_time.after_cancel(self.after_id)
        if askokcancel('Question',
            'Do you really want to cancel the whole Pomodoro cycle now?'):
                # get end time
                self.end_time = time.strftime(self.TIME_FORMAT_HMS)
                self.task_is_cancelled = True
                # terminal count down
                self.left_time = 0
        self.count_down()

    def count_down(self):
        '''count down and update widgets'''
        # update Status and Left Time label
        self.left_time_var.set(self.STATUS_LEFT_TIME_FORMAT.format(
             self.status, time_format(self.left_time)))

        # Work or Rest not finished
        if self.left_time > 0:
            self.left_time -= 1
            self.after_id = self.lbl_left_time.after(1000, self.count_down)
        else:
            self.change_status()

    def change_status(self):
        # Work finished
        if self.status == self.WORKING:
            if self.task_is_cancelled:
                self.get_and_add_task()
                self.status = self.IDLE
                self.update_widgets()
                self.task_is_cancelled = False
                self.idle_check()
            else:
                # cycles not finished
                if self.cycle_count > 1:
                    showinfo('Information',
                        'You have worked for {0}, have a break now.'.format(
                        time_format(self.pomodoro_time)))
                    self.get_and_add_task()
                    self.left_time = self.rest_time
                    self.status = self.RESTING
                    self.update_widgets()
                    self.count_down()
                # all cycles finished
                else:
                    showinfo('Information',
                        'You have finished all Pomodoro cycles. \
                        Have a longer break now.')
                    self.get_and_add_task()
                    self.continue_cycle = False
                    self.status = self.IDLE
                    self.update_widgets()
                    self.idle_check()

        # Rest finished
        elif self.status == self.RESTING:
            if self.task_is_cancelled:
                self.status = self.IDLE
                self.update_widgets()
                self.task_is_cancelled = False
                self.idle_check()
            else:
                self.cycle_count -= 1
                self.status = self.IDLE
                if askokcancel('Question',
                    'You have finished a Pomodoro cycle. \
                    Do you want to continue?'):
                        self.continue_cycle = True
                        self.cmd_start()
                else:
                    self.continue_cycle = False
                    self.update_widgets()
                    self.idle_check()

        else:
            pass

    def get_and_add_task(self):
        # get task data
        self.task_content = self.task_var.get()
        if self.task_is_cancelled:
            task_is_valid = 0
        else:
            task_is_valid = 1
        self.task_end_time = time.time()
        date = time.strftime(self.DATE_FORMAT_YMD,
            time.localtime(self.task_start_time))
        start = time.strftime(self.TIME_FORMAT_HMS,
            time.localtime(self.task_start_time))
        minutes = (self.task_end_time - self.task_start_time) // 60
        task = (self.task_content, task_is_valid, date, start, minutes)
        # insert to db
        insert_task(con, cur, task)
        self.cmd_search()

    def cmd_edit(self):
        tid = self.get_selected_task_id()
        if tid != None:
            self.task_var.set(get_task_by_id(self.con, self.cur, tid))
            self.editing_task_id = tid

    def cmd_save(self):
        self.task_content = self.task_var.get()
        if self.task_content:
            if self.editing_task_id != -1:
                task = (self.editing_task_id, ) + (self.task_content, )
                update_task(self.con, self.cur, task)
                self.cmd_search()
                self.editing_task_id = -1
        else:
            showerror('Invalid input', '"Task" can not be empty!')

    def cmd_get_date(self):
        tkCalendar(self.parent, self.this_year, self.this_month, self.today,
            self.date_var)

    def cmd_search(self):
        date = self.date_var.get()
        if date:
            rows = get_tasks_by_date(self.cur, date)
        else:
            rows = get_all_tasks(self.cur)
        self.refresh_task_list(rows)

    def invalid_input_msg_of(self, var_name):
    # display message for invalid input
        showerror('Invalid Input',
            'Invalid input. "{0}" must be Integer and greater than 0.'.format(
            var_name))

    def refresh_task_list(self, rows):
        list_size = self.mlb_pomodoro.size()
        if list_size > 0:
            del(self.number_to_id[:])
            self.mlb_pomodoro.delete(0, list_size-1)
        #rows = get_all_tasks(self.cur)
        i = 0
        for row in rows:
            self.number_to_id.append(row[0])
            i += 1
            self.mlb_pomodoro.insert(self.mlb_pomodoro.size(),
                (i, row[1], self.TASK_STATUS[row[2]], row[3], row[4], row[5]))

    def get_selected_task_id(self):
        if len(self.mlb_pomodoro.curselection()) > 0:
            list_no = int(self.mlb_pomodoro.curselection()[0])
            return self.number_to_id[list_no]
        else:
            return None

    def idle_check(self):
        if self.IDLE_REMINDER <= 0:
            pass
        else:
            if self.idle_time < self.IDLE_REMINDER:
                self.idle_time += 1
                self.idle_id = self.lbl_left_time.after(60000, self.idle_check)
            else:
                if askokcancel('Question', "You've idled for {0} minutes. Do \
                    you want to start working now?".format(self.IDLE_REMINDER)):
                    self.cmd_start()
                else:
                    self.idle_time = 0
                    self.idle_check()


def time_format(time_in_sec):
    # convert the second count into HH:MM:SS format
    time_hrs = time_in_sec // 3600
    time_sec = time_in_sec % 60
    if time_hrs:
        time_min = (time_in_sec - time_hrs * 3600) // 60
        return '{0}:{1:0>2}:{2:0>2}'.format(time_hrs, time_min, time_sec)
    else:
        time_min = time_in_sec // 60
        return '{0:0>2}:{1:0>2}'.format(time_min, time_sec)


def get_int(var_input):
    # verify input value
    var_int = 0
    if var_input:
        try:
            var_int = int(var_input)
        except Exception as e:
            print(e)
    else:
        pass
    return var_int


def init_db(con, cur):
    # database initialize
    cur.execute("""
        CREATE TABLE Pomodoro (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            task       TEXT,
            is_valid   INTEGER,
            date       TEXT,
            start_time TEXT,
            duration   INTEGER
            );
        """)
    con.commit()


def get_all_tasks(cur):
    query = """SELECT id, task, is_valid, date, start_time, duration
        FROM Pomodoro;
        """
    cur.execute(query)
    return cur.fetchall()


def get_tasks_by_date(cur, date):
    query = """SELECT id, task, is_valid, date, start_time, duration
        FROM Pomodoro
        WHERE
        date=?;
        """
    cur.execute(query, (date, ))
    return cur.fetchall()


def insert_task(con, cur, task):
    query = """
        INSERT INTO Pomodoro
        (task, is_valid, date, start_time, duration)
        VALUES
        (?, ?, ?, ?, ?);
        """
    cur.execute(query, task)
    con.commit()


def get_task_by_id(con, cur, task_id):
    query = """
        SELECT id, task FROM Pomodoro
        WHERE id=?;
        """
    cur.execute(query, (task_id, ))
    row = cur.fetchone()
    return row[1]


def update_task(con, cur, task):
    query = """
        UPDATE Pomodoro
        SET task=?
        WHERE id=?;
        """
    cur.execute(query, (task[1], task[0]))
    con.commit()


def delete_task(con, cur, task_id):
    query = """
        DELETE FROM Task
        WHERE id=?;
        """
    cur.execute(query, (task_id, ))
    con.commit()


if __name__ == '__main__':
    db_name = 'pomodoroTk.db'
    db_path = os.path.join(os.path.expanduser('~'), db_name)

    needs_init = False
    if not os.path.isfile(db_path):
        needs_init = True

    con = sqlite3.connect(db_path)
    con.isolation_level = None
    cur = con.cursor()

    if needs_init:
        try:
            init_db(con, cur)
        except Exception as e:
            print(e)

    app = Tk()
    app.title('PomodoroTk')
    window = PomodoroTk(app, con, cur)
    app.mainloop()
    con.close()
