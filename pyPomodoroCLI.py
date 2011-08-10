#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time


def main():
    work_time = 60 * get_int_input(
        "Please enter an Integer for the Pomodoro (default 25 minutes): ", 25)
    rest_time = 60 * get_int_input(
        "Please enter an Integer for the Rest time (default 5 minutes): ", 5)

    count_down(work_time, "Pomodoro time left {0}")
    print("Press Enter to start rest {0}".format(
        time_format(rest_time)))
    input()

    count_down(rest_time, "Rest time left {0}")
    print("Go back to work! Please press Enter.")
    input()

    return 0


def get_int_input(msg, default_value):
    int_value = default_value

    print(msg)

    while True:
        line = input()
        if line:
            try:
                int_value = int(line)
                break
            except Exception as err:
                print(err)
                print(msg)
                continue
        else:
            break

    return int_value


def count_down(total_time, msg):
    for past_time in range(total_time):
        print(msg.format(time_format(total_time - past_time)))
        time.sleep(1)


def time_format(time_in_seconds):
    minutes = time_in_seconds // 60
    seconds = time_in_seconds % 60
    return "{0:0>2}:{1:0>2}".format(minutes, seconds)


if __name__ == '__main__':
    main()
