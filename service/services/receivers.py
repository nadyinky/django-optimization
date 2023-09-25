# Django signals

from django.conf import settings
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_delete


@receiver(post_delete, sender=None)
def delete_cache_total_sum(*args, **kwargs):
    # cache invalidation
    cashe.delete(settings.PRICE_CACHE_NAME)