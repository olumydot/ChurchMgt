from django.contrib import admin
from ChurchM.models import Ministry, Role, Household, BibleReading, Event, EventType, People, DonationType, Fund, BankDetails, AccountDetails, Attendance
# Register your models here.

admin.site.register(Ministry)
admin.site.register(Role)
admin.site.register(Household)
admin.site.register(BibleReading)
admin.site.register(DonationType)
admin.site.register(Fund)
admin.site.register(BankDetails)
admin.site.register(AccountDetails)
admin.site.register(People)
admin.site.register(Event)
admin.site.register(EventType)
admin.site.register(Attendance)



