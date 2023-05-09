from django.db.models import Sum
from django.shortcuts import render, redirect
from .models import Transaction, Investor, Stock
from .forms import RegisterTransaction
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
#modelo para realizar uma busca mais elaborada
from django.db.models import Q
from django.contrib import messages
from django.contrib.messages import constants


@login_required
def home(request):

    user = request.user
    if user.is_authenticated == False:
        return redirect('user_signin')
    else:
        transactions = Transaction.objects.filter(investor=user.id).order_by('-date_done')
        investor = Investor.objects.get(user=request.user)
    #busca operaões de compra e venda
        transacoes = Transaction.objects.filter(investor=investor)
#listar as ações do usuaro
        stocks =[]
        for transation in transacoes:
            if transation.stock not in stocks:
                stocks.append(transation.stock)

        context = {
            'user_loged':user,
            'transactions': transactions,
            'stocks': stocks
        }
        messages.add_message(request, constants.SUCCESS, "Logado com Sucesso!")
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


@login_required
def transaction_save(request):
    
    if request.method == 'GET':
        return render(request, 'my_wallet/transaction.html')
    
    elif request.method == "POST":
        stock_req = Stock.objects.get(pk=request.POST.get('stock'))
        investor = Investor.objects.get(user=request.user)
        date =request.POST.get('date_done')
        transaction = Transaction(
            date_done= date.timezone.strftime('%Y-%m-%d %H:%M:%S'), 
            stock= stock_req, 
            quantity_stock= int(request.POST.get('quantity_stock')), 
            unite_price= request.POST.get('unite_price').replace(',', '.'), 
            type_of=request.POST.get('type_of'), 
            brokerage= request.POST.get('brokerage').replace(',', '.'),
            investor = investor
        )
        investor = Investor.objects.get(user=request.user)
        transactions = Transaction.objects.filter(investor=investor).order_by('-date_done')
        context = {
            'user_loged': request.user,
            'transactions': transactions
        }
        transaction.save()
        messages.add_message(request, constants.SUCCESS, 'Transação salva com SUCESSO!')
        return render(request,'my_wallet/all_transactions.html', context=context)

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
    
    messages.add_message(request, constants.SUCCESS, 'Transação atualizada com SUCESSO!')
    return render(request, 'my_wallet/edit_transactions.html', context=context )

@login_required
def transaction_delete(request, transactiont_id):
    transaction = Transaction.objects.get(pk=transactiont_id)
    transaction.delete()
    messages.add_message(request, constants.ERROR, 'Trasação deletada com SUCESSO!')
    return redirect('transaction_all')

@login_required
def find_stock(request):
    stock_req = request.POST.get('stock')
    investor = Investor.objects.get(user=request.user)
    if stock_req:
        transactions_stock = Transaction.objects.filter(investor=investor).filter(Q(stock__code__istartswith=stock_req))
        context = {
        'transactions': transactions_stock,
        'user_loged': request.user
        }
        return render(request, 'my_wallet/all_transactions.html', context=context)
    else:
        
        return redirect('transaction_all')


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
