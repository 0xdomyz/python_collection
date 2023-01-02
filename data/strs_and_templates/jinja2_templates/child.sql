{% extends "base.sql" %}

{% block columns %}
    cola,
    colb,
    colc
{% endblock %}

{% block where_clauses %}
    cola > 3 and
    colb is not null
{% endblock %}

{% block group_by %}
    {{ super() }}
    colb,
    colc
{% endblock %}
