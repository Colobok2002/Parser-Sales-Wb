from datetime import datetime
from toSite import updatePrise, updatePriseNabor
from apscheduler.schedulers.blocking import BlockingScheduler


def run_script():
    print("[{}] Running updatePrise...".format(datetime.now()))
    updatePrise()
    print("[+] Finish")
    print("[{}] Running updatePriseNabor...".format(datetime.now()))
    updatePriseNabor()
    print("[+] Finish")


if __name__ == "__main__":
    run_script()
    scheduler = BlockingScheduler()
    scheduler.add_job(run_script, "interval", hours=1)

    print("[+] run script")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
