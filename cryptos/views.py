from cryptos.serializer import CriptosSerializer, CriptosUserSerializer
from cryptos.models import Criptos
from django.http import HttpResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def home(request):
    return HttpResponse("Welcome to the CryptotrackerAPI!")

class CriptosList(APIView):
    def get_object(self,pk):
        try:            
            return Criptos.objects.get(pk = pk)
        except Criptos.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        criptos = self.get_object(pk)
        serializer = CriptosUserSerializer(criptos)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        cripto = self.get_object(pk)
        serializer = CriptosSerializer(cripto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('update success')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        cripto = self.get_object(pk)
        serializer = CriptosSerializer(cripto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('delete success')
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def post(self, request):        
        serializer = CriptosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class Portfolio(generics.ListAPIView):
    serializer_class= CriptosUserSerializer

    def get_queryset(self):
        user = self.request.user
        criptos = Criptos.objects.filter(user_fk_id=self.request.user, able=0)
        return criptos