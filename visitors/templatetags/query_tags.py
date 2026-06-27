from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def query_string(context, **kwargs):
    """
    現在のGETパラメータを保持しながら、指定キーだけ上書き・追加する。
    例: {% query_string sort='visitor_name' %}
    → 現在のフィルター条件を維持したままソートキーだけ差し替えたURLを生成
    """
    request = context['request']
    params = request.GET.copy()
    for key, value in kwargs.items():
        if value is None:
            params.pop(key, None)
        else:
            params[key] = value
    return params.urlencode()