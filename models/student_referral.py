from odoo import models, fields, api, _


class StudentLeadsReferral(models.Model):
    _name = 'student.lead.referral'
    _description = 'Student Lead Referral'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Existing Student Name")
    course = fields.Char(string="Course")
    year_of_batch = fields.Char(string="Year Of Batch")
    branch = fields.Char(string="Branch")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    account_no = fields.Char(string="Account No")
    account_holder_name = fields.Char(string="Account Holder Name")
    ifsc_code = fields.Char(string="IFSC Code")
