from jinja2 import Environment

env = Environment()

def bind(template_str, data):
    return env.from_string(template_str).render(data)


print(bind(
    "select {{ fields }} from table",
    {"fields": "a"}
))


print(bind(
    """
select
    {% for i in fields[:-1] -%}
        {{ i }},
    {%- endfor %}
    {{ fields[-1] }}
from table
    """,
    {"fields": ["a","b", "c"]}
))


print(bind(
    """
select
    {{ fields | join(', ') }}
from table
    """,
    {"fields": ["a","b"]}
))


print(bind(
    """
select
    {% if fields is divisibleby 3 %}
        {{ fields }}
    {% endif %}
from table
    """,
    {"fields": 6}
))

print(bind(
    """
select
    {% if fields is divisibleby 3 -%}
        {{ fields }}
    {%- endif %}
from table
    """,
    {"fields": 6}
))


print(bind(
    "select {{ fields }} from table"
    ""
    "",
    {"fields": "a"}
))

print(bind(
    """
select {{ fields }} from table
""",
    {"fields": "a"}
))

print(bind(
    """

select {{ fields }} from table


""",
    {"fields": "a"}
))


