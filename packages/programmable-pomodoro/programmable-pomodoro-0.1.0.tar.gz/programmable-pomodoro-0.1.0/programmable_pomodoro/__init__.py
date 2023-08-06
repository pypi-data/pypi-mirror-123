__version__ = '0.1.0'

import asyncio
from datetime import datetime, timedelta
from aioconsole import ainput
from os import name, system
import colorama
import simpleaudio as sa
import importlib.resources
from . import audio

# Load the audio file
with importlib.resources.path(audio, "alarm.wav") as alarmPath:
    wave_obj = sa.WaveObject.from_wave_file(str(alarmPath))

# Provide cross platform coloring for Windows users.
colorama.init()

# Cross platform clear screen.
def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')

# To print timedeltas.
def formatTimeDelta(td: timedelta) -> str:
    seconds = td.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))

# Color and format the display for a task.
def formatWorkCompletion(task: str, current: timedelta, goal: timedelta) -> str:
    progress = f'{formatTimeDelta(current)}/{formatTimeDelta(goal)}'
    timesUp = current >= goal
    return f'{colorama.Fore.GREEN if timesUp else ""} {task} - {progress} {colorama.Fore.RESET}'

# A single work/break time interval.
class PomodoroTask:
    def __init__(self, task: str, workInterval: timedelta):
        self.finished = False
        self.task = task
        self.startTime = datetime.now()
        self.endTime = datetime.now()
        self.workInterval = workInterval
    def __repr__(self):
        return formatWorkCompletion(self.task, self.endTime - self.startTime, self.workInterval)

# Contains and manages PomodoroTask objects. Manages console output and user input.
class Pomodoro:
    # This flag is set True when user inputs 'q' so that the program can exit.
    finished = False
    # Initializes a Pomodoro object. Initially self.tasks is a single task.
    def __init__(self, 
            task: str, 
            workInterval: timedelta = timedelta(minutes=25), 
            breakInterval: timedelta = timedelta(minutes=5), 
            goal: timedelta = timedelta(hours=3)
        ):
        self.task = task
        self.workInterval = workInterval
        self.breakInterval = breakInterval
        self.goal = goal
        self.tasks = [PomodoroTask(task, workInterval)]
    # Displays the Pomodoro's state.
    def __repr__(self):
        workHistory = '\n'.join(str(task) for task in self.tasks)
        goalProgress = sum((task.endTime - task.startTime for task in self.tasks if task.task != 'break'), timedelta())
        goalProgressDisplay = formatWorkCompletion('Goal', goalProgress, self.goal)
        return f'{workHistory}\n\n{goalProgressDisplay}'
    # Listen for user input. enter to finish a task. q to quit.
    async def listen(self):
        while True:
            content = await ainput("")
            if content == '':
                if self.tasks[-1].task != 'break':
                    self.tasks.append(PomodoroTask('break', self.breakInterval))
                else:
                    self.tasks.append(PomodoroTask(self.task, self.workInterval))
            elif content == 'q':
                self.finished = True
                break
    # Polls the Pomodoro's state and displays it.
    async def display(self):
        clear()
        while True and not self.finished:
            task = self.tasks[-1]
            task.endTime = datetime.now()
            if not task.finished and task.endTime - task.startTime >= task.workInterval:
                wave_obj.play()
                task.finished = True
            print(self)
            await asyncio.sleep(1)
            clear()
    # Concurrently listen and display. Return user data when finished.
    async def work(self):
        await asyncio.gather(self.listen(), self.display())
        return [(task.task, task.startTime, task.endTime) for task in self.tasks]