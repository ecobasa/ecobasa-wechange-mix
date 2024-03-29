# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

from cosinnus.models import CosinnusGroup


class TaggedReferenceService(TaggedItemBase):
    content_object = models.ForeignKey('Reference')

    class Meta:
        app_label = 'ecobasa'


class TaggedReferenceSkill(TaggedItemBase):
    content_object = models.ForeignKey('Reference')

    class Meta:
        app_label = 'ecobasa'


class TaggedReferenceProduct(TaggedItemBase):
    content_object = models.ForeignKey('Reference')

    class Meta:
        app_label = 'ecobasa'

RECOMMEND_CHOICES = ((True, 'Yes'), (False, 'No'))

class Reference(models.Model):
    giver = models.ForeignKey(settings.COSINNUS_USER_PROFILE_MODEL,
        related_name='%(app_label)s_%(class)s_giver',
        help_text=_('Who gave this reference'),
        blank=False,
        null=False,
    )
    receiver_pioneer = models.ForeignKey(settings.COSINNUS_USER_PROFILE_MODEL,
        related_name='%(app_label)s_%(class)s_receiver_pioneer',
        help_text=_('The pioneer who receives this reference'),
        blank=True,
        null=True,
    )
    receiver_community = models.ForeignKey(settings.COSINNUS_GROUP_OBJECT_MODEL,
        related_name='%(app_label)s_%(class)s_receiver_community',
        help_text=_('The community which receives this reference'),
        blank=True,
        null=True,
    )
    date = models.DateField(
        _('date'),
        auto_now=True,
    )
    recommend = models.BooleanField(
        choices=RECOMMEND_CHOICES,
        default=True,
    )
    text = models.TextField(
        _('reference text'),
        help_text=_('How was your volunteer experience?'),
        blank=False,
    )

    products = TaggableManager(_('products offered by the receiver'),
        through=TaggedReferenceProduct,
        related_name='reference_product',
        blank=True, help_text=_('A comma-separated list of tags. You can type anything here. You can also chose from other users tags. Connect two words with a "-" to have one tag.'))
    services = TaggableManager(_('services rendered by the receiver'),
        through=TaggedReferenceService,
        related_name='reference_service',
        blank=True, help_text=_('A comma-separated list of tags. You can type anything here. You can also chose from other users tags. Connect two words with a "-" to have one tag.'))
    skills = TaggableManager(_('skills receiver could teach you'),
        through=TaggedReferenceSkill,
        related_name='reference_skill',
        blank=True, help_text=_('A comma-separated list of tags. You can type anything here. You can also chose from other users tags. Connect two words with a "-" to have one tag.'))

    class Meta:
        app_label = 'ecobasa'
        verbose_name = _('Reference')
        verbose_name_plural = _('References')
        unique_together = (
            ('giver', 'receiver_pioneer'),
            ('giver', 'receiver_community'),
        )

    def __unicode__(self):
        if self.receiver_pioneer:
            receiver = _('Pioneer %s') % self.receiver_pioneer
        elif self.receiver_community:
            receiver = _('Community %s') % self.receiver_community
        else:
            receiver = _('None')

        return '%s -> %s' % (self.giver, receiver)

    def clean(self):
        msg = None

        if not (self.receiver_pioneer or self.receiver_community):
            msg = _('Please choose either pioneer or community as receiver')
            raise ValidationError(msg)
        elif self.receiver_pioneer and self.receiver_community:
            msg = _('Please choose either pioneer or community as receiver')
            raise ValidationError(msg)
        elif self.giver == self.receiver_pioneer:
            msg = _('Giver cannot be the same as receiver')

        if msg:
            raise ValidationError(msg)

    def unique_error_message(self, model_class, unique_check):
        class_is_self = model_class == type(self)
        check_is_pioneer = unique_check == ('giver', 'receiver_pioneer')
        check_is_community = unique_check == ('giver', 'receiver_community')
        if class_is_self and (check_is_pioneer or check_is_community):
            return _('The giver has already given a reference to the receiver')
        else:
            return super(Reference, self).unique_error_message(
                model_class, unique_check)
