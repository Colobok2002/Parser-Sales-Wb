from datetime import datetime
from toSite import addWbOtchet
from apscheduler.schedulers.blocking import BlockingScheduler


def run_script():
    print("[{}] Running reit.py...".format(datetime.now()))
    addWbOtchet()
    print("[+] Finish")


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(run_script, "cron", hour=15, minute=15)

    print("[+] run script")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
