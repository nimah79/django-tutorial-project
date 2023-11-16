from django.contrib import admin, messages


from spotify.models import Post


class PostInline(admin.StackedInline):
    model = Post


# @admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "gender", "email"]
    sortable_by = ["id", "username", "email"]
    list_filter = ["gender"]
    # list_editable = ['email']
    search_fields = ["id", "username", "gender", "email"]
    readonly_fields = ["email"]
    inlines = [PostInline]
    actions = [
        "set_gender_to_female",
        "set_gender_to_male",
    ]

    def set_gender_to_female(self, request, queryset):
        self._set_gender(request, queryset, "f", "female")

    def set_gender_to_male(self, request, queryset):
        self._set_gender(request, queryset, "m", "male")

    def _set_gender(self, request, queryset, gender_value, gender_label):
        updated_rows_count = queryset.update(gender=gender_value)
        self.message_user(
            request,
            f"Gender of {updated_rows_count} users has been set to {gender_label}.",
            messages.SUCCESS,
        )


admin.site.register(Post)
