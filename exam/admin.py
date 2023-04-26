from django.contrib import admin
from .models import (CourseModel,
                     StreamModel,
                     SubStreamModel,
                     QuestionModel)

# Register your models here.

admin.site.register(CourseModel)
admin.site.register(StreamModel)
admin.site.register(SubStreamModel)
admin.site.register(QuestionModel)
