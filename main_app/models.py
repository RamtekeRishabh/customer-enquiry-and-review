from django.db import models

# Create your models here.
class CustEnq(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    email = models.EmailField()
    query = models.CharField(max_length=500)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'

class EnqDtl(models.Model):
    enqno = models.ForeignKey(CustEnq,on_delete=models.CASCADE)
    qry_response = models.CharField(max_length=500,null=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Enquiry Details for {self.id}'

class Review(models.Model):
    # STAR_CHOICES = (
    #     ("0", "0"), ("1", "1"), ("2", "2"),
    #     ("3", "3"), ("4", "4"), ("5", "5"))
    # stars = models.Choices(choices = STAR_CHOICES,)
    enqno = models.ForeignKey(CustEnq, on_delete=models.CASCADE,null=True)
    rspno = models.ForeignKey(EnqDtl, on_delete=models.CASCADE,null=True)
    satisfied = models.CharField(max_length=10,null=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Customer Reviewed by {self.rspno.enqno.name}'
