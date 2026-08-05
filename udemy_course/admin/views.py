from udemy_course.db.models import UserProfile, Category, Course, Lesson, Review
from sqladmin import ModelView


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.first_name, UserProfile.last_name]

class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]

class CourseAdmin(ModelView, model=Course):
    column_list = [Course.course_name, Course.level]

class LessonAdmin(ModelView, model=Lesson):
    column_list = [Lesson.title, Lesson.content]

class ReviewAdmin(ModelView, model=Review):
    column_list = [Review.stars, Review.text]
