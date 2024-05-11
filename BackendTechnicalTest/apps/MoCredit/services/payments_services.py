from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from ..models import Customers, Loans, Payments, PaymentsDetail
from ..services import customers_services as cs
import json


@csrf_exempt
def create_payment(request):
    try:
        if request.method == 'POST':
            # Obtener los datos del cuerpo de la solicitud POST
            data = json.loads(request.body)

            # Obtener el external_id de la solicitud GET
            customer_external_id = data.get('customer_external_id')
            total_amount = data.get('total_amount')
            external_id = data.get('external_id')
            total_debt =0

            customer = Customers.objects.get(external_id=customer_external_id)
            if customer.id is not None:

                customer_id = customer.id

                loans = Loans.objects.filter(customer_id=customer_id)

                for loan in loans:
                    total_debt += float(loan.outstanding)
                print(f'El total adeudado por el cliente es {total_debt}')

                for loan in loans:
                    print(loan.status)

                if total_amount > total_debt:
                    return JsonResponse({'error': 'El monto a pagar es mayor que la deuda. Pago rechazado.'}, status=200)
                else:
                    payment = Payments.objects.create(
                        external_id=data.get('external_id'),
                        customer_id=customer,  
                        total_amount=total_amount,
                        status=1
                    )

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

                            payment_loan_detail = PaymentsDetail.objects.create(
                                    amount=payment_detail,
                                    loan_id=loan,
                                    payment_id=payment,  # Asignar el cliente encontrado como clave foránea
                                    )


                        else:
                            print('El credito ya esta cerrado.')

                        if total_amount <= 0:
                            print('Ya no hay dinero para seguir abonando.')
                            break

                return JsonResponse({'message': 'Pago almacenado exitosamente'}, status=200, safe=False)                


 
    except Customers.DoesNotExist as e:
            return JsonResponse({'error': 'El cliente no existe'}, status=500)
        
    except Exception as e:
            return JsonResponse({'error':{e}}, status=500)
    
def get_payments_by_customer(request):

    customer_external_id = request.GET.get('customer_external_id')

    if customer_external_id is not None:
        try:
            # Buscar el cliente por external_id
            id_customer = Customers.objects.get(external_id=customer_external_id)

            # Obtener todos los préstamos asociados al cliente
            loans = Loans.objects.filter(customer_id=id_customer.id)

            payments_info = []
            payments_customer =[]
            for loan in loans:
                id_loan = loan.id
                external_id_loan = loan.external_id
                loan_amount = loan.amount

                # Obtener todos los préstamos asociados al cliente
                payments_info = PaymentsDetail.objects.filter(loan_id=id_loan)
                print(payments_info)


                
                for payment_info in payments_info:
                    # Obtener todos los préstamos asociados al cliente
                    payments_id = Payments.objects.filter(id=payment_info.payment_id.id)


                    for payment_id in payments_id:
                        payments_detail = []
                        actual_payment_id = payment_id.external_id
                        actual_payment_status = payment_id.status
                        actual_payment_amount = payment_id.total_amount
                        
                        print('El grande',actual_payment_id)
                        print('El micro',payment_info.payment_id.external_id)

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
                return JsonResponse({'info': f'El cliente con external_id existe, pero no tiene préstamos registrados.'}, status=200, safe=False)

        except Customers.DoesNotExist as e:
            return JsonResponse({'error': f'El cliente con external_id no existe.'}, status=404)

        except Customers.UnboundLocalError as e:  
            return JsonResponse({'error': f'El cliente con external_id no existe.'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Se requiere el parámetro external_id.'}, status=400)
