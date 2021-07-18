release: python ng_task/manage.py migrate; web: python ng_task/manage.py collectstatic --no-input
web: gunicorn --pythonpath ng_task ng_task.wsgi