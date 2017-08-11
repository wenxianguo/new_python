#!/usr/bin/python
# -*- coding:utf-8 -*-
import datetime, time
from flask_sqlalchemy import SQLAlchemy
from init import app
db = SQLAlchemy(app, session_options={'autocommit': False})


class Single(db.Model):
    __tablename__ = 'tb_single'
    __table_args__ = ({'extend_existing': False})
    """
    单件商品11111
    """
    single_id = db.Column(db.INTEGER(), primary_key=True, autoincrement=True, nullable=False, unique=True)
    code = db.Column(db.VARCHAR(32), unique=True, nullable=False, server_default='')
    name = db.Column(db.VARCHAR(50), unique=True, nullable=False, server_default='')
    dateline = db.Column(db.INTEGER(),  nullable=False, server_default='0')

    def __repr__(self):
        return '%r <商品 %r>' % (self.id, self.name)

    def __init__(self, name='', code=''):
        self.name = name
        self.code = code
        self.dateline = time.time()


class SingleCost(db.Model):
    __tablename__ = 'tb_single_cost'
    __table_args__ = (
        db.UniqueConstraint('single_id', 'date', name='uix_1'),
        {'extend_existing': False}
    )
    """
    单件商品成本
    """
    id = db.Column(db.INTEGER(), primary_key=True, autoincrement=True, nullable=False, unique=True)
    single_id = db.Column(db.INTEGER(),  nullable=False)
    code = db.Column(db.VARCHAR(32), nullable=False, server_default='')
    date = db.Column(db.Date(), default=datetime.datetime.now())
    cost = db.Column(db.Numeric(precision=10, scale=2), nullable=False)

    def __repr__(self):
        return '<单件成本 %r>' % self.cost


class Sku(db.Model):
    """
    SKU 表 一对多
    """
    __tablename__ = 'tb_sku'
    __table_args__ = ({'extend_existing': False})
    id = db.Column(db.INTEGER(), primary_key=True, autoincrement=True, nullable=False, unique=True)
    goods_id = db.Column(db.INTEGER(), server_default='0', nullable=False)
    name = db.Column(db.VARCHAR(50), unique=True, nullable=False, server_default='')

    def __init__(self, name='', goods_id=0):
        self.name = name
        self.goods_id = goods_id


class SkuSingle(db.Model):
    """
    SKU 表 一对多
    """
    __tablename__ = 'tb_sku_single'
    __table_args__ = (
        db.UniqueConstraint('sku_id', 'single_id', name='uix_1'),
        {'extend_existing': False},
    )
    id = db.Column(db.INTEGER(), primary_key=True, autoincrement=True, nullable=False, unique=True)
    sku_id = db.Column(db.INTEGER(), server_default='0', nullable=False)
    single_id = db.Column(db.INTEGER(), server_default='0', nullable=False)
    single_num = db.Column(db.INTEGER(), server_default='0', nullable=False)


class Order(db.Model):
    """
    订单表
    """
    __tablename__ = 'tb_order'
    __table_args__ = ({'extend_existing': False})
    id = db.Column(db.INTEGER(), primary_key=True, autoincrement=True, nullable=False, unique=True)
    order_id = db.Column(db.CHAR(50), unique=True, nullable=True, server_default='')
    title = db.Column(db.VARCHAR(128),  nullable=True, server_default='')
    dateline = db.Column(db.INTEGER(), server_default='0', nullable=False)
    username = db.Column(db.VARCHAR(16),  nullable=True, server_default='')
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False, server_default='0.00')
    sku_id = db.Column(db.INTEGER(), server_default='0', nullable=False)
    sku_title = db.Column(db.VARCHAR(128),  nullable=True, server_default='')
    goods_count = db.Column(db.INTEGER(), server_default='0', nullable=False)


class Goods(db.Model):
    """
    商品表
    """
    __tablename__ = 'tb_goods'
    __table_args__ = ({'extend_existing': False})
    goods_id = db.Column(db.INTEGER(), primary_key=True, autoincrement=True, nullable=False, unique=True)
    code = db.Column(db.VARCHAR(32), unique=True, nullable=False, server_default='')
    name = db.Column(db.VARCHAR(50), unique=True, nullable=False, server_default='')
    dateline = db.Column(db.INTEGER(), nullable=False, server_default='0')