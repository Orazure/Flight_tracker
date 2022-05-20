from celery import Celery
from celery.schedules import crontab
from loguru import logger
import redis
from flask_mail import Message
from apps.celery import celery
from apps import mail

# celery = Celery(__name__)
# celery.config_from_object("apps.configuration.celery")

REDIS_CLIENT = redis.Redis(host="redis", port=6379, db=0)


def single_operation(function=None, key="", timeout=None):
    """Ensure only one celery task gets invoked at a time."""

    def _dec(run_func):
        def _caller(*args, **kwargs):

            func_result = None
            have_lock = False
            lock = REDIS_CLIENT.lock(key, timeout=timeout)
            try:
                have_lock = lock.acquire(blocking=False)
                if have_lock:
                    func_result = run_func(*args, **kwargs)
            finally:
                if have_lock:
                    lock.release()
            if func_result:
                return func_result

        return _caller

    return _dec(function) if function is not None else _dec


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Set up task for a periodic execution."""
    # Update data of flights every 15 minutes
    sender.add_periodic_task(
        crontab(minute="*/15"),
        task_update_flights_information.s(),
    )
    # Update data of live flights every 5 minutes
    sender.add_periodic_task(
        crontab(minute="*/5"),
        task_update_live_flights.s(),
    )
    # Update airports every month
    sender.add_periodic_task(
        crontab(0, 0, day_of_month="1"),
        task_update_airports.s(),
    )
    # Update airlines every month
    sender.add_periodic_task(
        crontab(0, 0, day_of_month="1"),
        task_update_airlines.s(),
    )


@celery.task(name="data_importer.update_flights_information")
@single_operation(key="update_flights_information", timeout=60)
def task_update_flights_information():
    logger.info("Update flights information")
    from apps.airlabs.flights_importer import update_flights_information

    update_flights_information()
    return True


@celery.task(name="data_importer.update_live_flights")
@single_operation(key="update_live_flights", timeout=60)
def task_update_live_flights():
    logger.info("Update live flights")
    from apps.airlabs.live_flights_importer import update_live_flights

    update_live_flights()
    return True


@celery.task(name="data_importer.update_airports")
@single_operation(key="airports", timeout=60)
def task_update_airports():
    logger.info("Update airports")
    from apps.airlabs.airports_importer import update_airports_info

    update_airports_info()
    return True


@celery.task(name="data_importer.update_airlines")
@single_operation(key="airlines", timeout=60)
def task_update_airlines():
    logger.info("Update airlines")
    from apps.airlabs.airlines_importer import add_airline_information

    add_airline_information()
    return True


@celery.task(name="email.sendmail")
def send_email(to_email: str, message: str, subject: str):
    """Send email."""
    logger.info(f"Sending an email to {to_email}")
    msg = Message(
        html=message,
        recipients=[to_email],
        subject=subject,
        extra_headers={"Content-Type": "text/html"},
    )
    mail.send(msg)
