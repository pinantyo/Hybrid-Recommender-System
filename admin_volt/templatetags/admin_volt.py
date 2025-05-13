import re
import os
from django import template
from django.utils.html import format_html
from admin_volt.utils import get_menu_items
from django.utils.safestring import mark_safe
from django.contrib.admin.views.main import (PAGE_VAR)
from django.template.loader import get_template
from app.model_development import saved_models

# Model
from django.db.models import Sum
from app import models

register = template.Library()
assignment_tag = register.assignment_tag if hasattr(register, 'assignment_tag') else register.simple_tag


@register.filter
def clean_text(value):
    res = value.replace('\n', ' ')
    return res


@register.filter
def checkbox(value):
    res = re.sub(r"</?(?i:td)(.|\n)*?>", "", value)
    return res


@assignment_tag(takes_context=True)
def admin_get_menu(context):
    return get_menu_items(context)


@assignment_tag(takes_context=True)
def get_direction(context):
    res = {
        'panel': 'text-left',
        'notify': 'right',
        'float': 'float-right',
        'reverse_panel': 'text-right',
        'nav': 'ml-auto'
    }

    if context.get('LANGUAGE_BIDI'):
        res['panel'] = 'text-right'
        res['notify'] = 'left'
        res['float'] = ''
        res['reverse_panel'] = 'text-left'
        res['nav'] = 'mr-auto'
    return res


@assignment_tag(takes_context=True)
def get_admin_setting(context):
    # user = context.get('request').user
    # admin_black_setting = user.admin_black_setting if hasattr(user, 'admin_black_setting') else None
    res = {
        # 'sidebar_background': admin_black_setting.sidebar_background if admin_black_setting else 'primary',
        # 'dark_mode': admin_black_setting.dark_mode if admin_black_setting else True,
        # 'input_bg_color': '#ffffff' if admin_black_setting and not admin_black_setting.dark_mode else '#27293c'
    }

    return res


@register.simple_tag
def paginator_number(cl, i):
    """
    Generate an individual page index link in a paginated list.
    """
    if i == cl.paginator.ELLIPSIS:
        return format_html('{} ', cl.paginator.ELLIPSIS)
    elif i == cl.page_num:
        return format_html('<a href="" class="page-link">{}</a> ', i)
    else:
        return format_html(
            '<a href="{}" class="page-link {}">{}</a> ',
            cl.get_query_string({PAGE_VAR: i}),
            mark_safe('end' if i == cl.paginator.num_pages else ''),
            i,
        )


@register.filter
def sum_number(value, number):
    return value + number


@register.filter
def neg_num(value, number):
    return value - number

@register.filter(is_safe=True)
@register.simple_tag
def get_database_data():
    res = models.AccountCustom.objects.all().count()
    return res

@register.filter(is_safe=True)
@register.simple_tag
def get_total_revenue():
    res = models.Reservation.objects.aggregate(Sum('place__price'))['place__price__sum']
    return res

@register.filter(is_safe=True)
@register.simple_tag
def get_total_reservation():
    res = models.Reservation.objects.all().count()
    return res


template_admin_account = get_template('admin/admin_members_list.html')
@register.filter(is_safe=True)
@register.inclusion_tag(template_admin_account)
def get_admin_account():
    admins = models.AccountCustom.objects.filter(is_admin = True).values_list('email','is_active',named=True)
    return {'admins':admins}


template_models_train = get_template('admin/admin_train_model_form.html')
@register.filter(is_safe=True)
@register.inclusion_tag(template_models_train)
def get_models_train():
    models = os.listdir(os.path.join(os.getcwd(),'./app/model_development/saved_models'))
    return {'models':models}

