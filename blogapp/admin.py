from django.contrib import admin
from .models import Post,Tag,Comment,Subscribe,Profile,WebsiteMeta
# Register your models here.
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Subscribe)
admin.site.register(WebsiteMeta)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_img', 'bio', 'slug']

admin.site.register(Profile, ProfileAdmin)