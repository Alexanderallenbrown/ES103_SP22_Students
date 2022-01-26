{%- extends 'full.tpl' -%} {% block input_group %}
    {%- if not(cell.metadata.get('hide_input', False)) -%}
        {{ super() }}
    {%- endif -%}
{% endblock input_group %}
