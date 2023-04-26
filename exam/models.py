from django.db import models
# from django.contrib.auth import get_user_model

# Create your models here.


class CourseModel(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class StreamModel(models.Model):
    course = models.ForeignKey(CourseModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class SubStreamModel(models.Model):
    stream = models.ForeignKey(StreamModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


answer_choices = [("1", "Option 1"), ("2", "Option 2"), ("3", "Option 3"), ("4", "Option 4")]


class QuestionModel(models.Model):
    main_stream = models.ForeignKey(StreamModel, on_delete=models.DO_NOTHING)
    sub_stream = models.ForeignKey(SubStreamModel, on_delete=models.DO_NOTHING, null=True)
    question = models.TextField()
    option_one = models.CharField(max_length=100)
    option_two = models.CharField(max_length=100)
    option_three = models.CharField(max_length=100)
    option_four = models.CharField(max_length=100)
    answer = models.CharField(max_length=20, choices=answer_choices)

    def __str__(self):
        return self.question + f" ({self.main_stream})"


class ScoreModel(models.Model):
    student = models.ForeignKey('accounts.UserAccounts', on_delete=models.CASCADE)
    score = models.IntegerField()
    out_of = models.IntegerField()
    top_stream = models.ForeignKey(SubStreamModel, on_delete=models.CASCADE)
    exam_date = models.DateTimeField(auto_now_add=True)
