from rest_framework.viewsets import ModelViewSet
from apps.MoCredit.models import Customers, Loans, Payments, PaymentsDetail
from apps.MoCredit.api.serializers import CustomersSerializer, LoansSerializer, PaymentsSerializer, PaymentsDetailSerializer
from ..models import Customers, Loans

class CustomerApiViewSet(ModelViewSet):
    serializer_class = CustomersSerializer
    queryset = Customers.objects.all()

class LoansApiViewSet(ModelViewSet):
    serializer_class = LoansSerializer
    queryset = Loans.objects.all()

class PaymentsApiViewSet(ModelViewSet):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

class PaymentsDetailApiViewSet(ModelViewSet):
    serializer_class = PaymentsDetailSerializer
    queryset = PaymentsDetail.objects.all()




   