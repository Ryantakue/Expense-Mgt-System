from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns=[
    path('', views.index, name='expenses'),
    path('add-expense', views.add_expense, name="add-expenses"),
    path('edit-expense/<int:id>', views.expense_edit, name="expense-edit"),
    path('expense-delete/<int:id>', views.delete_expense, name="expense-delete"),
    path('expense_category_summary', views.expense_category_summary,
         name="expense_category_summary"),
    path('export_csv', views.export_csv,name="export_csv")
]