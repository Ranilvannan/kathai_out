from odoo import models, fields


class KathaiKuduTags(models.Model):
    _name = "kathai.kudu.tags"
    _description = "Kathai Kudu Tags"
    _rec_name = "name"

    name = fields.Char(string="Name")
