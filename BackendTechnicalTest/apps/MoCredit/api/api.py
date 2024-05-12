from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import api_view
from apps.MoCredit.models import Customers, Loans
from apps.MoCredit.api.serializers import CustomersSerializer, LoansSerializer


### Customers api views 

@swagger_auto_schema(
    method='post', 
    request_body=CustomersSerializer,
    responses={200: CustomersSerializer(many=True)}
)
@api_view(['GET','POST'])
def customer_api_view(request):

    if request.method == 'GET':
        customers = Customers.objects.all()
        customers_serializer = CustomersSerializer(customers, many = True)
        
        return Response(customers_serializer.data)  
    
    elif request.method == 'POST':
        customers_serializer = CustomersSerializer(data=request.data)
        if customers_serializer.is_valid():
            customers_serializer.save()
            return Response(customers_serializer.data)
        return Response(customers_serializer.errors)


@swagger_auto_schema(
    method='post', 
    request_body=CustomersSerializer,
    responses={200: CustomersSerializer(many=True)}
)
@api_view(['POST'])
def create_customer(request):
    if request.method == 'POST':
        customers_serializer = CustomersSerializer(data=request.data)
        if customers_serializer.is_valid():
            customers_serializer.save()
            return Response(customers_serializer.data)
        return Response(customers_serializer.errors)        


@api_view(['GET'])
def by_external_id(request, external_id):
      if request.method == 'GET':
          external_id = Customers.objects.filter(external_id=external_id).first()
          customer_serializer = CustomersSerializer(external_id)
          return Response(customer_serializer.data)



@api_view(['GET'])
def balance(request, external_id):
      if request.method == 'GET':
          external_id = Customers.objects.filter(external_id=external_id).first()

          if external_id:
            customer_serializer = CustomersSerializer(external_id)
            customer_score = customer_serializer["score"].value
            customer_id = customer_serializer["id"].value
            customer_external_id = customer_serializer["external_id"].value
            # Obtain all loans associated with the customer.

            loans = Loans.objects.filter(id=customer_id)

            total_debt = 0.00

            for loan in loans:
                total_debt += float(loan.outstanding)
                
            print(total_debt)

            # Aassign to this variable the difference between what you were initially approved to lend vs what you owe..
            available_amount = float(customer_score) - total_debt

            customer_balance = {
                    'external_id': customer_external_id,
                    'score': float(customer_score),
                    'available_amount':available_amount,
                    'total_debt':total_debt
                }
            return Response(customer_balance)
          else:
            return Response('No data to the customer sugested! The customer does not exist.')


### Loans api views 
@swagger_auto_schema(
    method='post', 
    request_body=LoansSerializer,
    responses={200: LoansSerializer(many=True)}
)
@api_view(['GET','POST'])
def loans_api_view(request):

    if request.method == 'GET':
        loans = Loans.objects.all()
        loans_serializer = LoansSerializer(loans, many = True)
        
        return Response(loans_serializer.data)  
    
    elif request.method == 'POST':
        loans_serializer = LoansSerializer(data=request.data)
        if loans_serializer.is_valid():
            loans_serializer.save()
            return Response(loans_serializer.data)
        return Response(loans_serializer.errors)



@swagger_auto_schema(
    method='post', 
    request_body=LoansSerializer,
    responses={200: LoansSerializer(many=True)}
)
@api_view(['POST'])
def create_loan(request):
    if request.method == 'POST':
        loans_serializer = LoansSerializer(data=request.data)
        if loans_serializer.is_valid():
            customer_external_id = loans_serializer['customer_id'].value
            #loans_serializer.save()
            return Response(customer_external_id)
        return Response(loans_serializer.errors)        

@api_view(['GET'])
def loans_by_customer(request, customer_external_id):
      if request.method == 'GET':
          external_id = Customers.objects.filter(external_id=customer_external_id).first()

          if external_id:
            customer_serializer = CustomersSerializer(external_id)
            customer_id = customer_serializer["id"].value
            customer_external_id = customer_serializer["external_id"].value
            # Obtain all loans associated with the customer.

            loans = Loans.objects.filter(id=customer_id)

            # Aassign to this variable the difference between what you were initially approved to lend vs what you owe..
            loans_info = []
            for loan in loans:
                loan_info  = {
                    'external_id': loan.external_id,
                    'customer_external_id':customer_external_id,
                    'amount':loan.amount,
                    'outstanding':loan.outstanding,
                    'status':loan.status
                }

                loans_info.append(loan_info)

            return Response(loans_info)
          else:
            return Response('No data to the customer sugested! The customer does not exist.')

