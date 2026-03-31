from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from recruiter_app.models import Recruiter,RecruiterDetail,JobDetail,JobApplied
import smtplib
from email.mime.text import MIMEText
def homepage(request):
  return render(request,"./recruiter_app/home.html")
def page_not_found(request, invalid_path=None):
    return render(request, "./recruiter_app/404.html")
def send_email(receiver, subject, message):

    sender = "Nehruraja9485@gmail.com"
    gmail_password = "dxsy tboe iddq veks"

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, gmail_password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(e)
def recruiter_signup(request):
  if request.method == "POST":
    username = request.POST.get("username")
    name = request.POST.get("fullname")
    email = request.POST.get("email")
    phone = request.POST.get("phone")
    password = request.POST.get("password")
    
    Recruiter.objects.create(
      username=username,
      name = name,
      email = email,
      phone = phone,
      password = password
    )

    # Email Send
    subject = "Recruiter Account Created"
    message = f"""
Hello {name},

Your recruiter account has been successfully created.

Username : {username}
Email : {email}

You can now login and start posting jobs.

Best Regards,
Job Portal Team
"""

    send_email(email, subject, message)

    return redirect("recruiter_login")

  else:
    return render(request,"./recruiter_app/signup.html")

def recruiter_login(request):
  if request.method == "POST":
    username = request.POST.get("username")
    password = request.POST.get("password")
    
    user = Recruiter.objects.filter(username = username,password = password).first()
    
    if user:
      request.session["recruiter_id"] = user.id
      request.session["recruiter_username"] = user.username
      request.session["recruiter_name"] = user.name
      request.session["recruiter_email"] = user.email
      request.session["recruiter_phone"] = user.phone

      # Email Send
      subject = "Recruiter Login Alert"
      message = f"""
Hello {user.name},

You have successfully logged into your recruiter account.

Username : {user.username}

If this was not you, please change your password immediately.

Best Regards,
Job Portal Team
"""

      send_email(user.email, subject, message)

      return redirect("recruiter_dashboard")
    else:
      return redirect("recruiter_login")

  else:
    return render(request,"./recruiter_app/login.html")


def recruiter_dashboard(request):
  if "recruiter_username" not in request.session:
    return redirect("recruiter_login")
  username = request.session.get("recruiter_name")
  return render(request,"./recruiter_app/dashboard.html",{"username":username})


def recruiter_profile(request):
  if "recruiter_username" not in request.session:
    return redirect("recruiter_login")
  
  userid  = request.session.get("recruiter_id")
  name = request.session.get("recruiter_name")
  email = request.session.get("recruiter_email")
  
  user = RecruiterDetail.objects.filter(user_id = userid).first()
  
  if user:
    bio = user.bio
    address = user.address
    profile_pic  = user.profile_pic
  else:
    bio = None
    address = None
    profile_pic = None
  
  context = {"name":name,"email":email,"bio":bio,"address":address,"profile_pic":profile_pic}
  return render(request,"./recruiter_app/profile.html",context)

def recruiter_profile_update(request):
  if "recruiter_username" not in request.session:
    return redirect("recruiter_login")
  
  if request.method == "POST":
    bio = request.POST.get("bio")
    address = request.POST.get("address")
    city = request.POST.get("city")
    state = request.POST.get("state")
    image = request.FILES.get("image")
    
    id = request.session.get("recruiter_id")
    recruiter_id = Recruiter.objects.filter(id = id).first()
    
    RecruiterDetail.objects.update_or_create(
      user = recruiter_id,
      defaults={
        "bio":bio,
        "address":address,
        "city":city,
        "state":state,
        "profile_pic":image
      }
    )
    return redirect("recruiter_profile")
  else:
    return render(request,"./recruiter_app/profile_update.html")
  
  
def job_details(request):
  if "recruiter_username" not in request.session:
    return redirect(recruiter_login)
  id = request.session.get("recruiter_id")
  recruiter = Recruiter.objects.filter(id = id).first()
  
  if request.method == "POST":
    company_name = request.POST.get("company_name")
    company_address = request.POST.get("company_address")
    company_image = request.FILES.get("company_image")
    job_role = request.POST.get("job_role")
    job_description = request.POST.get("job_description")
    skills = request.POST.get("skills")
    salary = request.POST.get("salary")
    experience = request.POST.get("experience")
    qualification = request.POST.get("qualification")
    vacancy = request.POST.get("vacancy")
    employment_type = request.POST.get("employment_type")
    location = request.POST.get("location")
    industry = request.POST.get("industry")
    job_posted = request.POST.get("job_posted")
    last_date = request.POST.get("last_date")
    hiring_process = request.POST.get("hiring_process")
    
    JobDetail.objects.create(
      recruiter=recruiter,
      company_name = company_name,
      company_address = company_address,
      company_image = company_image,
      job_role = job_role,
      skills_required = skills,
      job_decription = job_description,
      salary_range = salary,
      experience_rqeuired = experience,
      qualifications = qualification,
      vacancy = vacancy,
      job_location = location,
      employment_type = employment_type,
      industry_type = industry,
      job_posted_on = job_posted,
      last_date = last_date,
      hiring_process = hiring_process
    )
    return redirect("recruiter_dashboard")
  else:
    return render(request,"./recruiter_app/job_detail.html")
  
  
def applied_job(request):
  if "recruiter_username" not in request.session:
    return redirect("recruiter_login")
  
  recruiter_id = request.session.get("recruiter_id")

  jobs = JobApplied.objects.filter(recruiter = recruiter_id)
  return render(request,"./recruiter_app/applied_job.html",{"a":jobs})


def approve(request,id):
  if "recruiter_username" not in request.session:
    return redirect("recruiter_login")
  
  job = get_object_or_404(JobApplied,id = id)
  job.scheduled = True
  job.save()
  return redirect("recruiter_dashboard")
  
  
  
  

def recruiter_logout(request):
  request.session.flush()
  return redirect("recruiter_login")
  
  
      
    
