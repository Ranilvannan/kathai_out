from odoo import models, fields, api


class KathaiOutStory(models.Model):
    _name = "kathai.out.story"
    _description = "Story"
    _rec_name = "title"

    sequence = fields.Char(string="Sequence")

    url = fields.Text(string="URL")
    title = fields.Text(string="Title")
    preview = fields.Text(string="Preview")
    content_ids = fields.One2many(comodel_name="kathai.out.content", inverse_name="story_id")

    tag_ids = fields.Many2many(comodel_name="kathai.out.tags")

    @api.model_create_multi
    def create(self, vals_list):
        return super(KathaiOutStory, self).create(vals_list)


class KathaiOutContent(models.Model):
    _name = "kathai.out.content"
    _description = "Content"

    order_seq = fields.Integer(string="Order Sequence")
    paragraph = fields.Text(string="Paragraph")
    story_id = fields.Many2one(comodel_name="kathai.out.story", string="Story", ondelete="cascade")
