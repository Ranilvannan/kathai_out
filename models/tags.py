from odoo import models, fields


class KathaiOutTags(models.Model):
    _name = "kathai.out.tags"
    _description = "Tags"
    _rec_name = "name"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
