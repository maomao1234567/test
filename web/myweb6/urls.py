from django.conf.urls import url
from django.contrib import admin
from myweb6 import views
myweb6 = 'myweb6'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/(.*?)$', views.book_page, name='book_page'),
    url(r'^$', views.hh, name='pyecharts')

]
