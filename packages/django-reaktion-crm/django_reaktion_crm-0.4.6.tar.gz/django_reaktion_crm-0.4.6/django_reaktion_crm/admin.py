import os

from django.db.models import F
from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import resolve_url
from django.contrib.admin.templatetags.admin_urls import admin_urlname

from .models import ClientHistory
from .models import Clients
from .models import Visits
from .models import Newsletter
from .models import NewsletterLink


def find_correct_field():
    if 'SHOW_EMAILS' in os.environ:
        show_email = os.environ['SHOW_EMAILS']
    else:
        show_email = True

    if show_email == True:
        field = 'email'
    else:
        field = 'name'

    return field


class HistoryInline(admin.TabularInline):
    fieldsets = [
        (None, {'fields': ['action', 'note', ]}),
    ]
    model = ClientHistory
    extra = 1


class NewsletterLinksInline(admin.TabularInline):
    fieldsets = [
        (None, {'fields': ['link']}),
    ]
    model = NewsletterLink
    extra = 1


class ClientsAdmin(admin.ModelAdmin):
    field = find_correct_field()

    list_filter = ('campaigns',)

    list_display = (
        'kund',
        'company',
        'org_number',
        'phone',
        'active',
        'selected_client',
        'last_7_days_visits',
        'last_30_days_visits',
        'all_visits',
        'last_visit'
    )

    search_fields = (field, 'company', 'org_number', 'phone',)
    readonly_fields = ('last_7_days_visits', 'last_30_days_visits', 'all_visits')
    inlines = [HistoryInline]
    ordering = [F('last_visit').desc(nulls_last=True)]

    fieldsets = (
        ('Kund', {
            'classes': ('',),
            'fields': (
                'active',
                field,
                'selected_client',
                'company',
                'position',
                'org_number',
                'phone',
                'last_7_days_visits',
                'last_30_days_visits',
                'all_visits'
            )
        }),
    )

    def get_queryset(self, request):
        qs = super(ClientsAdmin, self).get_queryset(request)
        return qs.filter(last_30_days_visits__gte=os.environ['FILTER_NUMBER_OF_VISITS_30_DAYS']).filter(bot=0)

    def kund(self, obj):
        if 'SHOW_EMAILS' in os.environ:
            show_email = os.environ['SHOW_EMAILS']
        else:
            show_email = True

        if show_email is True:
            return obj.email

        else:
            if len(obj.name) > 2:
                return obj.name
            else:
                return "-"

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}

        """
        Get all visits for person
        """
        person = self.get_object(request, object_id)
        pages = Visits.objects.filter(uid=person.uid).order_by('-created_at').all()

        """
        Create graphs for last 7 days
        """

        extra_context['urls'] = pages
        extra_context['graph_data'] = {}
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )


class VisitsAdmin(admin.ModelAdmin):
    list_display = ('find_person_other', 'url', 'created_at')
    search_fields = ('url',)
    ordering = ['-created_at']

    def create_url_for_client(self, item):
        url = resolve_url(admin_urlname(Clients._meta, 'change'), item.id)
        return format_html('<a href="{url}">{name}</a>'.format(url=url, name=str(item)))

    def find_person_other(self, obj):

        try:
            client = Clients.objects.filter(uid=obj.uid).get()
        except Clients.DoesNotExist as e:
            return "-"

        return self.create_url_for_client(client)

    find_person_other.short_description = 'Kund'


class NewsletterAdmin(admin.ModelAdmin):
    inlines = [NewsletterLinksInline]


admin.site.register(Visits, VisitsAdmin)
admin.site.register(Clients, ClientsAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
