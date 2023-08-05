#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipay.aop.api.response.AlipayResponse import AlipayResponse


class KoubeiCateringDishRemovedishDeleteResponse(AlipayResponse):

    def __init__(self):
        super(KoubeiCateringDishRemovedishDeleteResponse, self).__init__()
        self._retry = None

    @property
    def retry(self):
        return self._retry

    @retry.setter
    def retry(self, value):
        self._retry = value

    def parse_response_content(self, response_content):
        response = super(KoubeiCateringDishRemovedishDeleteResponse, self).parse_response_content(response_content)
        if 'retry' in response:
            self.retry = response['retry']
