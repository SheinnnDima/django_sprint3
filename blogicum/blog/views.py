from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post


def get_published_posts():
    now = timezone.now()
    return (
        Post.objects.select_related("author", "category", "location")
        .filter(
            pub_date__lte=now,
            is_published=True,
            category__is_published=True,
        )
        .order_by("-pub_date")
    )


def index(request):
    post_list = get_published_posts()[:5]
    return render(request, "blog/index.html", {"post_list": post_list})


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if not category.is_published:
        raise Http404
    post_list = get_published_posts().filter(category=category)
    return render(
        request,
        "blog/category.html",
        {
            "category": category,
            "post_list": post_list,
        },
    )


def post_detail(request, post_id):
    now = timezone.now()
    post = get_object_or_404(
        Post,
        pk=post_id,
        is_published=True,
        pub_date__lte=now,
        category__is_published=True,
    )
    return render(request, "blog/detail.html", {"post": post})
