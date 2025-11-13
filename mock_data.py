from database import SessionLocal, engine, Base
from models.user import User
from models.role import Role
from models.access import BusinessElement, AccessRule
from auth.jwt import hash_password

Base.metadata.create_all(engine)
db = SessionLocal()

# Роли
admin_role = db.query(Role).filter(Role.name == "admin").first() or Role(name="admin")
user_role = db.query(Role).filter(Role.name == "user").first() or Role(name="user")
db.add_all([admin_role, user_role])
db.commit()

# Админ
if not db.query(User).filter(User.email == "admin@example.com").first():
    admin = User(
        email="admin@example.com", password_hash=hash_password("admin123"), first_name="Админ"
    )
    admin.roles.append(admin_role)
    db.add(admin)
    db.commit()

# Элементы
for name in ["products", "orders"]:
    if not db.query(BusinessElement).filter(BusinessElement.name == name).first():
        db.add(BusinessElement(name=name))
db.commit()

# Правила
element = db.query(BusinessElement).filter(BusinessElement.name == "products").first()
if (
    element
    and not db.query(AccessRule)
    .filter(AccessRule.role_id == admin_role.id, AccessRule.element_id == element.id)
    .first()
):
    db.add(AccessRule(role_id=admin_role.id, element_id=element.id, can_read=True, can_create=True))
    db.commit()
