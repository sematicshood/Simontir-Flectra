# -*- coding: utf-8 -*-

from flectra import models, fields, api
# try:
#     from flectra.addons.management_api.controllers.google import *
# except Exception as identifier:
#     pass


class roles_users(models.Model):
    _inherit = 'res.users'

    role = fields.Char()


class Partner(models.Model):
    _inherit = 'res.partner'

    is_sync = fields.Boolean(default=False, string="Apakah sudah diupload")

    def createGoogleContact(self, record):
        pass
        # try:
        #     if record[0].is_sync == False:
        #         license = self.env['fleet.vehicle'].sudo().search_read(
        #             [('driver_id', '=', record[0].id)], fields=["license_plate"])

        #         if len(license) >= 0:
        #             payload = ({
        #                 "names": [
        #                     {
        #                         "givenName": record[0]['name'],
        #                         "middleName": "license[0]['license_plate']"
        #                     }
        #                 ],
        #                 "phoneNumbers": [
        #                     {
        #                         "value": record[0]['phone'],
        #                         "type": "Mobile"
        #                     }
        #                 ],
        #                 "emailAddresses": [
        #                     {
        #                         "value": record[0]['email']
        #                     }
        #                 ]
        #             })

        #             google = Google()

        #             google.createContact(payload)

        #             record[0].write({
        #                 'is_sync': True
        #             })
        # except Exception as identifier:
        #     print(identifier)
