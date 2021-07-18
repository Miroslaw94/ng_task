release: python ng_task/manage.py migrate; python ng_task/manage.py collectstatic --no-input
web: gunicorn --pythonpath ng_task ng_task.wsgi