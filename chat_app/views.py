from chat_app.models import Message
from recruiter_app.models import JobApplied
from django.shortcuts import redirect,render
from django.utils.timezone import localtime

def chat_view(request, id):
    application = JobApplied.objects.get(id=id)
    messages = application.messages.all().order_by("timestamp")

    # detect user type
    if "candidate_username" in request.session:
        user_type = "candidate"
    elif "recruiter_username" in request.session:
        user_type = "recruiter"
    else:
        return redirect("homepage")

    return render(request, "./chat_app/chat.html", {
        "application": application,
        "messages": messages,
        "user_type": user_type
    })
    
def send_message(request, id):
    application = JobApplied.objects.get(id=id)
    msg = request.POST.get("message")

    if not msg:
        return redirect("chat_view", id=id)

    if "candidate_username" in request.session:
        Message.objects.create(
            application=application,
            sender_type="candidate",
            candidate_id=request.session.get("candidate_id"),
            recruiter=application.recruiter,
            message=msg
        )

    elif "recruiter_username" in request.session:
        Message.objects.create(
            application=application,
            sender_type="recruiter",
            recruiter_id=request.session.get("recruiter_id"),
            candidate=application.candidate,
            message=msg
        )

    return redirect("chat_view", id=id)
  
  
  
from django.http import JsonResponse
from django.http import JsonResponse
from chat_app.models import Message
from recruiter_app.models import JobApplied

def get_messages(request, id):
    application = JobApplied.objects.get(id=id)
    messages = application.messages.all().order_by("timestamp")

    data = []

    for msg in messages:
        data.append({
            "sender": msg.sender_type,
            "message": msg.message,
            "time": localtime(msg.timestamp).strftime("%d %b %I:%M %p")
        })

    return JsonResponse({"messages": data})