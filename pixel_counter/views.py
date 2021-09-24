from django.shortcuts import render
from .forms import ImageForm
from PIL import Image


def main_view(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            image_object = form.instance
            image_opened = Image.open(image_object.image)
            pixels = image_opened.getdata()
            image_opened.close()
            black_pixel_count = 0
            white_pixel_count = 0

            for pixel in pixels:
                if pixel == (0, 0, 0):
                    black_pixel_count += 1
                elif pixel == (255, 255, 255):
                    white_pixel_count += 1

            message = ''
            if white_pixel_count > black_pixel_count:
                message = 'Белых пикселей больше чем черных'
            elif black_pixel_count > white_pixel_count:
                message = 'Черных пикселей больше чем белых'
            elif black_pixel_count == 0 & white_pixel_count == 0:
                message = 'Абсолютно белые и абсолютно черные пиксели отсутсвуют'
            else:
                message = 'Одинаковое количество черных и белых пикселей'

            return render(request, 'page.html', {'form': form, 'image_object': image_object, 'message': message})
    else:
        form = ImageForm()
    return render(request, 'page.html', {'form': form})
