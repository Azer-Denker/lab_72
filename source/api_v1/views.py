from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS, IsAdminUser

from api_v1.serrializers import ProductSerializer, OrderSerializer
from webapp.models import Product, Order, OrderProduct


class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permissions_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return super().get_permissions()


class OrderApiView(APIView):
    permissions_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        order = Order.objects.all()
        srl = OrderSerializer(order, many=True)
        return Response(srl.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        order = Order.objects.create(name=data['name'], address=data['address'], phone=data['phone'])
        for i in data['order_products']:
            product = Product.objects.get(pk=i['product'])
            order_product = OrderProduct.objects.create(product=product, order=order, qty=i['qty'])
        return Response({"message": "Заказ был создан"}, status=204)

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            return []
        return super().get_permissions()


# class CartApiView(APIView):
#     permission_classes = [IsAdminUser]
#
#     def get(self, request, *args, **kwargs):
#         if 'pk' in kwargs.keys():
#             article = get_object_or_404(Article, pk=kwargs.get('pk'))
#             slr = ArticleSerializer(article)
#             return JsonResponse(slr.data)
#
#     def put(self, request, *args, **kwargs):
#         article = get_object_or_404(Article.objects.all(), pk=kwargs.get('pk'))
#         data = json.loads(request.body)
#         srl = ArticleSerializer(instance=article, data=data, partial=True)
#         if srl.is_valid(raise_exception=True):
#             article = srl.update(article, srl.validated_data)
#             return JsonResponse(srl.data, safe=False)
#         else:
#             response = JsonResponse(srl.errors, safe=False)
#             response.status_code = 400
#             return response
