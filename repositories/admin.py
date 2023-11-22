from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'website', 'saved_repositories_count')  # Add 'saved_repositories_count' here

    def saved_repositories_count(self, obj):
        return obj.saved_repositories.count()  # Show the count of saved repositories

    saved_repositories_count.short_description = 'Saved Repositories Count'  # Customizes the column header

admin.site.register(UserProfile, UserProfileAdmin)
