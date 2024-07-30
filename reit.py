from datetime import datetime, timedelta
from toSite import addWbOtchet, addWbOtchetNew
from apscheduler.schedulers.blocking import BlockingScheduler


def run_script():
    print("[{}] Running reit.py...".format(datetime.now()))
    addWbOtchetNew()
    print("[+] Finish")


def generate_date_range(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    date_range = []
    current_date = start
    while current_date <= end:
        date_range.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)

    return date_range


if __name__ == "__main__":

    date_range = generate_date_range("2024-04-01", "2024-05-13")
    print(date_range)
    for date in date_range:
        addWbOtchetNew(date)
    
    scheduler = BlockingScheduler()
    scheduler.add_job(run_script, "cron", hour=10, minute=0)

    print("[+] run script")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
