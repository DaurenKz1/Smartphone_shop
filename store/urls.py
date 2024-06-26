from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
	path('', views.index, name="index"),
	path('login', views.signin, name="signin"),
	path('logout', views.signout, name="signout"),
	path('registration', views.registration, name="registration"),
	path('smartphone/<int:id>', views.get_smartphone, name="smartphone"),
	path('smartphones', views.get_smartphones, name="smartphones"),
	path('brand/<int:id>', views.get_smartphone_brand, name="brand"),
	path('contact/', views.contact, name='contact'),
	path('category/<int:id>', views.get_category, name="category"),
]