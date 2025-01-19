from django import template

register = template.Library()

@register.simple_tag
def get_contact_labels(contact):
    return contact.labels.all()