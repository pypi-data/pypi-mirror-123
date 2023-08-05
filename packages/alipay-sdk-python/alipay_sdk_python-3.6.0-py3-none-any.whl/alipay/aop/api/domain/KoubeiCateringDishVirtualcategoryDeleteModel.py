#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipay.aop.api.constant.ParamConstants import *


class KoubeiCateringDishVirtualcategoryDeleteModel(object):

    def __init__(self):
        self._catetory_name = None
        self._out_shop_id = None
        self._shop_id = None

    @property
    def catetory_name(self):
        return self._catetory_name

    @catetory_name.setter
    def catetory_name(self, value):
        self._catetory_name = value
    @property
    def out_shop_id(self):
        return self._out_shop_id

    @out_shop_id.setter
    def out_shop_id(self, value):
        self._out_shop_id = value
    @property
    def shop_id(self):
        return self._shop_id

    @shop_id.setter
    def shop_id(self, value):
        self._shop_id = value


    def to_alipay_dict(self):
        params = dict()
        if self.catetory_name:
            if hasattr(self.catetory_name, 'to_alipay_dict'):
                params['catetory_name'] = self.catetory_name.to_alipay_dict()
            else:
                params['catetory_name'] = self.catetory_name
        if self.out_shop_id:
            if hasattr(self.out_shop_id, 'to_alipay_dict'):
                params['out_shop_id'] = self.out_shop_id.to_alipay_dict()
            else:
                params['out_shop_id'] = self.out_shop_id
        if self.shop_id:
            if hasattr(self.shop_id, 'to_alipay_dict'):
                params['shop_id'] = self.shop_id.to_alipay_dict()
            else:
                params['shop_id'] = self.shop_id
        return params

    @staticmethod
    def from_alipay_dict(d):
        if not d:
            return None
        o = KoubeiCateringDishVirtualcategoryDeleteModel()
        if 'catetory_name' in d:
            o.catetory_name = d['catetory_name']
        if 'out_shop_id' in d:
            o.out_shop_id = d['out_shop_id']
        if 'shop_id' in d:
            o.shop_id = d['shop_id']
        return o


