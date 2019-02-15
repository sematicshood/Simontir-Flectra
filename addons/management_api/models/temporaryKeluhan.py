from flectra import models, fields, api

class keluhan(models.Model):
    _name = 'temporary.keluhan'

    x_ref_so = fields.Char()
    x_keluhan = fields.Char()
