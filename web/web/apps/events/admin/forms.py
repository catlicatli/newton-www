"""Forms for Zinnia admin"""
from django import forms
from django.db.models import ManyToOneRel
from django.db.models import ManyToManyRel
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper

from tagging.forms import TagField

from mptt.forms import TreeNodeChoiceField

from events.models.entry import Entry
from events.models.category import Category
from events.admin.widgets import TagAutoComplete
from events.admin.widgets import MPTTFilteredSelectMultiple
from events.admin.fields import MPTTModelMultipleChoiceField


class CategoryAdminForm(forms.ModelForm):
    """
    Form for Category's Admin.
    """
    parent = TreeNodeChoiceField(
        label=_('Parent category'),
        level_indicator='|--', required=False,
        empty_label=_('No parent category'),
        queryset=Category.objects.all())

    def __init__(self, *args, **kwargs):
        super(CategoryAdminForm, self).__init__(*args, **kwargs)
        rel = ManyToOneRel(Category._meta.get_field('tree_id'),
                           Category, 'id')
        self.fields['parent'].widget = RelatedFieldWidgetWrapper(
            self.fields['parent'].widget, rel, self.admin_site)

    def clean_parent(self):
        """
        Check if category parent is not selfish.
        """
        data = self.cleaned_data['parent']
        if data == self.instance:
            raise forms.ValidationError(
                _('A category cannot be parent of itself.'))
        return data

    class Meta:
        """
        CategoryAdminForm's Meta.
        """
        model = Category
        fields = forms.ALL_FIELDS


class EntryAdminForm(forms.ModelForm):
    """
    Form for Entry's Admin.
    """
    categories = MPTTModelMultipleChoiceField(
        label=_('Categories'), required=False,
        queryset=Category.objects.all(),
        widget=MPTTFilteredSelectMultiple(_('categories'), False,
                                          attrs={'rows': '10'}))

    tags = TagField(
        label=_('Tags'), required=False,
        widget=TagAutoComplete())

    def __init__(self, *args, **kwargs):
        super(EntryAdminForm, self).__init__(*args, **kwargs)
        rel = ManyToManyRel(Category, 'id')
        self.fields['categories'].widget = RelatedFieldWidgetWrapper(
            self.fields['categories'].widget, rel, self.admin_site)
        self.fields['sites'].initial = [Site.objects.get_current()]

    class Meta:
        """
        EntryAdminForm's Meta.
        """
        model = Entry
        fields = forms.ALL_FIELDS
