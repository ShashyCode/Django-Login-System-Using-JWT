from decimal import Context
from django.contrib.messages import api
from django.http import response, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import serializers
from rest_framework.views import APIView, Response
from rest_framework.renderers import TemplateHTMLRenderer
from Users.serializers import UserSerializer
from Users.models import Users
from django.contrib import messages
import jwt, datetime

# Create your views here.
class SignupView(APIView):

    def get(self, request):
       return render(request, 'signup.html')

    def post(self, request):
        if request.method == "POST":
            #data = {
                #'email': request.POST.get("email"),
                #'password': request.POST.get("password"),
               # 'username': request.POST.get("username"),
               # 'address': request.POST.get("address")
            #}

            #the data dict was throwing some error


            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                messages.success(request, "The User has been created!")
            return redirect("login")
                #return Response(serializer.data)

            


class LoginView(APIView):

    def get(self, request):
        return render(request, 'login.html')


    def post(self, request):
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")

            user = Users.objects.filter(email = email).first()
            if user is None:
                messages.warning(request, 'Invalid Credentials')
                return render(request, 'login.html')

            if not user.check_password(password):
                messages.warning(request, "Incorrect Password")
                return render(request, "login.html")
        
            payload = {
                "id": user.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                "iat" : datetime.datetime.utcnow()
            }

            token = jwt.encode(payload, 'secret', algorithm='HS256')

            response = Response()
            response.set_cookie(key="jwt", value=token, httponly=True)

            return response and redirect("users")

class UserView(APIView):
    def get(self, request):
        queryset = Users.objects.all()
        context = {
            "profiles" : queryset
        }
        return render(request, "users.html", context=context)

    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            messages.warning(request, "No token")
            return redirect("login")
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            messages.warning(request, "Unauthenticated")
            return redirect("login")
        
        queryset = Users.objects.all()
        context = {
            "profiles" : queryset
        }
        return render(request, "users.html", context=context)
        

class DelView(APIView):
    def get(self, request, pk):
        instance = get_object_or_404(Users, pk = pk)
        instance.delete()

        return redirect("users")


class LogoutView(APIView):
    def get(self, request):
        response = Response()
        response.delete_cookie('jwt')

        return redirect("login")



