from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models import Prefetch, F, Sum
from django.core.cache import cache

from clients.models import Client
from services.models import Subscription
from services.serializers import SubscriptionSerializer
from django.conf import settings


class SubscriptionView(ReadOnlyModelViewSet):
    # ORM-query optimization: prefetch_related, Prefetch, annotate
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        # 'service',  # as one option how to optimize this query
        Prefetch('client', queryset=Client.objects.all()
                                                  .select_related('user')
                                                  .only('company_name',
                                                        'user__email'))
        )#.annotate(price=F('service__full_price') -
         #                F('service__full_price') * F('plan__discount_percent') / 100.00)
    serializer_class = SubscriptionSerializer

    # Aggregate function
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())  # 'queryset' from SubscriptionView+filter
        response = super().list(request, *args, **kwargs)

        price_cache = cache.get(settings.PRICE_CACHE_NAME)
        if price_cache:
            total_price = price_cache
        else:
            total_price = queryset.aggregate(total=Sum('price')).get('total')
            cache.set(settings.PRICE_CACHE_NAME, total_price, 60 * 60)

        response_data = {'result': response.data}
        # Since we use 'annotate' at the DB level, it's good to use 'aggregate' at the DB level
        # for aggregating these annotated data
        response_data['total_amount'] = total_price

        response.data = response_data

        return response

