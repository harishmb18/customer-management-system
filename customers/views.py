from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
import csv
from django.http import HttpResponse
from .models import Customer, ActivityLog
from .forms import CustomerForm


@login_required
def customer_list(request):

    query = request.GET.get("q")
    status_filter = request.GET.get("status")

    customers = Customer.objects.filter(created_by=request.user)

    if query:
        customers = customers.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(company__icontains=query)
        )

    if status_filter:
        customers = customers.filter(status=status_filter)

    paginator = Paginator(customers, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "customers/customer_list.html", {
        "page_obj": page_obj,
        "query": query
    })


@login_required
def add_customer(request):

    if request.method == "POST":

        form = CustomerForm(request.POST)

        if form.is_valid():

            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.save()

            ActivityLog.objects.create(
                user=request.user,
                customer=customer,
                action="Created Customer"
            )

            return redirect("customer_list")

    else:
        form = CustomerForm()

    return render(request, "customers/add_customer.html", {"form": form})


@login_required
def edit_customer(request, id):

    customer = get_object_or_404(Customer, id=id, created_by=request.user)

    if request.method == "POST":

        form = CustomerForm(request.POST, instance=customer)

        if form.is_valid():
            form.save()

            ActivityLog.objects.create(
                user=request.user,
                customer=customer,
                action="Updated Customer"
            )

            return redirect("customer_list")

    else:
        form = CustomerForm(instance=customer)

    return render(request, "customers/edit_customer.html", {"form": form})


@login_required
def delete_customer(request, id):

    customer = get_object_or_404(Customer, id=id, created_by=request.user)

    ActivityLog.objects.create(
        user=request.user,
        customer=customer,
        action="Deleted Customer"
    )

    customer.delete()

    return redirect("customer_list")


@login_required
def dashboard(request):

    total_customers = Customer.objects.filter(created_by=request.user).count()

    active_customers = Customer.objects.filter(
        created_by=request.user,
        status="active"
    ).count()

    last_month = timezone.now() - timedelta(days=30)

    new_customers = Customer.objects.filter(
        created_by=request.user,
        created_at__gte=last_month
    ).count()

    return render(request, "dashboard/dashboard.html", {
        "total_customers": total_customers,
        "active_customers": active_customers,
        "new_customers": new_customers
    })


@login_required
def export_customers(request):

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="customers.csv"'

    writer = csv.writer(response)

    writer.writerow([
        "Name",
        "Email",
        "Phone",
        "Company",
        "Status"
    ])

    customers = Customer.objects.filter(created_by=request.user)

    for customer in customers:

        writer.writerow([
            customer.name,
            customer.email,
            customer.phone,
            customer.company,
            customer.status
        ])

    return response