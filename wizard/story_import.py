from odoo import models, fields


class KathaiKuduImport(models.TransientModel):
    _name = "kathai.kudu.import"
    _description = "Story Import"

    name = fields.Char(string="Name")

    def trigger_import(self):
        pass


