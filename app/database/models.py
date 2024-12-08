from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(primary_key=True)
    tg_id = fields.BigIntField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return str(self.tg_id)

class Material(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    category = fields.CharField(max_length=50)

    def __str__(self):
        return self.name

class Idea(Model):
    id = fields.IntField(pk=True)
    description = fields.TextField()
    instruction = fields.TextField()
    materials = fields.ManyToManyField('models.Material', related_name='ideas')
    

    def __str__(self):
        return self.description

class Question(Model):
    id = fields.IntField(pk=True)
    text = fields.TextField()
    idea = fields.ForeignKeyField('models.Idea', related_name='questions')

    def __str__(self):
        return self.text