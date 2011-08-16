#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import Tk, Entry, Label, Button, Frame, IntVar, StringVar

from tkinter.messagebox import showinfo


class PyPomodoro(Frame):

    def __init__(self, parent):

        super().__init__(parent)
        self.parent = parent
        self.grid(row=0, column=0)

        self.pomodoro_lbl = Label(parent, text='Pomodoro:')
        self.pomodoro_lbl.grid(row=0, column=0)

        self.pomodoro_time_value = IntVar()
        self.pomodoro_time_entry = Entry(parent, 
                                         textvariable=self.pomodoro_time_value, 
                                         width=6)
        self.pomodoro_time_entry.grid(row=0, column=1)
        self.pomodoro_time_value.set(25)

        self.pomodoro_min_lbl = Label(parent, text='minutes')
        self.pomodoro_min_lbl.grid(row=0, column=2)

        self.rest_time_lbl = Label(parent, text='Rest Time:')
        self.rest_time_lbl.grid(row=1, column=0)

        self.rest_time_value = IntVar()
        self.rest_time_entry = Entry(parent, 
                                     textvariable=self.rest_time_value, 
                                     width=6)
        self.rest_time_entry.grid(row=1, column=1)
        self.rest_time_value.set(5)

        self.rest_time_min_lbl = Label(parent, text='minutes')
        self.rest_time_min_lbl.grid(row=1, column=2)

        self.start_btn = Button(parent, text='Start', command=self.start)
        self.start_btn.grid(row=2, column=0)

        self.pause_btn = Button(parent, text='Pause', command=self.pause, 
                               state='disabled')
        self.pause_btn.grid(row=2, column=1)

        self.stop_btn = Button(parent, text='Stop', command=self.stop, 
                              state='disabled')
        self.stop_btn.grid(row=2, column=2)

        self.left_time_value = IntVar()
        self.left_time_lbl = Label(parent, textvariable=self.left_time_value)
        self.left_time_lbl.grid(row=3, column=1)

        self.pomodoro_time = 0
        self.rest_time = 0
        self.left_time = 0
        self.paused = False
        self.cancel_id = 0

    def start(self):
        self.start_btn.configure(state='disabled')
        self.pause_btn.configure(state='normal')
        self.stop_btn.configure(state='normal')
        self.pomodoro_time = self.pomodoro_time_value.get() # * 60
        self.rest_time = self.rest_time_value.get() # * 60

        self.left_time = self.pomodoro_time
        self.update()

        self.left_time = self.rest_time
        self.update()
        
    def pause(self):
        if self.paused:
            self.paused = False
            self.pause_btn.configure(text='Pause')
            self.update()
        else:
            self.paused = True
            self.pause_btn.configure(text='Continue')
            self.left_time_lbl.after_cancel(self.cancel_id)

    def stop(self):
        self.left_time = 0
        self.paused = False
        self.start_btn.configure(state='normal')
        self.pause_btn.configure(text='Pause', state='disabled')
        self.stop_btn.configure(state='disabled')
        self.update()

    def update(self):
        if not self.paused:
            self.left_time_value.set(self.left_time)
            if self.left_time > 0:
                self.left_time -= 1
                self.cancel_id = self.left_time_lbl.after(1000, self.update)


app = Tk()
app.title('PyPomodoro')
window = PyPomodoro(app)
app.mainloop()
