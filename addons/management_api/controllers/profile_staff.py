from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication
from . rest_exception import *
import datetime
import traceback
from itertools import groupby


class ProfileAPI(http.Controller):
    @http.route('/simontir/profile/staff/<int:id>', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def getStaff(self, id, month=None, year=None):
        print(id)
