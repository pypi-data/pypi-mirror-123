from django.db.models import Manager, Value, F
from django.db.models.functions import Concat


class UserNameManager(Manager):

    def get_queryset(self):
        return super().get_queryset().annotate(
            name=Concat(F('first_name'), Value(' '), F('last_name'))
        )
