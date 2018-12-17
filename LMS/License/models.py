from _decimal import Decimal

from django.core.validators import RegexValidator
from django.db import models


# class Test(models.Model):
#     Name = models.CharField(max_length=255, default='', blank=True, null=False)
#     Email = models.EmailField(max_length=255, unique=True)
#
#     class Meta:
#         db_table = 'test-check'
#         ordering = ('Name',)
#
#     def __str__(self):
#         return self.Name


class Company(models.Model):
    phone = RegexValidator(r'^((\+92)|(0092))-{0,1}\d{3}-{0,1}\d{7}$|^\d{11}$|^\d{4}-\d{7}$')
    email = models.EmailField(unique=True, blank=False, null=False, max_length=254)
    name = models.CharField(max_length=254, blank=False, null=False)
    address = models.CharField(max_length=509, default='')
    contact_person = models.CharField(max_length=254, default='')
    contact_no = models.CharField(max_length=254, default='', validators=[phone])
    logo = models.ImageField(upload_to='company_logo', blank=False)

    class Meta:
        db_table = 'company'
        ordering = ('name',)

    def __str__(self):
        return self.name


class License(models.Model):
    price = RegexValidator(r'^(\d+)(\.00)')
    percent = RegexValidator(r'd{2}')
    subscription_start_date = models.DateField()
    subscription_end_date = models.DateField()
    charges = models.DecimalField(blank=False, null=False, default=0.00, validators=[price], max_digits=9, decimal_places=2)
    centangle_percentage = models.IntegerField(blank=False, null=False, validators=[percent])

    class Meta:
        db_table = 'license'
        ordering = ('charges',)

    def __str__(self):
        return "{0} - {1} - {2}".format(self.subscription_start_date, self.subscription_end_date, self.centangle_percentage)


class Branch(models.Model):
    companyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    licenseID = models.OneToOneField(License, on_delete=models.CASCADE)
    branch_name = models.CharField(max_length=254, null=False, blank=False)
    branch_location = models.CharField(max_length=254, default='')
    branch_address = models.CharField(max_length=254, default='')

    class Meta:
        db_table = 'branch'
        ordering = ('branch_name',)

    def __str__(self):
        return self.branch_name


class Service(models.Model):
    price = RegexValidator(r'^(\d+)(\.00)')
    branchID = models.ForeignKey(Branch, on_delete=models.CASCADE, parent_link=True)
    name = models.CharField(max_length=254, blank=False, default=False)
    charges = models.DecimalField(blank=False, null=False, default=0.00, validators=[price], max_digits=9,
                                  decimal_places=2)

    class Meta:
        db_table = 'service'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Report(models.Model):
    price = RegexValidator(r'^(\d+)(\.00)')
    branchID = models.ForeignKey(Branch, on_delete=models.CASCADE)
    nol = models.IntegerField(default=0, blank=True, null=True)
    cylc = models.DecimalField(validators=[price], default=0.00, max_digits=9, decimal_places=2)
    paid_cylc = models.BooleanField(default=False)
    tottic = models.DecimalField(validators=[price], default=0.00, max_digits=9, decimal_places=2)
    paid_tottic = models.BooleanField(default=False)

    class Meta:
        db_table = 'report'
        ordering = ('nol',)

    def __str__(self):
        return "{0} - {1} - {2}".format(self.licenseID, self.cylc, self.paid_cylc)


# class Payment(models.Model):
#     payment_amount = models.DecimalField()
#     payment_medium = models.CharField(max_length=255)
#     payment_date = models.DateField()
#
#     class Meta:
#         db_table = 'payment'
#         ordering = ('amount',)
#
#     def __str__(self):
#         return "{0} - {1}".format(self.payment_amount, self.payment_medium)

