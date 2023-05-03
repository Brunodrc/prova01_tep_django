from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('transaction_new/', views.transaction_new, name='transaction_new'),
    path('transaction_save/', views.transaction_save, name='transaction_save'),
    path('transaction_detail/<int:transactiont_id>/', views.transaction_detail, name='transaction_detail'),
    path('transaction_delete/<int:transactiont_id>/', views.transaction_delete, name='transaction_delete'),
    path('transaction_edit/<int:transactiont_id>/', views.transaction_edit, name='transaction_edit'),
    path('find_stock/', views.find_stock, name='find_stock'),
    path('transaction_all/', views.transaction_all, name='transaction_all'),
]