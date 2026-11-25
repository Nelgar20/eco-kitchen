from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipes_list, name='recipes'),
    path('<int:meal_id>/', views.recipe_detail, name='recipe_detail'),

]
