# -*- coding: utf-8 -*-
from sqlalchemy import String, ForeignKey, create_engine, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


# 镜头表
class Shot(Base):
    __tablename__ = 'shots'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    path: Mapped[str] = mapped_column(String(200))
    tag_list = relationship('Tag', secondary='shot_tag', backref='shot_list')


# 标签表
class Tag(Base):
    __tablename__ = 'tags'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)


# 镜头标签关系表
class Shot2Tag(Base):
    __tablename__ = 'shot_tag'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    shot_id: Mapped[int] = mapped_column(ForeignKey('shots.id'), nullable=False)
    tag_id: Mapped[int] = mapped_column(ForeignKey('tags.id'), nullable=False)

    # 建立联合唯一
    __table_args__ = (
        UniqueConstraint('shot_id', 'tag_id'),
    )


def init_db():
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/jumbla')
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    init_db()
