import FreeSimpleGUI as sg
from time import sleep

from FreeSimpleGUI import SYMBOL_CIRCLE


# Outputs  "3...2...1" one
# character at a time.
def countdown(window):
    for i in range(0, 3):
        if i == 0:
            # Allows communication between thread and main thread.
            window.write_event_value(('-THREAD-', '-TITLE-'), i)
            window.write_event_value(('-THREAD-', '-THREE-'), i)
        if i == 1:
            window.write_event_value(('-THREAD-', '-TWO-'), i)
        if i == 2:
            window.write_event_value(('-THREAD-', '-ONE-'), i)
            sleep(0.5)
            window.write_event_value(('-THREAD-', '-OPEN_WINDOW-'), i)
        for c in range(0, 3):
            sleep(0.25)
            if i == 0:
                if c == 0:
                    window.write_event_value(('-THREAD-', '-PERIOD1-'), c)
                if c == 1:
                    window.write_event_value(('-THREAD-', '-PERIOD2-'), c)
                if c == 2:
                    window.write_event_value(('-THREAD-', '-PERIOD3-'), c)
                    sleep(0.25)
            if i == 1:
                if c == 0:
                    window.write_event_value(('-THREAD-', '-PERIOD4-'), c)
                if c == 1:
                    window.write_event_value(('-THREAD-', '-PERIOD5-'), c)
                if c == 2:
                    window.write_event_value(('-THREAD-', '-PERIOD6-'), c)
                    sleep(0.25)

# The first window for the GUI.
# The user presses Begin to start calibration.
def window_one():
    # Layout for window one.
    layout_one = [[sg.Push(), sg.Text("Welcome!", text_color='white', auto_size_text=True), sg.Push()],
                 [sg.Push(), sg.Text('Press "Begin" to start calibration.', text_color='gold'), sg.Push()],
                 [sg.Push(), sg.Button('Begin'), sg.Push()],
                 [sg.Push(), sg.Text(key='-INTRO-'), sg.Push()],
                 [(sg.Text(key='-DIGIT_ONE-', text_color='white'),
                   sg.Text(key='-P1-', text_color='white'),
                   sg.Text(key='-P2-', text_color='white'),
                   sg.Text(key='-P3-', text_color='white'),
                   sg.Text(key='-DIGIT_TWO-', text_color='white'),
                   sg.Text(key='-P4-', text_color='white'),
                   sg.Text(key='-P5-', text_color='white'),
                   sg.Text(key='-P6-', text_color='white'),
                   sg.Text(key='-DIGIT_THREE-', text_color='white'))],
                ]
    # Window is created.
    window = sg.Window("Blink Calibrator", layout_one,
                       size=(250, 200), auto_size_text=True)

    # Main Loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Begin':
            # Begins the thread
            window.start_thread(lambda: countdown(window), ('-THREAD-', '-THREAD ENDED-'))
        # A series of if statements that update the corresponding
        # window to based on the event received from the main
        # thread.
        elif event[0] == '-THREAD-':
            if event[1] == '-THREE-':
                window['-DIGIT_ONE-'].update('3')
                window['-INTRO-'].update('Beginning in: ')
            elif event[1] == '-TWO-':
                window['-DIGIT_TWO-'].update('2')
            elif event[1] == '-ONE-':
                window['-DIGIT_THREE-'].update('1')
            elif event[1] == '-PERIOD1-':
                window['-P1-'].update('.')
            elif event[1] == '-PERIOD2-':
                window['-P2-'].update('.')
            elif event[1] == '-PERIOD3-':
                window['-P3-'].update('.')
            elif event[1] == '-PERIOD4-':
                window['-P4-'].update('.')
            elif event[1] == '-PERIOD5-':
                window['-P5-'].update('.')
            elif event[1] == '-PERIOD6-':
                window['-P6-'].update('.')
            elif event[1] == '-OPEN_WINDOW-':
                window.close()
                window_two()
                break

# Changes the color of a red dot to
# green every 5 seconds over 75 seconds.
def blink_dot(windows):
    for i in range(0, 15):
        windows.write_event_value(('-THREAD-', '-GREEN_DOT-'), i)
        sleep(0.5)
        if i == 14:
            windows.write_event_value(('-THREAD-', '-DOT_DONE-'), i)
        for c in range(0, 5):
            windows.write_event_value(('-THREAD-', '-RED_DOT-'), c)
            sleep(1)

# The second window for the GUI.
# The screen shows a red dot that changes to green.
# The user is asked to blink each time the color changes.
def window_two():
    layout_two =  [[sg.Push(background_color='white'), sg.Text('Focus on the red dot in front of you.\n'
                        'Blink once each time the color changes.', text_color='black',
                                   background_color='white'),
                sg.Push(background_color='white')],
               [sg.Text(background_color='white')],
               [sg.Text(background_color='white')],
               [sg.Push(background_color='white'), sg.Text('🔴', key='-DOT-', background_color='white')
                   , sg.Push(background_color='white')]
               ]
    new_window = sg.Window("Calibration", layout_two, size=(250, 150), background_color='white')

    # Begins the thread right away.
    new_window.start_thread(lambda: blink_dot(new_window), ('-THREAD-', '-THREAD ENDED-'))
    # Main Loop
    while True:
        event, values = new_window.read()

        if event == sg.WIN_CLOSED:
            break

        if event [0] == '-THREAD-':
            if event [1] == '-GREEN_DOT-':
                new_window['-DOT-'].update('🟢')
            elif event [1] == '-RED_DOT-':
                new_window['-DOT-'].update('🔴')
            elif event [1] == '-DOT_DONE-':
                new_window.close()
                window_three()
                break

# The third window for the GUI.
# It says: "Calibration Complete"!
def window_three():
    layout_three = [[sg.Text()], [sg.Text()], [sg.Text()],
              [sg.Text()],[sg.Text("Calibration Complete!")], [sg.Text()],
              [sg.Text()],[sg.Text()],[sg.Text()]
              ]
    newer_window = sg.Window("Calibration Complete", layout_three)

    while True:
        event, values = newer_window.read()

        if event == sg.WIN_CLOSED:
            break


if __name__ == '__main__':
    window_one()