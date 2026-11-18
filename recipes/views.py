from django.shortcuts import render

from .mealdb_api import mealdb
from .mealdb_api.mealdb import MealDBError


def recipes(request):
    query = request.GET.get('q', '').strip()
    recipes = []
    error = None
    
    if query:
        try:
            recipes = mealdb.search_recipes(query)
        except MealDBError:
            error = 'Sorry, something went wrong.'
    
    try:
        random_recipe = mealdb.get_random_recipe()
    except MealDBError:
        random_recipe = None
    
    return render(
        request,
        'recipes/recipes.html',
        {
            'query': query,
            'recipes': recipes,
            'error': error,
            'random_recipe': random_recipe,
        }
    )