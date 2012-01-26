# -*- encoding: utf-8 -*-
############################################################################################
#
#    Zoook. OpenERP e-sale, e-commerce Open Source Management Solution
#    Copyright (C) 2011 Zikzakmedia S.L. (<http://www.zikzakmedia.com>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################################

from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language

from transmeta import TransMeta
from transurl import catalog_url, product_url

from datetime import datetime

'''OpenERP Models'''
class ProductCategory(models.Model):
    """ProductCategory OpenERP"""
    __metaclass__ = TransMeta

    name = models.CharField(_('Name'), max_length=128)
    description = models.TextField(_('Description'), null=True, blank=True)
    slug = models.SlugField(_('slug'), max_length=128, help_text=_("This is a unique identifier that allows your contents to display its detail view, ex 'how-can-i-contribute'"), unique=True)
    fslug = models.CharField(_('Full Slug'), max_length=256, null=True, blank=True)
    metatitle = models.CharField(_('Title'), max_length=128, null=True, blank=True)
    metakeyword = models.TextField(_('Keyword'), null=True, blank=True)
    metadescription = models.TextField(_('Description'), null=True, blank=True)
    AVAILABLE_SORT_BY_CHOICES = (
        ('default', 'Use Config Settings'),
        ('position', 'Best Value'),
        ('name', 'Name'),
        ('price', 'Price')
    )
    available_sort_by = models.CharField(_('Available Product Listing (Sort By)'), choices=AVAILABLE_SORT_BY_CHOICES, default='default', max_length=40)
    DEFAULT_SORT_BY_CHOICES = (
        ('default', 'Use Config Settings'),
        ('position', 'Best Value'),
        ('name', 'Name'),
        ('price', 'Price')
    )
    default_sort_by = models.CharField(_('Default Product Listing Sort (Sort By)'), choices=DEFAULT_SORT_BY_CHOICES,  default='default', max_length=40)
    status = models.BooleanField(_('Status'), default=False)
    parent = models.ForeignKey('ProductCategory', null=True, blank=True)
    sequence = models.IntegerField(_('Sequence'), null=True, blank=True)
    
    """ Custom fields model """

    class Meta:
        db_table = 'product_category'
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        translate = (
            'name',
            'description',
            'slug',
            'fslug',
            'metatitle',
            'metakeyword',
            'metadescription',
            )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/%s/%s/%s' % (get_language(), catalog_url[get_language()], self.fslug)

class ProductTemplate(models.Model):
    """ProductTemplate OpenERP"""
    __metaclass__ = TransMeta

    created_on = models.DateTimeField(_('created on'), default=datetime.now, editable=False)
    name = models.CharField(_('Name'), max_length=128)
    categ = models.ManyToManyField('ProductCategory', null=True, blank=True, related_name='categ_s')
    shortdescription = models.TextField(_('Short Description'), null=True, blank=True)
    description = models.TextField(_('Sale Description'), null=True, blank=True)
    slug = models.CharField(_('Slug'), max_length=128, null=True, blank=True)
    VISIBILITY_CHOICES = (
        ('all', 'All'),
        ('search', 'Search'),
        ('catalog', 'Catalog'),
        ('none', 'None'),
    )
    visibility = models.CharField(_('Visibility'), choices=VISIBILITY_CHOICES, default='', max_length=40)
    metatitle = models.CharField(_('Meta Title'), max_length=128, null=True, blank=True)
    metadescription = models.TextField(_('Meta Description'), null=True, blank=True)
    metakeyword = models.TextField(_('Meta Keyword'), null=True, blank=True)
    crosssells = models.ManyToManyField('ProductTemplate', blank=True, related_name='crosssells_s')
    related = models.ManyToManyField('ProductTemplate', blank=True, related_name='related_s')
    upsells = models.ManyToManyField('ProductTemplate', blank=True, related_name='upsells_s')
    uom = models.CharField(_('Unit Of Measure'), max_length=128)
    uos = models.CharField(_('Unit of Sale'), max_length=128)
    volume = models.FloatField(_('Volume'), null=True, blank=True)
    warranty = models.FloatField(_('Warranty (months)'),null=True, blank=True)
    weight = models.FloatField(_('Gross weight'),null=True, blank=True)
    weight_net = models.FloatField(_('Net weight'), null=True, blank=True)
    status = models.BooleanField(_('Status'), default=False)

    """ Custom fields model """

    class Meta:
        db_table = 'product_template'
        verbose_name = _('template')
        verbose_name_plural = _('templates')
        translate = ('name', 'slug', 'shortdescription', 'description', 'metadescription', 'metakeyword', 'metatitle')

    def __unicode__(self):
        return self.name

    def save(self):
        self.created_on = datetime.now()
        super(ProductTemplate, self).save()

    def get_absolute_url(self):
        return '/%s/%s/%s' % (get_language(), product_url[get_language()], self.slug)

class ProductProduct(models.Model):
    """ProductProduct OpenERP"""
    __metaclass__ = TransMeta

    product_tmpl = models.ForeignKey('ProductTemplate')
    active = models.BooleanField(_('Active'), default=False)
    code = models.CharField(_('Code'), max_length=128, null=True) #Reference
    ean13 = models.CharField(_('EAN13'), max_length=128, null=True, blank=True)
    price = models.CharField(_('Price'), max_length=64, null=True, blank=True)
    manufacturer = models.CharField(_('Manufacturer'), max_length=128, null=True, blank=True)
    attribute_group = models.CharField(_('Attribute Group'), max_length=128, null=True, blank=True)
    cartdescription = models.CharField(_('Cart Description'), max_length=256, blank=True)

    """ Custom fields model """

    class Meta:
        db_table = 'product_product'
        verbose_name = _('product')
        verbose_name_plural = _('products')
        translate = (
            'cartdescription',
        )

    def __unicode__(self):
        return self.code

class ProductImages(models.Model):
    """ProductImages OpenERP"""

    name = models.CharField(_('Image Title'), max_length=128, null=True, blank=True)
    product = models.ForeignKey('ProductProduct', null=True, blank=True)
    filename = models.CharField(_('File Location'), max_length=128, null=True, blank=True)
    base_image = models.BooleanField(_('Base Image'), default=False)
    exclude = models.BooleanField(_('Exclude'), default=False)

    """ Custom fields model """

    class Meta:
        db_table = 'product_images'
        verbose_name = _('image')
        verbose_name_plural = _('images')

    def __unicode__(self):
        return self.name