from django.db.models import Sum
from django.shortcuts import render, redirect
from .models import Transaction, Investor, Stock
from .forms import RegisterTransaction
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# mensagens de sucesso ou KeyError

@login_required
def home(request):
    user = request.user
    transactions = Transaction.objects.filter(investor=user.id).order_by('-date_done')
    investor = Investor.objects.get(user=user)
    total_stocks = Transaction.objects.filter(investor=investor).aggregate(total_stocks=Sum('quantity_stock'))
    context = {
        'user_loged':user,
        'transactions': transactions,
        'total_stocks': total_stocks['total_stocks'] if total_stocks['total_stocks'] is not None else 0,
    }
    if user.is_authenticated == False:
        return redirect('user_signin')
    else:
       return render(request, 'my_wallet/dahsboard.html', context=context)

@login_required
def transaction_new(request):
    investor = Investor.objects.get(user=request.user)
    stocks = Stock.objects.all()
    
    context = {
        'date_done': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        'investor': investor,
        'user_loged': request.user,
        'stocks': stocks,
        'types_transactions': Transaction.TYPE_OF_TRANSACTION
    }
    return render(request, 'my_wallet/transaction.html', context=context) 
# @login_required
# def transaction_save(request):
#     investor = Investor.objects.get(user=request.user)
#     form = RegisterTransaction(request.POST, instance=investor)
#     # trasaction = Transaction(date_done= form.data['date_done'], 
#     #                          stock= form.data['stock'], 
#     #                          quantity_stock= form.data['quantity_stock'], 
#     #                          unite_price= form.data['unite_price'], 
#     #                          type_of=form.data['type_of'], 
#     #                          brokerage=form.data['brokerage'],
#     #                          investor = investor)
#     if form.is_valid():
#         form.save()
#         print(f'{form.data}')
#         return redirect('home')
#     else:
#         return HttpResponse(f'{investor}---{form}')

@login_required
def transaction_save(request):
    
    stock_req = Stock.objects.get(pk=request.POST.get('stock'))
    investor = Investor.objects.get(user=request.user)
    transaction = Transaction(
        date_done= request.POST.get('date_done'), 
        stock= stock_req, 
        quantity_stock= int(request.POST.get('quantity_stock')), 
        unite_price= float(request.POST.get('unite_price')), 
        type_of=request.POST.get('type_of'), 
        brokerage= float(request.POST.get('brokerage')),
        investor = investor
    )
    context = {
        'user_loged': request.user,
    }
    transaction.save()
    return redirect('home')

@login_required
def transaction_all(request):
    investor = Investor.objects.get(user=request.user)
    transactions = Transaction.objects.filter(investor=investor).order_by('-date_done')
    context = {
        'transactions': transactions,
        'user_loged': request.user
    }
    return render(request, 'my_wallet/all_transactions.html', context=context)

@login_required
def transaction_detail(request, transactiont_id):
    transaction = Transaction.objects.get(pk=transactiont_id)
    context = {
        'transaction': transaction,
        'user_loged': request.user
    }
    return render(request, 'my_wallet/detail_transaction.html', context=context)

@login_required
def transaction_edit(request, transactiont_id):
    transaction = Transaction.objects.get(pk=transactiont_id)
    date_formated = transaction.date_done.strftime('%Y-%m-%d %H:%M:%S')
    unit_price = transaction.unite_price
    quantity_stock = int(transaction.quantity_stock)
    brokerage = transaction.brokerage
    context = {
        'transaction': transaction,
        'date_formated':date_formated,
        'user_loged': request.user,
        'unit_price': unit_price,
        'quantity_stock': quantity_stock,
        'brokerage': brokerage
    }
    return render(request, 'my_wallet/edit_transactions.html', context=context )

@login_required
def transaction_delete(request, transactiont_id):
    transaction = Transaction.objects.get(pk=transactiont_id)
    transaction.delete()

    return redirect('transaction_all')
