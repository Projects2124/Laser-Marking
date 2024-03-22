from django.shortcuts import render
from django.shortcuts import redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout 
from django.urls import reverse
from .models import lm_tbl,part_tbl,running_part_tbl
from .forms import PartForm
from django.db import connection
from django.db import IntegrityError
from datetime import datetime

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('data_screen')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def Part(request):
    data = {index + 1: item for index, item in enumerate(part_tbl.objects.all().order_by('-id'))}
    # Create an instance of the PLATFORM form.
    form = PartForm()

    # Check if the request method is POST.
    if request.method == 'POST':
        # Bind the form with the POST data.
        form = PartForm(request.POST)
        # Check if the form data is valid.
        if form.is_valid():
            # Get the ID of the record from the POST data.
            record_id = request.POST.get('record_id')
            # If a record ID is provided, get the corresponding Platform object from the database.
            if record_id:
                record = get_object_or_404(part_tbl, pk=record_id)
                # Bind the form with the instance of the Platform object.
                form = PartForm(request.POST, instance=record)
            # Save the form data to the database.
            form.save()
            # Redirect to the PlatForm view after saving.
            return redirect('Part')
    
    # Render the PlatForm.html template with the form and data.
    return render(request, 'PartName.html', {'form': form, 'data': data})

# Define a view function for editing an existing platform record.
def Part_edit(request, pk):
    # Get the Platform record with the given primary key (pk) from the database.
    record = get_object_or_404(part_tbl, pk=pk)

    # Check if the request method is POST.
    if request.method == 'POST':
        # Bind the form with the POST data and the instance of the Platform object to be edited.
        form = PartForm(request.POST, instance=record)
        # Check if the form data is valid.
        if form.is_valid():
            # Save the updated form data to the database.
            form.save()
            # Redirect to the PlatForm view after saving.
            return redirect('Part')

    # If the request method is GET, create a form instance with the Platform object to be edited.
    else:
        form = PartForm(instance=record)

    # Render the PlatForm.html template with the form and additional context for editing.
    return render(request, 'PartName.html', {'form': form, 'record_id': pk, 'edit_Part_open': True})

# Define a view function for deleting a platform record.
def Part_delete(request, pk):
    # Get the Platform record with the given primary key (pk) from the database.
    record = get_object_or_404(part_tbl, pk=pk)
    # Delete the retrieved Platform record from the database.
    record.delete()
    # Redirect to the PlatForm view after deleting.
    return redirect('Part')

    return render(request,'PartName.html')  


def data_screen(request):
    parts = part_tbl.objects.all()
    default_part = parts.first().PartName  # Assuming the default part is the first one in the database

    selected_part_name = default_part  # Set the default part as the selected part name

    # Fetch data from lm_tbl based on the selected part's PartName using raw SQL query
    with connection.cursor() as cursor:
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("SELECT PartName, QR_Code, DATE_FORMAT(time_stamp, '%%d-%%m-%%Y'), TIME_FORMAT(time_stamp, '%%H:%%i:%%s') FROM rpa_lm_tbl WHERE PartName = %s AND time_stamp <= %s ORDER BY time_stamp DESC LIMIT 10", [selected_part_name, current_timestamp])
        data = cursor.fetchall()
        # Convert the fetched data to the desired format
        formatted_data = [(part_name, qr_code, f"{date} {time}") for part_name, qr_code, date, time in data]

    return render(request, 'DataScreen.html', {'parts': parts, 'selected_part_name': selected_part_name, 'selected_part_data': formatted_data})


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


