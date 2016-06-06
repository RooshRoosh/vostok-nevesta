from django.shortcuts import render

# Create your views here.

from gallery.models import Image


def index(request):
    '''
    This View display 20 photo on main page
    '''
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
    positive_tags = ['tag'+str(i) for i in range(1, 6)]
    negative_tags = ['excl_tag'+str(i) for i in range(1, 4)]

    positive_values = {tag:request.GET.get(tag) for tag in positive_tags if request.GET.get(tag)}
    negative_values = {tag:request.GET.get(tag) for tag in negative_tags if request.GET.get(tag)}

    order_by = _order_by[request.GET.get('order_by', 'date')]

    query = '''
    SELECT i.id, i.url, i.create_at, GROUP_CONCAT(DISTINCT all_tags.title SEPARATOR \',\') as i_tags
    from gallery_image as i
    '''

    for (index, value) in enumerate(positive_values.values()):
        query+="""
        INNER JOIN gallery_image_tags AS git{index} ON git{index}.image_id = i.id
        INNER JOIN gallery_tag AS t{index} ON
            git{index}.tag_id = t{index}.id and t{index}.title = '{value}' \n""".format(
            value=value,
            index=index
        )

    query+='''
    INNER JOIN gallery_image_tags AS all_git ON all_git.image_id = i.id
    INNER JOIN gallery_tag AS all_tags ON all_git.tag_id = all_tags.id
    GROUP BY i.id
    '''
    if positive_values or negative_values:
        query+='HAVING \n'

    if positive_values:
        query+="sum(if(all_tags.title in({positive_values}),1,0)) = {positive_count} \n".format(
            positive_values=','.join("'"+i+"'" for i in positive_values.values()),
            positive_count=len(positive_values)
        )
    if positive_values and negative_values:
        query+='AND\n'

    if negative_values:
        query+= "sum(if(all_tags.title in({negative_values}),1,0)) = 0 \n".format(
            negative_values=','.join("'"+i+"'" for i in negative_values.values())
        )

    query+='''
    ORDER BY {order_by} DESC
    LIMIT 20
    OFFSET {offset}
    '''.format(
        offset=(page-1)*20,
        order_by=order_by
    )

    image_list = []

    negative_values.values()

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
        'next':page+1,
        'nextnext':page+2,

    }

    return render(
        request=request,
        context=context,
        template_name='index.html'
    )




# SELECT i.id, i.likes, i.url, i.create_at, GROUP_CONCAT(DISTINCT all_tags.title) as i_tag from gallery_image as i
#
# INNER JOIN gallery_image_tags AS git1 ON git1.image_id = i.id
# INNER JOIN gallery_tag AS t1 ON git1.tag_id = t1.id and t1.title = '1'
#
# INNER JOIN gallery_image_tags AS git2 ON git2.image_id = i.id
# INNER JOIN gallery_tag AS t2 ON git2.tag_id = t2.id and t2.title = '2'
#
# INNER JOIN gallery_image_tags AS git3 ON git3.image_id = i.id
# INNER JOIN gallery_tag AS t3 ON git3.tag_id = t3.id and t3.title = '3'
#
# INNER JOIN gallery_image_tags AS all_git ON all_git.image_id = i.id
# INNER JOIN gallery_tag AS all_tags ON all_git.tag_id = all_tags.id
#
# GROUP BY (i.id)
#
# HAVING sum(if(all_tags.title in('1','2','3'),1,0)) = 3
#     AND sum(if(all_tags.title in('6'),1,0)) =0
#
# LIMIT 20 OFFSET 20



# SELECT i.id, i.url, i.create_at, GROUP_CONCAT(DISTINCT all_tags.title SEPARATOR ',') as i_tags
# from gallery_image as i
# INNER JOIN gallery_image_tags AS all_git ON all_git.image_id = i.id
# INNER JOIN gallery_tag AS all_tags ON all_git.tag_id = all_tags.id
# GROUP BY i.id
# HAVING
# sum(if(all_tags.title in('1','2','3'),1,0)) = 3
# AND
# sum(if(all_tags.title in('6'),1,0)) = 0
#
# ORDER BY i.create_at DESC
# LIMIT 20
# OFFSET 0