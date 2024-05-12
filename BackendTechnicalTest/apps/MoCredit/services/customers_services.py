from django.http import JsonResponse
from django.db.utils import IntegrityError
from ..models import Customers, Loans
import json


def create_customer(request) -> JsonResponse:
    
    if request.method == 'POST':

        # Get the data from the body of the POST request
        data = json.loads(request.body)

        try:
            # Validate that the input variable they are providing indicates that the user's state will be active
            if data.get('status') != 1:
                return JsonResponse({'error': 'The user must be created with Active status (1).'}, status=400)
            
            # Verify that the Score is numerical and greater than zero. TODO, a minimum limit can be set for the Score.
            if not isinstance(data.get('score'), (int, float)) or data.get('score') <= 0:
                return JsonResponse({'error': 'The score must be numerical and greater than zero.'}, status=400)
            
            score = data.get('score')
            score = '{:.2f}'.format(score)

            # Create the JSON object with the data related to the appropriate fields
            customers = Customers(
                external_id=data.get('external_id'),
                status=data.get('status'),
                score=score
            )

            # Save the new customer in the database
            customers.save()

            # Return status 201 indicating the success of the transaction in the DB
            return JsonResponse({'message': 'Customer created successfully'}, status=201)
        
        except IntegrityError as e:
            external_id = data.get('external_id')
            error_message = f'The client could not be created. The external_id "{external_id}" already exists.'   
            
        return JsonResponse({'error': error_message}, status=400)
        
    else:
        return JsonResponse({'error': 'A POST request is expected to create a customer(s)'}, status=400)

def get_customer_by_external_id(request) -> JsonResponse:

    # Obtain the value of the parameter that tells us which customer should be consulted.
    external_id = request.GET.get('external_id')

    # Validate that it actually exists before proceeding
    if external_id is not None:
        try:

            customer = Customers.objects.get(external_id=external_id)
            
            # Create the JSON to deliver in the response.
            data = {
                'external_id': customer.external_id,
                'score': customer.score,
                'status': customer.status,
                'preapproved_at': customer.preapproved_at.strftime('%Y-%m-%d %H:%M:%S') if customer.preapproved_at else None
            }

            return JsonResponse(data, status=200)

        except Customers.DoesNotExist:
            return JsonResponse({'error': f'The client with external_id {external_id} does not exist.'}, status=404)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=404)
    else:
        return JsonResponse({'error': 'External_id parameter required.'}, status=400)

def get_customer_balance(request) -> JsonResponse:
    try:

        # We start from the external_id of the customer, to generate and present its balance.
        external_id = request.GET.get('customer_external_id')
        customer = Customers.objects.get(external_id=external_id)
        customer_score = customer.score

        # Validate that it actually exists before proceeding
        if customer.id is not None:

                # Obtain all loans associated with the customer.
                loans = Loans.objects.filter(customer_id=customer.id)

                # Initialize the variable that will store the total owed by the customer.
                total_debt = 0.00

                # We charge the balance corresponding to the debt of the outstanding amount of the loans you have.
                for loan in loans:
                    total_debt += float(loan.outstanding)

                # Aassign to this variable the difference between what you were initially approved to lend vs what you owe..
                available_amount = float(customer_score) - total_debt

                
                customer_balance = {
                        'external_id': customer.external_id,
                        'score': float(customer_score),
                        'available_amount':available_amount,
                        'total_debt':total_debt
                    }
                
                return JsonResponse(customer_balance, status=200, safe=False)
                
        else:
            return JsonResponse({'error': 'El cliente no existe.'}, status=400)

    except Customers.DoesNotExist as e:
        return JsonResponse({'error': 'El cliente no existe'}, status=500)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

