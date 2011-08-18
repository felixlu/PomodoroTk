#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
PyPomodoro is a simple timer based on The Pomodoro Technique
( www.pomodorotechnique.com ), written in Python 3 and Tkinter.
author:  Felix Lu
email:   lugh82@gmail.com
version: 0.1
date:    2011-08-16
'''

from tkinter import Tk, Entry, Label, Button, Frame, IntVar, StringVar

from tkinter.messagebox import showinfo, showerror


class PyPomodoro(Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.grid(row=0, column=0)

        # create widgets
        
        # create Pomodoro label and input field
        self.pomodoro_lbl = Label(parent, text='Pomodoro:')
        self.pomodoro_lbl.grid(row=0, column=0, sticky='E')

        self.pomodoro_time_value = StringVar()
        self.pomodoro_time_entry = Entry(parent, 
                                 textvariable=self.pomodoro_time_value, 
                                 justify='right', width=6)
        self.pomodoro_time_entry.grid(row=0, column=1)
        self.pomodoro_time_value.set(25)

        self.pomodoro_min_lbl = Label(parent, text='minutes')
        self.pomodoro_min_lbl.grid(row=0, column=2, sticky='W')

        # create Rest Time label and input field
        self.rest_time_lbl = Label(parent, text='Rest Time:')
        self.rest_time_lbl.grid(row=1, column=0, sticky='E')

        self.rest_time_value = StringVar()
        self.rest_time_entry = Entry(parent, 
                                     textvariable=self.rest_time_value, 
                                     justify='right', width=6)
        self.rest_time_entry.grid(row=1, column=1)
        self.rest_time_value.set(5)

        self.rest_time_min_lbl = Label(parent, text='minutes')
        self.rest_time_min_lbl.grid(row=1, column=2, sticky='W')

        # create buttons
        self.start_btn = Button(parent, text='Start', 
                                command=self.start, width=7)
        self.start_btn.grid(row=2, column=0)

        self.pause_btn = Button(parent, text='Pause', 
                                command=self.pause, 
                                state='disabled', width=7)
        self.pause_btn.grid(row=2, column=1)

        self.stop_btn = Button(parent, text='Stop', command=self.stop, 
                              state='disabled', width=7)
        self.stop_btn.grid(row=2, column=2)

        # create label to display the Left Time
        self.status_lbl = Label(parent, text='Idle', 
                                font=('times', 20, 'bold'), bg='red')
        self.status_lbl.grid(row=3, column=0, sticky='EW')

        self.left_time_value = IntVar()
        self.left_time_lbl = Label(parent, 
                                   textvariable=self.left_time_value,
                                   font=('times', 20, 'bold'), bg='red')
        self.left_time_lbl.grid(row=3, column=1, columnspan=2, sticky='EW')
        self.left_time_value.set('0:00:00')

        # data initialize
        self.pomodoro_time = 0
        self.rest_time = 0
        self.left_time = 0
        self.paused = False # indicator of pause status
        self.cancel_id = 0  # used when canceling .after
        self.status = 0     # indicator of Pomodoro or Rest status
                            # 0 for Pomodoro start and finish
                            # 1 for Rest and auto finish
                            # 2 for manual stop

    # command of Start button
    def start(self):
        # get verified input
        self.pomodoro_time = self.get_int(
                                    self.pomodoro_time_value.get()) * 60
        self.rest_time = self.get_int(self.rest_time_value.get()) * 60

        if self.pomodoro_time > 0:
            if self.rest_time > 0:
                # update status of buttons and label
                self.start_btn.configure(state='disabled')
                self.pause_btn.configure(state='normal')
                self.stop_btn.configure(state='normal')
                self.status_lbl.configure(text='Working', bg='green')
                self.left_time_lbl.configure(bg='green')
                # reset status indicator
                self.status = 0
                self.left_time = self.pomodoro_time
                # start count down for Pomodoro
                self.update()
            else:
                self.invalid_input_msg_of('Rest Time')
        else:
            self.invalid_input_msg_of('Pomodoro')

    # command of Pause button
    def pause(self):
        # continue
        if self.paused:
            # switch pause indicator
            self.paused = False
            self.pause_btn.configure(text='Pause')
            if self.status == 0:
                self.status_lbl.configure(text='Working', bg='green')
                self.left_time_lbl.configure(bg='green')
            elif self.status == 1:
                self.status_lbl.configure(text='Resting', bg='blue')
                self.left_time_lbl.configure(bg='blue')
            else:
                pass
            # continue count down
            self.update()
        # pause
        else:
            # switch pause indicator
            self.paused = True
            self.pause_btn.configure(text='Continue')
            self.status_lbl.configure(text='Paused', bg='yellow')
            self.left_time_lbl.configure(bg='yellow')
            # pause count down
            self.left_time_lbl.after_cancel(self.cancel_id)

    # command of Stop button
    def stop(self):
        # reset pause indicator
        self.paused = False
        self.start_btn.configure(state='normal')
        self.pause_btn.configure(text='Pause', state='disabled')
        self.stop_btn.configure(state='disabled')
        self.status_lbl.configure(text='Idle', bg='red')
        self.left_time_lbl.configure(bg='red')
        # set manual stop status
        self.status = 2
        # terminal count down
        self.left_time = 0
        self.update()

    # count down
    def update(self):
        if not self.paused:
            # update Left Time label
            self.left_time_value.set(self.time_format(self.left_time))
            # Pomodoro or Rest not finished
            if self.left_time > 0:
                self.left_time -= 1
                self.cancel_id = self.left_time_lbl.after(1000, 
                                                          self.update)
            # Pomodoro finished
            elif self.status == 0:
                self.status = 1
                showinfo('Information', 'You have worked for {0}, '
                         'have a break now.'.format(
                         self.time_format(self.pomodoro_time)))
                # reset Left Time to Rest Time
                self.left_time = self.rest_time
                # update status label
                self.status_lbl.configure(text='Resting', bg='blue')
                self.left_time_lbl.configure(bg='blue')
                # continue count down for Rest
                self.update()
            # Rest finished
            elif self.status == 1:
                showinfo('Information', 'You have finished a Pomodoro '
                         'cycle. You can go ahead to the next one.')
                self.start_btn.configure(state='normal')
                self.pause_btn.configure(text='Pause', state='disabled')
                self.stop_btn.configure(state='disabled')
                self.status_lbl.configure(text='Idle', bg='red')
                self.left_time_lbl.configure(bg='red')
            # manual stopped
            else:
                pass
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
        showerror('Invalid Input', 
             '{0} must be Integer and greater than 0.'.format(var_name))

    # convert the second count into HH:MM:SS format
    def time_format(self, time_in_sec):
        time_hrs = time_in_sec // 3600
        time_sec = time_in_sec % 60
        if time_hrs:
            time_min = (time_in_sec - time_hrs * 3600) // 60
        else:
            time_min = time_in_sec // 60
        return '{0}:{1:0>2}:{2:0>2}'.format(time_hrs, 
                                            time_min, time_sec)


app = Tk()
app.title('PyPomodoro')
window = PyPomodoro(app)
app.mainloop()
