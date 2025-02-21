from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from userincome.models import Source,UserIncome
from expenses.models import Category, Expense
from userpreferences.models import UserPreference
from django.utils import timezone
import json
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.contrib import messages
from django.db.models.functions import TruncMonth
from django.utils import timezone

# Create your views here.
@login_required(login_url='/authentication/login')
def index(request):
    current_month=timezone.now().month
    current_year=timezone.now().year

    total_expenses=Expense.objects.filter(owner=request.user, date__month=current_month,date__year=current_year).aggregate(total=Coalesce(Sum('amount'),0.0))
    total_income=UserIncome.objects.filter(owner=request.user,date__month=current_month,date__year=current_year).aggregate(total=Coalesce(Sum('amount'),0.0))
    currency = UserPreference.objects.filter(user=request.user).get(user=request.user).currency

    exp_category_totals=Expense.objects.filter(owner=request.user, date__month=current_month,date__year=current_year).values('category').annotate(total=Sum('amount'))
    
    categories=json.dumps([item['category'] for item in exp_category_totals])
    cat_amounts=json.dumps([item['total'] for item in exp_category_totals])

    monthly_expenses=Expense.objects.filter(owner=request.user,date__year=current_year).annotate(month=TruncMonth('date')).values('month').annotate(total_amount=Sum('amount')).order_by('month')
    monthly_income=UserIncome.objects.filter(owner=request.user,date__year=current_year).annotate(month=TruncMonth('date')).values('month').annotate(total_amount=Sum('amount')).order_by('month')
    
    exp_mon=json.dumps([expense['month'].strftime ("%m-%Y") for expense in monthly_expenses])
    monthly_exp_amount=json.dumps([expense['total_amount'] for expense in monthly_expenses])

    inc_mon=json.dumps([income['month'].strftime ("%m-%Y") for income in monthly_income])
    monthly_inc_amount=json.dumps([income['total_amount'] for income in monthly_income])

    context={
        'categories': categories,
        'cat_amounts':cat_amounts,
        'currency':currency,
        'total_expenses': total_expenses['total'],
        'total_income':total_income['total'],
        'inc_mon': inc_mon,
        'monthly_inc_amount': monthly_inc_amount,
        'monthly_exp_amount': monthly_exp_amount,
        'exp_mon': exp_mon,
    }

    if total_income['total'] < total_expenses['total']:
        messages.info(request,'Your expenditure is above income. Reduce expenditure and make follow ups on repayments !!')

    return render(request, 'dashboard.html',context)
