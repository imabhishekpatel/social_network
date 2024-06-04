from django.urls import path
from user_management.views import *

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[

    path('login/', UserToken.as_view()),
    path('signup/', SignupView.as_view()),
    path('search/', UserSearchView.as_view(), name='user-search'),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)