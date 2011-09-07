#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
PomodoroTk is a simple timer based on The Pomodoro Technique
( www.pomodorotechnique.com ), written in Python 3 and Tkinter.
author:  Felix Lu
email:   lugh82@gmail.com
version: 0.2
date:    2011-08-20
'''

from tkinter import Tk, Entry, Label, Button, Frame, StringVar
from tkinter.messagebox import showinfo, showerror, askokcancel
from multilistbox import MultiListbox
import sqlite3
import os


class PomodoroTk(Frame):

    # create widgets
    def create_widgets(self):
        # create Pomodoro label and input field
        self.pomodoro_lbl = Label(self.parent, text='Pomodoro:')
        self.pomodoro_lbl.grid(row=0, column=0, sticky='E')

        self.pomodoro_time_value = StringVar()
        self.pomodoro_time_entry = Entry(self.parent,
                          textvariable=self.pomodoro_time_value,
                          justify='right', width=11)
        self.pomodoro_time_entry.grid(row=0, column=1)

        self.pomodoro_min_lbl = Label(self.parent, 
                                      text='minutes')
        self.pomodoro_min_lbl.grid(row=0, column=2, 
                                   sticky='W')

        # create Rest Time label and input field
        self.rest_time_lbl = Label(self.parent, 
                                   text='Rest Time:')
        self.rest_time_lbl.grid(row=1, column=0, sticky='E')

        self.rest_time_value = StringVar()
        self.rest_time_entry = Entry(self.parent,
                              textvariable=self.rest_time_value,
                              justify='right', width=11)
        self.rest_time_entry.grid(row=1, column=1)

        self.rest_time_min_lbl = Label(self.parent, 
                                       text='minutes')
        self.rest_time_min_lbl.grid(row=1, column=2, sticky='W')

        # create Cycle label and input field
        self.cycle_lbl = Label(self.parent, text='Cycle:')
        self.cycle_lbl.grid(row=2, column=0, sticky='E')

        self.cycle_value = StringVar()
        self.cycle_entry = Entry(self.parent, 
                                 textvariable=self.cycle_value, 
                                 justify='right', width=11)
        self.cycle_entry.grid(row=2, column=1)

        # create buttons
        self.start_btn = Button(self.parent,
                                command=self.start_cmd, width=8)
        self.start_btn.grid(row=3, column=2)

        self.cancel_btn = Button(self.parent,
                               command=self.cancel_cmd, width=8)
        self.cancel_btn.grid(row=3, column=0)

        self.rest_btn = Button(self.parent,
                               command=self.rest_cmd, width=8)
        self.rest_btn.grid(row=3, column=1)

        # create label to display the Left Time
        #self.status_lbl = Label(self.parent, 
        #                        font=('times', 12, 'bold'))
        #self.status_lbl.grid(row=4, column=0, sticky='EWNS')

        self.left_time_value = StringVar()
        self.left_time_lbl = Label(self.parent,
                              font=('monospace', 12, 'bold'),
                              textvariable=self.left_time_value)
        self.left_time_lbl.grid(row=4, column=0, columnspan=3,
                                sticky='EWNS')

        # pomodoro list
        self.pomodoro_list = MultiListbox(self.parent,
                                          (('No.', 5),
                                           ('Start', 10),
                                           ('End', 10),
                                           ('Task', 15),
                                           ('Status', 5)))
        self.pomodoro_list.grid(row=5, column=0, columnspan=3)

        # data initialize
        self.pomodoro_time_value.set(25)
        self.rest_time_value.set(5)
        self.cycle_value.set(4)
        self.left_time_value.set('{0:<10}{1:>8}'.format(
                                     self.STATUS_IDLE, '00:00'))

    # update widgets' status
    def update_widgets(self, status):
        self.left_time_value.set('{0:<10}{1:>8}'.format(status, 
                              self.time_format(self.left_time)))
        if status == self.STATUS_IDLE:
            self.start_btn.configure(text=self.LBL_START,
                                     state='normal')
            self.cancel_btn.configure(text=self.LBL_CANCEL,
                                      state='disabled')
            self.rest_btn.configure(text=self.LBL_REST,
                                    state='disabled')
            #self.status_lbl.configure(text=self.STATUS_IDLE,
            #                          bg=self.COLOR_IDLE)
            self.left_time_lbl.configure(bg=self.COLOR_IDLE)
        elif status == self.STATUS_WORKING:
            self.start_btn.configure(text=self.LBL_PAUSE)
            self.cancel_btn.configure(state='normal')
            self.rest_btn.configure(state='normal')
            #self.status_lbl.configure(text=self.STATUS_WORKING,
            #                          bg=self.COLOR_WORKING)
            self.left_time_lbl.configure(bg=self.COLOR_WORKING)
        elif status == self.STATUS_PAUSED:
            self.start_btn.configure(text=self.LBL_CONTINUE)
            #self.status_lbl.configure(text=self.STATUS_PAUSED,
            #                          bg=self.COLOR_PAUSED)
            self.left_time_lbl.configure(bg=self.COLOR_PAUSED)
        elif status == self.STATUS_RESTING:
            self.start_btn.configure(text=self.LBL_PAUSE)
            self.rest_btn.configure(state='disabled')
            #self.status_lbl.configure(text=self.STATUS_RESTING,
            #                          bg=self.COLOR_RESTING)
            self.left_time_lbl.configure(bg=self.COLOR_RESTING)
        else:
            pass

    # command of Start/Pause/Continue button
    def start_cmd(self):
        # start from Idle
        if self.status == self.STATUS_IDLE:
            if not self.continue_cycle:
                # get verified input
                self.pomodoro_time = self.get_int(
                            self.pomodoro_time_value.get()) * 60
                self.rest_time = self.get_int(
                                self.rest_time_value.get()) * 60
                self.cycle_count = self.get_int(
                                         self.cycle_value.get())

            if self.pomodoro_time > 0:
                if self.rest_time > 0:
                    # reset status and indicator
                    self.status = self.STATUS_WORKING
                    self.paused = False
                    self.left_time = self.pomodoro_time
                    self.update_widgets(self.status)
                    # start count down for Pomodoro
                    self.update()
                else:
                    self.invalid_input_msg_of('Rest Time')
            else:
                self.invalid_input_msg_of('Pomodoro')

        # pause/continue for working or resting
        elif (self.status == self.STATUS_WORKING
           or self.status == self.STATUS_RESTING):
            # pause
            if not self.paused:
                # switch pause indicator
                self.paused = True
                # change widgets' state, but don't change status
                self.update_widgets(self.STATUS_PAUSED)
                # pause count down
                self.left_time_lbl.after_cancel(self.after_id)
            # continue
            else:
                # switch pause indicator
                self.paused = False
                self.update_widgets(self.status)
                # continue count down
                self.update()

        # to be extended
        else:
            pass

    # command of Cancel button
    def cancel_cmd(self):
        self.left_time_lbl.after_cancel(self.after_id)
        if askokcancel('Question', 'Do you really want to '
                    'cancel the whole Pomodoro cycle now?'):
            # update status indicator
            self.status = self.STATUS_CANCELLED
            # terminal count down
            self.left_time = 0
            if self.paused:
                self.paused = False
        self.update()

    # command of Rest button
    def rest_cmd(self):
        self.left_time_lbl.after_cancel(self.after_id)
        if self.status == self.STATUS_WORKING:
            if askokcancel('Question', 'Do you really want to '
                  'terminal the Pomodoro and have a Rest Now?'):
                self.pomodoro_time -= (self.left_time + 1)
                self.left_time = 0
                if self.paused:
                    self.paused = False
        else:
            pass
        self.update()

    # count down
    def update(self):
        if not self.paused:
            # update Left Time label
            self.left_time_value.set('{0:<10}{1:>8}'.format(
                 self.status, self.time_format(self.left_time)))
            # Pomodoro or Rest not finished
            if self.left_time > 0:
                self.left_time -= 1
                self.after_id = self.left_time_lbl.after(1000,
                                                    self.update)
            # Pomodoro finished
            elif self.status == self.STATUS_WORKING:
                showinfo('Information', 'You have worked for '
                         '{0}, have a break now.'.format(
                         self.time_format(self.pomodoro_time)))
                # reset Left Time to Rest Time
                self.left_time = self.rest_time
                # update status and label
                self.status = self.STATUS_RESTING
                self.update_widgets(self.status)
                # continue count down for Rest
                self.update()
            # Rest finished
            elif self.status == self.STATUS_RESTING:
                self.cycle_count -= 1
                self.status = self.STATUS_IDLE
                if (self.cycle_count > 0 
                   and askokcancel('Question', 
                          'You have finished a Pomodoro cycle. '
                          'Do you want to continue?')):
                    self.continue_cycle = True
                    self.start_cmd()
                else:
                    showinfo('Information', 
                       'You have finished all Pomodoro cycles. '
                       'Have a long break now.')
                    self.continue_cycle = False
                    self.update_widgets(self.status)
            # manual stopped
            else:
                self.status = self.STATUS_IDLE
                self.update_widgets(self.status)
        # paused
        else:
            pass

    # verify input value
    def get_int(self, var_input):
        var_int = 0
        if var_input:
            try:
                var_int = int(var_input)
            except Exception as e:
                print(e)
        else:
            pass
        return var_int

    # display message for invalid input
    def invalid_input_msg_of(self, var_name):
        showerror('Invalid Input', 'Invalid input. "{0}" must '
              'be Integer and greater than 0.'.format(var_name))

    # convert the second count into HH:MM:SS format
    def time_format(self, time_in_sec):
        time_hrs = time_in_sec // 3600
        time_sec = time_in_sec % 60
        if time_hrs:
            time_min = (time_in_sec - time_hrs * 3600) // 60
            return '{0}:{1:0>2}:{2:0>2}'.format(time_hrs,
                                             time_min, time_sec)
        else:
            time_min = time_in_sec // 60
            return '{0:0>2}:{1:0>2}'.format(time_min, time_sec)

    # database initialize
    def init_db(self):
        self.cur.execute("""
            create table Pomodoro (
                id         integer primary key autoincrement,
                start_time text,
                end_time   text,
                task       text,
                is_valid   integer
            );
        """)
        self.con.commit()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.grid(row=0, column=0)

        self.LBL_START = 'Start'
        self.LBL_PAUSE = 'Pause'
        self.LBL_CONTINUE = 'Continue'
        self.LBL_CANCEL = 'Cancel'
        self.LBL_REST = 'Rest Now'

        self.COLOR_IDLE = 'red'
        self.COLOR_WORKING = 'green'
        #self.COLOR_WORKING_PAUSED = 'yellow'
        self.COLOR_RESTING = '#86ceff'
        #self.COLOR_RESTING_PAUSED = 'orange'
        self.COLOR_PAUSED = 'yellow'

        self.STATUS_IDLE = 'Idle'
        self.STATUS_WORKING = 'Working'
        #self.STATUS_WORKING_PAUSED = 'Paused'
        self.STATUS_RESTING = 'Resting'
        #self.STATUS_RESTING_PAUSED = 'Paused'
        self.STATUS_PAUSED = 'Paused'
        self.STATUS_CANCELLED = 'Cancelled'

        self.create_widgets()
        
        self.db_name = 'pomodoroTk.db'
        self.db_path = os.path.join(os.path.expanduser('~'), self.db_name)
        
        self.con = sqlite3.connect(self.db_path)
        self.con.isolation_level = None
        self.cur = self.con.cursor()

        if not os.path.isfile(self.db_path):
            self.init_db()

        # data initialize
        self.pomodoro_time = 0
        self.rest_time = 0
        self.left_time = 0
        self.paused = False             # pause status indicator
        self.after_id = 0               # for canceling .after
        self.status = self.STATUS_IDLE  # indicator of status
        self.cycle_count = 0
        self.continue_cycle = False

        self.update_widgets(self.status)


app = Tk()
app.title('PomodoroTk')
window = PomodoroTk(app)
app.mainloop()
