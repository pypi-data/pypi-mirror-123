# The MIT License (MIT)
#
# Copyright (c) 2021 Moritz E. Beber.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


"""Provide a compound name ORM model."""


from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from . import Base
from .compound import Compound
from .mixins import TimeStampMixin
from .registry import Registry


class CompoundName(TimeStampMixin, Base):
    """Model a compound's names from various namespaces.

    Attributes
    ----------
    id : int
        The primary key in the table.
    compound_id : int
        The foreign key of the related compound.
    registry_id : int
        The foreign key of the related registry.
    registry : Registry
        The name's namespace registry in a many-to-one relationship.
    name : str
        A name or synonym intended for human consumption.
    is_preferred : bool
        Whether this is the compound's preferred name within the namespace.

    """

    __tablename__ = "compound_names"

    # SQLAlchemy column descriptors.
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    compound_id: int = Column(Integer, ForeignKey(Compound.id), nullable=False)
    registry_id: int = Column(Integer, ForeignKey(Registry.id), nullable=False)
    registry: Registry = relationship(Registry, lazy="selectin")
    name: str = Column(String, nullable=False, index=True)
    is_preferred: bool = Column(Boolean, default=False, nullable=False)

    __table_args__ = (UniqueConstraint("compound_id", "registry_id", "name"),)

    def __init__(self, *, is_preferred: bool = False, **kwargs) -> None:
        """Create an instance with a default value."""
        super().__init__(**kwargs)
        self.is_preferred = is_preferred

    def __repr__(self):
        """Return a string representation of the object."""
        return (
            f"{type(self).__name__}("
            f"compound={self.compound_id}, "
            f"registry={repr(self.registry)}, "
            f"name={self.name}, "
            f"is_preferred={self.is_preferred})"
        )
