from django.db import models
from candidate_app.models import Candidate

class Recruiter(models.Model):
  username = models.CharField(max_length=200)
  name = models.CharField(max_length=200)
  email = models.EmailField()
  phone = models.PositiveBigIntegerField()
  password = models.CharField(max_length=200)
  
  def __str__(self):
    return self.name
  
class RecruiterDetail(models.Model):
  user = models.OneToOneField(Recruiter,on_delete=models.CASCADE)
  bio = models.TextField()
  address = models.TextField()
  city = models.CharField(max_length=200)
  state = models.CharField(max_length=200)
  pincode = models.CharField(max_length=50)
  country = models.CharField(max_length=200)
  profile_pic = models.ImageField(upload_to="recruiterdp/",null=True)
  
  def __str__(self):
    return self.user.name
  
  
class JobDetail(models.Model):
  recruiter = models.ForeignKey(Recruiter,on_delete=models.CASCADE)
  company_name = models.CharField(max_length=200)
  company_address = models.TextField()
  company_image = models.ImageField(upload_to="companyimage/",null=True)
  job_role = models.CharField(max_length=200)
  skills_required = models.TextField()
  job_decription = models.TextField()
  salary_range = models.CharField(max_length=200)
  experience_rqeuired = models.CharField(max_length=200)
  qualifications = models.CharField(max_length=200)
  vacancy = models.CharField(max_length=100)
  job_location = models.CharField(max_length=200)
  employment_type = models.CharField(max_length=200)
  industry_type = models.CharField(max_length=200)
  job_posted_on = models.DateField(auto_now_add=True)
  last_date = models.DateField()
  hiring_process = models.TextField()
  
  def __str__(self):
    return self.job_role
  
class JobApplied(models.Model):
  job_detail = models.ForeignKey(JobDetail,on_delete=models.CASCADE)
  recruiter = models.ForeignKey(Recruiter,on_delete=models.CASCADE)
  candidate = models.ForeignKey(Candidate,on_delete=models.CASCADE)
  scheduled = models.BooleanField(default=False)
  email_sent = models.BooleanField(default=False)
  
  def __str__(self):
    return f"{self.candidate.name} applied for {self.job_detail.job_role}"
  