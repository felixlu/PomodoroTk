#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from tkinter import *
from multilistbox import MultiListbox
from tkinter.messagebox import *


def init_db():
    cur.execute("""
        create table Task (
            id             integer primary key autoincrement,
            parent_task_id integer,
            title          text,
            task           text,
            index_no       integer,
            pomodoro_count integer,
            pomodoro_ids   text,
            estimated_mins integer,
            spent_time     integer,
            status         integer
        );
    """)
    cur.execute("""
        create table Pomodoro (
            id         integer primary key autoincrement,
            start_time text,
            end_time   text,
            duration   integer,
            is_broken  integer,
            remark     text
        );
    """)
    conn.commit()


def get_task():
    task_title = task_title_value.get()
    task_text = task_value.get()
    if task_title and task_text:
        task_title_value.set('')
        task_value.set('')
        return (task_title, task_text)
    else:
        return None


def get_id(action):
    while True:
        line = input(
                'Please enter Task ID to {0}: '.format(action))
        if line:
            try:
                tid = int(line)
                return tid
            except Exception as e:
                if line == 'A' or line == 'a':
                    return line
                else:
                    print(e)
                    continue
        else:
            continue


def insert_task(task):
    query = """
        INSERT INTO Task (title, task)
        VALUES('{0[0]}', '{0[1]}');""".format(task)
    cur.execute(query)
    conn.commit()


def update_task(task):
    query = """
        UPDATE Task
        SET title='{0[1]}',task='{0[2]}'
        WHERE id='{0[0]}';""".format(task)
    cur.execute(query)
    conn.commit()


def delete_task(task_id):
    query = """
        DELETE FROM Task
        WHERE id='{0}';""".format(task_id)
    cur.execute(query)
    conn.commit()


def show_tasks(task_id):
    if task_id == 'A' or task_id == 'a':
        query = """
            SELECT id, title, task FROM Task;"""
    else:
        query = """
            SELECT id, title, task FROM Task
            WHERE id='{0}';""".format(task_id)

    cur.execute(query)
    rows = cur.fetchall()

    #    keys = ('id', 'parent', 'title',
    #        'task', 'index', 'p.count',
    #        'p.ids', 'est.', 'spent')
    keys = ('id', 'title', 'task')
    if len(rows) > 0:
        for k in keys:
            print(k, end='\t')
        print()
    else:
        print('No tasks in the database...')

    for row in rows:
        for v in row:
            print(v, end='\t')
        print()


def get_task_by_id(task_id):
    query = """
        SELECT id, title, task FROM Task
        WHERE id='{0}';""".format(task_id)
    cur.execute(query)
    row = cur.fetchone()
    return (row[1], row[2])


def refresh_task_list():
    list_size = task_list.size()
    if list_size > 0:
        del(number_to_id[:])
        task_list.delete(0, list_size-1)
    query = """SELECT id, title, task FROM Task;"""
    cur.execute(query)
    rows = cur.fetchall()
#    task_count = len(rows)
#    columns = ('No.', 'Title', 'Task')
#    task_list.insert(columns)
    i = 0
    for row in rows:
        number_to_id.append(row[0])
        i += 1
        task_list.insert(END, (i, row[1], row[2]))


def get_selected_task_id():
    if len(task_list.curselection()) > 0:
        list_no = int(task_list.curselection()[0])
        return number_to_id[list_no]
    else:
        return None


def save_task_cmd():
    task = get_task()
    global editing_task_id
    if task:
        if editing_task_id == -1:
            insert_task(task)
            refresh_task_list()
        elif editing_task_id >= 0:
            task = (editing_task_id, ) + task
            update_task(task)
            refresh_task_list()
            editing_task_id = -1


def edit_task_cmd():
    tid = get_selected_task_id()
    global editing_task_id
    if tid != None:
        task = get_task_by_id(tid)
        task_title_value.set(task[0])
        task_value.set(task[1])
        editing_task_id = tid


def delete_task_cmd():
    tid = get_selected_task_id()
    if tid != None:
        if askokcancel('Confirmation', 'Are you sure to '
                       'delete the selected Task?'):
            delete_task(tid)
            refresh_task_list()


#def create_widgets():



if __name__ == '__main__':
    conn = sqlite3.connect('pytask.db')
    conn.isolation_level = None
    cur = conn.cursor()

    app = Tk()
#    create_widgets()

    task_title_lbl = Label(app, text='Title:')
    task_title_lbl.grid(row=0, column=0)

    task_title_value = StringVar()
    task_title_entry = Entry(app, textvariable=task_title_value)
    task_title_entry.grid(row=0, column=1)

    save_task_btn = Button(app, 
                           text='Save', command=save_task_cmd)
    save_task_btn.grid(row=0, column=2)

    task_lbl = Label(app, text='Task:')
    task_lbl.grid(row=1, column=0)

    task_value = StringVar()
    task_entry = Entry(app, textvariable=task_value)
    task_entry.grid(row=1, column=1)

    edit_task_btn = Button(app, 
                           text='Edit', command=edit_task_cmd)
    edit_task_btn.grid(row=1, column=2)

    delete_task_btn = Button(app, 
                         text='Delete', command=delete_task_cmd)
    delete_task_btn.grid(row=2, column=2)

    task_list = MultiListbox(app, 
                      (('No.', 5), ('Title', 15), ('Task', 30)))
    task_list.grid(row=3, column=0, columnspan=3)

    number_to_id = []
    list_no = 0
    editing_task_id = -1
    refresh_task_list()

    app.mainloop()
