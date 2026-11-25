from django.shortcuts import render
from django.http import Http404

from .mealdb_api import mealdb
from .mealdb_api.mealdb import MealDBError


def recipes_list(request):
    query = request.GET.get('q', '').strip()
    recipes = []
    error = None
    
    if query:
        try:
            recipes = mealdb.filter_by_ingredient(query)
        except MealDBError:
            error = 'Sorry, something went wrong.'
    
    try:
        random_recipe = mealdb.get_random_recipe()
    except MealDBError:
        random_recipe = None
    
    return render(
        request,
        'recipes/recipes_list.html',
        {
            'query': query,
            'recipes': recipes,
            'error': error,
            'random_recipe': random_recipe,
        }
    )


def recipe_detail(request, meal_id):
    """Display a detailed recipe from TheMealDB."""
    try:
        recipe = mealdb.get_recipe(meal_id)
    except MealDBError:
        return render(
            request,
            'recipes/recipe_detail.html',
            {'error': 'Sorry, we could not load this recipe. Please try again.'},
            status=503,
        )

    if recipe is None:
        raise Http404('Recipe not found.')

    ingredients = mealdb.get_ingredients(recipe)

    return render(
        request,
        'recipes/recipe_detail.html',
        {
            'recipe': recipe,
            'ingredients': ingredients,
        },
    )