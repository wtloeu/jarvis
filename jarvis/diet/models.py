import datetime

from django.db import models
from django.utils import timezone

class Food(models.Model):
    CUPS = 'c'
    GRAMS = 'g'
    OUNCES = 'oz'
    POUNDS = 'lb'
    TABLESPOONS = 'tbsp'
    TEASPOONS= 'tsp'
    SERVING_UNIT_CHOICES = (
            (CUPS, 'cups'),
            (GRAMS, 'grams'),
            (OUNCES, 'ounces'),
            (POUNDS, 'pounds'),
            (TABLESPOONS, 'tablespoons'),
            (TEASPOONS, 'teaspoons')
            )

    name = models.CharField(max_length=200)
    serving_size = models.DecimalField(max_digits=5, decimal_places=2)
    serving_unit = models.CharField(max_length=32, choices=SERVING_UNIT_CHOICES,default=GRAMS)
    calories = models.DecimalField(max_digits=5, decimal_places=2)
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=2)
    fat = models.DecimalField(max_digits=5, decimal_places=2)
    fiber = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name + ' (' + self.serving_unit + ')'

class Entry(models.Model):
    """ This is a record in the tracker. Used to describe 1 entry into the diet tracker."""
    entry_date = models.DateField('date consumed',default=datetime.date.today)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    servings = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    serving_unit = models.CharField(max_length=200, editable=False)
    calories = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    protein = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    fat = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    fiber = models.DecimalField(max_digits=5, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.serving_unit = self.food.serving_unit
        self.calories = (self.servings / self.food.serving_size) * self.food.calories
        self.protein = (self.servings / self.food.serving_size) * self.food.protein
        self.carbohydrates = (self.servings / self.food.serving_size) * self.food.carbohydrates
        self.fat = (self.servings / self.food.serving_size) * self.food.fat
        self.fiber = (self.servings / self.food.serving_size) * self.food.fiber
        super(Entry,self).save(*args, **kwargs)

    def __str__(self):
        return self.food.name + ' (' + str(self.servings).rstrip('0').rstrip('.') + self.serving_unit + ')'
