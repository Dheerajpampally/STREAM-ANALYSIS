from django.shortcuts import render, redirect, reverse
from django.db.models import Q, Count
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test, login_required

from .models import CourseModel, StreamModel, SubStreamModel, QuestionModel, ScoreModel
from counsellor_agent.models import CounsellorNotification
from accounts.models import UserAccounts


# Create your views here.


@login_required
@user_passes_test(lambda u: u.is_student)
def pick_exam_stream(request):
    if request.method == "POST":
        course = request.POST.get("course")
        stream = request.POST.get("stream")
        if not stream:
            stream = "null"

        return redirect(reverse("exam:testpage", kwargs={"course": course, "stream": stream}))

    else:
        courses = CourseModel.objects.all()
        streams = courses[0].streammodel_set.all()

        context = {"courses": courses, "streams": streams}
        return render(request, "exam/pick_stream.html", context)


@login_required
@user_passes_test(lambda u: u.is_student)
def get_stream_from_course(request, id):
    course = CourseModel.objects.get(id=id)
    streams = course.streammodel_set.all().values("id", "name")
    return JsonResponse(list(streams), safe=False)


@login_required
@user_passes_test(lambda u: u.is_student)
def get_substream_from_stream(request, id):
    stream = StreamModel.objects.get(id=id)
    substreams = stream.substreammodel_set.all().values("id", "name")
    return JsonResponse(list(substreams), safe=False)


@login_required
@user_passes_test(lambda u: u.is_student)
def exam_view(request, course, stream):
    if stream == "null":
        stream = ""

    if request.method == "POST":
        answers = request.POST.dict()
        answers.pop("csrfmiddlewaretoken")

        answers = {int(qsn[1:]): anw for qsn, anw in answers.items()}
        print(answers)

        questions = QuestionModel.objects.filter(id__in=answers)

        score = 0
        main_stream = {}
        sub_stream = {}

        for q in questions:

            if q.answer == answers[q.id]:
                score += 1

                if q.sub_stream:
                    if sub_stream.get(q.sub_stream.id):
                        sub_stream[q.sub_stream.id] += 1
                    else:
                        sub_stream[q.sub_stream.id] = 1

                else:
                    if main_stream.get(q.main_stream.id):
                        main_stream[q.main_stream.id] += 1
                    else:
                        main_stream[q.main_stream.id] = 1

        if sub_stream:
            max_key = max(sub_stream, key=sub_stream.get)
            stream = SubStreamModel.objects.get(id=max_key)
        else:
            stream = questions[0].sub_stream

        score_obj = ScoreModel(student=request.user, score=score, out_of=len(questions), top_stream=stream)
        score_obj.save()

        counsellor = UserAccounts.objects.filter(is_counsellor=True).order_by("-last_login").first()
        print("counsellor", counsellor)
        if counsellor:
            CounsellorNotification.objects.create(score=score_obj, counsellor=counsellor)

        return redirect("exam:exam_completed")

    else:
        if course and not stream:
            questions = QuestionModel.objects.filter(main_stream__course__id=course)
        elif course and stream:
            questions = QuestionModel.objects.filter(main_stream__id=stream)

        return render(request, "exam/test_page.html", {"questions": questions})


@login_required
@user_passes_test(lambda u: u.is_student)
def exam_completed(request):
    return render(request, "exam/finished_exam.html")


@login_required
@user_passes_test(lambda u: u.is_student)
def exam_history(request):
    history = ScoreModel.objects.filter(student = request.user)
    return render(request, "exam/test_history.html", {'history': history})
