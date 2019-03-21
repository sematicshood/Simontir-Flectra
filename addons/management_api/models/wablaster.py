from flectra import models, fields

class Wablaster(models.Model):
    _name = 'wablaster'

    phones      = fields.Many2many('res.partner', String='Nomer Telephone', ondelete='cascade')
    user_id     = fields.Many2one('res.users', default=lambda self: self.env.user)
    messages    = fields.Text('Messages')