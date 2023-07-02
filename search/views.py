from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .models import Like


# This view function serves as the root of our app
def home(request):
    # retrieves all Recipe objects from the database
    r = Recipe.objects.all()
    # creates a paginator with a page size of 4
    paginator = Paginator(r, 4)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)
    # renders the retrieved data in the 'home.html' template
    return render(request, 'home.html', {"recipes": recipes})


# This view function handles all search functionality.
def search(request):
    # intercepts query data from the incoming http post request and stores it in a variable 'searchTerm'
    searchTerm = request.GET.get('search')
    # retrieves all Recipe objects from the database where name contains searchTerm
    r = Recipe.objects.filter(name__icontains=searchTerm)
    # creates a paginator with a page size of 4
    paginator = Paginator(r, 4)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)
    # renders the retrieved data in the 'home.html' template
    return render(request, 'home.html', {"recipes": recipes, "searchTerm": searchTerm})


# This view function handles all filter functionality.
def queryfilter(request):
    # intercepts query data from the incoming http post request and stores it in a variable 'cuisine'
    cuisine = request.GET.get('cuisine')
    # performs a conditional logic to validate if cuisine contains any data
    if cuisine:
        # retrieves all Recipe objects from the database where cuisine_type contains cuisine
        r = Recipe.objects.filter(cuisine_type=cuisine)
    else:
        # else it retrieves all Recipe objects from the database
        r = Recipe.objects.all()
    # intercepts query data from the incoming http post request and stores it in a variable 'preparation_time'
    preparation_time = request.GET.get('preparation_time')
    # performs a conditional logic to validate if preparation_time contains any data
    if preparation_time:
        # retrieves all Recipe objects from the database where preparation_time is less preparation_time
        r = r.filter(preparation_time__lte=preparation_time)
    # intercepts query data from the incoming http post request and stores it in a variable 'ingredients'
    ingredients = request.GET.get('ingredients')
    # performs a conditional logic to validate if ingredients contains any data
    if ingredients:
        # retrieves all Recipe objects from the database where ingredients contains ingredients
        r = r.filter(ingredients__icontains=ingredients)
    # creates a paginator with a page size of 4
    paginator = Paginator(r, 4)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)
    # renders the retrieved data in the 'home.html' template
    return render(request, 'home.html', {"recipes": recipes})


# This view function handles the like functionality.
def like(request, recipe_id):
    # creates a variable user where value is the user sending the request
    user = request.user
    # get recipe object from database where id equals the request object id
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    # creating a current_likes variable value is the recipe object like column
    current_likes = recipe.likes
    # checks if the current user is signed in
    if user.is_authenticated:
        # retrieves the like object from the database that belongs to the current user and recipe
        # and stores to the liked variable
        liked = Like.objects.filter(user=user, recipe=recipe).count()
        # if the current recipe is not liked
        if not liked:
            # creates a like object with the current user and the current recipe
            liked = Like.objects.create(user=user, recipe=recipe)
            # increment the current_likes variable by one
            current_likes = current_likes + 1
        # if the current recipe is already liked by current user
        else:
            # deletes the like object of the current user and the current recipe
            liked = Like.objects.filter(user=user, recipe=recipe).delete()
            # decrement the current_likes variable by one
            current_likes = current_likes - 1
        # assign the value of current_likes to the recipe object like column
        recipe.likes = current_likes
        # save the above query to the database
        recipe.save()
    # redirect to the home page
    return redirect('home')

