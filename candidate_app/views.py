from django.shortcuts import render, redirect
from django.http import HttpResponse
from candidate_app.models import Candidate, CandidateDetail
from recruiter_app.models import JobDetail,Recruiter,JobApplied
from django.views.decorators.cache import never_cache
import smtplib
from email.mime.text import MIMEText

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
def candidate_signup(request):
  if request.method == "POST":
    username = request.POST.get("username")
    name = request.POST.get("fullname")
    email = request.POST.get("email")
    phone = request.POST.get("phone")
    password = request.POST.get("password")
    
    Candidate.objects.create(
      username=username,
      name = name,
      email = email,
      phone = phone,
      password = password
    )
    return redirect("candidate_login")
  else:
    return render(request,"./candidate_app/signup.html")
  
@never_cache
def candidate_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = Candidate.objects.filter(username=username, password=password).first()

        if user:

            sender = "Nehruraja9485@gmail.com"
            receiver = user.email
            gmail_password = "dxsy tboe iddq veks"
            message = "Login successful"
            subject = "Login Attempt"

            msg = MIMEText(message)
            msg["Subject"] = subject
            msg["From"] = sender
            msg["To"] = receiver

            request.session["candidate_id"] = user.id
            request.session["candidate_username"] = user.username
            request.session["candidate_name"] = user.name
            request.session["candidate_email"] = user.email
            request.session["candidate_phone"] = user.phone

            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(sender, gmail_password)
                server.send_message(msg)
                server.quit()
            except Exception as e:
                print(e)

            return redirect("candidate_dashboard")

        else:
            return redirect("candidate_login")

    else:
        return render(request, "./candidate_app/login.html")
@never_cache
def candidate_dashboard(request):
  if "candidate_username" not in request.session:
    return redirect("candidate_login")
  username = request.session.get("candidate_name")
  
  a = JobDetail.objects.all()
  return render(request,"./candidate_app/dashboard.html",{"username":username,"a":a})

@never_cache
def candidate_profile(request):
  if "candidate_username" not in request.session:
    return redirect("candidate_login")
  
  userid  = request.session.get("candidate_id")
  name = request.session.get("candidate_name")
  email = request.session.get("candidate_email")
  
  user = CandidateDetail.objects.filter(user_id = userid).first()
  
  if user:
    bio = user.bio
    address = user.address
    profile_pic  = user.profile_pic
  else:
    bio = None
    address = None
    profile_pic = None
  
  context = {"name":name,"email":email,"bio":bio,"address":address,"profile_pic":profile_pic}
  return render(request,"./candidate_app/profile.html",context)

@never_cache
def candidate_profile_update(request):
    if "candidate_username" not in request.session:
        return redirect("candidate_login")

    if request.method == "POST":
        bio = request.POST.get("bio")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        image = request.FILES.get("image")

        candidate_id = request.session.get("candidate_id")

        candidate = Candidate.objects.get(id=candidate_id)

        CandidateDetail.objects.update_or_create(
            user=candidate,
            defaults={
                "bio": bio,
                "address": address,
                "city": city,
                "state": state,
                "profile_pic": image
            }
        )

        return redirect("candidate_profile")

    return render(request, "./candidate_app/profile_update.html")
  
from recruiter_app.models import RecruiterDetail

@never_cache
def view_detail(request, id):
    if "candidate_username" not in request.session:
        return redirect("candidate_login")

    job = JobDetail.objects.select_related('recruiter').filter(id=id).first()

    recruiter_detail = RecruiterDetail.objects.filter(
        user=job.recruiter
    ).first()

    candidate_id = request.session.get("candidate_id")

    # ✅ check applied
    applied = JobApplied.objects.filter(
        candidate_id=candidate_id,
        job_detail=job
    ).exists()

    context = {
        "job": job,
        "recruiter": job.recruiter,
        "recruiter_detail": recruiter_detail,
        "applied": applied   # 👈 send to template
    }

    return render(request, "./candidate_app/view_detail.html", context)

from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.cache import never_cache

@never_cache
def apply_job(request, id):
    if "candidate_username" not in request.session:
        return redirect("candidate_login")

    candidate_id = request.session.get("candidate_id")

    candidate = get_object_or_404(Candidate, id=candidate_id)
    job = get_object_or_404(JobDetail, id=id)

    # ✅ Check duplicate
    if JobApplied.objects.filter(candidate=candidate, job_detail=job).exists():
        return redirect("candidate_dashboard")

    # ✅ Create application
    JobApplied.objects.create(
        job_detail=job,
        recruiter=job.recruiter,
        candidate=candidate,
        scheduled=False
    )

    return redirect("candidate_dashboard")

@never_cache
def scheduled(request):
    if "candidate_username" not in request.session:
        return redirect("candidate_login")

    userid = request.session.get("candidate_id")
    user = JobApplied.objects.filter(candidate=userid)

    for i in user:
        if i.scheduled and not i.email_sent:

            sender = "Nehruraja9485@gmail.com"
            receiver = i.candidate.email
            gmail_password = "gmdy cvqp ufsm erme"

            subject = "Interview Scheduled"

            message = f"""
Hello {i.candidate.name},

Your interview has been scheduled.

Company : {i.job_detail.company_name}
Role : {i.job_detail.job_role}
Location : {i.job_detail.job_location}

Recruiter will contact you soon.

Best Regards,
Job Portal Team
"""

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

                i.email_sent = True
                i.save()

            except Exception as e:
                print(e)

    return render(request, "./candidate_app/result.html", {"user": user})
  
@never_cache
def candidate_logout(request):
  request.session.flush()
  return redirect("candidate_login")



@never_cache
def applied_jobs(request):
    if "candidate_username" not in request.session:
        return redirect("candidate_login")

    candidate_id = request.session.get("candidate_id")

    jobs = JobApplied.objects.filter(candidate=candidate_id)

    return render(request, "./candidate_app/applied_jobs.html", {"jobs": jobs})