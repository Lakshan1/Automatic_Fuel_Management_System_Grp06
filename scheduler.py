import schedule 
import requests

def task():
    print("working")
    requests.get("https://automatic-fuel-management-system.onrender.com/api/refreshQuota/")


schedule.every(5).minutes.do(task)

while True:
    schedule.run_pending()
