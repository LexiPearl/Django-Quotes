from django.shortcuts import render, redirect, HttpResponse
from datetime import datetime
from django.contrib import messages
from django.db.models import Count
from django.core.urlresolvers import reverse
from ..loginAndRegistration.models import User
from .models import Quote, FavoriteQuote

def existingUser(request):
    return 'name' in request.session

def dashboard(request):
    if not existingUser(request):
        return redirect(reverse("loginAndRegistration:index"))

    currUser=request.session['user_id']

    Favorites=FavoriteQuote.objects.filter(quote_favoriter_id=request.session['user_id'])
        #all of the quotes favorited by the current user

    nonFavorites= Quote.objects.all()
    for x in Favorites:
        nonFavorites=nonFavorites.exclude(id=x.quote_id.id)
        #all of the quotes except those favorited by the current user

    context={
        "currUser": currUser,
        "nonFavorites": nonFavorites,
        "Favorites":Favorites,
    }
    return render(request, "beltThreeApp/index.html", context)

def addQuote(request):
    if not existingUser(request):
        return redirect(reverse("loginAndRegistration:index"))
    postData={
        "speaker":request.POST['speaker'],
        "quote": request.POST['quote'],
        "user_id": request.session['user_id'],
    }
    print postData
    results=Quote.objects.add_quote(postData)
    if results[0]:
        for err in results[1]:
            messages.error(request,err)
        return redirect(reverse('beltThreeApp:dashboard'))
    return redirect(reverse("beltThreeApp:dashboard"))


def addFavorite(request, quote_id):
    if not existingUser(request):
        return redirect(reverse("loginAndRegistration:index"))
    postData={
        "quote_id":quote_id,
        "quote_favoriter":request.session['user_id']
    }
    print postData
    results=FavoriteQuote.objects.add_favorite(postData)
    return redirect(reverse("beltThreeApp:dashboard"))


def removeFavorite(request, quote_id):
    if not existingUser(request):
        return redirect(reverse("loginAndRegistration:index"))
    user_id=request.session['user_id']
    if FavoriteQuote.objects.filter(quote_id=quote_id, quote_favoriter=user_id).delete():
        return redirect (reverse("beltThreeApp:dashboard"))

def userInfo(request, user_id):
    if not existingUser(request):
        return redirect(reverse("loginAndRegistration:index"))
    user=User.objects.get(id=user_id)
    quotes=Quote.objects.filter(quoteAdder=user_id)
    numQuotes=len(quotes)
    context={
        "user":user,
        "quotes":quotes,
        "numQuotes":numQuotes,
    }
    return render(request,'beltThreeApp/posts.html',context)


def logout(request):
    if not existingUser(request):
        return redirect(reverse("loginAndRegistration:index"))
    request.session.pop('user_id')
    request.session.pop('name')
    request.session.pop('alias')
    return redirect(reverse("loginAndRegistration:index"))
