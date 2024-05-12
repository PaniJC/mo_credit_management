from rest_framework.serializers import ModelSerializer
from apps.MoCredit.models import Customers, Loans, Payments, PaymentsDetail

# Convierte cualquier estructura a json
class CustomersSerializer(ModelSerializer):
    class Meta:
        model = Customers
        fields = '__all__'

class LoansSerializer(ModelSerializer):
    class Meta:
        model = Loans
        fields = '__all__'

class PaymentsSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'

class PaymentsDetailSerializer(ModelSerializer):
    class Meta:
        model = PaymentsDetail
        fields = '__all__'
        