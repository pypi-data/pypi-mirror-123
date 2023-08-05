#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipay.aop.api.constant.ParamConstants import *


class ServiceConsultQueryResponse(object):

    def __init__(self):
        self._consult_event_id = None
        self._content = None
        self._gmt_create = None
        self._gmt_finished = None
        self._gmt_modified = None
        self._images = None
        self._merchant_order_no = None
        self._phone_no = None
        self._question_type = None
        self._second_question_type = None
        self._status = None
        self._target_id = None
        self._target_type = None
        self._trade_no = None

    @property
    def consult_event_id(self):
        return self._consult_event_id

    @consult_event_id.setter
    def consult_event_id(self, value):
        self._consult_event_id = value
    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value
    @property
    def gmt_create(self):
        return self._gmt_create

    @gmt_create.setter
    def gmt_create(self, value):
        self._gmt_create = value
    @property
    def gmt_finished(self):
        return self._gmt_finished

    @gmt_finished.setter
    def gmt_finished(self, value):
        self._gmt_finished = value
    @property
    def gmt_modified(self):
        return self._gmt_modified

    @gmt_modified.setter
    def gmt_modified(self, value):
        self._gmt_modified = value
    @property
    def images(self):
        return self._images

    @images.setter
    def images(self, value):
        if isinstance(value, list):
            self._images = list()
            for i in value:
                self._images.append(i)
    @property
    def merchant_order_no(self):
        return self._merchant_order_no

    @merchant_order_no.setter
    def merchant_order_no(self, value):
        self._merchant_order_no = value
    @property
    def phone_no(self):
        return self._phone_no

    @phone_no.setter
    def phone_no(self, value):
        self._phone_no = value
    @property
    def question_type(self):
        return self._question_type

    @question_type.setter
    def question_type(self, value):
        self._question_type = value
    @property
    def second_question_type(self):
        return self._second_question_type

    @second_question_type.setter
    def second_question_type(self, value):
        self._second_question_type = value
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
    @property
    def target_id(self):
        return self._target_id

    @target_id.setter
    def target_id(self, value):
        self._target_id = value
    @property
    def target_type(self):
        return self._target_type

    @target_type.setter
    def target_type(self, value):
        self._target_type = value
    @property
    def trade_no(self):
        return self._trade_no

    @trade_no.setter
    def trade_no(self, value):
        self._trade_no = value


    def to_alipay_dict(self):
        params = dict()
        if self.consult_event_id:
            if hasattr(self.consult_event_id, 'to_alipay_dict'):
                params['consult_event_id'] = self.consult_event_id.to_alipay_dict()
            else:
                params['consult_event_id'] = self.consult_event_id
        if self.content:
            if hasattr(self.content, 'to_alipay_dict'):
                params['content'] = self.content.to_alipay_dict()
            else:
                params['content'] = self.content
        if self.gmt_create:
            if hasattr(self.gmt_create, 'to_alipay_dict'):
                params['gmt_create'] = self.gmt_create.to_alipay_dict()
            else:
                params['gmt_create'] = self.gmt_create
        if self.gmt_finished:
            if hasattr(self.gmt_finished, 'to_alipay_dict'):
                params['gmt_finished'] = self.gmt_finished.to_alipay_dict()
            else:
                params['gmt_finished'] = self.gmt_finished
        if self.gmt_modified:
            if hasattr(self.gmt_modified, 'to_alipay_dict'):
                params['gmt_modified'] = self.gmt_modified.to_alipay_dict()
            else:
                params['gmt_modified'] = self.gmt_modified
        if self.images:
            if isinstance(self.images, list):
                for i in range(0, len(self.images)):
                    element = self.images[i]
                    if hasattr(element, 'to_alipay_dict'):
                        self.images[i] = element.to_alipay_dict()
            if hasattr(self.images, 'to_alipay_dict'):
                params['images'] = self.images.to_alipay_dict()
            else:
                params['images'] = self.images
        if self.merchant_order_no:
            if hasattr(self.merchant_order_no, 'to_alipay_dict'):
                params['merchant_order_no'] = self.merchant_order_no.to_alipay_dict()
            else:
                params['merchant_order_no'] = self.merchant_order_no
        if self.phone_no:
            if hasattr(self.phone_no, 'to_alipay_dict'):
                params['phone_no'] = self.phone_no.to_alipay_dict()
            else:
                params['phone_no'] = self.phone_no
        if self.question_type:
            if hasattr(self.question_type, 'to_alipay_dict'):
                params['question_type'] = self.question_type.to_alipay_dict()
            else:
                params['question_type'] = self.question_type
        if self.second_question_type:
            if hasattr(self.second_question_type, 'to_alipay_dict'):
                params['second_question_type'] = self.second_question_type.to_alipay_dict()
            else:
                params['second_question_type'] = self.second_question_type
        if self.status:
            if hasattr(self.status, 'to_alipay_dict'):
                params['status'] = self.status.to_alipay_dict()
            else:
                params['status'] = self.status
        if self.target_id:
            if hasattr(self.target_id, 'to_alipay_dict'):
                params['target_id'] = self.target_id.to_alipay_dict()
            else:
                params['target_id'] = self.target_id
        if self.target_type:
            if hasattr(self.target_type, 'to_alipay_dict'):
                params['target_type'] = self.target_type.to_alipay_dict()
            else:
                params['target_type'] = self.target_type
        if self.trade_no:
            if hasattr(self.trade_no, 'to_alipay_dict'):
                params['trade_no'] = self.trade_no.to_alipay_dict()
            else:
                params['trade_no'] = self.trade_no
        return params

    @staticmethod
    def from_alipay_dict(d):
        if not d:
            return None
        o = ServiceConsultQueryResponse()
        if 'consult_event_id' in d:
            o.consult_event_id = d['consult_event_id']
        if 'content' in d:
            o.content = d['content']
        if 'gmt_create' in d:
            o.gmt_create = d['gmt_create']
        if 'gmt_finished' in d:
            o.gmt_finished = d['gmt_finished']
        if 'gmt_modified' in d:
            o.gmt_modified = d['gmt_modified']
        if 'images' in d:
            o.images = d['images']
        if 'merchant_order_no' in d:
            o.merchant_order_no = d['merchant_order_no']
        if 'phone_no' in d:
            o.phone_no = d['phone_no']
        if 'question_type' in d:
            o.question_type = d['question_type']
        if 'second_question_type' in d:
            o.second_question_type = d['second_question_type']
        if 'status' in d:
            o.status = d['status']
        if 'target_id' in d:
            o.target_id = d['target_id']
        if 'target_type' in d:
            o.target_type = d['target_type']
        if 'trade_no' in d:
            o.trade_no = d['trade_no']
        return o


