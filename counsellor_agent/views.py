from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from django.db.models import Q
from .models import Chat, CounsellorNotification, AgentNotification, CollegeModel, StudentNotification
from accounts.models import UserAccounts, AgencyDetail
from exam.models import CourseModel, ScoreModel, SubStreamModel

# Create your views here.


@login_required
def chat_home(request):
    chats = Chat.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    chats = set([i.sender for i in chats] + [i.receiver for i in chats])
    try:
        chats.remove(request.user)
    except:
        pass
    return render(request, "counsellor_agent/chat_home.html", {"chats": chats})


@login_required
def chat_box(request, id):
    user_data = UserAccounts.objects.get(id=id)
    if request.method == "POST":
        message = request.POST["message"]
        if message != "":
            Chat.objects.create(sender=request.user, receiver=user_data, message=message)
        return redirect(reverse("counsellor_agent:chat_box", kwargs={"id": id}))
    chats = Chat.objects.filter(
        Q(sender=request.user, receiver=user_data) | Q(sender=user_data, receiver=request.user)
    ).order_by("created_at")
    return render(request, "counsellor_agent/chat_box.html", {"user_data": user_data, "chats": chats})


@login_required
@user_passes_test(lambda u: u.is_counsellor)
def counsellor_mark_as_read(request, id):
    notification = CounsellorNotification.objects.get(id=id)
    notification.read = True
    notification.save()
    return redirect("home")


@login_required
@user_passes_test(lambda u: u.is_agent)
def agency_mark_as_read(request, id):
    notification = AgentNotification.objects.get(id=id)
    notification.read = True
    notification.save()
    return redirect("home")


@login_required
@user_passes_test(lambda u: u.is_counsellor)
def select_agent(request, score):
    course = request.GET.get("course")
    courses = CourseModel.objects.all()

    if course is None or course == "":
        agencies = AgencyDetail.objects.all()
    else:
        agencies = AgencyDetail.objects.filter(courses__id=course)
    return render(
        request, "counsellor_agent/select_agent.html", {"agencies": agencies, "courses": courses, "score": score}
    )


@login_required
@user_passes_test(lambda u: u.is_counsellor)
def select_agent_complete(request, score, id):
    agency = UserAccounts.objects.get(id=id)
    score_obj = ScoreModel.objects.get(id=score)
    AgentNotification.objects.create(score=score_obj, counsellor=request.user, agency=agency)

    return render(request, "counsellor_agent/select_agent_completed.html")


@login_required
@user_passes_test(lambda u: u.is_counsellor)
def counsellor_notifications(request):
    notifications = CounsellorNotification.objects.filter(counsellor=request.user)
    return render(request, "counsellor_agent/counsellor_notifications.html", {"notifications": notifications})


@login_required
@user_passes_test(lambda u: u.is_agent)
def agency_notifications(request):
    notifications = AgentNotification.objects.filter(agency=request.user)
    return render(request, "counsellor_agent/agency_notifications.html", {"notifications": notifications})


@login_required
@user_passes_test(lambda u: u.is_agent)
def select_college(request, score):
    course = request.GET.get("course")
    courses = SubStreamModel.objects.all()

    if course is None or course == "":
        colleges = CollegeModel.objects.all()
    else:
        colleges = CollegeModel.objects.filter(sub_streams__id=course)
    return render(
        request, "counsellor_agent/select_college.html", {"colleges": colleges, "courses": courses, "score": score}
    )


@login_required
@user_passes_test(lambda u: u.is_agent)
def select_college_complete(request, score, id):
    college = CollegeModel.objects.get(id=id)
    score_obj = ScoreModel.objects.get(id=score)
    student = score_obj.student

    StudentNotification.objects.create(student=student, college=college, agency=request.user)
    return render(request, "counsellor_agent/select_college_completed.html")
