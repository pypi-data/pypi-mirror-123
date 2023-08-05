#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipay.aop.api.response.AlipayResponse import AlipayResponse
from alipay.aop.api.domain.GrmProjectInfoDTO import GrmProjectInfoDTO


class AntProdpaasGrmcoreProgramQueryResponse(AlipayResponse):

    def __init__(self):
        super(AntProdpaasGrmcoreProgramQueryResponse, self).__init__()
        self._result_data = None

    @property
    def result_data(self):
        return self._result_data

    @result_data.setter
    def result_data(self, value):
        if isinstance(value, GrmProjectInfoDTO):
            self._result_data = value
        else:
            self._result_data = GrmProjectInfoDTO.from_alipay_dict(value)

    def parse_response_content(self, response_content):
        response = super(AntProdpaasGrmcoreProgramQueryResponse, self).parse_response_content(response_content)
        if 'result_data' in response:
            self.result_data = response['result_data']
