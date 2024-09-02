import time
import ctypes
import psutil
import pygetwindow as gw
from prometheus_client import start_http_server, Counter

TIME = 15 # секунд
PORT = 8000
DEVICE = 'PC'

# Создаем счетчик для времени активного окна
active_window_time_counter = Counter('runtime_active_window', 'Time active windows are running', ['device', 'app'])

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

if __name__ == '__main__':
    # Запуск HTTP-сервера для Prometheus
    start_http_server(8000)

    try:
        while True:
            time.sleep(TIME)

            active_window = gw.getActiveWindow()

            if active_window is not None:
                # Получаем hWnd активного окна
                hwnd = active_window._hWnd
                
                # Получаем PID по hWnd
                pid = get_pid_from_hwnd(hwnd)
                
                # Получаем имя процесса по PID
                process_name = get_process_name_from_pid(pid)

                active_window_time_counter.labels(device=DEVICE, app=process_name).inc(TIME)
    except KeyboardInterrupt:
        pass
