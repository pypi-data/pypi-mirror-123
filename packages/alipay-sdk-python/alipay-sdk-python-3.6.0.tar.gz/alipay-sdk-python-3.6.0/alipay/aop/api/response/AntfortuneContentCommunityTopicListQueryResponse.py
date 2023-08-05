#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipay.aop.api.response.AlipayResponse import AlipayResponse
from alipay.aop.api.domain.TopicItemVo import TopicItemVo


class AntfortuneContentCommunityTopicListQueryResponse(AlipayResponse):

    def __init__(self):
        super(AntfortuneContentCommunityTopicListQueryResponse, self).__init__()
        self._topic_list = None

    @property
    def topic_list(self):
        return self._topic_list

    @topic_list.setter
    def topic_list(self, value):
        if isinstance(value, list):
            self._topic_list = list()
            for i in value:
                if isinstance(i, TopicItemVo):
                    self._topic_list.append(i)
                else:
                    self._topic_list.append(TopicItemVo.from_alipay_dict(i))

    def parse_response_content(self, response_content):
        response = super(AntfortuneContentCommunityTopicListQueryResponse, self).parse_response_content(response_content)
        if 'topic_list' in response:
            self.topic_list = response['topic_list']
