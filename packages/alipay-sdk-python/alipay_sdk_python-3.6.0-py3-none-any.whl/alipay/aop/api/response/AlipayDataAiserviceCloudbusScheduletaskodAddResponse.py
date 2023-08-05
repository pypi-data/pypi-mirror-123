#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipay.aop.api.response.AlipayResponse import AlipayResponse
from alipay.aop.api.domain.CloudbusCommonResult import CloudbusCommonResult


class AlipayDataAiserviceCloudbusScheduletaskodAddResponse(AlipayResponse):

    def __init__(self):
        super(AlipayDataAiserviceCloudbusScheduletaskodAddResponse, self).__init__()
        self._result = None

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        if isinstance(value, CloudbusCommonResult):
            self._result = value
        else:
            self._result = CloudbusCommonResult.from_alipay_dict(value)

    def parse_response_content(self, response_content):
        response = super(AlipayDataAiserviceCloudbusScheduletaskodAddResponse, self).parse_response_content(response_content)
        if 'result' in response:
            self.result = response['result']
