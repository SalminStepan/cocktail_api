from decimal import Decimal
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    ForeignKey,
    CheckConstraint,
    Numeric,
    DateTime,
    UniqueConstraint,
    func,
    false,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Cocktail(Base):
    __tablename__ = "cocktails"

    __table_args__ = (
        CheckConstraint(
            "parse_status IN ('ok', 'partial', 'failed')",
            name="cocktails_parse_status_check",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    source: Mapped[str] = mapped_column(nullable=False) 
    source_url: Mapped[str] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)
    image_url: Mapped[str | None] = mapped_column(nullable=True)
    glass: Mapped[str | None] = mapped_column(nullable=True)
    garnish: Mapped[str | None] = mapped_column(nullable=True)
    method: Mapped[str | None] = mapped_column(nullable=True)
    parse_status: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    ingredients: Mapped[list["Ingredient"]] = relationship(
        back_populates="cocktail"
        )


class Ingredient(Base):
    __tablename__ = "ingredients"

    __table_args__ = (
        CheckConstraint("amount > 0", name="ingredients_amount_check"),
        CheckConstraint("position > 0", name="ingredients_position_check"),
        UniqueConstraint(
            "cocktail_id", 
            "position", 
            name="ingredients_cocktail_id_position_key"
        ),
    ) 
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    cocktail_id: Mapped[int] =  mapped_column(
        BigInteger,
        ForeignKey('cocktails.id'),
        nullable=False
    )
    position: Mapped[int] = mapped_column(nullable=False)
    raw: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )
    unit: Mapped[str | None] = mapped_column(nullable=True)
    name: Mapped[str | None] = mapped_column(nullable=True)
    comment: Mapped[str | None] = mapped_column(nullable=True)
    unresolved: Mapped[bool] = mapped_column(
        nullable=False, 
        server_default=false(),
    )
    cocktail: Mapped["Cocktail"] = relationship(back_populates="ingredients")    
  