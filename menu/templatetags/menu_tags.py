from django import template

from menu.models import Item, Menu

register = template.Library()


def dict_to_html(dictionary: dict) -> str:
    """Преобразует dict в HTML меню."""
    html = "<ul>"
    for key, value in dictionary.items():
        href = f' href="{key.slug}"'
        html += f"<li><a{href}>{key}</a>"
        if isinstance(value, dict):
            html += dict_to_html(value)
        html += "</li>"
    html += "</ul>"
    return html


@register.inclusion_tag('menu_template.html', takes_context=True)
def draw_menu(context, menu_name):
    try:
        target_slug = context['request'].path
        menu = Menu.objects.select_related('items').get(name=menu_name)
        menu_items = menu.items.all()

        active_item = None
        # поиск активного элемента
        for item in menu_items:
            if item.slug == target_slug:
                active_item = item
                break

        # ищем дочерние элементы активного элемента
        down_lvl = {}
        for item in menu_items:
            if item.parent == active_item:
                down_lvl[item] = None

        res = {}
        # ищем элементы того же уровня, что и активный элемент
        for item in menu_items:
            if item.parent == active_item.parent:
                res[item] = None

        res[active_item] = down_lvl
        #строим дерево меню с помощью словарей
        parent = active_item.parent
        while parent is not None:
            parent_cur_lvl = {parent: res}
            for item in menu_items:
                if item != parent and item.parent == parent.parent:
                    parent_cur_lvl[item] = None
            res = parent_cur_lvl
            parent = parent.parent

        return {
            'menu_items': dict_to_html(res),
        }
    except Menu.DoesNotExist:
        return {}
