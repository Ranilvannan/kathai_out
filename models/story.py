from odoo import models, fields, api


class KathaiKuduStory(models.Model):
    _name = "kathai.kudu.story"
    _description = "Kathai Kdu Story"
    _rec_name = "title"

    sequence = fields.Char(string="Sequence")

    title = fields.Text(string="Title")
    preview = fields.Text(string="Preview")
    content_ids = fields.One2many(comodel_name="kathai.kudu.content", inverse_name="story_id")

    tag_ids = fields.Many2many(comodel_name="kathai.kudu.tags")

    @api.model_create_multi
    def create(self, vals_list):
        return super(KathaiKuduStory, self).create(vals_list)


class KathaiKuduContent(models.Model):
    _name = "kathai.kudu.content"
    _description = "Kathai Kudu Content"

    order_seq = fields.Integer(string="Order Sequence")
    paragraph = fields.Text(string="Paragraph")
    story_id = fields.Many2one(comodel_name="kathai.kudu.story", string="Story", ondelete="cascade")
