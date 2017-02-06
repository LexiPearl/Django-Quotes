from django.conf.urls import url
from views import dashboard, addFavorite, removeFavorite, addQuote, userInfo, logout
app_name= "beltThreeApp"
urlpatterns = [
    url(r'^$', dashboard, name='dashboard'),
    url(r'^addFavorite/(?P<quote_id>\d+)$', addFavorite, name='addFavorite'),
    url(r'^addQuote$', addQuote, name='addQuote'),
    url(r'^removeFavorite/(?P<quote_id>\d+)$', removeFavorite, name='removeFavorite'),
    url(r'^userInfo/(?P<user_id>\d+)$', userInfo, name='userInfo'),
    url(r'^logout$', logout, name='logout')
]
