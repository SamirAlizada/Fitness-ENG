from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import StudentForm, TrainerForm, BarForm, BarSoldForm, TariffsForm
from .models import Student, Trainer, Bar, BarSold, Tariffs
from django.contrib import messages
from datetime import datetime, date, timedelta
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.db.models import Sum, F, FloatField
from django.db.models.functions import Cast

# Add
def add_tariffs(request):
    if request.method == 'POST':
        form = TariffsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tariff added successfully.')
            return redirect('add_tariffs')
        else:
            messages.error(request, 'There are errors in the form. Please fix it.')
    else:
        form = TariffsForm()
    
    return render(request, 'tariffs/add_tariffs.html', {'form': form})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member added successfully.')
            return redirect('add_student') 
    else:
        form = StudentForm()
    return render(request, 'student/add_student.html', {'form': form})

def add_trainer(request):
    if request.method == 'POST':
        form = TrainerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Trainer added successfully.')
            return redirect('add_trainer') 
    else:
        form = TrainerForm()
    return render(request, 'trainer/add_trainer.html', {'form': form})

def add_bar(request):
    if request.method == 'POST':
        form = BarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('add_bar') 
    else:
        form = BarForm()
    return render(request, 'bar/add_bar.html', {'form': form})

def add_bar_sold(request):
    if request.method == 'POST':
        form = BarSoldForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sold product added successfully.')
            return redirect('add_bar_sold')
    else:
        form = BarSoldForm()
    return render(request, 'soldBar/add_bar_sold.html', {'form': form})
# ----------------------------------------------------------------

#List of classes
def trainer_list(request):
    trainers = Trainer.objects.all()

    query = request.GET.get('q')
    if query:
        trainers = trainers.filter(full_name__icontains=query)

    return render(request, 'trainer/trainer_list.html', {'trainers': trainers})

def student_list(request):
    today = date.today()
    
    # Retrieve the search query
    query = request.GET.get('q')
    
    # Get all students or filter based on the search query
    students = Student.objects.all()
    if query:
        students = students.filter(full_name__icontains=query)

    # Dictionary to group students by month
    grouped_students_dict = {}

    # Grouping students by month key and calculating monthly total payments
    for student in students:
        # Create month and year key from the registration date
        month_key = student.registration_date.strftime('%Y-%m')
        month_display = student.registration_date.strftime('%B %Y')

        # Group by month key
        if month_key not in grouped_students_dict:
            grouped_students_dict[month_key] = {
                'display': month_display,
                'students': [],
                'total_payment': 0  # Track total monthly payments
            }

        # Add the student to the corresponding month's group
        grouped_students_dict[month_key]['students'].append(student)

        # Add the student's payment to the total payment for the month
        grouped_students_dict[month_key]['total_payment'] += student.payment

    # Convert dictionary to a list and sort by key in descending order
    sorted_grouped_students_list = sorted(
        grouped_students_dict.items(),
        key=lambda x: x[0],
        reverse=True
    )

    # Convert sorted list back to dictionary
    sorted_grouped_students_dict = {
        item[1]['display']: {
            'students': item[1]['students'],
            'total_payment': item[1]['total_payment']
        }
        for item in sorted_grouped_students_list
    }

    # Filter students whose end_date is within one week from today
    students_near_end_date = students.filter(
        end_date__range=(today, today + timedelta(days=7))
    ).order_by('end_date')  # Sort by end_date in ascending order

    # Pass the data to the template
    return render(request, 'student/student_list.html', {
        'grouped_students': sorted_grouped_students_dict,
        'today': today,
        'students_near_end_date': students_near_end_date,
    })

def get_english_date(date):
    months = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
        7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    days = {
        'Monday': 'Monday', 'Tuesday': 'Tuesday', 'Wednesday': 'Wednesday',
        'Thursday': 'Thursday', 'Friday': 'Friday', 'Saturday': 'Saturday', 'Sunday': 'Sunday'
    }
    day = date.strftime('%A')
    month = date.month
    return f"{date.day} {months[month]} {days[day]}"

def daily_student_list(request):
    now = datetime.now()
    today = now.date()

    students = Student.objects.filter(end_date=today, is_renewed=False).exclude(tariffs__type='Günlük')

    query = request.GET.get('q')
    if query:
        students = students.filter(full_name__icontains=query)

    english_today = get_english_date(today)

    return render(request, 'student/daily_student_list.html', {'students': students, 'today': english_today})

def bar_list(request):
    bars = Bar.objects.all()

    query = request.GET.get('q')
    if query:
        bars = bars.filter(product_name__icontains=query)

    return render(request, 'bar/bar_list.html', {'bars': bars})

def bar_sold_list(request):
    today = date.today()

    # Retrieve the search query
    query = request.GET.get('q')

    # Get all bar_solds or filter based on the search query
    bar_solds = BarSold.objects.all()
    
    if query:
        bar_solds = bar_solds.filter(product_name__name__icontains=query)


    # Create a dictionary for grouping bar_solds by month
    grouped_bar_solds_dict = {}
    for bar_sold in bar_solds:
        # Extract month and year from `date`
        month_key = bar_sold.date.strftime('%Y-%m')
        month_display = bar_sold.date.strftime('%B %Y')

        # Calculate the sale amount for the bar_sold
        sale_amount = bar_sold.count * bar_sold.price

        # Group bar_solds by year-month key
        if month_key not in grouped_bar_solds_dict:
            grouped_bar_solds_dict[month_key] = {
                'display': month_display,
                'bar_solds': [],
                'total_sales': 0  # Initialize total monthly sales
            }

        # Add the bar_sold to the corresponding month's group
        grouped_bar_solds_dict[month_key]['bar_solds'].append(bar_sold)

        # Add the bar_sold's sale amount to the total sales for the month
        grouped_bar_solds_dict[month_key]['total_sales'] += sale_amount

    # Convert the dictionary to a list of tuples for sorting
    sorted_grouped_bar_solds_list = sorted(
        grouped_bar_solds_dict.items(),
        key=lambda x: x[0],
        reverse=True
    )

    # Convert the sorted list back to a dictionary
    sorted_grouped_bar_solds_dict = {
        item[1]['display']: {
            'bar_solds': item[1]['bar_solds'],
            'total_sales': item[1]['total_sales']
        }
        for item in sorted_grouped_bar_solds_list
    }

    # Pass the `grouped_bar_solds` data to the `bar_sold_list.html` template
    return render(request, 'soldBar/bar_sold_list.html', {
        'grouped_bar_solds': sorted_grouped_bar_solds_dict,
        'today': today,
    })
# ----------------------------------------------------------------

# Update
def update_trainer(request, pk):
    trainer = get_object_or_404(Trainer, pk=pk)
    form = TrainerForm(instance=trainer)
    if request.method == 'POST':
        form = TrainerForm(request.POST, instance=trainer)
        if form.is_valid():
            form.save()
            return redirect('trainer_panel')
    return render(request, 'trainer/update_trainer.html', {'form': form})

def update_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(instance=student)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_panel')
    return render(request, 'student/update_student.html', {'form': form})

def update_bar(request, pk):
    bar = get_object_or_404(Bar, pk=pk)
    form = BarForm(instance=bar)
    if request.method == 'POST':
        form = BarForm(request.POST, instance=bar)
        if form.is_valid():
            form.save()
            return redirect('bar_panel')
    return render(request, 'bar/update_bar.html', {'form': form})

def update_bar_sold(request, pk):
    bar_sold = get_object_or_404(BarSold, pk=pk)
    form = BarSoldForm(instance=bar_sold)
    if request.method == 'POST':
        form = BarSoldForm(request.POST, instance=bar_sold)
        if form.is_valid():
            form.save()
            return redirect('bar_sold_panel')
    return render(request, 'soldBar/update_bar_sold.html', {'form': form})

def update_tariffs(request, pk):
    tariffs = get_object_or_404(Tariffs, pk=pk)
    form = TariffsForm(instance=tariffs)
    if request.method == 'POST':
        form = TariffsForm(request.POST, instance=tariffs)
        if form.is_valid():
            form.save()
            return redirect('tariffs_panel')
    return render(request, 'tariffs/update_tariffs.html', {'form': form})
# ----------------------------------------------------------------

# Delete
def delete_trainer(request, pk):
    trainer = Trainer.objects.get(pk=pk)
    trainer.delete()
    return redirect('trainer/trainer_panel')

def delete_student(request, pk):
    student = Student.objects.get(pk=pk)
    student.delete()
    return redirect('student_panel')

def delete_bar(request, pk):
    bar = Bar.objects.get(pk=pk)
    bar.delete()
    return redirect('bar_panel')

def delete_bar_sold(request, pk):
    bar_sold = BarSold.objects.get(pk=pk)
    bar_sold.delete()
    return redirect('bar_sold_panel')

def delete_tariffs(request, pk):
    tariffs = Tariffs.objects.get(pk=pk)
    tariffs.delete()
    return redirect('tariffs_panel')
# ----------------------------------------------------------------

# Panel
def trainer_panel(request):
    trainers = Trainer.objects.all()

    query = request.GET.get('q')
    if query:
        trainers = trainers.filter(full_name__icontains=query)

    return render(request, 'trainer/trainer_panel.html', {'trainers': trainers})

def student_panel(request):
    today = date.today()

    query = request.GET.get('q')

    students = Student.objects.all()

    if query:
        students = students.filter(full_name__icontains=query)

    # Create a dictionary for grouping students by month
    grouped_students_dict = {}
    for student in students:
        # Extract month and year from `registration_date`
        month_key = student.registration_date.strftime('%Y-%m')
        month_display = student.registration_date.strftime('%B %Y')
        # Group students by year-month key
        if month_key not in grouped_students_dict:
            grouped_students_dict[month_key] = {
                'display': month_display,
                'students': [],
                'total_payment': 0  # Track total monthly payments
            }
        
        # Add the student to the corresponding month's group
        grouped_students_dict[month_key]['students'].append(student)

        # Add the student's payment to the total payment for the month
        grouped_students_dict[month_key]['total_payment'] += student.payment

    # Convert the dictionary to a list of tuples for sorting
    sorted_grouped_students_list = sorted(
        grouped_students_dict.items(),
        key=lambda x: x[0],
        reverse=True
    )

    # Convert sorted list back to dictionary
    sorted_grouped_students_dict = {
        item[1]['display']: {
            'students': item[1]['students'],
            'total_payment': item[1]['total_payment']
        }
        for item in sorted_grouped_students_list
    }

    # Pass the `grouped_students` data to the `student_list.html` template
    return render(request, 'student/student_panel.html', {
        'grouped_students': sorted_grouped_students_dict,
        'today': today})

def bar_panel(request):
    bars = Bar.objects.all()

    query = request.GET.get('q')
    if query:
        bars = bars.filter(product_name__icontains=query)

    return render(request, 'bar/bar_panel.html', {'bars': bars})

def bar_sold_panel(request):
    today = date.today()

    # Retrieve the search query
    query = request.GET.get('q')

    # Get all bar_solds or filter based on the search query
    bar_solds = BarSold.objects.all()

    if query:
        bar_solds = bar_solds.filter(product_name__icontains=query)

    # Create a dictionary for grouping bar_solds by month
    grouped_bar_solds_dict = {}
    for bar_sold in bar_solds:
        # Extract month and year from `date`
        month_key = bar_sold.date.strftime('%Y-%m')
        month_display = bar_sold.date.strftime('%B %Y')

        # Calculate the sale amount for the bar_sold
        sale_amount = bar_sold.count * bar_sold.price

        # Group bar_solds by year-month key
        if month_key not in grouped_bar_solds_dict:
            grouped_bar_solds_dict[month_key] = {
                'display': month_display,
                'bar_solds': [],
                'total_sales': 0  # Initialize total monthly sales
            }

        # Add the bar_sold to the corresponding month's group
        grouped_bar_solds_dict[month_key]['bar_solds'].append(bar_sold)

        # Add the bar_sold's sale amount to the total sales for the month
        grouped_bar_solds_dict[month_key]['total_sales'] += sale_amount

    # Convert the dictionary to a list of tuples for sorting
    sorted_grouped_bar_solds_list = sorted(
        grouped_bar_solds_dict.items(),
        key=lambda x: x[0],
        reverse=True
    )

    # Convert the sorted list back to a dictionary
    sorted_grouped_bar_solds_dict = {
        item[1]['display']: {
            'bar_solds': item[1]['bar_solds'],
            'total_sales': item[1]['total_sales']
        }
        for item in sorted_grouped_bar_solds_list
    }

    # Pass the `grouped_bar_solds` data to the `bar_sold_panel.html` template
    return render(request, 'soldBar/bar_sold_panel.html', {
        'grouped_bar_solds': sorted_grouped_bar_solds_dict,
        'today': today,
    })

def tariffs_panel(request):
    tariffs = Tariffs.objects.all().order_by('price')
    return render(request, 'tariffs/tariffs_panel.html', {'tariffs': tariffs})
# ----------------------------------------------------------------

# User
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('student_list')
        else:
            messages.error(request, 'Username or password is incorrect.')
    return render(request, 'account/login.html')

def user_logout(request):
    logout(request)
    return redirect('student_list')
# ----------------------------------------------------------------

def renew_student(request, student_id):
    # Find the relevant student
    student = get_object_or_404(Student, id=student_id)
    
    # Create a new student object with the same attributes
    new_student = Student(
        full_name=student.full_name,
        registration_date=timezone.now(),
        tariffs=student.tariffs,
        trainer=student.trainer,
        payment=student.payment,
        # Assuming the duration field is in months
        end_date=timezone.now() + relativedelta(months=student.tariffs.month_duration)
    )
    
    # Save the new student object
    new_student.save()

    # Mark the old student as renewed
    student.is_renewed = True
    student.save()

    # Redirect to an updated student related page or listing page
    return redirect('student_panel')
# ----------------------------------------------------------------

# Operations
def increase_stock(request, bar_id):
    bar = get_object_or_404(Bar, pk=bar_id)
    bar.stock_number += 1
    bar.save()
    return redirect('bar_panel')

def decrease_stock(request, bar_id):
    bar = get_object_or_404(Bar, pk=bar_id)
    # to check before reducing stock_number
    # you can add any stock control (for example, negative value prevention).
    if bar.stock_number > 0:
        bar.stock_number -= 1
        bar.save()
    return redirect('bar_panel')

def increase_sold(request, pk):
    bar_sold = get_object_or_404(BarSold, pk=pk)
    bar_sold.count += 1
    bar_sold.save()
    return redirect('bar_sold_panel')

def decrease_sold(request, pk):
    bar_sold = get_object_or_404(BarSold, pk=pk)
    # to check before reducing count
    # you can add any count control (for example, negative value prevention).
    if bar_sold.count > 0:
        bar_sold.count -= 1
        bar_sold.save()
    return redirect('bar_sold_panel')
# ----------------------------------------------------------------

# Charts
def student_monthly_payments(selected_year):
    student_monthly_payments_data = (
        Student.objects.filter(registration_date__year=selected_year)
        .annotate(month=Cast('registration_date__month', FloatField()))
        .values('month')
        .annotate(total_payment=Sum('payment', output_field=FloatField()))
        .order_by('month')
    )

    months_en = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    student_labels = [months_en[int(entry['month']) - 1] for entry in student_monthly_payments_data]
    total_payments = [entry['total_payment'] for entry in student_monthly_payments_data]

    return student_labels, total_payments

def sales_chart(request):
    years = BarSold.objects.dates('date', 'year')
    years = [year.year for year in years]

    selected_year = request.GET.get('year', date.today().year)

    sales_data = (
        BarSold.objects.filter(date__year=selected_year)
        .annotate(month=Cast('date__month', FloatField()))
        .values('month')
        .annotate(total_sales=Sum(F('count') * F('price'), output_field=FloatField()))
        .order_by('month')
    )

    months_en = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    labels = [months_en[int(entry['month']) - 1] for entry in sales_data]
    total_sales = [entry['total_sales'] for entry in sales_data]

    context = {
        "years": years,
        "selected_year": int(selected_year),
        "labels": labels,
        "total_sales": total_sales,
    }

    return context

def price_comparison_chart(request):
    # Get the current year
    current_year = date.today().year

    # Get the earliest year from the Bar and BarSold data
    first_bar_year = Bar.objects.earliest('date').date.year if Bar.objects.exists() else current_year
    first_bar_sold_year = BarSold.objects.earliest('date').date.year if BarSold.objects.exists() else current_year
    start_year = min(first_bar_year, first_bar_sold_year)

    # Get all years from the data starting from the earliest year
    years = range(start_year, current_year + 1)

    months = [
        {'value': 1, 'name': 'January'},
        {'value': 2, 'name': 'February'},
        {'value': 3, 'name': 'March'},
        {'value': 4, 'name': 'April'},
        {'value': 5, 'name': 'May'},
        {'value': 6, 'name': 'June'},
        {'value': 7, 'name': 'July'},
        {'value': 8, 'name': 'August'},
        {'value': 9, 'name': 'September'},
        {'value': 10, 'name': 'October'},
        {'value': 11, 'name': 'November'},
        {'value': 12, 'name': 'December'},
    ]

    # Get selected year and month from the request or use the current year and month
    selected_year = int(request.GET.get('year', current_year))
    selected_month = int(request.GET.get('month', date.today().month))
    
    # Get the student payments for the selected year
    student_labels, monthly_payments = student_monthly_payments(selected_year)

    # Get the payment for the selected month
    selected_month_payment = monthly_payments[selected_month - 1] if selected_month <= len(monthly_payments) else 0

    # Calculate the total cost (Bar prices * stock_number) for the selected month and year
    total_cost = sum(bar.price * bar.stock_number for bar in Bar.objects.filter(date__year=selected_year, date__month=selected_month))

    # Calculate the total income (BarSold prices * count) for the selected month and year
    total_income = sum(bar_sold.price * bar_sold.count for bar_sold in BarSold.objects.filter(date__year=selected_year, date__month=selected_month)) + selected_month_payment

    # Calculate the total price difference including payments
    total_price_difference = total_income - total_cost

    context = {
        "years": years,
        "months": months,
        "selected_year": selected_year,
        "selected_month": selected_month,
        "total_cost": total_cost,
        "total_income": total_income,
        "total_price_difference": total_price_difference,
        "selected_month_payment": selected_month_payment,
    }

    return context

def combined_charts_view(request):
    sales_context = sales_chart(request)
    price_comparison_context = price_comparison_chart(request)

    selected_year = int(request.GET.get('year', date.today().year))
    student_labels, total_payments = student_monthly_payments(selected_year)

    context = {
        **sales_context,
        **price_comparison_context,
        "student_labels": student_labels,
        "total_payments": total_payments,
    }

    return render(request, 'charts.html', context)
