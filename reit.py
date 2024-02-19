from datetime import datetime
from toSite import addWbOtchet, addWbOtchetNew
from apscheduler.schedulers.blocking import BlockingScheduler


def run_script():
    print("[{}] Running reit.py...".format(datetime.now()))
    addWbOtchetNew()
    print("[+] Finish")


if __name__ == "__main__":

    # date_range = [
    #     "2024-02-13",
    #     "2024-02-14",
    #     "2024-02-15",
    #     "2024-02-16",
    #     "2024-02-17",
    #     "2024-02-18",
    # ]
    # for date in date_range:
    #     addWbOtchetNew(date)
    
    scheduler = BlockingScheduler()
    scheduler.add_job(run_script, "cron", minute=10)

    print("[+] run script")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
