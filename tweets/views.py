import random

from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url

from .models import Tweet
from .forms import TweetForm

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)

def tweet_create_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = TweetForm(request.POST or None)
        next_url = request.POST.get("next") or None
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            if request.is_ajax():
                return JsonResponse(obj.serialize(), status=201)

            if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
                return redirect(next_url)

            #do more form related logic here
        if form.errors:
            if request.is_ajax():
                return JsonResponse(form.errors, status=400)
        return render(request, 'components/forms.html', context={"form": form})

def tweet_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript
    Return JSON data
    """
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list,
    }
    return JsonResponse(data)

def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript
    Return JSON data
    """
    data = {
        "id": tweet_id,
    }

    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content

    except:
        data['message'] = "Not Found"
        status = 404

    return JsonResponse(data, status=status)