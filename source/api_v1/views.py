from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api_v1.serrializers import QuoteCreateSerializer, QuoteUpdateSerializer, QuoteSerializer
from webapp.models import Quote, Vote
from api_v1.permission import QuotePermissions


class QuoteViewSet(ModelViewSet):
    permission_classes = [QuotePermissions]

    def get_queryset(self):
        if self.request.method == 'GET' and \
                not self.request.user.has_perm('webapp.quote_view'):
            return Quote.get_moderated()
        return Quote.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuoteCreateSerializer
        elif self.request.method == 'PUT':
            return QuoteUpdateSerializer
        return QuoteSerializer


class VoteApiView(APIView):
    def get(self, request, *args, **kwargs):
        quote = get_object_or_404(Quote, pk=kwargs.get('pk'))
        try:
            Vote.objects.get(session_key=self.request.session.session_key, quote_id=quote)
            return Response({'message': 'you already voted it'}, status=200)
        except Vote.DoesNotExist:
            if self.request.path.split('/')[-1] == 'like':
                Vote.objects.create(session_key=self.request.session.session_key, quote=quote, rating=1)
                quote.rating += 1
                quote.save()
                return Response({'message': 'you like it'}, status=200)
            else:
                Vote.objects.create(session_key=self.request.session.session_key, quote=quote, rating=-1)
                quote.rating -= 1
                quote.save()
                return Response({'message': 'you dislike it'}, status=200)
