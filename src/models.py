from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    climate: Mapped[str] = mapped_column(String(250))
    terrain: Mapped[str] = mapped_column(String(250))
    population: Mapped[str] = mapped_column(String(120))

    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="planet", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population
        }


class People(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    gender: Mapped[str] = mapped_column(String(50))
    birth_year: Mapped[str] = mapped_column(String(50))
    eye_color: Mapped[str] = mapped_column(String(50))

    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="people", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color
        }


class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int | None] = mapped_column(
        ForeignKey("planet.id"), nullable=True)
    people_id: Mapped[int | None] = mapped_column(
        ForeignKey("people.id"), nullable=True)

    user: Mapped["User"] = relationship(back_populates="favorites")
    planet: Mapped["Planet"] = relationship(back_populates="favorites")
    people: Mapped["People"] = relationship(back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet": self.planet.name if self.planet else None,
            "people": self.people.name if self.people else None
        }

class LearnMore(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    planet_id: Mapped[int | None] = mapped_column(ForeignKey("planet.id"), nullable=True)
    people_id: Mapped[int | None] = mapped_column(ForeignKey("people.id"), nullable=True)

    planet: Mapped["Planet"] = relationship()
    people: Mapped["People"] = relationship()

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "planet_id": self.planet_id,
            "people_id": self.people_id
        }
