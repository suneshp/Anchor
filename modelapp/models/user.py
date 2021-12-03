from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), primary_key=False, nullable=False, unique=True)
    password = db.Column(db.String(2048), nullable=False)
    email = db.Column(db.String(120), nullable=True,default=None)
    design = db.relationship("DesignModel",back_populates="user",lazy="dynamic")
    result = db.relationship("ResultModel",back_populates="saved_user",lazy="dynamic")

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
