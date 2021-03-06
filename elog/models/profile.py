from passlib.apps import custom_app_context as pwd_context  # type: ignore

from elog import db  # type: ignore
from elog.models import CASCADE, LAZY, Base


# noinspection PyMethodMayBeStatic,SpellCheckingInspection
class User(Base):
    __tablename__ = "users"

    last_auth_time = db.Column(db.DateTime)  # type: ignore
    username = db.Column(db.String(32), index=True, nullable=False, unique=True)  # type: ignore
    password_hash = db.Column(db.String(128))  # type: ignore

    def set_password(self, password):
        self.password_hash = pwd_context.hash(
            password
        )  # uses sha512_crypt with a min round of 535000

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return str(self.id)

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


class UserAccess(Base):
    __tablename__ = "user_accesses"
    __table_args__ = (db.UniqueConstraint("users_id", "ip_address", "external_app_id"),)  # type: ignore

    ip_address = db.Column(db.String(15), index=True, nullable=False)  # type: ignore
    external_app_id = db.Column(db.String(15), index=True, nullable=False, unique=True)  # type: ignore

    users_id = db.Column(  # type: ignore
        db.BigInteger,  # type: ignore
        db.ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),  # type: ignore
        nullable=False,
    )
    belongs_to = db.relationship(  # type: ignore
        "User", backref=db.backref("known_access", cascade=CASCADE), lazy=LAZY  # type: ignore
    )
