#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipay.aop.api.response.AlipayResponse import AlipayResponse


class AlipayIserviceCcmInstanceGetResponse(AlipayResponse):

    def __init__(self):
        super(AlipayIserviceCcmInstanceGetResponse, self).__init__()
        self._create_time = None
        self._creator_id = None
        self._description = None
        self._external_id = None
        self._id = None
        self._name = None
        self._status = None
        self._update_time = None
        self._updater_id = None

    @property
    def create_time(self):
        return self._create_time

    @create_time.setter
    def create_time(self, value):
        self._create_time = value
    @property
    def creator_id(self):
        return self._creator_id

    @creator_id.setter
    def creator_id(self, value):
        self._creator_id = value
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value
    @property
    def external_id(self):
        return self._external_id

    @external_id.setter
    def external_id(self, value):
        self._external_id = value
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
    @property
    def update_time(self):
        return self._update_time

    @update_time.setter
    def update_time(self, value):
        self._update_time = value
    @property
    def updater_id(self):
        return self._updater_id

    @updater_id.setter
    def updater_id(self, value):
        self._updater_id = value

    def parse_response_content(self, response_content):
        response = super(AlipayIserviceCcmInstanceGetResponse, self).parse_response_content(response_content)
        if 'create_time' in response:
            self.create_time = response['create_time']
        if 'creator_id' in response:
            self.creator_id = response['creator_id']
        if 'description' in response:
            self.description = response['description']
        if 'external_id' in response:
            self.external_id = response['external_id']
        if 'id' in response:
            self.id = response['id']
        if 'name' in response:
            self.name = response['name']
        if 'status' in response:
            self.status = response['status']
        if 'update_time' in response:
            self.update_time = response['update_time']
        if 'updater_id' in response:
            self.updater_id = response['updater_id']
