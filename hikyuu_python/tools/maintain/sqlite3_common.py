# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2010-2017 fasiondog/hikyuu
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sqlite3

from common import MARKETID, get_stktype_list


def create_database(connect):
    """创建SQLITE3数据库表"""
    try:
        cur = connect.cursor()
        filename = os.path.dirname(__file__) + '/sqlite_upgrade/createdb.sql'
        with open(filename, 'r', encoding='utf8') as sqlfile:
            cur.executescript(sqlfile.read())
        connect.commit()
        cur.close()
    except sqlite3.OperationalError:
        print("相关数据表可能已经存在，忽略创建。如需重建，请手工删除相关数据表。")
        pass
    except Exception as e:
        raise(e)


def get_marketid(connect, market):
    cur = connect.cursor()
    a = cur.execute("select marketid, market from market where market='{}'".format(market.upper()))
    marketid = [i for i in a]
    marketid = marketid[0][0]
    cur.close()
    return marketid


def get_codepre_list(connect, marketid, quotations):
    """获取前缀代码表"""
    stktype_list = get_stktype_list(quotations)
    sql = "select codepre, type from coderuletype " \
          "where marketid={marketid} and type in {type_list}"\
        .format(marketid=marketid, type_list=stktype_list)
    cur = connect.cursor()
    a = cur.execute(sql)
    a = a.fetchall()
    cur.close()
    return sorted(a, key=lambda k: len(k[0]), reverse=True)


def update_last_date(connect, marketid, lastdate):
    cur = connect.cursor()
    cur.execute("update Market set lastDate={} where marketid='{}'".format(lastdate, marketid))
    #if marketid == MARKETID.SH:
    #    cur.execute("update LastDate set date={}".format(lastdate))
    connect.commit()
    cur.close()


def get_last_date(connect, marketid):
    cur = connect.cursor()
    a = cur.execute("select lastDate from market where marketid='{}'".format(marketid))
    last_date = [x[0] for x in a][0]
    connect.commit()
    cur.close()
    return last_date


def get_stock_list(connect, market, quotations):
    marketid = get_marketid(connect, market)
    stktype_list = get_stktype_list(quotations)
    sql = "select stockid, marketid, code, valid, type from stock where marketid={} and type in {}"\
        .format(marketid, stktype_list)
    cur = connect.cursor()
    a = cur.execute(sql).fetchall()
    connect.commit()
    cur.close()
    return a