from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.db.models import Sum
from .forms import AddEntryForm, AddFoodForm, DeleteEntryForm, UpdateFoodForm
from fatsecret import Fatsecret
import datetime, decimal, json

from .models import Entry, Food

def index(request):
    add_entry_form = AddEntryForm()
    add_food_form = AddFoodForm()
    delete_entry_form = DeleteEntryForm()
    todays_entry_list = Entry.objects.filter(entry_date=datetime.date.today())

    if not todays_entry_list:
        total_calories = 0
        total_fat = 0
        total_carbohydrates = 0
        total_fiber = 0
        total_protein = 0
    else:
        total_calories = todays_entry_list.aggregate(Sum('calories'))['calories__sum']
        total_fat = todays_entry_list.aggregate(Sum('fat'))['fat__sum']
        total_carbohydrates = todays_entry_list.aggregate(Sum('carbohydrates'))['carbohydrates__sum']
        total_fiber = todays_entry_list.aggregate(Sum('fiber'))['fiber__sum']
        total_protein = todays_entry_list.aggregate(Sum('protein'))['protein__sum']
    context = {'add_entry_form': add_entry_form,
               'add_food_form': add_food_form, 
               'delete_entry_form': delete_entry_form, 
               'todays_entry_list': todays_entry_list, 
               'total_calories': total_calories,
               'total_protein': total_protein,
               'total_fat': total_fat,
               'total_carbohydrates': total_carbohydrates,
               'total_fiber': total_fiber,
               'total_protein': total_protein
                }
    return render(request, 'diet/index.html', context)

def detail(request, food_id):
    food = get_object_or_404(Food, pk=food_id)
    update_food_form = UpdateFoodForm()
    context = {'food': food,
               'update_food_form': update_food_form
               }
    return render(request, 'diet/detail.html', context)

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            txt = str(obj)
            dec_string = txt.rstrip('0').rstrip('.') if '.' in txt else txt
            return dec_string
        return json.JSONEncoder.default(self, obj)

def food_info(request, food_id):
    food = get_object_or_404(Food, pk=food_id)
    nutrition_facts = {
            'serving_size': food.serving_size,
            'calories': food.calories,
            'fat': food.fat,
            'carbohydrates': food.carbohydrates,
            'fiber': food.fiber,
            'protein': food.protein
        }
    data = json.dumps(nutrition_facts, cls=DecimalEncoder)
    return HttpResponse(data, content_type='application/json')

def add_entry(request):
    if request.method == "POST":
        new_entry = AddEntryForm(request.POST)
        if new_entry.is_valid():
            new_entry.save()
            messages.success(request, 'Entry added!')
        else:
            messages.error(request, 'Could not add entry.')
    return redirect('index')

def delete_entry(request, entry_id):
    if request.method == "POST":
        doomed_entry = get_object_or_404(Entry,pk=entry_id)
        delete_form = DeleteEntryForm(request.POST,instance=doomed_entry)
        if delete_form.is_valid():
            doomed_entry.delete()
            messages.success(request, 'Entry deleted!')
        else:
            messages.error(request, 'Could not delete entry.')
    return redirect('index')

def add_food(request):
    if request.method == "POST":
        new_food = AddFoodForm(request.POST)
        if new_food.is_valid():
            new_food.save()
            messages.success(request, 'Food added!')
        else:
            messages.error(request, new_food.errors)
    return redirect('index')

def search_fatsecret(request, search_term):
    fs = Fatsecret(consumer_key, consumer_secret) 
    foods = fs.foods_search(search_term, max_results=20)
    data = json.dumps(foods)
    return HttpResponse(data, content_type='application/json')

def get_fatsecret_food(request, food_id):
    fs = Fatsecret(consumer_key, consumer_secret) 
    food = fs.food_get(food_id)
    data = json.dumps(food)
    return HttpResponse(data, content_type='application/json')


def update_food(request, food_id):
    food = get_object_or_404(Food, pk=food_id)
    if request.method == "POST":
        update_food_form = UpdateFoodForm(request.POST, instance=food)
        if update_food_form.is_valid():
            update_food_form.save()
            messages.success(request, 'Food updated!')
        else:
            messages.error(request, 'Could not update food.')
            return redirect('index')
    else:
        update_food_form = UpdateFoodForm(instance=food)

    context = {'food': food,
                'update_food_form': update_food_form
                }
    return render(request, 'diet/detail.html', context)
