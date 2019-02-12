from flectra import models, fields, api

class analisa(models.Model):
    _name = 'temporary.analisa'

    x_ref_so = fields.Char()
    x_analisa = fields.Char()
    x_saran = fields.Char()
