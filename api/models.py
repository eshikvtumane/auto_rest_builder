from django.db.models import CharField, IntegerField, Model


class TestModel(Model):
    first_column = CharField(
        max_length=255,
    )

    second_column = IntegerField()
