select
    {% block columns %}
    {% endblock %}
from {{ table_name }}
where
    {% block where_clauses %}
    {% endblock %}
group by
    {% block group_by %}
    cola,
    {% endblock %}
