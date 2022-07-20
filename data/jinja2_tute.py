from jinja2 import Environment, FileSystemLoader

#based on strings
def bind(template_str, *args, **kwargs):
    env = Environment()
    return env.from_string(template_str).render(*args, **kwargs)

def pbind(template_str, *args, **kwargs):
    print(bind(template_str, *args, **kwargs))

#based on file sys
def fbind(template_name, *args, **kwargs):
    env = Environment(loader=FileSystemLoader("data/jinja2_templates"))
    return env.get_template(template_name).render(*args, **kwargs)

def pfbind(template_name, *args, **kwargs):
    print(fbind(template_name, *args, **kwargs))

pfbind("base.html",{})


#variables
pbind(
    "select {{ foo.bar }}, {{ foo['bar'] }} from table",
    foo = dict(bar=1)
)

#filters
pbind(
    """
select
    {{ fields | join(', ') | title}}
from table
    """,
    {"fields": ["aa","bb"]}
)


#tests
pbind(
    """
select
    a
from table
{% if condition is divisibleby 3 %}where a is not null{% endif %}
    """,
    {"condition": 6}
)

#white space
pbind("""
<div>
    {% if True %}
        yay
    {% endif %}
</div>
""",{"a":1})

pbind("""
{% for item in seq -%}
    {{ item }}
{%- endfor %}
""", {"seq":[1,2,3]})

#escape
pbind("""
{% raw %}
    {{ item }}
{% endraw %}
""", {})

#line state

#template





#for loop
pbind(
    """
select
    {% for i in fields[:-1] -%}
        {{ i }},
    {%- endfor %}
    {{ fields[-1] }}
from table
    """,
    {"fields": ["a","b", "c"]}
)






