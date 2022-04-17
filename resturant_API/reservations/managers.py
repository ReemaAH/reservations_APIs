from datetime import datetime, timezone

from django.db import models
from django.db.models import QuerySet


class SoftDeleteQuerySet(QuerySet):
    """
    Prevents objects from being hard-deleted. Instead, sets the
    ``date_deleted``, effectively soft-deleting the object.
    """

    def delete(self):
        for obj in self:
            obj.deleted_on = datetime.now(timezone.utc)
            obj.save()


class SoftDeleteManager(models.Manager):
    """
    Only exposes objects that have NOT been soft-deleted.
    """

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(
            deleted_on__isnull=True)


class SoftDelete(models.Model):
    """
        SoftDelete model

        - Fields
            1. deleted_on
            2. objects (instances that have not been deleted)
            3. original_objects (all the instances of the model)
    
        - Functions
            1- delete
    """
    class Meta:
        abstract = True

    deleted_on = models.DateTimeField(null=True, blank=True)
    objects = SoftDeleteManager()
    original_objects = models.Manager()

    def delete(self, *args, **kwargs):
        self.deleted_on = datetime.now(timezone.utc)
        self.save()
