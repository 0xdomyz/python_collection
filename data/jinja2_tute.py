from jinja2 import Environment

env = Environment()

def bind(template_str, data):
    return env.from_string(template_str).render(data)

bind(
    "select {{ fields }} from table",
    {"fields": "a"}
)

print(bind(
    """
select
    {% for i in fields[:-1] -%}
        {{ i }},
    {%- endfor %}
    {{ fields[-1] }}
from table
    """,
    {"fields": ["a","b"]}
))



