# tracking/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Count, Q
import csv
from .models import Container, ContainerStatus
from .forms import ContainerForm, ContainerSearchForm

def dashboard(request):
    # Stats for charts
    status_counts = Container.objects.values('status').annotate(total=Count('status'))
    arrived = Container.objects.filter(status=ContainerStatus.ARRIVED).count()
    delayed = sum(1 for c in Container.objects.all() if c.is_delayed())
    in_transit = Container.objects.filter(status=ContainerStatus.IN_TRANSIT).count()

    context = {
        'status_counts': status_counts,
        'arrived': arrived,
        'delayed': delayed,
        'in_transit': in_transit,
    }
    return render(request, 'tracking/dashboard.html', context)
def container_list(request):
    form = ContainerSearchForm(request.GET or None)
    qs = Container.objects.all().order_by('-created_at')

    if form.is_valid():
        q = form.cleaned_data.get('query') or ''
        status = form.cleaned_data.get('status') or ''
        origin = form.cleaned_data.get('origin') or ''
        destination = form.cleaned_data.get('destination') or ''
        if q:
            qs = qs.filter(Q(container_number__icontains=q) | Q(origin__icontains=q) | Q(destination__icontains=q))
        if status:
            qs = qs.filter(status=status)
        if origin:
            qs = qs.filter(origin__icontains=origin)
        if destination:
            qs = qs.filter(destination__icontains=destination)

    # 🔄 اینجا دوباره داده‌ها رو به قالب می‌فرستیم
    return render(request, 'tracking/container_list.html', {
        'containers': qs,
        'form': form
    })

def container_create(request):
    if request.method == 'POST':
        form = ContainerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tracking:container_list')
    else:
        form = ContainerForm()
    return render(request, 'tracking/container_form.html', {'form': form, 'title': 'Create container'})

def container_update(request, pk):
    obj = get_object_or_404(Container, pk=pk)
    if request.method == 'POST':
        form = ContainerForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('tracking:container_list')
    else:
        form = ContainerForm(instance=obj)
    return render(request, 'tracking/container_form.html', {'form': form, 'title': 'Update container'})

def container_delete(request, pk):
    obj = get_object_or_404(Container, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('tracking:container_list')
    return render(request, 'tracking/container_confirm_delete.html', {'obj': obj})

def export_csv(request):
    qs = Container.objects.all().order_by('container_number')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="containers.csv"'
    writer = csv.writer(response)
    writer.writerow(['Container', 'Origin', 'Destination', 'Status', 'DepartTime', 'DistanceKM', 'AvgSpeedKMH', 'ETA', 'IsDelayed'])
    for c in qs:
        writer.writerow([c.container_number, c.origin, c.destination, c.status, c.depart_time, c.distance_km, c.avg_speed_kmh, c.eta(), c.is_delayed()])
    return response
