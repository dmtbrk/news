import datetime as dt
import logging
import os
import time
from threading import Timer, Event


import django
from django.conf import settings

from news.settings import DATABASES, INSTALLED_APPS

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news.settings")
settings.configure(
    DEBUG=True, INSTALLED_APPS=INSTALLED_APPS, DATABASES=DATABASES
)
django.setup()

from feed.models import Post  # noqa E402

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)

HOUR = int(os.environ.get("RESET_HOUR", 0))
MINUTE = int(os.environ.get("RESET_MINUTE", 0))
SECOND = int(os.environ.get("RESET_SECOND", 0))


def reset_votes(event: Event):
    logging.info("resetting votes...")
    for post in Post.objects.all():
        post.votes = 0
        post.save()
    event.set()


def main():
    while True:
        now = dt.datetime.utcnow()
        target = now.replace(hour=HOUR, minute=MINUTE, second=SECOND)
        if target < now:
            target += dt.timedelta(days=1)
        delta = target - now  # timedelta to the next HOUR:MINUTE:SECOND
        print(delta.seconds, delta.microseconds)

        event = Event()
        Timer(delta.seconds, reset_votes, args=[event]).start()
        event.wait()

        time.sleep(1)  # delay preventing from firing the task multiple times


if __name__ == "__main__":
    main()
