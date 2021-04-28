import csv

from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.views.generic import ListView, DetailView, TemplateView
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from profiles.models import Profile
from sales.models import Sale, Position, CSV
from products.models import Product
from customers.models import Customer

from .models import Report
from .forms import ReportForm
from .utils import get_report_image

from xhtml2pdf import pisa

class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'reports/main.html'


class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'reports/detail.html'

class UploadTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/from_file.html'

@login_required
def csv_upload_view(request):
    if request.method == 'POST':
        csv_file_name = request.FILES.get('file').name
        csv_file = request.FILES.get('file')
        obj, created = CSV.objects.get_or_create(file_name=csv_file_name)

        if created:
            obj.csv_file = csv_file
            obj.save()
            with open(obj.csv_file.path, 'r') as f:
                reader = csv.reader(f)
                reader.__next__()
                for row in reader:
                    
                    row.pop()
                    
                    transaction_id = row[1]
                    product = row[2]
                    quantity = int(row[3])
                    customer = row[4]
                    date = parse_date(row[5])

                    try:
                        product_obj = Product.objects.get(name__iexact=product)
                    except Product.DoesNotExist:
                        product_obj = None

                    if product_obj is not None:
                        customer_obj, _ = Customer.objects.get_or_create(name=customer)
                        salesman_obj = Profile.objects.get(user=request.user)
                        position_obj = Position.objects.create(product=product_obj, quantity=quantity, created_at=date)

                        sale_obj, _ = Sale.objects.get_or_create(transaction_id=transaction_id, customer=customer_obj, salesman=salesman_obj, created_at=date)
                        sale_obj.positions.add(position_obj)
                        sale_obj.save()

                return JsonResponse({'ex': False})

        return JsonResponse({'ex': True})

    return HttpResponse()


"""
def create_report_view(request):
    if request.is_ajax():
        
        name = request.POST.get('name')
        remarks = request.POST.get('remarks')
        image = request.POST.get('image')

        img = get_report_image(image)

        author = Profile.objects.get(user=request.user)
        Report.objects.create(name=name, remarks=remarks, image=img, author=author)
        return JsonResponse({'msg': 'send'})
    return JsonResponse({'msg': 'not ajax'})
"""
@login_required
def create_report_view(request):
    form = ReportForm(request.POST or None)
    if request.is_ajax():

        image = request.POST.get('image')
        img = get_report_image(image)
        author = Profile.objects.get(user=request.user)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.image = img
            instance.author = author
            instance.save()
        
        return JsonResponse({'msg': 'send'})
    return JsonResponse({'msg': 'not ajax'})

@login_required
def render_pdf_view(request, pk):

    template_path = 'reports/pdf.html'
    # obj = Report.objects.get(id=pk)
    obj = get_object_or_404(Report, pk=pk)
    context = {'obj': obj}
    
    response = HttpResponse(content_type='application/pdf')

    # If download
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # If display
    response['Content-Disposition'] = 'filename="report.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
       html, dest=response)
    
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response