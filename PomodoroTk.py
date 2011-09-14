#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
PomodoroTk is a simple timer based on The Pomodoro Technique
( www.pomodorotechnique.com ), written in Python 3 and Tkinter.
author:  Felix Lu
email:   lugh82@gmail.com
version: 0.4
date:    2011-09-15
'''

import os
import time
import sqlite3
from tkinter import Tk, Entry, Label, Button, Frame, StringVar
from tkinter.messagebox import showinfo, showerror, askokcancel

from multilistbox import MultiListbox

from dlgCalendar import tkCalendar


class PomodoroTk(Frame):

    def create_widgets(self):
    # create widgets
        # create Pomodoro label and input field
        self.pomodoro_lbl = Label(self.parent, text='Pomodoro:')
        self.pomodoro_lbl.grid(row=0, column=0, sticky='E')

        self.pomodoro_time_value = StringVar()
        self.pomodoro_time_entry = Entry(self.parent, justify='right',
            textvariable=self.pomodoro_time_value)
        self.pomodoro_time_entry.grid(row=0, column=1)

        self.pomodoro_min_lbl = Label(self.parent, text='minutes')
        self.pomodoro_min_lbl.grid(row=0, column=2, sticky='W')

        # create Rest Time label and input field
        self.rest_time_lbl = Label(self.parent, text='Rest Time:')
        self.rest_time_lbl.grid(row=1, column=0, sticky='E')

        self.rest_time_value = StringVar()
        self.rest_time_entry = Entry(self.parent, justify='right',
            textvariable=self.rest_time_value)
        self.rest_time_entry.grid(row=1, column=1)

        self.rest_time_min_lbl = Label(self.parent, text='minutes')
        self.rest_time_min_lbl.grid(row=1, column=2, sticky='W')

        # create Cycle label and input field
        self.cycle_lbl = Label(self.parent, text='Cycle:')
        self.cycle_lbl.grid(row=2, column=0, sticky='E')

        self.cycle_value = StringVar()
        self.cycle_entry = Entry(self.parent, justify='right',
            textvariable=self.cycle_value)
        self.cycle_entry.grid(row=2, column=1)

        # create buttons
        self.start_btn = Button(self.parent, command=self.start_cmd)
        self.start_btn.grid(row=2, column=2)

        # task
        self.task_value = StringVar()
        self.task_lbl = Label(self.parent, text='Task:')
        self.task_lbl.grid(row=3, column=0, sticky='E')
        self.task_entry = Entry(self.parent, textvariable=self.task_value)
        self.task_entry.grid(row=3, column=1)
        self.edit_btn = Button(self.parent, text='Edit', command=self.edit_cmd)
        self.edit_btn.grid(row=3, column=2)
        self.save_btn = Button(self.parent, text='Save', command=self.save_cmd)
        self.save_btn.grid(row=3, column=3)

        # date
        self.date_var = StringVar()
        self.date_lbl = Label(self.parent, text='Date:')
        self.date_lbl.grid(row=4, column=0, sticky='E')
        self.date_entry = Entry(self.parent, textvariable=self.date_var)
        self.date_entry.grid(row=4, column=1)
        self.get_date_btn = Button(self.parent, text='Get Date',
            command=self.get_date_cmd)
        self.get_date_btn.grid(row=4, column=2)
        self.search_btn = Button(self.parent, text='Search',
            command=self.search_cmd)
        self.search_btn.grid(row=4, column=3)

        # pomodoro list
        self.pomodoro_list = MultiListbox(self.parent,
            (('No.', 3), ('Task', 30), ('Status', 10), ('Date', 11),
            ('Start', 9), ('Minutes', 5)))
        self.pomodoro_list.grid(row=5, column=0, columnspan=4)

        # left time and status
        self.left_time_value = StringVar()
        self.left_time_lbl = Label(self.parent,
            textvariable=self.left_time_value, font=('monospace', 12, 'bold'))
        self.left_time_lbl.grid(row=6, column=0, columnspan=4, sticky='EWNS')

        # data initialize
        self.pomodoro_time_value.set(25)
        self.rest_time_value.set(5)
        self.cycle_value.set(4)
        self.date_var.set(time.strftime('%Y-%m-%d', time.localtime()))
        self.left_time_value.set('{0:<10}{1:>8}'.format(
            self.STATUS_IDLE, '00:00'))

    def update_widgets(self, status):
    # update widgets' status
        self.left_time_value.set('{0:<10}{1:>8}'.format(status,
            time_format(self.left_time)))
        if status == self.STATUS_IDLE:
            self.start_btn.configure(text=self.LBL_START)
            self.left_time_lbl.configure(bg=self.COLOR_IDLE)
        elif status == self.STATUS_WORKING:
            self.start_btn.configure(text=self.LBL_CANCEL)
            self.left_time_lbl.configure(bg=self.COLOR_WORKING)
        elif status == self.STATUS_RESTING:
            self.left_time_lbl.configure(bg=self.COLOR_RESTING)
        else:
            pass

    def start_cmd(self):
    # command of Start/Cancel button
        if self.status == self.STATUS_IDLE:
        # start from Idle
            if not self.continue_cycle:
                # get verified input
                self.pomodoro_time = get_int(
                    self.pomodoro_time_value.get()) * 60
                self.rest_time = get_int(self.rest_time_value.get()) * 60
                self.cycle_count = get_int(self.cycle_value.get())

            if self.pomodoro_time > 0:
                if self.rest_time > 0:
                    # get start time
                    self.task_start_time = time.time()
                    # reset status and indicator
                    self.status = self.STATUS_WORKING
                    self.left_time = self.pomodoro_time
                    self.update_widgets(self.status)
                    # start count down for Pomodoro
                    self.update()
                else:
                    self.invalid_input_msg_of('Rest Time')
            else:
                self.invalid_input_msg_of('Pomodoro')

        elif self.status == self.STATUS_WORKING:
        # cancel work
            self.cancel_cmd(self.STATUS_W_CANCELLED)

        elif self.status == self.STATUS_RESTING:
        # cancel rest
            self.cancel_cmd(self.STATUS_R_CANCELLED)

        else:
        # to be extended
            pass

    def cancel_cmd(self, status):
    # command of Cancel button
        self.left_time_lbl.after_cancel(self.after_id)
        if askokcancel('Question',
            'Do you really want to cancel the whole Pomodoro cycle now?'):
                # get end time
                self.end_time = time.strftime('%H:%M:%S')
                self.is_valid = 0
                # update status indicator
                self.status = status
                # terminal count down
                self.left_time = 0
        self.update()

    def edit_cmd(self):
    # command of Edit button
        tid = self.get_selected_task_id()
        if tid != None:
            self.task_value.set(get_task_by_id(self.con, self.cur, tid))
            self.editing_task_id = tid

    def save_cmd(self):
    # command of Save button
        self.task_content = self.task_value.get()
        if self.task_content:
            if self.editing_task_id != -1:
                task = (self.editing_task_id, ) + (self.task_content, )
                update_task(self.con, self.cur, task)
                self.search_cmd()
                self.editing_task_id = -1
        else:
            showerror('Invalid input', '"Task" can not be empty!')

    def get_date_cmd(self):
    # command of select date from calendar
        tkCalendar(self.parent, self.this_year, self.this_month, self.today,
            self.date_var)

    def search_cmd(self):
    # command of search pomodoro by date, empty for all pomodoros
        date = self.date_var.get()
        if date:
            rows = get_tasks_by_date(self.cur, date)
        else:
            rows = get_all_tasks(self.cur)
        self.refresh_task_list(rows)

    def update(self):
    # count down
        # update Left Time label
        self.left_time_value.set('{0:<10}{1:>8}'.format(
             self.status, time_format(self.left_time)))

        if self.left_time > 0:
        # Pomodoro or Rest not finished
            self.left_time -= 1
            self.after_id = self.left_time_lbl.after(1000, self.update)

        elif self.status == self.STATUS_WORKING:
        # Pomodoro finished
            if self.cycle_count > 1:
                showinfo('Information',
                    'You have worked for {0}, have a break now.'.format(
                    time_format(self.pomodoro_time)))
                # get task end time and insert to db
                self.task_finished(True)
                # reset Left Time to Rest Time
                self.left_time = self.rest_time
                # update status and label
                self.status = self.STATUS_RESTING
                self.update_widgets(self.status)
                # continue count down for Rest
                self.update()
            else:
                showinfo('Information',
                    'You have finished all Pomodoro cycles. '
                    'Have a longer break now.')
                self.task_finished(True)
                self.continue_cycle = False
                self.status = self.STATUS_IDLE
                self.update_widgets(self.status)

        elif self.status == self.STATUS_RESTING:
        # Rest finished
            self.cycle_count -= 1
            self.status = self.STATUS_IDLE
            if askokcancel('Question',
                'You have finished a Pomodoro cycle. '
                'Do you want to continue?'):
                    self.continue_cycle = True
                    self.start_cmd()
            else:
                self.update_widgets(self.status)

        elif self.status == self.STATUS_W_CANCELLED:
        # Cancel work
            self.task_finished(False)
            self.status = self.STATUS_IDLE
            self.update_widgets(self.status)

        elif self.status == self.STATUS_R_CANCELLED:
        # Cancel rest
            self.status = self.STATUS_IDLE
            self.update_widgets(self.status)

        else:
            pass

    def invalid_input_msg_of(self, var_name):
    # display message for invalid input
        showerror('Invalid Input',
            'Invalid input. "{0}" must be Integer and greater than 0.'.format(
            var_name))

    def task_finished(self, task_is_valid):
        if task_is_valid:
            self.task_is_valid = 1
        else:
            self.task_is_valid = 0
        self.task_content = self.task_value.get()
        self.task_end_time = time.time()
        date = time.strftime('%Y-%m-%d', time.localtime(self.task_start_time))
        start = time.strftime('%H:%M:%S', time.localtime(self.task_start_time))
        minutes = (self.task_end_time - self.task_start_time) // 60
        task = (self.task_content, self.task_is_valid, date, start, minutes)
        insert_task(con, cur, task)
        self.search_cmd()

    def refresh_task_list(self, rows):
        list_size = self.pomodoro_list.size()
        if list_size > 0:
            del(self.number_to_id[:])
            self.pomodoro_list.delete(0, list_size-1)
        #rows = get_all_tasks(self.cur)
        i = 0
        for row in rows:
            self.number_to_id.append(row[0])
            i += 1
            self.pomodoro_list.insert(self.pomodoro_list.size(),
                (i, row[1], self.TASK_STATUS[row[2]], row[3], row[4], row[5]))

    def get_selected_task_id(self):
        if len(self.pomodoro_list.curselection()) > 0:
            list_no = int(self.pomodoro_list.curselection()[0])
            return self.number_to_id[list_no]
        else:
            return None

    def __init__(self, parent, con, cur):
        super().__init__(parent)
        self.parent = parent
        self.con = con
        self.cur = cur
        self.grid(row=0, column=0)

        self.LBL_START = 'Start'
        self.LBL_CANCEL = 'Cancel'

        self.COLOR_IDLE = 'red'
        self.COLOR_WORKING = 'green'
        self.COLOR_RESTING = 'yellow'

        self.STATUS_IDLE = 'Idle'
        self.STATUS_WORKING = 'Working'
        self.STATUS_RESTING = 'Resting'
        self.STATUS_W_CANCELLED = 'Work Cancelled'
        self.STATUS_R_CANCELLED = 'Rest Cancelled'

        self.TASK_STATUS = ['Cancelled', 'Finished']

        self.this_year = time.localtime()[0]
        self.this_month = time.localtime()[1]
        self.today = time.localtime()[2]

        self.create_widgets()

        # data initialize
        self.pomodoro_time = 0
        self.rest_time = 0
        self.left_time = 0
        self.after_id = 0               # for canceling .after
        self.status = self.STATUS_IDLE  # indicator of status
        self.cycle_count = 0
        self.continue_cycle = False
        # task
        self.task_content = None
        self.task_is_valid = 0
        self.task_start_time = None
        self.task_end_time = None
        self.editing_task_id = -1

        self.number_to_id = []

        self.update_widgets(self.status)
        self.search_cmd()


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
        date='{0}';
        """.format(date)
    cur.execute(query)
    return cur.fetchall()


def insert_task(con, cur, task):
    query = """
        INSERT INTO Pomodoro
        (task, is_valid, date, start_time, duration)
        VALUES
        ('{0[0]}', '{0[1]}', '{0[2]}', '{0[3]}', '{0[4]}');
        """.format(task)
    cur.execute(query)
    con.commit()


def get_task_by_id(con, cur, task_id):
    query = """
        SELECT id, task FROM Pomodoro
        WHERE id='{0}';
        """.format(task_id)
    cur.execute(query)
    row = cur.fetchone()
    return row[1]


def update_task(con, cur, task):
    query = """
        UPDATE Pomodoro
        SET task='{0[1]}'
        WHERE id='{0[0]}';
        """.format(task)
    cur.execute(query)
    con.commit()


def delete_task(con, cur, task_id):
    query = """
        DELETE FROM Task
        WHERE id='{0}';
        """.format(task_id)
    cur.execute(query)
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
