# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2021/5/21 15:17
:LastEditTime: 2021/5/21 15:17
:LastEditors: SunYiTan
:Description: 
"""
import decimal

from seven_framework import TimeHelper

from seven_cmstar_platform.models.db_models.ezgame.ezgame_user_statistics_log_model import EzgameUserStatisticsLogModel, \
    EzgameUserStatisticsLog


class UserStatisticsLogModelEx(EzgameUserStatisticsLogModel):

    def __init__(self, db_connect_key='db_platform', sub_table=None, db_transaction=None, context=None):
        super().__init__(db_connect_key, sub_table, db_transaction, context)

    def add_log(self, user_id: int, third_auth_id: int, orm_id: int, inc_value):
        """
        添加记录
        :param user_id:
        :param third_auth_id
        :param orm_id:
        :param inc_value:
        :return:
        """
        now_date = TimeHelper.get_now_datetime()
        now_day = int(TimeHelper.datetime_to_format_time(now_date, "%Y%m%d"))

        statistics_log = self.get_entity(where="user_id=%s AND auth_id=%s AND orm_id=%s AND create_day=%s",
                                         params=[user_id, third_auth_id, orm_id, now_day])

        if statistics_log:
            statistics_log.inc_value = decimal.Decimal(statistics_log.inc_value) + decimal.Decimal(inc_value)
            self.update_entity(statistics_log)
        else:
            statistics_log = EzgameUserStatisticsLog()
            statistics_log.user_id = user_id
            statistics_log.auth_id = third_auth_id
            statistics_log.orm_id = orm_id
            statistics_log.inc_value = inc_value
            statistics_log.create_day = now_day
            statistics_log.create_date = now_date

            self.add_entity(statistics_log)
