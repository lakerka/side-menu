from django.db import models


class LtreeField(models.TextField):
    description = 'ltree'

    def __init__(self, *args, **kwargs):
        super(LtreeField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'ltree'
