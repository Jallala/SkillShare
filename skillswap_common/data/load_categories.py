import os
import sys
import django

# Set the base directory to the parent of the manage.py file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillswap_project.settings')  
django.setup()

from skillswap_common.models import Category

def populate_categories():
    category_names = ['Sports', 'Education', 'Music', 'Cooking', 'Travel']
    for name in category_names:
        category, created = Category.objects.get_or_create(category_name=name)
        if created:
            print(f"Added category: {name}")
        else:
            print(f"Category already exists: {name}")

if __name__ == "__main__":
    populate_categories()
