# API Lib
from rest_framework import permissions, status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

# Backend Lib
# from django.contrib import messages
# from django.contrib.auth import authenticate
# from django.http import Http404
# from django.shortcuts import redirect, render
# from django.views.decorators.csrf import csrf_exempt, csrf_protect

# Models, API Serializers, Forms
from app import models, serializers, optimize
from app.model_development import models as rec

# Caching
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

# from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

# Asynchronous
from asgiref.sync import sync_to_async
import asyncio

# Rendering
# permissions.DjangoModelPermissionsOrAnonReadOnly

# Create your views here.

"""
	Pagination API
	to segment data refers to this approach:
	
	paginator = optimize.LowResultsSetPagination()
	paginate_result = paginator.paginate_queryset(query_from_DB, request)
	serializer = serializers.AnySerializers(paginate_result, many=True, context={'request':request})

	To retrieve data from Django REST Pagination
	refer to this url:

	/api/sites/?page=3

"""

# Global Var
if getattr(settings, 'CACHES_CONFIG', 0):
	CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


MODEL_RECC = None

# Create your views here.
"""
	API for users CRUD
	Referensi:
	How to set permissions per handler function with APIView? Stackoverflow, 
	answered Mar 28, 2020 at 23:30, user1720845
"""
class AbstractPermissionView(APIView):
	def get_permissions(self):
		"""
			Instantiates and returns the list of permissions that this view requires.
		"""
		return {key: [permission() for permission in permissions] for key, permissions in self.permission_classes.items()}


	def check_permissions(self, request):
		"""
			Check if the request should be permitted.
			Raises an appropriate exception if the request is not permitted.
		"""

		for permission in self.get_permissions()[request.method.lower()]:
			if not permission.has_permission(request, self):
				self.permission_denied(
					request,
					message=getattr(permission, 'message', None),
					code=getattr(permission, 'code', None)
				)



class User(AbstractPermissionView):
	permission_classes = {
		'get':[permissions.IsAuthenticated],
		'patch':[permissions.IsAuthenticated]
	}

	def get_user(self, id):
		return models.AccountCustom.objects.get(id=id)

	def get(self, request, id):
		serializer=serializers.UserGetSerializer(self.get_user(id))
		return Response(serializer.data, status=status.HTTP_200_OK)

	def patch(self, request, id):
		serializer=serializers.UserSerializer(self.get_user(id), request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
	API for Recommendation
"""
class Recommendation(AbstractPermissionView):
	permission_classes = {
		'get':[permissions.IsAuthenticated]
	}

	def get(self, request):
		global MODEL_RECC

		tourism = models.TourismPlace.objects.get_queryset().order_by('place_id')
		personalization = models.UserPersonalization.objects.filter(user=request.user).select_related('category').values('category__category_name')
		
		# Init model
		if MODEL_RECC is None:
			MODEL_RECC = rec.GenerateRecommenderSystem(tourism, ensemble=1)
		
		if request.user.is_authenticated:
			# recommendation = None
			# if personalization:
			recommendation = MODEL_RECC.regression_prediction(request.user, 5, personalization)
			# else:
			# 	personalization = None
			# 	recommendation = MODEL_RECC.regression_prediction(request.user, 5, personalization)

			recommendation = tourism.filter(pk__in=recommendation)
			rec_serializer = serializers.TourismSerializer(recommendation, many=True, context={'request':request})

			return Response(rec_serializer.data, status=status.HTTP_200_OK)
		
		return Response(status=status.HTTP_400_BAD_REQUEST)

class ItemBasedRecommendation(AbstractPermissionView):
	permission_classes = {
		'get':[permissions.AllowAny,]
	}

	def get(self, request, id):
		try:
			tourism = models.TourismPlace.objects.get_queryset().order_by('place_id')
			tourism = tourism.filter(pk__in=rec.ContentRecc(tourism).vectorized_similarity(id))
			serializer = serializers.TourismSerializer(tourism, many=True, context={'request':request})
		except:
			return Response(status=status.HTTP_404_NOT_FOUND)
		else:
			return Response(serializer.data, status=status.HTTP_200_OK)



"""
	API for Tourism CRUD
"""
class Tourism(AbstractPermissionView):
	permission_classes = {
		'get':[permissions.AllowAny],
		'post':[permissions.IsAdminUser]
	}

	# @sync_to_async
	# @method_decorator(cache_page(CACHE_TTL))
	def get(self, request):
		global MODEL_RECC

		tourism = models.TourismPlace.objects.get_queryset().order_by('place_id')

		paginator = optimize.LowResultsSetPagination()
		paginate_result = paginator.paginate_queryset(tourism, request)

		if paginate_result is not None:
			serializer = serializers.TourismSerializer(paginate_result, many=True, context={'request':request})
			return paginator.get_paginated_response(serializer.data)

		serializer = serializers.TourismSerializer(tourism, many=True, context={'request':request})
		return Response(serializer.data, status=status.HTTP_200_OK)



class TourismOne(AbstractPermissionView):

	permission_classes = {
		'get':[permissions.AllowAny],
	}

	def get_tourism(self, id):
		return models.TourismPlace.objects.get(place_id=id)

	
	# @method_decorator(cache_page(CACHE_TTL))
	def get(self, request, id): 
		count = models.Reservation.objects.all().count()

		serializer = serializers.TourismReservationSerializer(self.get_tourism(id))
		return Response({'data':serializer.data, 'count':count}, status=status.HTTP_200_OK)
		

"""
	API for Reservation CRUD
"""

class Reservation(AbstractPermissionView):
	permission_classes = {
		'get':[permissions.IsAuthenticated],
		'post':[permissions.IsAuthenticated],
	}

	# @method_decorator(cache_page(CACHE_TTL))
	def get(self, request):
		if request.user.is_authenticated:
			reservations = models.Reservation.objects.filter(user=request.user)

			paginator = optimize.LowResultsSetPagination()
			paginate_result = paginator.paginate_queryset(reservations, request)

			if paginate_result is not None:
				serializer = serializers.UserHistorySerializer(paginate_result, many=True, context={'request':request})
				return paginator.get_paginated_response(serializer.data)


			serializer = serializers.UserHistorySerializer(reservations, many=True, context={'request':request})
			return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request):
		global MODEL_RECC
		serializer = serializers.CreateReservationSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()

			# Init model
			if MODEL_RECC is None:
				tourism = models.TourismPlace.objects.get_queryset().order_by('place_id')
				MODEL_RECC = rec.GenerateRecommenderSystem(tourism, ensemble=1)

			personalization = models.UserPersonalization.objects.filter(user=request.user).select_related('category').values('category__category_name')

			MODEL_RECC.update_model({'user':[request.data['user']], 'place':[request.data['place']]}, personalization)
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(status=status.HTTP_400_BAD_REQUEST)

class RatingsModified(AbstractPermissionView):
	permission_classes = {
		'patch':[permissions.IsAuthenticated]
	}
	
	def patch(self, request, id):
		global MODEL_RECC
		tourism = models.TourismPlace.objects.get(place_id = id)
		
		try:
			latest_reservation = models.Reservation.objects.filter(user=request.user, place=tourism).latest('time')

			# Init model
			if MODEL_RECC is None:
				tourism = models.TourismPlace.objects.get_queryset().order_by('place_id')
				MODEL_RECC = rec.GenerateRecommenderSystem(tourism, ensemble=1)

			if(latest_reservation):
				latest_reservation.place_ratings = request.data['rating']
				latest_reservation.comments = request.data['feedback']
				latest_reservation.save()

				personalization = models.UserPersonalization.objects.filter(user=request.user).select_related('category').values('category__category_name')

				MODEL_RECC.update_model(latest_reservation, personalization, new_data=0)
		except:
			return Response(status=status.HTTP_404_NOT_FOUND)

		return Response(status=status.HTTP_200_OK)
