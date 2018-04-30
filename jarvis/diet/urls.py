from django.urls import path
from . import views

urlpatterns = [
    # ex: /diet/
    path('',views.index, name='index'),
    # ex: /diet/1/
    path('<int:food_id>/',views.update_food, name='update_food'),
    # ex: /diet/add_entry
    path('add_entry/',views.add_entry, name='add_entry'),
    # ex: /diet/add_food
    path('add_food/',views.add_food, name='add_food'),
    # ex: /diet/search_fatsecret/apple
    path('search_fatsecret/<str:search_term>/',views.search_fatsecret, name='search_fatsecret'),
    # ex: /diet/get_fatsecret_food/98274
    path('get_fatsecret_food/<int:food_id>/',views.get_fatsecret_food, name='get_fatsecret_food'),
    # ex: /diet/delete_entry
    path('delete_entry/<int:entry_id>/',views.delete_entry, name='delete_entry'),
    # ex: /diet/food_info/1/
    path('food_info/<int:food_id>/',views.food_info, name='food_info'),
]

