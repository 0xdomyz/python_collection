"""
https://github.com/sripathikrishnan/jinjasql
"""

#baisc
from jinjasql import JinjaSql
j = JinjaSql()

template = """
    SELECT project, timesheet, hours
    FROM timesheet
    WHERE user_id = {{ user_id }}
    {% if project_id %}
    AND project_id = {{ project_id }}
    {% endif %}
"""

data = {
    "project_id": 123,
    "user_id": u"sripathi"
}

query, bind_params = j.prepare_query(template, data)

"""
>>> print(query)

    SELECT project, timesheet, hours
    FROM timesheet
    WHERE user_id = %s

    AND project_id = %s

>>> bind_params
['sripathi', 123]
"""

#param style
j = JinjaSql(param_style='named')
query, bind_params = j.prepare_query(template, data)

"""
>>> print(query)

    SELECT project, timesheet, hours
    FROM timesheet
    WHERE user_id = :user_id_1

    AND project_id = :project_id_2

>>> bind_params
{'user_id_1': 'sripathi', 'project_id_2': 123}
"""

#tuple via jinja
query, bind_params = j.prepare_query(
"""
select 'x' from dual
where project_id in {{ project_ids | inclause }}
""",
    {"project_ids":[1,2,3]}
)
print(query)
bind_params


#mods
query, bind_params = j.prepare_query(
"""
select {{column_names | sqlsafe}} from dual
""",
    {"column_names":"aaaa,bbb"}
)
print(query)
bind_params




