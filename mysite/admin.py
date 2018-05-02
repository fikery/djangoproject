from django.contrib import admin
from . import models
# Register your models here.


class PollAdmin(admin.ModelAdmin):
    list_display = ('name','created_at','enabled')
    ordering = ('-created_at',)
    #保存当前登录用户名作为作者
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.auther=request.user.username
            obj.save()

class PollItemAdmin(admin.ModelAdmin):
    list_display = ('poll','name','vote','image_url')
    ordering = ('poll',)

admin.site.register(models.Poll,PollAdmin)
admin.site.register(models.PollItem,PollItemAdmin)
admin.site.register(models.VoteCheck)