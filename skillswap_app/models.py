# from django.db import models
# from django.contrib.auth.models import User

# class Category(models.Model):
#     category_name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.category_name

# class Skill(models.Model):
#     TYPE_CHOICES = [
#         ('offer', 'Offer'),
#         ('request', 'Request'),
#     ]

#     title = models.CharField(max_length=100)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     description = models.CharField(max_length=500)
#     availability = models.BooleanField()
#     location = models.CharField(max_length=50)
#     type = models.CharField(max_length=10, choices=TYPE_CHOICES)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.title} {self.description} ({self.get_type_display()})"
