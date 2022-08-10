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
#   super blocks
pfbind("child.html",{})
pfbind("child.sql",{"table_name":"table_a"})


#template objects
env = Environment(loader=FileSystemLoader("data/jinja2_templates"))
base = env.get_template("base.sql")
child2 = env.get_template("child2.sql")
print(child2.render(base=base))


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

pbind("""
select
{% for key, value in my_dict | dictsort %}
    {{ key }} as {{ value }},
{% endfor %}
from table
""",
{"my_dict":{"a":"A","b":"B","c":"C","d":"D"}}
)

pbind("""
select
{% for key, value in my_dict | dictsort %}
    {{ key }} as {{ value }}, {{ loop.cycle('#odd', '#even') }}
{% endfor %}
from table
""",
{"my_dict":{"a":"A","b":"B","c":"C","d":"D"}}
)

pbind(
    """
select
    {% for i in fields[:-1] if i not in ["a"] -%}
        {{ i }},
    {%- endfor %}
    {{ fields[-1] }}
from table
    """,
    {"fields": ["a","b", "c"]}
)

pbind(
    """
select
    {% for i in fields if False -%}
        {{ i }},
    {% else %}
        default
    {%- endfor %}
from table
    """,
    {"fields": ["a","b", "c"]}
)

pbind(
    """
select
    {% for i in fields -%}
        {% if not loop.last %}
        {{ i }},
        {% else %}
        {{ i }}
        {% endif %}
    {%- endfor %}
from table
    """,
    {"fields": ["a","b", "c"]}
)


