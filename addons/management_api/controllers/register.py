from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication

class RegisterAPIBentar(http.Controller):
    @http.route('/simontir/cekso', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    @authentication
    def onLoad(self):
        try:
            #cek SO dengan state quotation
            cek = self.cekSO()
            if len(cek) == 0 :
                createSO = request.env['sale.order'].sudo().create({
                    'partner_id': 1
                    })
                cek = self.cekSO()
                
            data = [{
                "id": data.id,
                "name": data.name
            }for data in cek]

            return data
        except Exception as e:
            print(str(e))

    def cekSO(self):
        cek = request.env['sale.order'].sudo().search([
            ('state', '=', 'draft')
            ])
        return cek

            