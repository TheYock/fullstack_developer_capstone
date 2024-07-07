# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # # path for registration

    # path for login
    path(route='login', view=views.login_user, name='login'),
    path(route='logout', view=views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    path('get_cars', views.get_cars, name='getcars'),

    # path for dealer reviews view
    path('get_dealers', views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>', views.get_dealerships, name='get_dealers_by_state'),
    path('get_dealer_details/<int:dealer_id>', views.get_dealer_details, name='get_dealer_details'),
    path('get_dealer_reviews/<int:dealer_id>', views.get_dealer_reviews, name='get_dealer_reviews'),

    # path for add a review view
    path('add_review', views.add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
