from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(primary_key=True)
    tg_id = fields.BigIntField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return str(self.tg_id)


class Favorite(Model):
    id = fields.IntField(primary_key=True)
    user = fields.ForeignKeyField(
        "models.User", related_name="Пользователь", on_delete=fields.CASCADE
    )
    idea = fields.ForeignKeyField(
        "models.Idea", related_name="Поделка", on_delete=fields.CASCADE
    )

    def __str__(self):
        return f"{self.id}: {self.user} - {self.idea}"


class Material(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=50)
    category = fields.CharField(max_length=50)

    def __str__(self):
        return self.name


class Idea(Model):
    id = fields.IntField(primary_key=True)
    description = fields.TextField()
    instruction = fields.TextField()
    materials = fields.ManyToManyField("models.Material", related_name="ideas")
    image = fields.CharField(max_length=255, null=True)

    def __str__(self):
        return self.description


class Answers(Model):
    id = fields.IntField(primary_key=True)
    answer = fields.CharField(max_length="128")


class Question(Model):
    id = fields.IntField(primary_key=True)
    text = fields.TextField()
    answers = fields.ManyToManyField("models.Answers", related_name="Question")

    def __str__(self):
        return self.text
