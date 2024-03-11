from datetime import datetime
from toSite import addWbOtchet, addWbOtchetNew
from apscheduler.schedulers.blocking import BlockingScheduler


def run_script():
    print("[{}] Running reit.py...".format(datetime.now()))
    addWbOtchetNew()
    print("[+] Finish")


if __name__ == "__main__":

    # date_range = [
    #     "2024-03-10",
    #     # "2024-02-23",
    #     # "2024-02-24",
    #     # "2024-02-25",
    #     # "2024-02-26",
    #     # "2024-02-27",
    #     # "2024-02-28",
    #     # "2024-03-01",
    #     # "2024-03-02",
    #     # "2024-03-03",
    #     # "2024-03-04",
    #     # "2024-03-05",
    #     # "2024-03-06",
    #     # "2024-03-07",
    #     # "2024-03-08",
    #     # "2024-03-09",
    # ]
    # for date in date_range:
    #     addWbOtchetNew(date)

    scheduler = BlockingScheduler()
    scheduler.add_job(run_script, "cron", hour=10, minute=0)

    print("[+] run script")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
