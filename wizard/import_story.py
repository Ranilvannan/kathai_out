from odoo import models, fields


class StoryImport(models.TransientModel):
    _name = "story.import"
    _description = "Story Import"

    name = fields.Char(string="Name")

    def trigger_import(self):
        pass
