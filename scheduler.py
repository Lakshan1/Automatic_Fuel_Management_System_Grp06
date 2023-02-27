import schedule 
import requests

def task():
    print("working")
    requests.get("https://auto-fuel-management-system.herokuapp.com/api/refreshQuota/")


# schedule.every(60).minutes.do(task)
schedule.every().sunday.at("12:00").do(task)

while True:
    schedule.run_pending()
