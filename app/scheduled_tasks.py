from datetime import datetime, timedelta
from celery import Celery
import subprocess
from config import config
from app.logger import log

CFG = config()


celery = Celery(__name__)
celery.conf.broker_url = CFG.REDIS_URL
celery.conf.result_backend = CFG.REDIS_URL
celery.conf.broker_connection_retry_on_startup = True


@celery.task
def delete_tickets_from_cart():
    log(log.INFO, "Periodic task delete_tickets_from_cart started at [%s]", datetime.now())
    process = subprocess.Popen(["poetry", "run", "flask", "unreserve"])
    process.communicate()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        timedelta(minutes=CFG.TICKETS_IN_CART_CLEAN_IN),
        delete_tickets_from_cart.s(),
        name="delete tickets from cart",
    )
