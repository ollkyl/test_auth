# Система RBAC

## Схема доступа

- `roles` — роли (admin, user)
- `business_elements` — объекты (products, orders)
- `access_rules` — права (read, create, update, delete)
- Пользователь → роли → правила → доступ

## Запуск
```bash
del test.db
python mock_data.py
uvicorn main:app --reload

http://127.0.0.1:8000/docs