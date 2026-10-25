{
    'name': 'Todo List',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/todo_data.xml',
        'views/todo_views.xml',
    ],
    'installable': True,
    'application': True,
}