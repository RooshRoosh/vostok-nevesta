from django.shortcuts import render

# Create your views here.

from gallery.models import Image, Tag


def index(request):
    '''
    This View display 20 photo on main page
    '''
    image_list = Image.objects.all()[:20]

    return render(
        request=request,
        context = {'image_list': image_list},
        template_name= 'index.html'
    )