from django.contrib.admin import AdminSite
from .models import Poll, Question, Choice, Vote
from django.contrib import admin


class MyAdminSite(AdminSite): #настроим сортировку моделей в ручном порядке
    def get_app_list(self, request):
        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        return app_list


class ModelPollAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return['start_date']
        return self.readonly_fields


admin.site = MyAdminSite()

admin.site.register(Poll, ModelPollAdmin)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Vote)



admin.site.site_title = 'Опросник'
admin.site.site_header = 'Опросник'
admin.site.index_title = 'Опросник'
