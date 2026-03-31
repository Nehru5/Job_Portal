from django.db import models
from django.core.validators import FileExtensionValidator

class Candidate(models.Model):
  username = models.CharField(max_length=200)
  name = models.CharField(max_length=200)
  email = models.EmailField()
  phone = models.PositiveBigIntegerField()
  password = models.CharField(max_length=200)
  
  def __str__(self):
    return self.name

class CandidateDetail(models.Model):
  user = models.OneToOneField(Candidate,on_delete=models.CASCADE)
  bio = models.TextField()
  address = models.TextField()
  city = models.CharField(max_length=200)
  state = models.CharField(max_length=200)
  pincode = models.CharField(max_length=50)
  country = models.CharField(max_length=200)
  profile_pic = models.ImageField(upload_to="candidatedp/",null=True)
  resume = models.FileField(
    upload_to="resume/",null=True,
    validators=[FileExtensionValidator(allowed_extensions=["pdf"])]
    )
  
  def __str__(self):
    return self.user.name
