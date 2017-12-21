from django.db import models
from django.db.models.fields import Field


# TODO investigate postgres GIST index
class LtreeField(models.TextField):
    description = 'ltree'

    def __init__(self, *args, **kwargs):
        super(LtreeField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'ltree'


@Field.register_lookup
class Root(models.Lookup):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)

    lookup_name = 'root'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        is_root = rhs_params[0].lower() in ['true', '1']
        if is_root:
            query = "%s ~ '*{1}'"
        else:
            query = "%s ~ '*{2,}'"
        return query % lhs, []
