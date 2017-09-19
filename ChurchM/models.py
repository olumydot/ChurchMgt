from django.db import models


# Create your models here.


class Ministry(models.Model):
    ADULT = "AD"
    YOUTH = "YT"
    YOUNG_ADULTS = "YA"
    CHILDREN = "CH"
    OTHER = "OT"
    MINISTRY_CHOICES = ((ADULT, "Adult"),
                        (YOUTH, "Youth"),
                        (YOUNG_ADULTS, "Young_Adults"),
                        (CHILDREN, "Children"),
                        (OTHER, "Other"))
    ministry = models.CharField(max_length=2, unique=False, blank=False, choices=MINISTRY_CHOICES,
                                default=ADULT,)
    Remarks = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.ministry + " " + self.Remarks

    class Meta:
        verbose_name_plural = "ministries"
        # verbose names should conventionally not be capitalized.. Django does that auto


class Role(models.Model):
    role = models.CharField(max_length=32, unique=True, blank=False)
    Remarks = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.role + " " + self.Remarks

    class Meta:
        verbose_name_plural = "roles"


class Household(models.Model):
    household = models.CharField(max_length=64, unique=True, blank=False)
    Remarks = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.household + " " + self.Remarks

    class Meta:
        verbose_name_plural = "households"


class EventType(models.Model):
    event_type = models.CharField(max_length=40, blank=False, unique=True, null=False)
    Remarks = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.event_type + " " + self.Remarks

    class Meta:
        verbose_name_plural = "event types"


class Event(models.Model):
    service_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    event_date = models.DateField()
    event_time_start = models.TimeField()
    event_end_time = models.TimeField()
    Remarks = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.service_type.event_type + " is on  " + str(self.event_date.strftime('%A %d %B %Y'))

    class Meta:
        verbose_name_plural = "events"


class BibleReading(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    bible_text = models.CharField(max_length=80, unique=False, blank=False)
    Remarks = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.bible_text + " is the bible reading text for " + str(self.event.event_date.strftime('%A %d %B %Y'))

    class Meta:
        verbose_name_plural = "bible readings"


class DonationType(models.Model):
    donation_type = models.CharField(max_length=16, unique=True, blank=False)
    Remarks = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.donation_type + " " + self.Remarks

    class Meta:
        verbose_name_plural = "donations type"


class Fund(models.Model):
    fund_type = models.CharField(max_length=16, unique=True, blank=False)
    Remarks = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.fund_type + " " + self.Remarks


class BankDetails(models.Model):
    bank_name = models.CharField(max_length=128, unique=True, blank=False)
    bank_add = models.TextField(max_length=256, unique=True)
    bank_email = models.EmailField(unique=False)
    bank_phone = models.CharField(max_length=10)
    Remarks = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.bank_name + " " + self.Remarks

    class Meta:
        verbose_name_plural = "bank details"


class AccountDetails(models.Model):
    bank_name = models.ForeignKey(BankDetails, on_delete=models.CASCADE)
    account_number = models.PositiveIntegerField(unique=True, blank=False)
    account_sort_code = models.PositiveIntegerField()
    account_balance = models.DecimalField(max_digits=8, decimal_places=2, blank=False,)
    Remarks = models.CharField(max_length=256, blank=True)

    def __str__(self):

        return "Account Number " + str(self.account_number) + " " + "has a balance of: " + str(self.account_balance)

    class Meta:
        verbose_name_plural = "account details"


class People(models.Model):
    MALE = "M"
    FEMALE = "F"
    SEX_CHOICES = (
        (MALE,"MALE"),
        (FEMALE, "FEMALE"),
    )
    firstname = models.CharField(unique=False, blank=False, max_length=128)
    lastname = models.CharField(unique=False, blank=False, max_length=128)
    lastname = models.CharField (unique=False, blank=True, max_length=128)
    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, unique=False)
    phone = models.CharField(max_length=10, unique=False, blank=True)
    email = models.CharField(max_length=60, unique=False, blank=True)
    house_address = models.TextField(max_length=256, blank=True, editable=True)
    ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    profile_img = models.ImageField(width_field=60, height_field=60)
    remarks = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.lastname + " " + self.firstname + "        " + self.house_address

    class Meta:
        verbose_name_plural = "people"


class Attendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    adult_male = models.IntegerField(blank=True)
    adult_female = models.IntegerField(blank=True)
    youth_male = models.IntegerField(blank=True)
    youth_female = models.IntegerField(blank=True)
    young_adults_male = models.IntegerField(blank=True)
    young_adults_female = models.IntegerField(blank=True)
    children = models.IntegerField(blank=True)
    total_male = models.IntegerField(default=0)
    total_female = models.IntegerField(default=0)
    total_attendance = models.IntegerField(default=0)

# redefining the save here makes sure that the calulations for the totals are made and the column updated

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.total_male:
            self.total_male = self.adult_male + self.youth_male + self.young_adults_male
        if not self.total_female:
            self.total_female = self.adult_female + self.youth_female + self.young_adults_female
        if not self.total_attendance:
            self.total_attendance = self.total_male + self.total_female + self.children
        return super(Attendance, self).save(force_insert=False, force_update=False, using=None,
                                            update_fields=None)

    def __str__(self):
        return "Total attendance last " + str(self.event.service_type) + str(self.event.event_date.strftime('%A %d %B %Y')) + " is " + str(self.total_attendance)

    class Meta:
        verbose_name_plural = "attendance"


class Project(models.Model):
    project_title = models.CharField(max_length=50, verbose_name="project")
    project_fund = models.ForeignKey(Fund, on_delete=models.CASCADE, verbose_name="Fund committed")

