from rest_framework.routers import DefaultRouter
from apps.MoCredit.api.views import CustomerApiViewSet, LoansApiViewSet, PaymentsApiViewSet, PaymentsDetailApiViewSet

router_customer = DefaultRouter()

router_customer.register(prefix='customers', basename='customers', viewset=CustomerApiViewSet)
router_customer.register(prefix='create_customer', basename='customers/create_customer', viewset=CustomerApiViewSet)



router_customer.register(prefix='loans', basename='loans', viewset=LoansApiViewSet)
router_customer.register(prefix='payments', basename='payments', viewset=PaymentsApiViewSet)
router_customer.register(prefix='paymentsdetail', basename='paymentsdetail', viewset=PaymentsDetailApiViewSet)