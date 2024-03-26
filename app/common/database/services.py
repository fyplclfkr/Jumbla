# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.common.database.models import Shot, Tag, Shot2Tag

engine = create_engine('mysql+pymysql://root:123456@localhost:3306/jumbla')
Session = sessionmaker(bind=engine)
session = Session()


# 上传镜头
def upload_shots(shot_list):
    pass


# 上传标签
def upload_tags(tag_list):
    pass


# 更改镜头标签
def change_shots_tag(shot_list, tag_list):
    pass


# 获取标签对应的镜头
def get_shots(tag_list: list):
    shot_list = []
    for tag in tag_list:
        shot = session.query(Shot).join(Shot2Tag).join(Tag).filter(Tag.name == tag).all()
        shot_list.extend(shot)
    print(shot_list)
    for shot in shot_list:
        print(shot.id, shot.name, shot.path)


# 写入测试数据
def init_test_data():
    shot1 = Shot(name='test1', path='test1_path')
    shot2 = Shot(name='test2', path='test2_path')
    shot3 = Shot(name='test3', path='test3_path')
    shot4 = Shot(name='test4', path='test4_path')

    tag1 = Tag(name='tag1')
    tag2 = Tag(name='tag2')
    tag3 = Tag(name='tag3')
    tag4 = Tag(name='tag4')

    try:
        session.add(shot1)
        session.add(shot2)
        session.add(shot3)
        session.add(shot4)
        session.add(tag1)
        session.add(tag2)
        session.add(tag3)
        session.add(tag4)

        session.add_all([
            Shot2Tag(shot_id=1, tag_id=1),
            Shot2Tag(shot_id=1, tag_id=2),
            Shot2Tag(shot_id=2, tag_id=2),
            Shot2Tag(shot_id=2, tag_id=3),
            Shot2Tag(shot_id=3, tag_id=3),
            Shot2Tag(shot_id=3, tag_id=4),
            Shot2Tag(shot_id=4, tag_id=4),
            Shot2Tag(shot_id=4, tag_id=1),
        ])

        session.commit()
        print('init test data success')
    except Exception as e:
        print(e)
        session.rollback()


if __name__ == '__main__':
    # init_test_data()
    get_shots(['tag1', 'tag2'])
