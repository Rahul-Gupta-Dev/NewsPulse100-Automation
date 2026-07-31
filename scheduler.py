import schedule
import time
import subprocess


def job():
    subprocess.run(["python", "main.py"])


schedule.every().day.at("08:00").do(job)

print("Scheduler Started...")

while True:
    schedule.run_pending()
    time.sleep(30)