# -*- coding: utf-8 -*-
# Part of Odoo, Flectra. See LICENSE file for full copyright and licensing details.
from werkzeug import urls

from flectra import api, models, fields


class Planner(models.Model):
    """Planner Model.
    Each Planner has link to an ir.ui.view record that is a template used
    to display the planner pages.
    Each Planner has link to ir.ui.menu record that is a top menu used to display the
    planner launcher(progressbar)

    Method _prepare_<planner_application>_data(self) (model method) that
    generates the values used to display in specific planner pages
    """

    _name = 'web.planner'
    _description = 'Planner'

    @api.model
    def _get_planner_application(self):
        return []

    name = fields.Char(string='Name', required=True)
    menu_id = fields.Many2one('ir.ui.menu', string='Menu', required=True)
    view_id = fields.Many2one('ir.ui.view', string='Template', required=True)
    progress = fields.Integer(string="Progress Percentage", company_dependent=True)
    # data field is used to store the data filled by user in planner(JSON Data)
    data = fields.Text(string="Data", company_dependent=True)
    tooltip_planner = fields.Html(string='Planner Tooltips', translate=True)
    planner_application = fields.Selection('_get_planner_application', string='Planner Application', required=True)
    active = fields.Boolean(string="Active", default=True, help="If the active field is set to False, it will allow you to hide the planner. This change requires a refresh of your page.")

    @api.model
    def render(self, template_id, planner_app):
        # prepare the planner data as per the planner application
        values = {
            'prepare_backend_url': self.prepare_backend_url,
            'is_module_installed': self.is_module_installed,
        }
        planner_find_method_name = '_prepare_%s_data' % planner_app
        if hasattr(self, planner_find_method_name):
            values.update(getattr(self, planner_find_method_name)()) # update the default value
        return self.env['ir.ui.view'].browse(template_id).render(values=values)

    @api.model
    def prepare_backend_url(self, action_xml_id, view_type='list', module_name=None):
        """ prepare the backend url to the given action, or to the given module view.
            :param action_xml_id : the xml id of the action to redirect to
            :param view_type : the view type to display when redirecting (form, kanban, list, ...)
            :param module_name : the name of the module to display (if action_xml_id is 'open_module_tree'), or
                                 to redirect to if the action is not found.
            :returns url : the url to the correct page
        """
        params = dict(view_type=view_type)
        # setting the action
        action = self.env.ref(action_xml_id, False)
        if action:
            params['action'] = action.id
            params['view_type'] = action.view_type or view_type
        else:
            params['model'] = 'ir.module.module'
        # setting the module
        if module_name:
            module = self.env['ir.module.module'].sudo().search([('name', '=', module_name)], limit=1)
            if module:
                params['id'] = module.id
            else:
                return "#show_enterprise"
        return "/web#%s" % (urls.url_encode(params),)

    @api.model
    def is_module_installed(self, module_name=None):
        return module_name in self.env['ir.module.module']._installed()

    @api.model
    def get_planner_progress(self, planner_application):
        return self.search([('planner_application', '=', planner_application)]).progress
