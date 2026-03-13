from django.urls import path
from .views import ThemeSettingDetail

urlpatterns = [
    # API endpoint ab static data dega
    path('theme-settings/', ThemeSettingDetail.as_view(), name='theme-settings'),
]