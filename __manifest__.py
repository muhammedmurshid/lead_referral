{
    'name': "Lead Referral",
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['base', 'mail','leads', 'logic_base'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/staff_referral.xml',
        'security/user_rules.xml',
        'views/student_referral.xml',
        'views/student_referral_web_form.xml',
        'views/teachers_referral.xml',
    ],
    'demo': [],
    'summary': "lead_referral",
    'description': "this_is_my_app",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': False
}
