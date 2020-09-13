from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import (
	IsAuthenticatedOrReadOnly,
	IsAuthenticated,
)
from rest_framework import (
	viewsets,
	status,
	filters,
)

from . import (
	serializers,
	models,
	permissions,
)


class HelloApiView(APIView):
	"""Test API View"""

	serializer_class = serializers.HelloSerializer

	def get(self, request, format=None):
		"""Return a list of APOView features"""

		an_apiview = [
			'Uses HTTP me....',
			'It is similar ....',
			'Gives most control...',
			'Is mapperd man...'
		]

		return Response({'message': "Hello", 'an_apiView':an_apiview})


	def post(self, request):
		"""Create a hello message"""
		serializer = serializers.HelloSerializer(data=request.data)

		if serializer.is_valid():
			name = serializer.data.get('name')
			message = 'Hello {}'.format(name)
			return Response({'message': message})
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def put(self, request, pk=None):
		"""UPDATE object"""
		return Response({'method':'put'})

	def patch(self, request, pk=None):
		"""Pathch request updates"""
		return Response({'method':'patch'})
	def delete(self, request, pk=None):
		return Response({"method":"delete"})


class HelloViewSet(viewsets.ViewSet):
	"""Test API ViewSet"""

	serializer_class = serializers.HelloSerializer

	def list(self, request):
		"""Return hello message"""
		a_viewset = [
			'Uses actions me....',
			'It is URLS ....',
			'Gives most MOERE FUNCTION...',
			'Is mapperd man...'
		]
		return Response({'message': "Hello", 'aa_viewset':a_viewset})

	def create(self, request):
		"""Create new Hello message"""
		serializer = serializers.HelloSerializer(data=request.data)

		if serializer.is_valid():
			name = serializer.data.get('name')
			message = 'Hello, {}'.format(name)
			return Response({'message':message})
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def retrieve(self, request, pk=None):
		"""Handles getting object by ID"""
		return Response({'http_method':'GET'})

	def update(self, request, pk=None):
		"""Handles updating object"""
		return Response({'http_method':'PUT'})
	def partial_update(self, request, pk=None):
		return Response({'http_method':'PATCH'})
	def destroy(self, request, pk=None):
		return Response({'http_method':'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):

	serializer_class = serializers.UserProfileSerializer
	queryset = models.UserProfile.objects.all()
	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.UpdataOwnProfile,)
	filter_backends = (filters.SearchFilter,)
	search_fields = ('name', 'email',)


class LoginViewSet(viewsets.ViewSet):
	"""Chaeck token"""
	serializer_class = AuthTokenSerializer

	def create(self, request):
		"""Use the ObtainAuthToken"""
		return ObtainAuthToken().post(request)


class UserProfileFeedViewSet(viewsets.ModelViewSet):

	authentication_classes = (TokenAuthentication,)
	serializer_class = serializers.ProfileFeedItemSerializer
	queryset = models.ProfileFeedItem.objects.all()
	permission_classes = (permissions.PostOwnStatus, IsAuthenticated)


	def perform_create(self, serializer):
		serializer.save(user_profile=self.request.user) #asdasda