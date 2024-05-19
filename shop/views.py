from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Product,Order,OrderProduct
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate,login
from .serializers import UserRegisterSerializer,UserLoginSerializer,OrderItemSerializer
from django.shortcuts import get_object_or_404

from .service import Cart
from rest_framework.permissions import IsAuthenticated

class ProductListView(APIView):
    
    @swagger_auto_schema()
    def get(self,request):
        products=Product.objects.all()
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data,status=200)
    
class ProductGetView(APIView):
    @swagger_auto_schema()
    def get(self,request,id):
        product=get_object_or_404(Product,id=id)
        serializer=ProductSerializer(product)
        return Response(serializer.data,status=200)

class OrderCreateView(APIView):
    permission_classes=(IsAuthenticated,)

    @swagger_auto_schema(request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={

                'products': [{"id":openapi.Schema(type=openapi.TYPE_INTEGER),
                            "quantity":openapi.Schema(type=openapi.TYPE_INTEGER)},
                            {"id":openapi.Schema(type=openapi.TYPE_INTEGER),
                            "quantity":openapi.Schema(type=openapi.TYPE_INTEGER)}]
            },
            example={
                    "products": [{
                            "id": 1,
                             "quantity": 5},
                             {
                            "id": 2,
                             "quantity": 5}
                             ]}))
    def post(self,request):
       
        order=Order.objects.create(user=request.user)
        serializer=OrderItemSerializer(request.data['products'],many=True)
        
        for product in serializer.data:
            product_in_db=get_object_or_404(Product,id=product['id'])
            order_product=OrderProduct.objects.create(order=order,
                                                      product=product_in_db,
                                                      quantity=int(product['quantity']),
                                                      price=product_in_db.price)
            
         
            return Response({'message':'Order succusfully created'},status=200)
        
            


class CartAPI(APIView):
    """
    Single API to handle cart operations
    """
    @swagger_auto_schema()
    def get(self, request, format=None):
        cart = Cart(request)

        return Response(
            {"data": list(cart.__iter__()), 
            "cart_total_price": cart.get_total_price()},
            status=status.HTTP_200_OK
            )
    

    @swagger_auto_schema(
     request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={

                'product': {"id":openapi.Schema(type=openapi.TYPE_INTEGER),
                            "price":openapi.Schema(type=openapi.TYPE_INTEGER)},
                "quantity":openapi.Schema(type=openapi.TYPE_INTEGER)
                
            },
            example={
                    "product": {
                            "id": 1,
                           
                            "price": "1800.00",
                        },
                "quantity": 5
                }
            
        ),)
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

class LoginView(APIView):

    @swagger_auto_schema(request_body=UserLoginSerializer)
    def post(self,request):
        if request.method == 'POST':
            print(request.data,'this is post--')
            print(request.data,'this is dataaa')

            print(request.data.get('username'))
            print(request.data.get('password'))
            # Authenticate the user
            user = authenticate(request, username=request.data.get('username'), password=request.data.get('password'))
            print(user , 'this is user')
            if user is not None:
                login(request, user)
                return Response({"message":"you have succesfully loged in"},status=200)
        return Response({"message":'something went wrong , try again'},status=404)


class UserRegistrationView(APIView):
    @swagger_auto_schema(request_body=UserRegisterSerializer,   properties={

                'username':openapi.Schema(type=openapi.TYPE_STRING),
                          
                "password":openapi.Schema(type=openapi.TYPE_STRING)
                
            },)
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        print()
        if serializer.is_valid():
          
            user = serializer.save()
            login(request, user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)