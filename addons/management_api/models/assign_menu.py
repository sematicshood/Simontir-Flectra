from flectra import models, fields, api

class analisa(models.Model):
    _name = 'assign.menu'

    job_id    = fields.Many2one('hr.job', string='Pekerjaan')
    menus     = fields.Text()