from odoo import models, fields


class StoryBook(models.Model):
    _name = "story.book"
    _description = "Story Book"
    _rec_name = "title"

    title = fields.Text(string="Title")
    preview = fields.Text(string="Preview")
    content_ids = fields.One2many(comodel_name="story.content", inverse_name="story_id")

    tag_ids = fields.Many2many(comodel_name="story.tags")


class StoryContent(models.Model):
    _name = "story.content"
    _description = "Story Content"

    order_seq = fields.Integer(string="Order Sequence")
    paragraph = fields.Text(string="Paragraph")
    story_id = fields.Many2one(comodel_name="story.book", string="Story")
