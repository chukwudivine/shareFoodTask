from django.contrib.auth.models import User
from django.db import models


# This model class creates a recipe database table with these columns.
class Recipe(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.TextField()
    instructions = models.TextField()
    preparation_time = models.IntegerField()
    cuisine_type = models.CharField(max_length=100)
    likes = models.IntegerField(default=0)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# This models class creates the database table to store likes,
# by creating a relationship between the user and the recipe been liked.
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
