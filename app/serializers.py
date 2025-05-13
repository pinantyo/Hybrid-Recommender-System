from dataclasses import fields
from rest_framework import serializers
from app import models


# Base Serializers
class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = models.CategoryTourism
		fields = ['category_id','category_name','img']

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.AccountCustom
		fields = ['email','created']
		
class TourismSerializer(serializers.ModelSerializer):
	category_details = CategorySerializer(source="category")

	class Meta:
		model = models.TourismPlace
		fields = [f.name for f in model._meta.get_fields()[2:] if f.name != 'category'] + ['category_details']

class ReservationSerializer(serializers.ModelSerializer):
	tourism_details = TourismSerializer(source="place")
	user_details = UserSerializer(source="user")
	
	class Meta:
		model = models.Reservation
		fields = ['reservation_id','user_details','tourism_details','place_ratings','comments','time','status','book_date']

class CreateReservationSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Reservation
		fields = ['user','place','place_ratings','comments','book_date']
# 
"""
	Note:
	Use source="field" to fetch parent's data from child
	Use many=True to fetch child's data from parent
"""
class UserGetSerializer(serializers.ModelSerializer):
	reservation_user_set = serializers.SerializerMethodField()

	class Meta:
		model = models.AccountCustom
		fields = ['id','age','location'] + ['reservation_user_set']
	
	"""
		Referensi:
		https://stackoverflow.com/questions/48247490/django-rest-framework-nested-serializer-order/48249910
	"""
	def get_reservation_user_set(self, obj):
		return ReservationSerializer(instance=obj.reservation_user_set.all().order_by('-time'), many=True).data


class TourismReservationSerializer(serializers.ModelSerializer):
	reservation_place_set = serializers.SerializerMethodField()
	category_details = CategorySerializer(source='category')

	class Meta:
		model = models.TourismPlace
		fields = [f.name for f in model._meta.get_fields()[1:] if f.name != 'category'] + ['reservation_place_set','category_details']
	
	def get_reservation_place_set(self, obj):
		return ReservationSerializer(instance=obj.reservation_place_set.all().order_by('-time'), many=True).data


class UserHistorySerializer(serializers.ModelSerializer):
	place_details = TourismSerializer(source='place')
	

	class Meta:
		model = models.Reservation
		fields = ['place_ratings','comments','time','book_date'] + ['place_details']