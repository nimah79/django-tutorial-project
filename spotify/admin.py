from django.contrib import admin


from spotify.models import User, Post


class PostInline(admin.StackedInline):
	model = Post


@admin.register(User)
class UserAmin(admin.ModelAdmin):
	list_display = ['id', 'username', 'gender', 'email']
	sortable_by = ['id', 'username', 'email']
	list_filter = ['gender']
	list_editable = ['email']
	search_fields = ['id', 'username', 'gender', 'email']
	readonly_fields = ['email']
	inlines = [PostInline]


admin.site.register(Post)
