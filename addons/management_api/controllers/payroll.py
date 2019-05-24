from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication
from . rest_exception import *
import datetime
import traceback
from itertools import groupby


class ProfileMekanikAPI(http.Controller):
    @http.route('/simontir/payroll/bonus', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def getMekanik(self):
        pass
