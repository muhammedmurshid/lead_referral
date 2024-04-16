from odoo import api, fields, models


class TeachersReferral(models.Model):
    _name = 'teachers.referral'
    _description = 'Teachers Referral'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    teacher_id = fields.Many2one('res.users', string='Teacher', default=lambda self: self.env.user, readonly=1)
    date = fields.Date(string='Date', required=1)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], default='draft', string='Status')
    referral_ids = fields.One2many('referral.students.details', 'referral_id', string='Referral Details')

    @api.onchange('teacher_id')
    def _onchange_get_referral_lead_source(self):
        source = self.env['leads.sources'].sudo().search([('name', '=', 'Student Referral')])
        print('source', source.id)
        domain = [('id', '=', source.id)]
        return {'domain': {'lead_source_id': domain}}

    lead_source_id = fields.Many2one('leads.sources', string='Lead Source', required=1,
                                     domain=_onchange_get_referral_lead_source)

    def action_add_to_lead(self):
        for i in self.referral_ids:
            leads = self.env['leads.logic'].sudo().create({
                'leads_source': self.lead_source_id.id,
                'lead_owner': self.teacher_id.employee_id.id,
                'mode_of_study': i.mode_of_study,
                'phone_number': i.contact_number,
                'name': i.student_name,
                'district': i.district,
                'course_type': i.course_type,
                'base_course_id': i.preferred_course_id.id,
                'branch': i.branch_id.id,
                'lead_quality': 'nil',
                'lead_status': 'nil',
                'referred_teacher': self.teacher_id.id,
                'lead_user_type': 'teacher',
                'course_level': i.course_level.id,
                'academic_year': i.academic_year,
                'preferred_batch_id': i.batch_id.id

            })
        self.state = 'confirm'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Your Referral Form Submitted Successfully',
                'type': 'rainbow_man',
            }
        }


    def _compute_display_name(self):
        for rec in self:
            if rec.teacher_id:
                rec.display_name = rec.teacher_id.name + ' - ' + rec.lead_source_id.name


class LeadsStudentsDetails(models.Model):
    _name = 'referral.students.details'
    _description = 'Referral Students Details'

    student_name = fields.Char(string='Student Name', required=1)
    contact_number = fields.Char(string='Contact Number', required=1)
    email = fields.Char(string='Email')
    batch_id = fields.Many2one('logic.base.batch', string='Batch')
    district = fields.Selection([('wayanad', 'Wayanad'), ('ernakulam', 'Ernakulam'), ('kollam', 'Kollam'),
                                 ('thiruvananthapuram', 'Thiruvananthapuram'), ('kottayam', 'Kottayam'),
                                 ('kozhikode', 'Kozhikode'), ('palakkad', 'Palakkad'), ('kannur', 'Kannur'),
                                 ('alappuzha', 'Alappuzha'), ('malappuram', 'Malappuram'), ('kasaragod', 'Kasaragod'),
                                 ('thrissur', 'Thrissur'), ('idukki', 'Idukki'), ('pathanamthitta', 'Pathanamthitta'),
                                 ('abroad', 'Abroad'), ('other', 'Other'), ('nil', 'Nil')],
                                string='District', required=True)
    mode_of_study = fields.Selection([('online', 'Online'), ('offline', 'Offline'), ('nil', 'Nil')],
                                     string='Mode of Study', required=1)
    course_type = fields.Selection([('indian', 'Indian'), ('international', 'International'), ('crash', 'Crash Course'),
                                    ('repeaters', 'Repeaters'), ('nil', 'Nil')], string='Course Type', required=1)
    academic_year = fields.Selection(
        [('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025'),
         ('2026', '2026'), ('nil', 'Nil')], string='Academic Year', required=True)

    branch_id = fields.Many2one('logic.base.branches', string='Branch', required=1)
    referral_id = fields.Many2one('teachers.referral', string='Referral Id', ondelete='cascade')

    @api.onchange('course_type','preferred_course_id')
    def _onchange_get_course_type_matched_course(self):
        source = self.env['logic.base.courses'].sudo().search([('type', '=', self.course_type), ('state', '=', 'done')])
        courses = []
        for i in source:
            courses.append(i.id)
        domain = [('id', 'in', courses)]
        return {'domain': {'preferred_course_id': domain}}

    preferred_course_id = fields.Many2one('logic.base.courses', string='Preferred Course',
                                          domain=[('type', '=', course_type)], required=1)

    course_level = fields.Many2one('course.levels', string='Course Level', required=1, domain="[('course_id', '=', preferred_course_id)]")

