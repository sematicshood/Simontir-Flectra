from flectra import models, fields, api

class purchase_order_line(models.Model):
    _inherit = 'purchase.order.line'

    @api.one
    def create(self, vals):
        same_line = self.search([('product_id', '=', vals.get('product_id', False)),
                                 ('order_id', '=', vals.get('order_id', False))])
        if same_line:
            total_qty = same_line.product_qty + vals.get('product_qty', 0)
            vals.update({
                'product_qty': total_qty,
            })
            same_line.write(vals)
            return same_line
        else:
            return super(purchase_order_line, self).create(vals)