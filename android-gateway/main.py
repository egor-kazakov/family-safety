import time
import yaml
import subprocess
from prometheus_client import start_http_server, Counter

# Загрузка конфигурации из settings.yml
with open("settings.yml", "r") as file:
    config = yaml.safe_load(file)

PORT = config.get("PORT", 8000)
TIME = config.get("TIME", 10)

IGNORE_APPS = config.get("IGNORE_APPS", [])

# Глобалыне переменные (счетчик активного окна)
active_window_time_counter = Counter('runtime_active_window', 'Time active windows are running', ['app'])

def get_active_window():
    try:
        result = subprocess.check_output(['adb', 'shell', 'dumpsys', 'window', 'windows'])
        for line in result.splitlines():
            line = line.decode('utf-8')
            if 'mCurrentFocus' in line:
                return line.split()[-1].split('/')[0]
    except subprocess.CalledProcessError as e:
        print(f"Error getting active window: {e}")
    return None

def count_active_window():
    active_window = "" #gw.getActiveWindow()

    if active_window is not None:
        process_name = "" #get_process_name_from_pid(pid)

        if process_name in IGNORE_APPS:
            return

        active_window_time_counter.labels(app=process_name).inc(TIME)

if __name__ == '__main__':
    # Запуск HTTP-сервера для Prometheus
    start_http_server(PORT)

    try:
        while True:
            time.sleep(TIME)
            count_active_window()
    except KeyboardInterrupt:
        pass
