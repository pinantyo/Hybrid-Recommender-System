from django.urls import path, include
from app import views

from rest_framework import routers


app_name='app'

urlpatterns = [
    # Users
    path('users/<int:id>', views.User.as_view(), name='user-detail'),

    # Recommendation
    path('sites/recommendation/', views.Recommendation.as_view(), name='recommendation_sites'),
    path('sites/similar/<int:id>', views.ItemBasedRecommendation.as_view(), name='recommendation_sites_based'),

    # Rating
    path('sites/rating/<int:id>', views.RatingsModified.as_view(), name='sites_rating'),

    # Tourism
    path('sites/', views.Tourism.as_view(), name='sites'),
    path('sites/<int:id>', views.TourismOne.as_view(), name='site-detail'),

    # Reservation
    path('reservation/', views.Reservation.as_view(), name='reservation'),
]