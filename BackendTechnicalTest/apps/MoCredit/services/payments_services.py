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
            customer = Customers.objects.get(external_id=customer_external_id)

            total_amount = data.get('total_amount')

            if customer.id is not None:

                    # Obtener todos los préstamos asociados al cliente
                    loans = Loans.objects.filter(customer_id=customer.id)

                    # Validamos si tiene algun prestamo activo
                    active_loans = False

                    for loan in loans:
                        if loan.status == 2:
                             active_loans = True
                             break
                    
                    
                    if active_loans == True:
                        # Como efectivamente tiene prestamos activos, pasamos a validar si el pago excede el monto de la deuda.
                        print('Como efectivamente tiene prestamos activos, pasamos a validar si el pago excede el monto de la deuda')
                        total_debt =0.00
                        for loan in loans:
                            total_debt += float(loan.outstanding)

                        balance = total_amount
                        if total_amount <= total_debt:
                            # Como efectivamente tiene prestamos activos, pasamos a validar si el pago excede el monto de la deuda.
                            print('Lo que va a pagar es menor o igual que la deuda total que tiene.')
                     
                            payment = Payments.objects.create(
                                external_id=data.get('external_id'),
                                customer_id=customer,  # Asignar el cliente encontrado como clave foránea
                                total_amount=data.get('total_amount'),
                                status=1
                            )
                            
                            payments_loan_detail = 0
                            for loan in loans:
                                if balance > loan.outstanding:
                                    payments_loan_detail = loan.outstanding
                                    loan.outstanding = 0.00
                                    loan.status = 4
                                    balance = float(balance) - float(loan.outstanding)
                                    payment.status = 1
                                    # Guardar los cambios en la base de datos
                                    loan.save()
                                    payment.save()

                                else:
                                    payments_loan_detail = balance
                                    loan.outstanding = float(loan.outstanding) - float(balance)
                                    loan.status = 2
                                    balance = 0
                                    payment.status = 1

                                    payment_loan_detail = PaymentsDetail.objects.create(
                                    amount=payments_loan_detail,
                                    loan_id=loan,
                                    payment_id=payment,  # Asignar el cliente encontrado como clave foránea
                                    )
                                    # Guardar los cambios en la base de datos
                                    loan.save()
                                    payment.save()
                                    break

                            return JsonResponse({'message': 'Pago almacenado exitosamente'}, status=200, safe=False)
                        
                        else:
                            # El pago debe ser rechazado porque es superior a la deuda.
                            print('El pago debe ser rechazado porque es superior a la deuda.')
                            payments_loan_detail = balance
                            loan.status = 2
                            # Guardar los cambios en la base de datos
                            loan.save()
                            return JsonResponse({'message': 'El pago debe ser rechazado porque es superior a la deuda.'}, status=200, safe=False)
                        
                    else:
                        return JsonResponse({'message': 'El pago es rechazado porque el cliente no tiene prestamos activos'}, status=400)
                    
            else:
                return JsonResponse({'error': 'El cliente no existe.'}, status=400)

    except Customers.DoesNotExist as e:
            return JsonResponse({'error': 'El cliente no existe'}, status=500)
        
    except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


    
def get_loans_by_customer(request):

    external_id = request.GET.get('customer_external_id')

    if external_id is not None:
        try:
            # Buscar el cliente por external_id
            id_customer = Customers.objects.get(external_id=external_id)
            print(f'El id a buscar --{id_customer.id}--{id_customer.external_id}')

            # Obtener todos los préstamos asociados al cliente
            loans = Loans.objects.filter(customer_id=id_customer.id)
            print(f'El Loans--{loans}')
            
            # Preparar los datos a devolver
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
                return JsonResponse({'info': f'El cliente con external_id {external_id} existe, pero no tiene préstamos registrados.'}, status=200, safe=False)

        except Customers.DoesNotExist as e:
            return JsonResponse({'error': f'El cliente con external_id {external_id} no existe.'}, status=404)

        except Customers.UnboundLocalError as e:  
            return JsonResponse({'error': f'El cliente con external_id {external_id} no existe.'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Se requiere el parámetro external_id.'}, status=400)
