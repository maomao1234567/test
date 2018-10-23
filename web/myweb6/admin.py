# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Book6
from django.contrib import admin


# Register your models here.
@admin.register(Book6)
class BookAdmin(admin.ModelAdmin):
    list_display = ('serial_name', )