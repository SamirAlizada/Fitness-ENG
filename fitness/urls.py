from django.urls import path
from .views import *

urlpatterns = [
    # Add
    path('add-student/', add_student, name='add_student'),
    path('add-trainer/', add_trainer, name='add_trainer'),
    path('add-tariffs/', add_tariffs, name='add_tariffs'),
    path('add-bar/', add_bar, name='add_bar'),
    path('add-bar-sold/', add_bar_sold, name='add_bar_sold'),

    # List
    path('trainer-list/', trainer_list, name='trainer_list'),
    path('', student_list, name='student_list'),
    path('bar-list/', bar_list, name='bar_list'),
    path('bar-sold-list/', bar_sold_list, name='bar_sold_list'),
    path('daily-student-list/', daily_student_list, name='daily_student_list'),

    # Panel
    path('trainer-panel/', trainer_panel, name='trainer_panel'),
    path('student-panel/', student_panel, name='student_panel'),
    path('bar-panel/', bar_panel, name='bar_panel'),
    path('bar-sold-panel/', bar_sold_panel, name='bar_sold_panel'),
    path('tariffs-panel/', tariffs_panel, name='tariffs_panel'),

    # Delete
    path('delete-trainer/<int:pk>/', delete_trainer, name='delete_trainer'),
    path('delete-student/<int:pk>/', delete_student, name='delete_student'),
    path('delete-bar/<int:pk>/', delete_bar, name='delete_bar'),
    path('delete-bar-sold/<int:pk>/', delete_bar_sold, name='delete_bar_sold'),
    path('delete-tariffs/<int:pk>/', delete_tariffs, name='delete_tariffs'),

    #Update
    path('update-trainer/<int:pk>/', update_trainer, name='update_trainer'),
    path('update-student/<int:pk>/', update_student, name='update_student'),
    path('update-bar/<int:pk>/', update_bar, name='update_bar'),
    path('update-bar-sold/<int:pk>/', update_bar_sold, name='update_bar_sold'),
    path('update-tariffs/<int:pk>/', update_tariffs, name='update_tariffs'),

    # Account
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('renew-student/<int:student_id>/', renew_student, name='renew_student'),
    path('increase/<int:bar_id>/', increase_stock, name='increase_stock'),
    path('decrease/<int:bar_id>/', decrease_stock, name='decrease_stock'),

    path('bar-sold-increase/<int:pk>/', increase_sold, name='increase_sold'),
    path('bar-sold-decrease/<int:pk>/', decrease_sold, name='decrease_sold'),

    path('charts/', combined_charts_view, name='charts'),


]