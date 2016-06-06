from django import template

register = template.Library()

@register.filter(name='display_tags')
def display_tags(image):
    if hasattr(image, 'tags_list'):
        return ' '.join(image.tags_list)
    else:
        return ' '.join([str(i) for i in image.tags.all()])
