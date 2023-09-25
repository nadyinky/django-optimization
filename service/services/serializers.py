from rest_framework import serializers
from services.models import Subscription, Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ('__all__')


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()  # If there are more serializers, 'annotate' is not very optimal
    client_name = serializers.CharField(source='client.company_name')
    email = serializers.CharField(source='client.user.email')
    price = serializers.SerializerMethodField()

    def get_price(self, instance):
        # Option without 'annotate' function in 'views':
        # return (instance.service.full_price -
        #         instance.service.full_price * (instance.plan.discount_percent / 100))
        # Instead of calculations here in Python, we can use 'annotate' in 'views'
        # and do it at the DB level
        return instance.price


    class Meta:
        model = Subscription
        fields = ('id', 'plan_id', 'client_name', 'email', 'plan', 'price')
