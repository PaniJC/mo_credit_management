from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
from ..models import Customers, Loans
import json

@csrf_exempt
def create_customer(request):
    if request.method == 'POST':
        # Obtener los datos del cuerpo de la solicitud POST
        data = json.loads(request.body)

        try:

            # Verificar si el status es igual a 1
            if data.get('status') != 1:
                return JsonResponse({'error': 'El usuario debe ser creado con status Activo (1).'}, status=400)
            
            # Verificar si el score es numérico y mayor a cero.
            if not isinstance(data.get('score'), (int, float)) or data.get('score') <= 0:
                return JsonResponse({'error': 'El score debe ser numérico y mayor a cero.'}, status=400)
            
            score = data.get('score')
            score = '{:.2f}'.format(score)
            # Crear un nuevo objeto Customer con los datos recibidos
            customers = Customers(
                external_id=data.get('external_id'),
                status=data.get('status'),
                score=score
            )

            # Guardar el nuevo cliente en la base de datos
            customers.save()

            # Devolver una respuesta exitosa
            return JsonResponse({'message': 'Cliente creado exitosamente'}, status=201)
        
        except IntegrityError as e:
            # Capturar el external_id que causa el error de integridad única
            external_id = data.get('external_id')
            error_message = f'No se pudo crear el cliente. El external_id "{external_id}" ya existe.'   
            
        return JsonResponse({'error': error_message}, status=400)
        
    else:
        # Si no es una solicitud POST, devolver un error
        return JsonResponse({'error': 'Se espera una solicitud POST para crear un(os) cliente(s)'}, status=400)
    
def get_customer_by_external_id(request):
    # Obtener el external_id de la solicitud GET
    external_id = request.GET.get('external_id')

    if external_id is not None:
        try:
            # Buscar el cliente por external_id
            customer = Customers.objects.get(external_id=external_id)
            
            # Preparar los datos a devolver
            data = {
                'external_id': customer.external_id,
                'score': customer.score,
                'status': customer.status,
                'preapproved_at': customer.preapproved_at.strftime('%Y-%m-%d %H:%M:%S') if customer.preapproved_at else None
            }

            return JsonResponse(data, status=200)

        except Customers.DoesNotExist:
            return JsonResponse({'error': f'El cliente con external_id {external_id} no existe.'}, status=404)
        

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Se requiere el parámetro external_id.'}, status=400)

def get_customer_balance(request):
    try:
        # Obtener el external_id de la solicitud GET
        external_id = request.GET.get('customer_external_id')
        customer = Customers.objects.get(external_id=external_id)
        customer_score = customer.score

        if customer.id is not None:

                # Obtener todos los préstamos asociados al cliente
                loans = Loans.objects.filter(customer_id=customer.id)

                total_debt =0.00
                for loan in loans:
                    total_debt += float(loan.outstanding)

                available_amount = float(customer_score) - total_debt

                # Crear el balance con los datos proporcionados
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

