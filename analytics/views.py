from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from userincome.models import Source,UserIncome
from expenses.models import Category, Expense
import json

# Create your views here.
@login_required(login_url='/authentication/login')
def analytics_stats(request):

    current_month=timezone.now().month
    current_year=timezone.now().year

    inc_source_totals=UserIncome.objects.filter(owner=request.user, date__month=current_month,date__year=current_year).values('source').annotate(total=Sum('amount'))
   
    inc_source=json.dumps([item['source'] for item in inc_source_totals])
    inc_amounts=json.dumps([item['total'] for item in inc_source_totals]) 

    daily_expenses=Expense.objects.filter(owner=request.user,date__month=current_month,date__year=current_year).annotate(day=TruncDay('date')).values('day').annotate(total_amount=Sum('amount')).order_by('day')
    daily_income=UserIncome.objects.filter(owner=request.user, date__month=current_month,date__year=current_year).annotate(day=TruncDay('date')).values('day').annotate(total_amount=Sum('amount')).order_by('day')

    exp_dates=json.dumps([expense['day'].strftime ("%d-%m") for expense in daily_expenses])
    daily_exp_amount=json.dumps([expense['total_amount'] for expense in daily_expenses])

    inc_dates=json.dumps([income['day'].strftime ("%d-%m") for income in daily_income])
    daily_inc_amount=json.dumps([income['total_amount'] for income in daily_income])

    exp_category_totals=Expense.objects.filter(owner=request.user, date__month=current_month,date__year=current_year).values('category').annotate(total=Sum('amount'))
    
    categories=json.dumps([item['category'] for item in exp_category_totals])
    cat_amounts=json.dumps([item['total'] for item in exp_category_totals])

    weekly_expenses=Expense.objects.filter(owner=request.user,date__month=current_month,date__year=current_year).annotate(week=TruncWeek('date')).values('week').annotate(total_amount=Sum('amount')).order_by('week')
    week_dates=json.dumps([expense['week'].strftime ("%d-%m") for expense in weekly_expenses])
    week_amounts=json.dumps([expense['total_amount'] for expense in weekly_expenses])
   
    weekly_income=UserIncome.objects.filter(owner=request.user,date__month=current_month,date__year=current_year).annotate(week=TruncWeek('date')).values('week').annotate(total_amount=Sum('amount')).order_by('week')
    week_inc_amounts=json.dumps([income['total_amount'] for income in weekly_income])
    context={
        'inc_source':inc_source,
        'inc_amounts': inc_amounts,
        'inc_dates': inc_dates,
        'daily_inc_amount': daily_inc_amount,
        'daily_exp_amount': daily_exp_amount,
        'exp_dates': exp_dates,
        'week_inc_amounts':week_inc_amounts,
        'categories': categories,
        'cat_amounts': cat_amounts,
        'week_dates': week_dates,
        'week_amounts': week_amounts
    }

    return render(request,'analytics.html', context)