# simple
from jinja2 import Environment

sql = """
select 
    {{ col }}
from table
"""

prepared = Environment().from_string(sql).render({"col": "column"})
print(prepared)

# comprehensive
from jinja2 import Environment, FileSystemLoader


# based on strings
def bind(template_str, *args, **kwargs):
    env = Environment()
    return env.from_string(template_str).render(*args, **kwargs)


def pbind(template_str, *args, **kwargs):
    print(bind(template_str, *args, **kwargs))


# based on file sys
def fbind(template_name, *args, **kwargs):
    env = Environment(loader=FileSystemLoader("data/jinja2_templates"))
    return env.get_template(template_name).render(*args, **kwargs)


def pfbind(template_name, *args, **kwargs):
    print(fbind(template_name, *args, **kwargs))


# variables
pbind("select {{ foo.bar }}, {{ foo['bar'] }} from table", foo=dict(bar=1))

# filters
pbind(
    """
select
    {{ fields | join(', ') | title}}
from table
    """,
    {"fields": ["aa", "bb"]},
)


# tests
pbind(
    """
select
    a
from table
{% if condition is divisibleby 3 %}where a is not null{% endif %}
    """,
    {"condition": 6},
)

# white space
pbind(
    """
<div>
    {% if True %}
        yay
    {% endif %}
</div>
""",
    {"a": 1},
)

pbind(
    """
{% for item in seq -%}
    {{ item }}
{%- endfor %}
""",
    {"seq": [1, 2, 3]},
)

# escape
pbind(
    """
{% raw %}
    {{ item }}
{% endraw %}
""",
    {},
)

# line state

# template
#   super blocks
pfbind("child.html", {})
pfbind("child.sql", {"table_name": "table_a"})


# template objects
env = Environment(loader=FileSystemLoader("data/jinja2_templates"))
base = env.get_template("base.sql")
child2 = env.get_template("child2.sql")
print(child2.render(base=base))


# for loop
pbind(
    """
select
    {% for i in fields[:-1] -%}
        {{ i }},
    {%- endfor %}
    {{ fields[-1] }}
from table
    """,
    {"fields": ["a", "b", "c"]},
)

pbind(
    """
select
{% for key, value in my_dict | dictsort %}
    {{ key }} as {{ value }},
{% endfor %}
from table
""",
    {"my_dict": {"a": "A", "b": "B", "c": "C", "d": "D"}},
)

pbind(
    """
select
{% for key, value in my_dict | dictsort %}
    {{ key }} as {{ value }}, {{ loop.cycle('#odd', '#even') }}
{% endfor %}
from table
""",
    {"my_dict": {"a": "A", "b": "B", "c": "C", "d": "D"}},
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
    {"fields": ["a", "b", "c"]},
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
    {"fields": ["a", "b", "c"]},
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
    {"fields": ["a", "b", "c"]},
)

# for
pbind(
    """
{% if users %}
<ul>
{% for user in users %}
    <li>{{ user }}</li>
{% endfor %}
</ul>
{% endif %}
""",
    {"users": [1, 2, 3]},
)


"""
{% if kenny.sick %}
    Kenny is sick.
{% elif kenny.dead %}
    You killed Kenny!  You bastard!!!
{% else %}
    Kenny looks okay --- so far
{% endif %}
"""

# macro
"""
{% macro input(name, value='', type='text', size=20) -%}
    <input type="{{ type }}" name="{{ name }}" value="{{
        value|e }}" size="{{ size }}">
{%- endmacro %}
"""

"""
<p>{{ input('username') }}</p>
<p>{{ input('password', type='password') }}</p>
"""

# call
"""
{% macro render_dialog(title, class='dialog') -%}
    <div class="{{ class }}">
        <h2>{{ title }}</h2>
        <div class="contents">
            {{ caller() }}
        </div>
    </div>
{%- endmacro %}

{% call render_dialog('Hello World') %}
    This is a simple dialog rendered by using a macro and
    a call block.
{% endcall %}
"""

"""
{% macro dump_users(users) -%}
    <ul>
    {%- for user in users %}
        <li><p>{{ user.username|e }}</p>{{ caller(user) }}</li>
    {%- endfor %}
    </ul>
{%- endmacro %}

{% call(user) dump_users(list_of_user) %}
    <dl>
        <dt>Realname</dt>
        <dd>{{ user.realname|e }}</dd>
        <dt>Description</dt>
        <dd>{{ user.description }}</dd>
    </dl>
{% endcall %}
"""

# filter
"""
{% filter upper %}
    This text becomes uppercase
{% endfilter %}
"""
