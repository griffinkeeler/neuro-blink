import FreeSimpleGUI as sg
from time import sleep


def countdown(window):
    """Background thread that outputs
      "3...2...1" one character at a time."""

    # Keys for each phase.
    phase_keys = {0: '-THREE-', 1: '-TWO-', 2: '-ONE-'}
    # Keys for each step.
    step_keys = {0: {0: '-PERIOD1-', 1: '-PERIOD2-', 2: '-PERIOD3-'},
                 1: {0: '-PERIOD4-', 1: '-PERIOD5-', 2: '-PERIOD6-'}}
    # Background thread.
    for phase in range(0, 3):
        key = phase_keys[phase]
        # write_event_value() is used to communicate between
        # background thread and main thread. It passes the
        # tuple as an event and 'phase' as the value.
        sleep(0.25)
        window.write_event_value(('-THREAD-', key), phase)
        if phase == 2:
            # Opens window two once thread is complete.
            sleep(0.25)
            window.write_event_value(('-THREAD-', '-OPEN_WINDOW_TWO-'), phase)
        if phase in step_keys:
            for step in range(0, 3):
                key = step_keys[phase][step]
                sleep(0.25)
                window.write_event_value(('-THREAD-', key), step)

# FIXME: MISSING THREAD QUEUE
def blink_dot(windows):
    """Background thread that changes the color of a red dot to
    green every 5 seconds over 75 seconds."""

    # Background thread.
    for i in range(0, 15):
        windows.write_event_value(('-THREAD-', '-GREEN_DOT-'), i)
        sleep(0.5)
        if i == 14:
            windows.write_event_value(('-THREAD-', '-DOT_DONE-'), i)
        for c in range(0, 5):
            windows.write_event_value(('-THREAD-', '-RED_DOT-'), c)
            sleep(1)

def window_one():
    """The first window for the GUI."""

    layout_one = [[sg.Push(),
                   sg.Text("Welcome!", text_color='white',
                           auto_size_text=True),
                   sg.Push()],
                  [sg.Push(),
                   sg.Text('Press "Begin" to start calibration.',
                           text_color='gold'),
                   sg.Push()],
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
                       size=(250, 200), auto_size_text=True, finalize=True)

    # Main Loop
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        if event == 'Begin':
            # Begins the thread
            window.start_thread(lambda: countdown(window),
                                ('-THREAD-', '-THREAD ENDED-'))
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
            elif event[1] == '-OPEN_WINDOW_TWO-':
                window.close()
                window_two()
                break

def window_two():
    """The second window for the GUI."""

    layout_two = [[sg.Push(background_color='white'),
                   sg.Text('Focus on the red dot in front of you.\n'
                            'Blink once each time the color changes.',
                             text_color='black',
                             background_color='white'),
                   sg.Push(background_color='white')],
                  [sg.Text(background_color='white')],
                  [sg.Text(background_color='white')],
                  [sg.Push(background_color='white'),
                   sg.Text('🔴', key='-DOT-', background_color='white')
                      , sg.Push(background_color='white')]
                  ]

    window = sg.Window("Calibration", layout_two,
                           size=(250, 150), background_color='white', finalize=True)

    # Begins the thread right away.
    window.start_thread(lambda: blink_dot(window),
                            ('-THREAD-', '-THREAD ENDED-'))
    # Main Loop
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event[0] == '-THREAD-':
            if event[1] == '-GREEN_DOT-':
                window['-DOT-'].update('🟢')
            elif event[1] == '-RED_DOT-':
                window['-DOT-'].update('🔴')
            elif event[1] == '-DOT_DONE-':
                window.close()
                window_three()
                break

def window_three():
    """The third window for the GUI."""

    layout_three = [[sg.Text()], [sg.Text()], [sg.Text()],
                    [sg.Text()],
                    [sg.Text("Calibration Complete!")],
                    [sg.Text()],
                    [sg.Text()], [sg.Text()], [sg.Text()]
                    ]
    window = sg.Window("Calibration Complete", layout_three, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break


if __name__ == '__main__':
    window_one()
