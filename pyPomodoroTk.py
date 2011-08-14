#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import Frame, IntVar, StringVar, Entry, Label, Button, Tk
from tkinter.messagebox import showinfo
import threading

class PyPomodoro(Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.grid(row = 0, column = 0)
        self.create_widgets()


    def create_widgets(self):
        self.pomodoro_time = IntVar()
        self.pomodoro_time.set(25)
        self.rest_time = IntVar()
        self.rest_time.set(5)
        self.left_time = StringVar()
        self.left_time.set('00:00')
        self.start_button_text = StringVar()
        self.pause_button_text = StringVar()
        self.stop_button_text = StringVar()
        self.btn_state = 0
        self.left_time_value = 0

        pomodoro_label = Label(self, text='Pomodoro:')
        pomodoro_text = Entry(self, 
            textvariable=self.pomodoro_time, width=6)
        pomodoro_minutes_label = Label(self, text='(minutes)')
        rest_label = Label(self, text='Rest Time:')
        rest_text = Entry(self, 
            textvariable=self.rest_time, width=6)
        rest_minutes_label = Label(self, text='(minutes)')
        left_time_title_label = Label(self, text='Time Left:')
        self.left_time_label = Label(self, textvariable=self.left_time)
        self.start_button = Button(self, command=self.state_start, 
             textvariable=self.start_button_text)
        self.pause_button = Button(self, command=self.state_pause, 
             textvariable=self.pause_button_text)
        self.stop_button = Button(self, command=self.state_stop, 
             textvariable=self.stop_button_text)
        self.update_btn_state()

        pomodoro_label.grid(row=0, column=0, padx=2, pady=2)
        pomodoro_text.grid(row=0, column=1, padx=2, pady=2)
        pomodoro_minutes_label.grid(row=0, column=2, padx=2, pady=2)
        rest_label.grid(row=1, column=0, padx=2, pady=2)
        rest_text.grid(row=1, column=1, padx=2, pady=2)
        rest_minutes_label.grid(row=1, column=2, padx=2, pady=2)
        left_time_title_label.grid(row=2, column=0, padx=2, pady=2)
        self.left_time_label.grid(row=2, column=1, padx=2, pady=2)
        self.start_button.grid(row=3, column=0, padx=2, pady=2)
        self.pause_button.grid(row=3, column=1, padx=2, pady=2)
        self.stop_button.grid(row=3, column=2, padx=2, pady=2)


    def state_start(self):
        self.btn_state = 1
        self.update_btn_state()


    def state_pause(self):
        if self.btn_state == 2:
            self.btn_state = 3
        elif self.btn_state in (0, 1, 3):
            self.btn_state = 2
        else:
            pass
        self.update_btn_state()


    def state_stop(self):
        self.btn_state = 0
        self.update_btn_state()


    def update_btn_state(self):
        if self.btn_state == 0:
            self.left_time.set(self.time_format(
                self.pomodoro_time.get() * 60))
            self.start_button.configure(state='normal')
            self.start_button_text.set('Start')
            self.pause_button.configure(state='disabled')
            self.pause_button_text.set('Pause')
            self.stop_button.configure(state='disabled')
            self.stop_button_text.set('Stop')
        elif self.btn_state == 1:
            self.left_time.set(self.time_format(
                self.pomodoro_time.get() * 60))
            self.start_button.configure(state='disabled')
            self.pause_button.configure(state='normal')
            self.pause_button_text.set('Pause')
            self.stop_button.configure(state='normal')
            self.pomodoro()
        elif self.btn_state == 2:
            self.start_button.configure(state='disabled')
            self.pause_button.configure(state='normal')
            self.pause_button_text.set('Continue')
            self.stop_button.configure(state='normal')
        elif self.btn_state == 3:
            self.start_button.configure(state='disabled')
            self.pause_button.configure(state='normal')
            self.pause_button_text.set('Pause')
            self.stop_button.configure(state='normal')
        else:
            pass


    def pomodoro(self):
        self.count_down(self.pomodoro_time.get()) # * 60
        showinfo('Congratulations!', 
            'Pomodoro finished. Have a break now.')
        self.count_down(self.rest_time.get()) # * 60
        showinfo("It's so sad.", 
            'Rest time out. You should go back to work now.')
        self.state_stop()


    def count_down(self, total_time):
        for past_time in range(total_time + 1):
            self.left_time_value = total_time - past_time
            self.delay_update()


    def time_format(self, time_in_seconds):
        minutes = time_in_seconds // 60
        seconds = time_in_seconds % 60
        return "{0:0>2}:{1:0>2}".format(minutes, seconds)


    def set_left_time(self):
        self.left_time.set(self.time_format(self.left_time_value))


    def delay_update(self):
        self.left_time_label.update_idletasks()
        self.left_time_label.after(1000, self.set_left_time())


app = Tk()
app.title('PyPomodoro')
window = PyPomodoro(app)
app.mainloop()
