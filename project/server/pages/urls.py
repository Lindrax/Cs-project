from django.urls import path

from .views import homePageView, transferView, confirmView, htmlView, balanceView, accountView

urlpatterns = [
    path('', homePageView, name='home'),
    path('transfer/', transferView, name='transfer'),
    path('confirm/', confirmView, name='confirm'),
    path('html/', htmlView, name = 'html'),
    path('balance/', balanceView, name='balance'),
    path('accounts/', accountView, name='accounts')
    

]
