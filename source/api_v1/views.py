from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS, IsAdminUser
from django.shortcuts import render, get_object_or_404

from api_v1.serrializers import *
from webapp.models import *


class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer = ProductSerializer
    permissions = [IsAdminUser]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return super().get_permissions()


class OrderApiView(APIView):
    permissions = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        print(request)
        order = get_object_or_404(Order, pk=kwargs.get('pk'))
        srl = OrderSerializer(order)
        return Response(srl.data)

    def post(self, request, *args, **kwargs):
        srl = OrderSerializer(data=request.data)
        if srl.is_valid():
            order = srl.save()
            return Response(srl.data)
        else:
            return Response(srl.errors, status=400)

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            return []
        return super().get_permissions()
