from django.contrib.gis.db import models


optional = dict(null=True, blank=True)

class Record(models.Model):
    identifier = models.CharField(max_length=256, unique=True, null=False)
    geometry = models.GeometryField()

    float_attribute = models.FloatField(**optional)
    int_attribute = models.IntegerField(**optional)
    str_attribute = models.CharField(max_length=256, **optional)
    datetime_attribute = models.DateTimeField(**optional)
    choice_attribute = models.PositiveSmallIntegerField(choices=[(1, 'ASCENDING'), (2, 'DESCENDING'),], **optional)


class RecordMeta(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='record_metas')

    float_meta_attribute = models.FloatField(**optional)
    int_meta_attribute = models.IntegerField(**optional)
    str_meta_attribute = models.CharField(max_length=256, **optional)
    datetime_meta_attribute = models.DateTimeField(**optional)
    choice_meta_attribute = models.PositiveSmallIntegerField(choices=[(1, 'X'), (2, 'Y'), (3, 'Z')], **optional)


FIELD_MAPPING = {
    'identifier': 'identifier',
    'geometry': 'geometry',
    'floatAttribute': 'float_attribute',
    'intAttribute': 'int_attribute',
    'strAttribute': 'str_attribute',
    'datetimeAttribute': 'datetime_attribute',
    'choiceAttribute': 'choice_attribute',

    # meta fields
    'floatMetaAttribute': 'record_metas__float_meta_attribute',
    'intMetaAttribute': 'record_metas__int_meta_attribute',
    'strMetaAttribute': 'record_metas__str_meta_attribute',
    'datetimeMetaAttribute': 'record_metas__datetime_meta_attribute',
    'choiceMetaAttribute': 'record_metas__choice_meta_attribute',
}

MAPPING_CHOICES = {
    'choiceAttribute': dict(Record._meta.get_field('choice_attribute').choices),
    'choiceMetaAttribute': dict(RecordMeta._meta.get_field('choice_meta_attribute').choices),
}

