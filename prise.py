from datetime import datetime
from toSite import updatePrise
from apscheduler.schedulers.blocking import BlockingScheduler


def run_script():
    print("[{}] Running prise.py...".format(datetime.now()))
    updatePrise()
    print("[+] Finish")


if __name__ == "__main__":
    updatePrise()
    scheduler = BlockingScheduler()
    scheduler.add_job(run_script, "interval", hours=1)

    print("[+] run script")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
