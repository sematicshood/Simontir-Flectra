from flectra import models, fields


class attendance(models.Model):
    _inherit = 'hr.attendance'

    intensif_part = fields.Integer(default=0)
    intensif_jasa = fields.Integer(default=0)
    intensif_counter = fields.Integer(default=0)
    total_part = fields.Integer(default=0)
    total_jasa = fields.Integer(default=0)
    total_ue = fields.Integer(default=0)
    ins_cuci_motor = fields.Integer(default=0)
