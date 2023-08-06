# -*- coding: utf-8 -*-

# MIT license
#
# Copyright (c) 2020-2021 Salvador E. Tropea
# Copyright (c) 2020-2021 Instituto Nacional de Tecnología Industrial
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Author information.
__author__ = 'Salvador Eduardo Tropea'
__webpage__ = 'https://github.com/set-soft/'
__company__ = 'INTI-CMNB - Argentina'

import copy
import os
import logging
import tqdm
from ..global_vars import DEFAULT_CURRENCY, DEBUG_HTTP_HEADERS, DEBUG_HTTP_RESPONSES
from .distributors_info import distributors_info

__all__ = ['distributor_class']


class TqdmLoggingHandler(logging.Handler):
    '''Overload the class to write the logging through the `tqdm`.'''
    def __init__(self, stream, level=logging.NOTSET):
        super(self.__class__, self).__init__(level)
        self.stream = stream

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.tqdm.write(msg, file=self.stream)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)


class distributor_class(object):
    registered = []
    priorities = []
    logger = None
    # distributor_dict contains the available distributors.
    # The distributors are added by the api_*/dist_*/scrape_* modules.
    # The information of each distributor is copied from distributors_info
    # Some modules can add new distributors, not found on distributors_info (from data in the fields)
    # The list of *used* distributors is handled separately.
    distributor_dict = {}
    label2name = {}

    @staticmethod
    def register(api, priority):
        index = 0
        for idx, prio in enumerate(distributor_class.priorities):
            index = idx
            if prio < priority:
                break
        else:
            index += 1
        distributor_class.registered.insert(index, api)
        distributor_class.priorities.insert(index, priority)

    @staticmethod
    def get_dist_parts_info(parts, distributors, currency=DEFAULT_CURRENCY):
        ''' Get the parts info using the modules API/Scrape/Local.'''
        for api in distributor_class.registered:
            if api.enabled:
                api.query_part_info(parts, distributors, currency)

    @staticmethod
    def init_dist_dict():
        ''' Initialize and update the dictionary of the registered distributors classes.'''
        # Clear distributor_dict, then let all distributor modules recreate their entries.
        distributor_class.distributor_dict = {}
        distributor_class.label2name = {}
        for api in distributor_class.registered:
            api.init_dist_dict()

    @staticmethod
    def get_distributors_iter():
        return distributor_class.distributor_dict.keys()

    @staticmethod
    def add_distributors(dists):
        ''' Adds a copy of the distributor info to the supported '''
        for dist in dists:
            # Here we copy the available distributors from distributors_info
            # We use a copy so they can be restored just calling this init again
            data = distributors_info[dist]
            distributor_class.distributor_dict[dist] = copy.deepcopy(data)
            distributor_class.label2name[data.label.name.lower()] = dist

    @staticmethod
    def add_distributor(name, data):
        ''' Adds a distributor to the list of supported '''
        distributor_class.distributor_dict[name] = data
        distributor_class.label2name[data.label.name.lower()] = name

    @staticmethod
    def get_distributor_template(name):
        ''' Get a copy of the distributor info from the original structure.
            Used internaly from the API to add distributors derived from others. '''
        return copy.deepcopy(distributors_info[name])

    @staticmethod
    def get_distributor_info(name):
        ''' Gets all the information about a supported distributor.
            This information comes from the list collected from the APIs, not from the fixed template. '''
        return distributor_class.distributor_dict[name]

    @staticmethod
    def log_request(url, data):
        distributor_class.logger.log(DEBUG_HTTP_HEADERS, 'URL ' + url + ' query:')
        distributor_class.logger.log(DEBUG_HTTP_HEADERS, data)
        if os.environ.get('KICOST_LOG_HTTP'):
            with open(os.environ['KICOST_LOG_HTTP'], 'at') as f:
                f.write(data + '\n')

    @staticmethod
    def log_response(response):
        distributor_class.logger.log(DEBUG_HTTP_RESPONSES, response.text)
        distributor_class.logger.log(DEBUG_HTTP_RESPONSES, 'Status Code: <{}>'.format(response.status_code))
        if os.environ.get('KICOST_LOG_HTTP'):
            with open(os.environ['KICOST_LOG_HTTP'], 'at') as f:
                f.write(response.text + '\n')

    @staticmethod
    def _get_api(api):
        # We currently assume the API is registered
        return next(x for x in distributor_class.registered if x.name == api)

    @staticmethod
    def set_api_options(api, **kwargs):
        ''' Configure an API (by name) '''
        # This is currently used to configure Octopart, which is always available.
        # In the future some check could be added.
        distributor_class._get_api(api).set_options(**kwargs)

    @staticmethod
    def set_api_status(api, enabled):
        ''' Enable/Disable a particular API '''
        distributor_class._get_api(api).enabled = enabled

    @staticmethod
    def get_api_status(api):
        ''' Find if an API is enabled '''
        return distributor_class._get_api(api).enabled

    # Abstract methods, implemented in distributor specific modules.
    @staticmethod
    def query():
        '''Send query to server and return results.'''
        raise NotImplementedError()

    @staticmethod
    def query_part_info():
        ''' Get the parts info of one distributor class.'''
        raise NotImplementedError()
