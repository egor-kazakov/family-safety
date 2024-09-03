import time
import ctypes
import psutil
import yaml
import pyautogui
import pygetwindow as gw
from prometheus_client import start_http_server, Counter

# Загрузка конфигурации из settings.yml
with open("settings.yml", "r") as file:
    config = yaml.safe_load(file)

PORT = config.get("PORT", 8000)
TIME = config.get("TIME", 10)
DEVICE = config.get("TIME", "PC")

IGNORE_APPS = config.get("IGNORE_APPS", [])
CURSOR_APPS = config.get("CURSOR_APPS", [])

# Глобалыне переменные (счетчик активного окна, положение курсора)
active_window_time_counter = Counter('runtime_active_window', 'Time active windows are running', ['device', 'app'])
last_cursor_position = pyautogui.position()

def get_pid_from_hwnd(hwnd):
    pid = ctypes.c_ulong()
    ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return pid.value

def get_process_name_from_pid(pid):
    try:
        process = psutil.Process(pid)
        return process.name()
    except psutil.NoSuchProcess:
        return None

def count_active_window():
    active_window = gw.getActiveWindow()

    if active_window is not None:
        # Получаем hWnd активного окна
        hwnd = active_window._hWnd

        # Получаем PID по hWnd
        pid = get_pid_from_hwnd(hwnd)

        # Получаем имя процесса по PID
        process_name = get_process_name_from_pid(pid)

        if process_name in IGNORE_APPS:
            return

        if process_name in CURSOR_APPS:
            if pyautogui.position() != last_cursor_position:
                active_window_time_counter.labels(device=DEVICE, app=process_name).inc(TIME)
            return

        active_window_time_counter.labels(device=DEVICE, app=process_name).inc(TIME)

if __name__ == '__main__':
    # Запуск HTTP-сервера для Prometheus
    start_http_server(8000)

    try:
        while True:
            time.sleep(TIME)
            count_active_window()
            last_cursor_position = pyautogui.position()
    except KeyboardInterrupt:
        pass
