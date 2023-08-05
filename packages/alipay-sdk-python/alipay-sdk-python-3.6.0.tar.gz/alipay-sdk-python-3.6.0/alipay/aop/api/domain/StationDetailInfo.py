#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipay.aop.api.constant.ParamConstants import *


class StationDetailInfo(object):

    def __init__(self):
        self._code = None
        self._ext_code = None
        self._name = None

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value
    @property
    def ext_code(self):
        return self._ext_code

    @ext_code.setter
    def ext_code(self, value):
        self._ext_code = value
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


    def to_alipay_dict(self):
        params = dict()
        if self.code:
            if hasattr(self.code, 'to_alipay_dict'):
                params['code'] = self.code.to_alipay_dict()
            else:
                params['code'] = self.code
        if self.ext_code:
            if hasattr(self.ext_code, 'to_alipay_dict'):
                params['ext_code'] = self.ext_code.to_alipay_dict()
            else:
                params['ext_code'] = self.ext_code
        if self.name:
            if hasattr(self.name, 'to_alipay_dict'):
                params['name'] = self.name.to_alipay_dict()
            else:
                params['name'] = self.name
        return params

    @staticmethod
    def from_alipay_dict(d):
        if not d:
            return None
        o = StationDetailInfo()
        if 'code' in d:
            o.code = d['code']
        if 'ext_code' in d:
            o.ext_code = d['ext_code']
        if 'name' in d:
            o.name = d['name']
        return o


