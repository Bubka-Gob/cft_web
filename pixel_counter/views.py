from django.shortcuts import render
from .forms import ImageForm


def main_view(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'page.html', {'form': form})
    else:
        form = ImageForm()
    return render(request, 'page.html', {'form': form})
