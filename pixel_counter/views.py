from django.shortcuts import render
from .forms import ImageForm
from PIL import Image
import logging

logger = logging.getLogger(__name__)
def make_log(message, request_to_log):
    logger.info(message, extra={'method': request_to_log.method, 'ip': request_to_log.META['REMOTE_ADDR']})


def main_view(request):
    if request.method == 'POST':
        make_log('REQUEST', request)
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            image_object = form.instance
            image_opened = Image.open(image_object.image)
            pixels = image_opened.getdata()
            image_opened.close()
            coloured_pixel_count = 0
            black_pixel_count = 0
            white_pixel_count = 0

            try:
                pixel_colour = (int(request.POST['colour_code'][1:3], 16),
                                int(request.POST['colour_code'][3:5], 16),
                                int(request.POST['colour_code'][5:], 16))
                for pixel in pixels:
                    if pixel == pixel_colour:
                        coloured_pixel_count += 1
                message1 = 'Количество пикселей с HEX кодом ' + \
                           str(request.POST['colour_code']) + ' = ' + str(coloured_pixel_count)
            except:
                message1 = 'Введен некорректный HEX код'

            for pixel in pixels:
                if pixel == (0, 0, 0):
                    black_pixel_count += 1
                elif pixel == (255, 255, 255):
                    white_pixel_count += 1

            if white_pixel_count > black_pixel_count:
                message2 = 'Белых пикселей больше чем черных'
            elif black_pixel_count > white_pixel_count:
                message2 = 'Черных пикселей больше чем белых'
            elif black_pixel_count == 0 & white_pixel_count == 0:
                message2 = 'Абсолютно белые и абсолютно черные пиксели отсутсвуют'
            else:
                message2 = 'Одинаковое количество черных и белых пикселей'

            make_log('RESPONSE', request)
            return render(request, 'page.html', {'form': form,
                                                 'image_object': image_object,
                                                 'message1': message1,
                                                 'message2': message2})

    make_log('REQUEST', request)
    form = ImageForm()
    make_log('RESPONSE', request)
    return render(request, 'page.html', {'form': form})
