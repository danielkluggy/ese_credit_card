from django.urls import path
from .views import AddCardView, GetValidCardsView, GetCardDetailsView

urlpatterns = [
    path('addcard/', AddCardView.as_view(), name='addcard'),
    path('getcard/<str:client_id>/', GetValidCardsView.as_view(), name='getcard'),
    path('getcard/<str:client_id>/<str:number>/', GetCardDetailsView.as_view(), name='getcard'),
]
