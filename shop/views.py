from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Product,Order,OrderProduct
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status

from .service import Cart


class ProductListView(APIView):
    def get(self,request):
        products=Product.objects.all()
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data,status=200)
    
class ProductGetView(APIView):
    def get(self,request,id):
        product=get_object_or_404(Product,id=id)
        serializer=ProductSerializer(product)
        return Response(serializer.data,status=200)

class OrderCreateView(APIView):
    def post(self,request):
        print(request.session.get('data'))
        cart=request.session.get('cart',{})
        print(cart,'this is cart view--------')

        order=Order.objects.create(user=request.user)
        print(cart.items(),'these items-----')

        for product_id, quantity in cart.items():
            product=Product.objects.get(id=product_id)
            print(product_id,'this is id of product')
            order_product=OrderProduct.objects.create(order=order,
                                                      product=product,
                                                      quantity=quantity['quantity'],
                                                      price=product.price)
            
            request.session['cart']={}
            return Response({'message':'Order succusfully created'},status=200)
        
            


class CartAPI(APIView):
    """
    Single API to handle cart operations
    """
    def get(self, request, format=None):
        cart = Cart(request)

        return Response(
            {"data": list(cart.__iter__()), 
            "cart_total_price": cart.get_total_price()},
            status=status.HTTP_200_OK
            )

    def post(self, request, **kwargs):
        cart = Cart(request)

        if "remove" in request.data:
            product = request.data["product"]
            cart.remove(product)

        elif "clear" in request.data:
            cart.clear()

        else:
            product = request.data
            cart.add(
                    product=product["product"],
                    quantity=product["quantity"],
                    overide_quantity=product["overide_quantity"] if "overide_quantity" in product else False
                )

        return Response(
            {"message": "cart updated"},)


