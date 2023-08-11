from datetime import datetime
from toSite import updatePrise
from apscheduler.schedulers.blocking import BlockingScheduler


def run_script():
    print("[{}] Running prise.py...".format(datetime.now()))
    updatePrise()
    print("[+] Finish")


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(run_script, "cron", hour=16, minute=00)

    print("[+] run script")

    try:
        run_script()
        # scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
