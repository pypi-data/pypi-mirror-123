#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipay.aop.api.constant.ParamConstants import *


class AlipaySocialBaseChatGmsgSendModel(object):

    def __init__(self):
        self._biz_memo = None
        self._biz_type = None
        self._client_msg_id = None
        self._delivery_mode = None
        self._hidden_side = None
        self._link = None
        self._push_str = None
        self._range_users = None
        self._receiver_id = None
        self._receiver_usertype = None
        self._template_code = None
        self._template_data = None

    @property
    def biz_memo(self):
        return self._biz_memo

    @biz_memo.setter
    def biz_memo(self, value):
        self._biz_memo = value
    @property
    def biz_type(self):
        return self._biz_type

    @biz_type.setter
    def biz_type(self, value):
        self._biz_type = value
    @property
    def client_msg_id(self):
        return self._client_msg_id

    @client_msg_id.setter
    def client_msg_id(self, value):
        self._client_msg_id = value
    @property
    def delivery_mode(self):
        return self._delivery_mode

    @delivery_mode.setter
    def delivery_mode(self, value):
        self._delivery_mode = value
    @property
    def hidden_side(self):
        return self._hidden_side

    @hidden_side.setter
    def hidden_side(self, value):
        self._hidden_side = value
    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        self._link = value
    @property
    def push_str(self):
        return self._push_str

    @push_str.setter
    def push_str(self, value):
        self._push_str = value
    @property
    def range_users(self):
        return self._range_users

    @range_users.setter
    def range_users(self, value):
        if isinstance(value, list):
            self._range_users = list()
            for i in value:
                self._range_users.append(i)
    @property
    def receiver_id(self):
        return self._receiver_id

    @receiver_id.setter
    def receiver_id(self, value):
        self._receiver_id = value
    @property
    def receiver_usertype(self):
        return self._receiver_usertype

    @receiver_usertype.setter
    def receiver_usertype(self, value):
        self._receiver_usertype = value
    @property
    def template_code(self):
        return self._template_code

    @template_code.setter
    def template_code(self, value):
        self._template_code = value
    @property
    def template_data(self):
        return self._template_data

    @template_data.setter
    def template_data(self, value):
        self._template_data = value


    def to_alipay_dict(self):
        params = dict()
        if self.biz_memo:
            if hasattr(self.biz_memo, 'to_alipay_dict'):
                params['biz_memo'] = self.biz_memo.to_alipay_dict()
            else:
                params['biz_memo'] = self.biz_memo
        if self.biz_type:
            if hasattr(self.biz_type, 'to_alipay_dict'):
                params['biz_type'] = self.biz_type.to_alipay_dict()
            else:
                params['biz_type'] = self.biz_type
        if self.client_msg_id:
            if hasattr(self.client_msg_id, 'to_alipay_dict'):
                params['client_msg_id'] = self.client_msg_id.to_alipay_dict()
            else:
                params['client_msg_id'] = self.client_msg_id
        if self.delivery_mode:
            if hasattr(self.delivery_mode, 'to_alipay_dict'):
                params['delivery_mode'] = self.delivery_mode.to_alipay_dict()
            else:
                params['delivery_mode'] = self.delivery_mode
        if self.hidden_side:
            if hasattr(self.hidden_side, 'to_alipay_dict'):
                params['hidden_side'] = self.hidden_side.to_alipay_dict()
            else:
                params['hidden_side'] = self.hidden_side
        if self.link:
            if hasattr(self.link, 'to_alipay_dict'):
                params['link'] = self.link.to_alipay_dict()
            else:
                params['link'] = self.link
        if self.push_str:
            if hasattr(self.push_str, 'to_alipay_dict'):
                params['push_str'] = self.push_str.to_alipay_dict()
            else:
                params['push_str'] = self.push_str
        if self.range_users:
            if isinstance(self.range_users, list):
                for i in range(0, len(self.range_users)):
                    element = self.range_users[i]
                    if hasattr(element, 'to_alipay_dict'):
                        self.range_users[i] = element.to_alipay_dict()
            if hasattr(self.range_users, 'to_alipay_dict'):
                params['range_users'] = self.range_users.to_alipay_dict()
            else:
                params['range_users'] = self.range_users
        if self.receiver_id:
            if hasattr(self.receiver_id, 'to_alipay_dict'):
                params['receiver_id'] = self.receiver_id.to_alipay_dict()
            else:
                params['receiver_id'] = self.receiver_id
        if self.receiver_usertype:
            if hasattr(self.receiver_usertype, 'to_alipay_dict'):
                params['receiver_usertype'] = self.receiver_usertype.to_alipay_dict()
            else:
                params['receiver_usertype'] = self.receiver_usertype
        if self.template_code:
            if hasattr(self.template_code, 'to_alipay_dict'):
                params['template_code'] = self.template_code.to_alipay_dict()
            else:
                params['template_code'] = self.template_code
        if self.template_data:
            if hasattr(self.template_data, 'to_alipay_dict'):
                params['template_data'] = self.template_data.to_alipay_dict()
            else:
                params['template_data'] = self.template_data
        return params

    @staticmethod
    def from_alipay_dict(d):
        if not d:
            return None
        o = AlipaySocialBaseChatGmsgSendModel()
        if 'biz_memo' in d:
            o.biz_memo = d['biz_memo']
        if 'biz_type' in d:
            o.biz_type = d['biz_type']
        if 'client_msg_id' in d:
            o.client_msg_id = d['client_msg_id']
        if 'delivery_mode' in d:
            o.delivery_mode = d['delivery_mode']
        if 'hidden_side' in d:
            o.hidden_side = d['hidden_side']
        if 'link' in d:
            o.link = d['link']
        if 'push_str' in d:
            o.push_str = d['push_str']
        if 'range_users' in d:
            o.range_users = d['range_users']
        if 'receiver_id' in d:
            o.receiver_id = d['receiver_id']
        if 'receiver_usertype' in d:
            o.receiver_usertype = d['receiver_usertype']
        if 'template_code' in d:
            o.template_code = d['template_code']
        if 'template_data' in d:
            o.template_data = d['template_data']
        return o


