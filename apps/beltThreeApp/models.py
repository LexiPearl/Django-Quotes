from __future__ import unicode_literals
from django.db import models
from ..loginAndRegistration.models import User

class QuoteManager(models.Manager):
    def add_quote(self, postData):
        flag=False
        errors=[]
        if len(postData['speaker'])<3:
            flag=True
            errors.append("Quoted by must be at least three characters!")
        if len(postData['quote'])<10:
            flag=True
            errors.append("Quote must be at least ten characters!")
        if not flag:
            addQuote=Quote.objects.create(quote=postData['quote'], speaker=postData['speaker'], quoteAdder_id=postData['user_id'])
            return(flag, addQuote)
        return (flag, errors)

class FavoriteManager(models.Manager):
    def add_favorite(self, postData):
        addFavorite=FavoriteQuote.objects.create(quote_favoriter_id=postData['quote_favoriter'],quote_id_id=postData['quote_id'])
        return(addFavorite)
    # def remove_favorite(self, postData):
    #     removeFavorite=FavoriteQuote.objects.delete(
    #     )
    #     return (removeFavorite)

class Quote(models.Model):
    quote=models.CharField(max_length=500)
    speaker=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add =True)
    updated_at=models.DateTimeField(auto_now =True)
    quoteAdder=models.ForeignKey(User, related_name="quoteAdder")
    objects=QuoteManager()

class FavoriteQuote(models.Model):
    quote_id=models.ForeignKey(Quote, related_name="quoteId")
    quote_favoriter=models.ForeignKey(User, related_name="quoteFavoriter")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=FavoriteManager()
