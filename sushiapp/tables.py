from typing import List
from datetime import datetime

import sqlalchemy
from sqlalchemy import String, TIMESTAMP, DateTime, func, ForeignKey, create_engine
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

from dotenv import load_dotenv
import os


class Base(DeclarativeBase):
    type_annotation_map = {
        datetime: TIMESTAMP(timezone=True),
    }


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(20), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    registration_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    orders: Mapped["Orders"] = relationship(back_populates="user")


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    kind: Mapped[str] = mapped_column(sqlalchemy.String, nullable=False)
    amount: Mapped[float] = mapped_column(sqlalchemy.Float, nullable=False)
    description: Mapped[str] = mapped_column(sqlalchemy.Text)
    data: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["Users"] = relationship(back_populates="orders")


class Products(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sqlalchemy.String(50))
    price: Mapped[int] = mapped_column(sqlalchemy.Float)
    description: Mapped[str] = mapped_column(sqlalchemy.String)
    weight: Mapped[int] = mapped_column(sqlalchemy.Float)

    categories: Mapped[list["Categories"]] = relationship(back_populates="products",
                                                          uselist=True,
                                                          secondary="categories_products")


class Categories(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))

    products: Mapped[list["Products"]] = relationship(back_populates="categories",
                                                      uselist=True,
                                                      secondary="categories_products")


class CategoriesProducts(Base):  # Secondary table for link Products & Categories
    __tablename__ = "categories_products"

    catogories_fk = mapped_column(ForeignKey("categories.id"), primary_key=True)
    products_fk = mapped_column(ForeignKey("products.id"), primary_key=True)
