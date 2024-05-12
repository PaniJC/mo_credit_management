from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from ..models import Customers, Loans
import json


def create_loan(request) -> JsonResponse:
    if request.method == 'POST':

        data = json.loads(request.body)

        # Get the external_id of the customer
        customer_external_id = data.get('customer_external_id')

        # Obtain the amount created for the loan and to validate that it is less than the authorized amount
        loan_amount = data.get('amount')

        try:
            # Search for the client by its external_id to obtain the score
            customer = get_object_or_404(Customers, external_id=customer_external_id)
            customer_score = customer.score

            # Load all loans associated with the customer
            loans = Loans.objects.filter(customer_id=customer.id)

            # Calculate if the customer has an available balance and if this is greater than or equal to the requested loan
            loans_outstanding_total =0.00
            for loan in loans:
                loans_outstanding_total += float(loan.outstanding)

            total_debt = float(loans_outstanding_total) +  float(loan_amount)
            available_amount = float(customer_score) - total_debt

            if available_amount >= 0.00 :

                # Create the loan with the data provided
                loan = Loans.objects.create(
                    external_id=data.get('external_id'),
                    customer_id=customer,
                    amount=data.get('amount'),
                    outstanding=data.get('amount'),
                    status=data.get('status')
                )

                return JsonResponse({'message': 'Loan created successfully.'}, status=201)
            
            else:
                return JsonResponse({'info': f'The client exceeds his debt capacity by $: {available_amount}.'}, status=200, safe=False)

        except Customers.DoesNotExist:
            return JsonResponse({'error': f'The client with external_id {customer_external_id} does not exist.'}, status=404)
        
        except IntegrityError as e:
            # Capturar el external_id que causa el error de integridad única
            external_id = data.get('external_id')
            error_message = f'The loan could not be created. The external_id "{external_id}" already exists.' 
            return JsonResponse({'error': error_message}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        # Handle the case where the request method is not POST.
        return JsonResponse({'error': 'Se espera una solicitud POST'}, status=405)
    
def get_loans_by_customer(request) -> JsonResponse:

    external_id = request.GET.get('customer_external_id')

    if external_id is not None:
        try:

            # Search the client by external_id
            id_customer = Customers.objects.get(external_id=external_id)

            # Get all loans associated with the client
            loans = Loans.objects.filter(customer_id=id_customer.id)
            
            # Prepare the data to be returned in the response
            loans_info = []
            for loan in loans:
                loan_info  = {
                    'external_id': loan.external_id,
                    'customer_external_id':id_customer.external_id,
                    'amount':loan.amount,
                    'outstanding':loan.outstanding,
                    'status':loan.status
                }

                loans_info.append(loan_info)

            if loans_info != []:
                return JsonResponse(loans_info, status=200, safe=False)
            else:
                return JsonResponse({'info': f'The customer with external_id {external_id} exists, but has no loans on file.'}, status=200, safe=False)

        except Customers.DoesNotExist as e:
            return JsonResponse({'error': f'The client with external_id {external_id} does not exist.'}, status=404)

        except Customers.UnboundLocalError as e:  
            return JsonResponse({'error': f'The client with external_id {external_id} does not exist.'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'The external_id parameter is required.'}, status=400)
