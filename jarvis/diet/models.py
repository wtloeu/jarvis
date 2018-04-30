import datetime

from django.db import models
from django.utils import timezone

class Food(models.Model):
    name = models.CharField(max_length=200)
    serving_size = models.CharField(max_length=32,  default='')
    calories = models.DecimalField(max_digits=5, decimal_places=2)
    fat = models.DecimalField(max_digits=5, decimal_places=2)
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=2)
    fiber = models.DecimalField(max_digits=5, decimal_places=2)
    protein = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name + ' (' + self.serving_size + ')'

class Entry(models.Model):
    """ This is a record in the tracker. Used to describe 1 entry into the diet tracker."""
    entry_date = models.DateField('date consumed',default=datetime.date.today)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    servings = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    serving_size = models.CharField(max_length=32, editable=False)
    calories = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    fat = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    fiber = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    protein = models.DecimalField(max_digits=5, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.serving_size = self.food.serving_size
        self.calories = self.servings * self.food.calories
        self.fat = self.servings * self.food.fat
        self.carbohydrates = self.servings * self.food.carbohydrates
        self.fiber = self.servings * self.food.fiber
        self.protein = self.servings * self.food.protein
        super(Entry,self).save(*args, **kwargs)

    def __str__(self):
        return self.food.name + ' (' + str(self.servings).rstrip('0').rstrip('.') + ' x ' + self.serving_size + ')'
