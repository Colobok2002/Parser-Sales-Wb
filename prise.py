from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

from toGoogle import ParserManager


def run_script() -> None:
    """Запуск парсинка"""
    pm = ParserManager()
    print(f"[{datetime.now()}] Running updatePrise...")
    pm.updatePrise()
    print("[+] Finish")


if __name__ == "__main__":
    run_script()
    scheduler = BlockingScheduler()
    scheduler.add_job(run_script, "interval", hours=1)

    print("[+] Запустился планировшик")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
