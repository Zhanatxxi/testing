migrations:
	echo "Enter migrate name: "
	read migrate_name
	alembic revision --autogenerate -m "$migrate_name"

run:
	uvicorn src.project_name.main:app --host 127.0.0.1 --port 8000 --reload