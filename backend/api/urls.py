from django.urls import path

from api.views import LetterCreatorView, UserView, TokenView

urlpatterns = [
    path('users/', UserView.as_view(), name="users"),
    path('tokens/', TokenView.as_view(), name="tokens"),
    path('application-creator/', LetterCreatorView.as_view(), name="application-creator")
]
    
