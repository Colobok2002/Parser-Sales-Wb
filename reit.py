from datetime import datetime
from toSite import addWbOtchetNew
from apscheduler.schedulers.blocking import BlockingScheduler


def run_script():
    print("[{}] Running reit.py...".format(datetime.now()))
    # addWbOtchet()
    addWbOtchetNew()
    print("[+] Finish")


if __name__ == "__main__":
    # date_range = ["2023-10-13", "2023-10-14", "2023-10-15", "2023-10-16"]
    # for date in date_range:
    #     addWbOtchet(date)
    scheduler = BlockingScheduler()
    scheduler.add_job(run_script, "cron",  minute=10)

    print("[+] run script")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
