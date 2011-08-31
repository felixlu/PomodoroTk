#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from tkinter import *
from multilistbox import MultiListbox


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
            spent_time     integer
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
    title = input('Task Title: ')
    task = input('Task: ')
    return (title, task)


def get_id(action):
    while True:
        line = input('Please enter Task ID to {0}: '.format(action))
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


def confirm_action(action, task_id):
    show_tasks(task_id)
    confirm = input('Do you want to {0} the above task? (y/N) '.format(action))
    if confirm in ('Y', 'y', 'Yes', 'YES', 'yes'):
        return True
    else:
        return False


def refresh_task_list():
    list_size = task_list.size()
    if list_size > 0:
        task_list.delete(0, list_size-1)
    query = """SELECT id, title, task FROM Task;"""
    cur.execute(query)
    rows = cur.fetchall()
#    task_count = len(rows)
#    columns = ('No.', 'Title', 'Task')
#    task_list.insert(columns)
    i = 0
    for row in rows:
        i += 1
        task_list.insert(END, (i, row[1], row[2]))


def save_task_cmd():
    task_title = task_title_value.get()
    task_text = task_value.get()
    if task_title and task_text:
        task = (task_title, task_text)
        insert_task(task)
        refresh_task_list()
    else:
        pass


def edit_task_cmd():
    pass


def delete_task_cmd():
    pass


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

    save_task_btn = Button(app, text='Save', command=save_task_cmd)
    save_task_btn.grid(row=0, column=2)

    task_lbl = Label(app, text='Task:')
    task_lbl.grid(row=1, column=0)

    task_value = StringVar()
    task_entry = Entry(app, textvariable=task_value)
    task_entry.grid(row=1, column=1)

    edit_task_btn = Button(app, text='Edit', command=edit_task_cmd)
    edit_task_btn.grid(row=1, column=2)

    delete_task_btn = Button(app, text='Delete', command=delete_task_cmd)
    delete_task_btn.grid(row=2, column=2)

    task_list = MultiListbox(app, (('No.', 5), ('Title', 15), ('Task', 30)))
    task_list.grid(row=3, column=0, columnspan=3)

    CLI = False
    while CLI:
        line = input('Action? (I)nitDB/(A)dd/(E)dit/(D)elete'
                     '/(S)how/Enter(Exit): ')
        if line == 'I' or line == 'i':
            init_db()
        elif line == 'A' or line == 'a':
            task = get_task()
            insert_task(task)
        elif line == 'E' or line == 'e':
            tid = get_id('update')
            if confirm_action('update', tid):
                task = (tid, ) + get_task()
                update_task(task)
        elif line == 'D' or line == 'd':
            tid = get_id('delete')
            if confirm_action('delete', tid):
                delete_task(tid)
        elif line == 'S' or line == 's':
            tid = get_id('show')
            show_tasks(tid)
        elif not line:
            break

        conn.close()

    refresh_task_list()

    app.mainloop()
