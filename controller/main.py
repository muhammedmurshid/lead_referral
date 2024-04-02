from odoo import http
from odoo.http import request


class WebsiteForm(http.Controller):
    @http.route(['/student_referral_form'], type='http', auth="public", website=True, csrf=False)
    def appointment(self, **kw):
        # partners = request.env['res.partner'].sudo().search([])
        # values = {}
        # values.update({'partners': partners})
        return request.render("lead_referral.online_referral_form_for_student")

    @http.route(['/student_referral_form/next'],  type='http', auth="public", website=True, csrf=False)
    def referral_next_form(self, **kw):
        print(kw, 'referrel ')
        # partners = request.env['res.partner'].sudo().search([])
        # values = {}
        # values.update({'partners': partners})
        return request.render("lead_referral.online_referral_next_form_for_student")

    @http.route(['/student_referral_form/next/submit'], type='http', auth="public", website=True, csrf=False)
    def referral_submit(self, **post):
        print(post.get('name'), 'ref')
        print(post.get('referral_next_form'), 'ref1')
        # print(self.referral_next_form().kw, 'ref2')
        # partners = request.env['res.partner'].sudo().search([])
        # values = {}
        # values.update({'partners': partners})
        return request.render("lead_referral.tmp_student_referral_form_success")
