#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipay.aop.api.constant.ParamConstants import *
from alipay.aop.api.domain.CorpEntity import CorpEntity
from alipay.aop.api.domain.NotaryFileVO import NotaryFileVO
from alipay.aop.api.domain.CorpEntity import CorpEntity


class AlipayBossProdAntlegalchainOrderApplyModel(object):

    def __init__(self):
        self._biz_code = None
        self._biz_name = None
        self._biz_unique_id = None
        self._main_agent_buc_user_no = None
        self._main_agent_person_cert_name = None
        self._main_agent_person_cert_no = None
        self._main_corp_entity = None
        self._main_corp_notify_email = None
        self._main_corp_notify_name = None
        self._main_corp_notify_phone = None
        self._notary_file_list = None
        self._rela_corp_entity = None
        self._rela_corp_notify_email = None
        self._rela_corp_notify_phone = None
        self._request_app_name = None
        self._request_time_stamp = None
        self._request_token = None
        self._sign_order = None
        self._submit_time = None

    @property
    def biz_code(self):
        return self._biz_code

    @biz_code.setter
    def biz_code(self, value):
        self._biz_code = value
    @property
    def biz_name(self):
        return self._biz_name

    @biz_name.setter
    def biz_name(self, value):
        self._biz_name = value
    @property
    def biz_unique_id(self):
        return self._biz_unique_id

    @biz_unique_id.setter
    def biz_unique_id(self, value):
        self._biz_unique_id = value
    @property
    def main_agent_buc_user_no(self):
        return self._main_agent_buc_user_no

    @main_agent_buc_user_no.setter
    def main_agent_buc_user_no(self, value):
        self._main_agent_buc_user_no = value
    @property
    def main_agent_person_cert_name(self):
        return self._main_agent_person_cert_name

    @main_agent_person_cert_name.setter
    def main_agent_person_cert_name(self, value):
        self._main_agent_person_cert_name = value
    @property
    def main_agent_person_cert_no(self):
        return self._main_agent_person_cert_no

    @main_agent_person_cert_no.setter
    def main_agent_person_cert_no(self, value):
        self._main_agent_person_cert_no = value
    @property
    def main_corp_entity(self):
        return self._main_corp_entity

    @main_corp_entity.setter
    def main_corp_entity(self, value):
        if isinstance(value, CorpEntity):
            self._main_corp_entity = value
        else:
            self._main_corp_entity = CorpEntity.from_alipay_dict(value)
    @property
    def main_corp_notify_email(self):
        return self._main_corp_notify_email

    @main_corp_notify_email.setter
    def main_corp_notify_email(self, value):
        self._main_corp_notify_email = value
    @property
    def main_corp_notify_name(self):
        return self._main_corp_notify_name

    @main_corp_notify_name.setter
    def main_corp_notify_name(self, value):
        self._main_corp_notify_name = value
    @property
    def main_corp_notify_phone(self):
        return self._main_corp_notify_phone

    @main_corp_notify_phone.setter
    def main_corp_notify_phone(self, value):
        self._main_corp_notify_phone = value
    @property
    def notary_file_list(self):
        return self._notary_file_list

    @notary_file_list.setter
    def notary_file_list(self, value):
        if isinstance(value, list):
            self._notary_file_list = list()
            for i in value:
                if isinstance(i, NotaryFileVO):
                    self._notary_file_list.append(i)
                else:
                    self._notary_file_list.append(NotaryFileVO.from_alipay_dict(i))
    @property
    def rela_corp_entity(self):
        return self._rela_corp_entity

    @rela_corp_entity.setter
    def rela_corp_entity(self, value):
        if isinstance(value, CorpEntity):
            self._rela_corp_entity = value
        else:
            self._rela_corp_entity = CorpEntity.from_alipay_dict(value)
    @property
    def rela_corp_notify_email(self):
        return self._rela_corp_notify_email

    @rela_corp_notify_email.setter
    def rela_corp_notify_email(self, value):
        self._rela_corp_notify_email = value
    @property
    def rela_corp_notify_phone(self):
        return self._rela_corp_notify_phone

    @rela_corp_notify_phone.setter
    def rela_corp_notify_phone(self, value):
        self._rela_corp_notify_phone = value
    @property
    def request_app_name(self):
        return self._request_app_name

    @request_app_name.setter
    def request_app_name(self, value):
        self._request_app_name = value
    @property
    def request_time_stamp(self):
        return self._request_time_stamp

    @request_time_stamp.setter
    def request_time_stamp(self, value):
        self._request_time_stamp = value
    @property
    def request_token(self):
        return self._request_token

    @request_token.setter
    def request_token(self, value):
        self._request_token = value
    @property
    def sign_order(self):
        return self._sign_order

    @sign_order.setter
    def sign_order(self, value):
        self._sign_order = value
    @property
    def submit_time(self):
        return self._submit_time

    @submit_time.setter
    def submit_time(self, value):
        self._submit_time = value


    def to_alipay_dict(self):
        params = dict()
        if self.biz_code:
            if hasattr(self.biz_code, 'to_alipay_dict'):
                params['biz_code'] = self.biz_code.to_alipay_dict()
            else:
                params['biz_code'] = self.biz_code
        if self.biz_name:
            if hasattr(self.biz_name, 'to_alipay_dict'):
                params['biz_name'] = self.biz_name.to_alipay_dict()
            else:
                params['biz_name'] = self.biz_name
        if self.biz_unique_id:
            if hasattr(self.biz_unique_id, 'to_alipay_dict'):
                params['biz_unique_id'] = self.biz_unique_id.to_alipay_dict()
            else:
                params['biz_unique_id'] = self.biz_unique_id
        if self.main_agent_buc_user_no:
            if hasattr(self.main_agent_buc_user_no, 'to_alipay_dict'):
                params['main_agent_buc_user_no'] = self.main_agent_buc_user_no.to_alipay_dict()
            else:
                params['main_agent_buc_user_no'] = self.main_agent_buc_user_no
        if self.main_agent_person_cert_name:
            if hasattr(self.main_agent_person_cert_name, 'to_alipay_dict'):
                params['main_agent_person_cert_name'] = self.main_agent_person_cert_name.to_alipay_dict()
            else:
                params['main_agent_person_cert_name'] = self.main_agent_person_cert_name
        if self.main_agent_person_cert_no:
            if hasattr(self.main_agent_person_cert_no, 'to_alipay_dict'):
                params['main_agent_person_cert_no'] = self.main_agent_person_cert_no.to_alipay_dict()
            else:
                params['main_agent_person_cert_no'] = self.main_agent_person_cert_no
        if self.main_corp_entity:
            if hasattr(self.main_corp_entity, 'to_alipay_dict'):
                params['main_corp_entity'] = self.main_corp_entity.to_alipay_dict()
            else:
                params['main_corp_entity'] = self.main_corp_entity
        if self.main_corp_notify_email:
            if hasattr(self.main_corp_notify_email, 'to_alipay_dict'):
                params['main_corp_notify_email'] = self.main_corp_notify_email.to_alipay_dict()
            else:
                params['main_corp_notify_email'] = self.main_corp_notify_email
        if self.main_corp_notify_name:
            if hasattr(self.main_corp_notify_name, 'to_alipay_dict'):
                params['main_corp_notify_name'] = self.main_corp_notify_name.to_alipay_dict()
            else:
                params['main_corp_notify_name'] = self.main_corp_notify_name
        if self.main_corp_notify_phone:
            if hasattr(self.main_corp_notify_phone, 'to_alipay_dict'):
                params['main_corp_notify_phone'] = self.main_corp_notify_phone.to_alipay_dict()
            else:
                params['main_corp_notify_phone'] = self.main_corp_notify_phone
        if self.notary_file_list:
            if isinstance(self.notary_file_list, list):
                for i in range(0, len(self.notary_file_list)):
                    element = self.notary_file_list[i]
                    if hasattr(element, 'to_alipay_dict'):
                        self.notary_file_list[i] = element.to_alipay_dict()
            if hasattr(self.notary_file_list, 'to_alipay_dict'):
                params['notary_file_list'] = self.notary_file_list.to_alipay_dict()
            else:
                params['notary_file_list'] = self.notary_file_list
        if self.rela_corp_entity:
            if hasattr(self.rela_corp_entity, 'to_alipay_dict'):
                params['rela_corp_entity'] = self.rela_corp_entity.to_alipay_dict()
            else:
                params['rela_corp_entity'] = self.rela_corp_entity
        if self.rela_corp_notify_email:
            if hasattr(self.rela_corp_notify_email, 'to_alipay_dict'):
                params['rela_corp_notify_email'] = self.rela_corp_notify_email.to_alipay_dict()
            else:
                params['rela_corp_notify_email'] = self.rela_corp_notify_email
        if self.rela_corp_notify_phone:
            if hasattr(self.rela_corp_notify_phone, 'to_alipay_dict'):
                params['rela_corp_notify_phone'] = self.rela_corp_notify_phone.to_alipay_dict()
            else:
                params['rela_corp_notify_phone'] = self.rela_corp_notify_phone
        if self.request_app_name:
            if hasattr(self.request_app_name, 'to_alipay_dict'):
                params['request_app_name'] = self.request_app_name.to_alipay_dict()
            else:
                params['request_app_name'] = self.request_app_name
        if self.request_time_stamp:
            if hasattr(self.request_time_stamp, 'to_alipay_dict'):
                params['request_time_stamp'] = self.request_time_stamp.to_alipay_dict()
            else:
                params['request_time_stamp'] = self.request_time_stamp
        if self.request_token:
            if hasattr(self.request_token, 'to_alipay_dict'):
                params['request_token'] = self.request_token.to_alipay_dict()
            else:
                params['request_token'] = self.request_token
        if self.sign_order:
            if hasattr(self.sign_order, 'to_alipay_dict'):
                params['sign_order'] = self.sign_order.to_alipay_dict()
            else:
                params['sign_order'] = self.sign_order
        if self.submit_time:
            if hasattr(self.submit_time, 'to_alipay_dict'):
                params['submit_time'] = self.submit_time.to_alipay_dict()
            else:
                params['submit_time'] = self.submit_time
        return params

    @staticmethod
    def from_alipay_dict(d):
        if not d:
            return None
        o = AlipayBossProdAntlegalchainOrderApplyModel()
        if 'biz_code' in d:
            o.biz_code = d['biz_code']
        if 'biz_name' in d:
            o.biz_name = d['biz_name']
        if 'biz_unique_id' in d:
            o.biz_unique_id = d['biz_unique_id']
        if 'main_agent_buc_user_no' in d:
            o.main_agent_buc_user_no = d['main_agent_buc_user_no']
        if 'main_agent_person_cert_name' in d:
            o.main_agent_person_cert_name = d['main_agent_person_cert_name']
        if 'main_agent_person_cert_no' in d:
            o.main_agent_person_cert_no = d['main_agent_person_cert_no']
        if 'main_corp_entity' in d:
            o.main_corp_entity = d['main_corp_entity']
        if 'main_corp_notify_email' in d:
            o.main_corp_notify_email = d['main_corp_notify_email']
        if 'main_corp_notify_name' in d:
            o.main_corp_notify_name = d['main_corp_notify_name']
        if 'main_corp_notify_phone' in d:
            o.main_corp_notify_phone = d['main_corp_notify_phone']
        if 'notary_file_list' in d:
            o.notary_file_list = d['notary_file_list']
        if 'rela_corp_entity' in d:
            o.rela_corp_entity = d['rela_corp_entity']
        if 'rela_corp_notify_email' in d:
            o.rela_corp_notify_email = d['rela_corp_notify_email']
        if 'rela_corp_notify_phone' in d:
            o.rela_corp_notify_phone = d['rela_corp_notify_phone']
        if 'request_app_name' in d:
            o.request_app_name = d['request_app_name']
        if 'request_time_stamp' in d:
            o.request_time_stamp = d['request_time_stamp']
        if 'request_token' in d:
            o.request_token = d['request_token']
        if 'sign_order' in d:
            o.sign_order = d['sign_order']
        if 'submit_time' in d:
            o.submit_time = d['submit_time']
        return o


