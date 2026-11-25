import requests
from django.conf import settings


class MealDBError(Exception):
    """ Raised when request fail or return invalid data """
    

def _get(endpoint, params=None):
    """ Send a request to TheMealDB and get back a json response """
    url = f'{settings.MEALDB_BASE_URL}/{settings.MEALDB_API_KEY}/{endpoint}'
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        raise MealDBError from error


def _recipes(data):
    """ Create a recipe list, or an empty list if no matches """
    recipes = data.get('meals')
    
    if not recipes:
        return []
    
    return recipes


def search_recipes(query):
    """ Search recipes by name """
    data = _get('search.php', params={'s': query})
    return _recipes(data)


def get_recipe(meal_id):
    """ Get a detailed recipe """
    data = _get('lookup.php', params={'i': meal_id})
    recipes = _recipes(data)
    
    return recipes[0] if recipes else None


def get_random_recipe():
    """ Get a random recipe """
    data = _get('random.php')
    recipes = _recipes(data)
    
    return recipes[0] if recipes else None


def get_categories():
    """ Get the recipe categories """
    data = _get('categories.php')
    return data.get('categories', [])


def filter_by_ingredient(ingredient):
    """ Get recipes filtered by ingredient """
    data = _get('filter.php', params={'i': ingredient})
    return _recipes(data)


def filter_by_category(category):
    """ Get recipes filtered by category """
    data = _get('filter.php', params={'c': category})
    return _recipes(data)


def filter_by_area(area):
    """ Get recipes filtered by cuisine style """
    data = _get('filter.php', params={'a': area})
    return _recipes(data)


def get_ingredients(recipe):
    """Return the recipe with ingredient's quantities."""
    ingredients = []

    for number in range(1, 21):
        name = (recipe.get(f'strIngredient{number}') or '').strip()
        measure = (recipe.get(f'strMeasure{number}') or '').strip()

        if name:
            ingredients.append({
                'name': name,
                'measure': measure,
            })

    return ingredients