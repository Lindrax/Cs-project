from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Account
from django.db import connection
from django.core import serializers
from django.contrib.auth.decorators import user_passes_test



@login_required
def confirmView(request):
	amount = request.session['amount']
	to_username = request.session['to']
	with connection.cursor() as cursor:
			cursor.execute(f"SELECT id FROM auth_user WHERE username = '{to_username}'")
			to_user_id = cursor.fetchone()[0]
	with connection.cursor() as cursor:
			cursor.executescript(f"UPDATE pages_account SET balance = balance + {amount} WHERE user_id = {to_user_id}")
	request.user.account.balance -= int(amount)
	request.user.account.save()

	#fixed query
	"""amount = request.session['amount']
	to = User.objects.get(username=request.session['to'])

	request.user.account.balance -= amount
	to.account.balance += amount

	request.user.account.save()
	to.account.save()"""

	return redirect('/')

#@login_required
def balanceView(request):
	if request.user.is_authenticated:
		return JsonResponse({'username': request.user.username, 'balance': request.user.account.balance})
	else:
		return JsonResponse({'username': 'anonymous', 'balance': 0})

#@user_passes_test(lambda u: u.is_superuser)
@login_required
def accountView(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM pages_account")
        accounts = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        accounts_list = [dict(zip(columns, account)) for account in accounts]

    return JsonResponse({'accounts': accounts_list})

@login_required
def transferView(request):
	request.session['to'] = request.GET.get('to')
	request.session['amount'] = request.GET.get('amount')
	return render(request, 'pages/confirm.html')


@login_required
def homePageView(request):
	accounts = Account.objects.exclude(user_id=request.user.id)
	return render(request, 'pages/index.html', {'accounts': accounts})

def htmlView(request):
	return render(request, 'pages/csrf.html')
