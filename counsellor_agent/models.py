from django.db import models


# Create your models here.


class CounsellorNotification(models.Model):
    score = models.ForeignKey("exam.ScoreModel", on_delete=models.DO_NOTHING)
    counsellor = models.ForeignKey("accounts.UserAccounts", on_delete=models.CASCADE)
    notified_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    @classmethod
    def unread_available(cls):
        count = cls.objects.filter(read=False).count()
        return bool(count)


class AgentNotification(models.Model):
    score = models.ForeignKey("exam.ScoreModel", on_delete=models.DO_NOTHING)
    counsellor = models.ForeignKey("accounts.UserAccounts", on_delete=models.DO_NOTHING, related_name="counsellor")
    agency = models.ForeignKey("accounts.UserAccounts", on_delete=models.CASCADE, related_name="agency")
    notified_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    @classmethod
    def unread_available(cls):
        count = cls.objects.filter(read=False).count()
        return bool(count)


class StudentNotification(models.Model):
    student = models.ForeignKey("accounts.UserAccounts", on_delete=models.CASCADE, related_name="student")
    agency = models.ForeignKey("accounts.UserAccounts", on_delete=models.DO_NOTHING, related_name="student_agency")
    college = models.ForeignKey("counsellor_agent.CollegeModel", on_delete=models.DO_NOTHING)
    notified_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)


class Chat(models.Model):
    sender = models.ForeignKey("accounts.UserAccounts", on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey("accounts.UserAccounts", on_delete=models.CASCADE, related_name="receiver")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class CollegeModel(models.Model):
    name = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    sub_streams = models.ManyToManyField("exam.SubStreamModel", verbose_name="Courses")

    def __str__(self):
        return self.name