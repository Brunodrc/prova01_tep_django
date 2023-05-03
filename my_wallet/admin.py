from django.contrib import admin
from .models import Investor, Stock, Transaction

admin.site.register([Investor, Stock, Transaction])

"""
user: adminwall
password: 20231234
"""