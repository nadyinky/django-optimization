import time
from datetime import datetime

from celery import shared_task
from celery_singleton import Singleton
from django.db.models import F
from django.db import transaction
from django.conf import settings
from django.core.cache import cache


@shared_task(base=Singleton)
def set_price(subscription_id):
    from services.models import Subscription

    with transaction.atomic():
        # time.sleep(5)
        # We use 'annotate' here, at the DB level
        subscription = Subscription.objects.select_for_update().filter(id=subscription_id).annotate(
            anotated_price=F('service__full_price') -
                           F('service__full_price') * F('plan__discount_percent') / 100.00).first()

        # time.sleep(20)
        subscription.price = subscription.anotated_price
        subscription.save()
    # print('here program do something else')

    # Cache invalidation
    cache.delete(settings.PRICE_CACHE_NAME)


@shared_task(base=Singleton)
def set_comment(subscription_id):
    from services.models import Subscription

    # print('here program do something else')
    with transaction.atomic():
        subscription = Subscription.objects.select_for_update().get(id=subscription_id)
        # time.sleep(27)
        subscription.comment = str(datetime.now())
        subscription.save()
    # print('here program do something else')

    # Cache invalidation
    cache.delete(settings.PRICE_CACHE_NAME)