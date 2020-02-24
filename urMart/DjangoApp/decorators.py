from .models import Product, Order

from django.views.decorators.csrf import requires_csrf_token
from django.http import JsonResponse

import json, logging
import functools

def vip_required(func):
    @functools.wraps(func)
    def wrap(request, *args,**kargs):
        data = json.loads(request.body.decode()) # order data
        p_obj = Product.objects.get(p_id=data['product_id'])
        p_obj.vip = bool(data['prod_vip'])

        if p_obj.vip and not data['vip']:
            logging.warning('You are not allowed to order this product.')
            return JsonResponse({'status':False, 'message':'You are not allowed to order this product.'}, status=201)
        else:
            return func(request)
    return wrap

def qty_enough(func):
    @functools.wraps(func)
    def wrap(request, *args,**kargs):
        data = json.loads(request.body.decode())
        p_obj = Product.objects.get(p_id=data['product_id'])
        notisify = False
        actions = data['action']
        # Stock from zero to n.
        if actions=='del' and p_obj.s_pcs==0 and int(data['qty'])>0:
            logging.warning('Enter the goods.')
            notisify = True
   
        # Not enough stock.
        if actions=='add' and p_obj.s_pcs < int(data['qty']):
            logging.warning('There is out of stock.')
            return JsonResponse({'status':False, 'message':'There is out of stock.'}, status=201)
        return func(request,notisify=notisify)
    
    return wrap    

