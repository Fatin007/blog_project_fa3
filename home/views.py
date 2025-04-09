from django.shortcuts import render, redirect
from posts.models import Post
from categories.models import Category
from django.core.paginator import Paginator
from django.db.models import Q
import requests

# Create your views here.
def get_random_hero_image():
    categories = Category.objects.all()
    category_names = [cat.name for cat in categories]
    query = ",".join(category_names)
    try:
        response = requests.get(
            "https://api.unsplash.com/photos/random",
            params={
                "query": query,
                "orientation": "landscape",
                "size": "regular",
                "client_id": "zm-9boI1TX8SSwK--qzFM4G1lDha48nbvCYP67g9VDA"
            }
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("urls", {}).get("regular")
    except Exception as e:
        print(f"Error fetching Unsplash image: {e}")
    
    return "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80"

def home(request, slug=None):
    posts = Post.objects.all().order_by('-created_at')
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | Q(body__icontains=search_query)
        )
    
    # Filter by category
    if slug is not None:
        category = Category.objects.get(slug=slug)
        posts = posts.filter(category=category)
    
    # Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page', 1)
    posts = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    header_image = get_random_hero_image()
    
    context = {
        'posts': posts,
        'categories': categories,
        'is_home': slug is None,
        'search_query': search_query,
        'header_image': header_image
    }
    
    return render(request, 'home.html', context)

def category_posts(request, slug):
    category = Category.objects.get(slug=slug)
    posts = Post.objects.filter(category=category).order_by('-created_at')
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    header_image = get_random_hero_image()
    
    context = {
        'posts': page_obj,
        'categories': categories,
        'is_home': False,
        'header_image': header_image
    }
    
    return render(request, 'home.html', context)