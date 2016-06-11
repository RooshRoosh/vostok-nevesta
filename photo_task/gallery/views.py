# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.conf import settings
# Create your views here.

from gallery.models import Image, init_tag_cache


def index(request):
    '''
    This View display 20 photo on main page
    '''
    TAGS = init_tag_cache()

    if not bool(request.GET):
        image_list = Image.objects.all()[:20].select_related()
        return render(
            request=request,
            context={
                'image_list': image_list,
                'prevprev': None,
                'prev': None,
                'page': 1,
                'next': 2,
                'nextnext': 3,
            },
            template_name='index.html'
        )

    page=int(request.GET.get('page', 1))
    _order_by = {
        'date': 'i.create_at',
        'like': 'i.likes',
    }
    order_by = _order_by[request.GET.get('order_by', 'date')]
    positive_tags = ['tag'+str(i) for i in range(1, 6)]
    negative_tags = ['excl_tag'+str(i) for i in range(1, 4)]

    positive_values = {tag:request.GET.get(tag) for tag in positive_tags if request.GET.get(tag)}
    negative_values = {tag:request.GET.get(tag) for tag in negative_tags if request.GET.get(tag)}


    # Определяем id фоток, у которых есть ВСЕ запрашиваемые теги.
    query = '''SELECT i.id, i.url, i.create_at, GROUP_CONCAT(all_tags.title SEPARATOR ',') as i_tags FROM
        (
            SELECT git.image_id, COUNT(*) as c FROM gallery_image_tags as git
            WHERE git.tag_id in ({positive_values})
            GROUP BY git.image_id
        ) as data

        JOIN gallery_image as i ON i.id = data.image_id
        JOIN gallery_image_tags AS all_git ON all_git.image_id = data.image_id
        JOIN gallery_tag AS all_tags ON all_git.tag_id = all_tags.id

        WHERE data.c ={count_of_positive}

        GROUP BY i.id
    '''.format(
        positive_values=','.join("'"+TAGS[i]+"'" for i in positive_values.values()),
        count_of_positive=len(positive_values)
    )

    # Оставляем только те, которые не содержат не нужные теги.
    if negative_values:
        query += 'HAVING \n'
        query += "sum(if(all_git.tag_id in({negative_values}),1,0)) = 0 \n".format(
            negative_values=','.join("'"+TAGS[i]+"'" for i in negative_values.values())
        )

    # Сортируем подрезаем
    query += '''
        ORDER BY {order_by} DESC
        LIMIT 20
        OFFSET {offset}
        '''.format(
            offset=(page-1)*20,
            order_by=order_by
        )

    print(query)

    image_list = []
    for image in Image.objects.raw(query):
        image.tags_list = sorted(image.i_tags.split(','))
        image_list.append(image)

    context = {
        'image_list': image_list,
        'positive_values': positive_values,
        'negative_values': negative_values,
        'prevprev': page-2,
        'prev': page-1,
        'page': page,
        'next': page+1,
        'nextnext': page+2,

    }

    return render(
        request=request,
        context=context,
        template_name='index.html'
    )