from django.http import JsonResponse
from ..models import Customers, Loans, Payments, PaymentsDetail
import json


def create_payment(request) -> JsonResponse:
    
    try:

        if request.method == 'POST':

            data = json.loads(request.body)

            # Set the variables with which we will carry out the calculations later
            customer_external_id = data.get('customer_external_id')
            total_amount = data.get('total_amount')
            external_id = data.get('external_id')
            total_debt =0

            customer = Customers.objects.get(external_id=customer_external_id)

            # Validate that the customer does exist
            if customer.id is not None:

                customer_id = customer.id

                # Get all the customer loans
                loans = Loans.objects.filter(customer_id=customer_id)

                # Calculate the current total debt that the customer has
                for loan in loans:
                    total_debt += float(loan.outstanding)

                # Validate that the amount to be paid is not greater than the amount owed
                if total_amount > total_debt:
                    return JsonResponse({'error': 'El monto a pagar es mayor que la deuda. Pago rechazado.'}, status=200)
                
                else:

                    # Record the corresponding payment in the table
                    payment = Payments.objects.create(
                        external_id=data.get('external_id'),
                        customer_id=customer,  
                        total_amount=total_amount,
                        status=1
                    )

                    # Validate each customer loan to define wich of it must be paid and how many can be
                    for loan in loans:
                        if loan.status == 2:
                            outsanding_mount = loan.outstanding
                            if total_amount >= outsanding_mount:

                                total_amount -= outsanding_mount
                                payment_detail = outsanding_mount
                                outsanding_mount = 0
                                loan.outstanding = outsanding_mount
                                loan.status = 4
                                loan.save()

                            else:

                                outsanding_mount -= total_amount
                                payment_detail = total_amount
                                loan.outstanding = outsanding_mount
                                total_amount = 0
                                loan.status = 2
                                loan.save()

                            # Create the record in the PaymentsDetail table (model) for each loan evaluated
                            payment_loan_detail = PaymentsDetail.objects.create(
                                    amount=payment_detail,
                                    loan_id=loan,
                                    payment_id=payment, 
                                    )


                        else:
                            return JsonResponse({'message': 'The credit is already closed.'}, status=400, safe=False)

                        if total_amount <= 0:
                            return JsonResponse({'message': 'Credits are paid up to the amount paid by the customer.'}, status=200, safe=False)


                return JsonResponse({'message': 'Credits are paid up to the amount paid by the customer.'}, status=200, safe=False)                

 
    except Customers.DoesNotExist as e:
            return JsonResponse({'error': 'Customer does not exist.'}, status=400)
        
    except Exception as e:
            return JsonResponse({'error':{e}}, status=500)
    
def get_payments_by_customer(request) -> JsonResponse:

    customer_external_id = request.GET.get('customer_external_id')

    if customer_external_id is not None:
        try:

            id_customer = Customers.objects.get(external_id=customer_external_id)

            # Get all loans associated with the client
            loans = Loans.objects.filter(customer_id=id_customer.id)

            # Initialize the arrays to append the payment information
            payments_info = []
            payments_customer =[]

            for loan in loans:
                id_loan = loan.id
                external_id_loan = loan.external_id

                # Get all the payments info associated with the customer
                payments_info = PaymentsDetail.objects.filter(loan_id=id_loan)

                for payment_info in payments_info:
                    
                    # Get all loans associated with the client
                    payments_id = Payments.objects.filter(id=payment_info.payment_id.id)

                    # Get all data of every payment with his detail, grouping in an array into the json object
                    for payment_id in payments_id:
                        payments_detail = []
                        actual_payment_id = payment_id.external_id
                        actual_payment_status = payment_id.status
                        actual_payment_amount = payment_id.total_amount

                        if actual_payment_id == payment_info.payment_id.external_id:
                            payment_detail  = {
                                'payment_detail_id': payment_info.payment_id.external_id,
                                'amount':float(payment_info.amount),
                                'payment_date':payment_info.created_at,
                            }
                            payments_detail.append(payment_detail)
                                        
                        payment_customer  = {
                                'customer_id': id_customer.external_id,
                                'loan_id': external_id_loan,
                                'payment_id': actual_payment_id,
                                'total_amount':float(actual_payment_amount),
                                'status': actual_payment_status,
                                'payment_detail': payments_detail,
                            }

                        payments_customer.append(payment_customer)


            if payments_customer != []:
                return JsonResponse(payments_customer, status=200, safe=False)
            else:
                return JsonResponse({'info': f'The customer with external_id exists, but has no loans registered.'}, status=200, safe=False)

        except Customers.DoesNotExist as e:
            return JsonResponse({'error': f'The client with external_id does not exist.'}, status=404)

        except Customers.UnboundLocalError as e:  
            return JsonResponse({'error': f'The client with external_id does not exist.'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'The external_id parameter is required.'}, status=400)
