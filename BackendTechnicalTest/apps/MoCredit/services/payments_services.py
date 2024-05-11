from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from ..models import Customers, Loans, Payments
import json


@csrf_exempt
def create_payment(request):
    if request.method == 'POST':
        # Obtener los datos del cuerpo de la solicitud POST
        data = json.loads(request.body)

        # Obtener el external_id del cliente del JSON
        customer_external_id = data.get('customer_external_id')
        loan_external_id = data.get('loan_external_id')
        total_payment = data.get('total_amount')


        try:
            # Buscar al cliente por su external_id
            customer = get_object_or_404(Customers, external_id=customer_external_id)
            customer_id = customer.id
            customer_score = customer.score

            loan = get_object_or_404(Loans, external_id=loan_external_id)

            print(f'''EL valor a pagar: {loan.amount}''')

            if total_payment > customer_score:
                print(f'''El valor a pagar es mayor al que se adeuda:
                      Valor adeudado: {customer_score} 
                      Valor a pagar: {total_payment}''')

            print(f'El id del cliente {customer_id}')
            print(f'El score del cliente {customer_score}')


            # Crear el pago con los datos proporcionados
            payment = Payments.objects.create(
                external_id=data.get('external_id'),
                total_amount=data.get('amount'),
                status=data.get('status')
            )

            return JsonResponse({'message': 'Pago creado correctamente'}, status=201)

        except Customers.DoesNotExist:
            return JsonResponse({'error': f'El cliente con external_id {customer_external_id} no existe'}, status=404)
        
        except IntegrityError as e:
            # Capturar el external_id que causa el error de integridad única
            external_id = data.get('external_id')
            error_message = f'No se pudo crear el pago. El external_id "{external_id}" ya existe.' 
            return JsonResponse({'error': error_message}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        # Manejar el caso en que el método de solicitud no sea POST
        return JsonResponse({'error': 'Se espera una solicitud POST'}, status=405)
    
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
