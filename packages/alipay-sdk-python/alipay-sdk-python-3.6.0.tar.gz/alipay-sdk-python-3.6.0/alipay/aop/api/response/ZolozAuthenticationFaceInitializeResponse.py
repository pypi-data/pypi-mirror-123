#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipay.aop.api.response.AlipayResponse import AlipayResponse


class ZolozAuthenticationFaceInitializeResponse(AlipayResponse):

    def __init__(self):
        super(ZolozAuthenticationFaceInitializeResponse, self).__init__()
        self._result = None
        self._ret_code_sub = None
        self._ret_message_sub = None
        self._zim_id = None

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        self._result = value
    @property
    def ret_code_sub(self):
        return self._ret_code_sub

    @ret_code_sub.setter
    def ret_code_sub(self, value):
        self._ret_code_sub = value
    @property
    def ret_message_sub(self):
        return self._ret_message_sub

    @ret_message_sub.setter
    def ret_message_sub(self, value):
        self._ret_message_sub = value
    @property
    def zim_id(self):
        return self._zim_id

    @zim_id.setter
    def zim_id(self, value):
        self._zim_id = value

    def parse_response_content(self, response_content):
        response = super(ZolozAuthenticationFaceInitializeResponse, self).parse_response_content(response_content)
        if 'result' in response:
            self.result = response['result']
        if 'ret_code_sub' in response:
            self.ret_code_sub = response['ret_code_sub']
        if 'ret_message_sub' in response:
            self.ret_message_sub = response['ret_message_sub']
        if 'zim_id' in response:
            self.zim_id = response['zim_id']
