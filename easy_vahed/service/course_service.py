from easy_vahed.models import Course
from core.models import Student

class CourseService:
    
    @classmethod
    def take_course(cls,student_id: int,course_name: str):
        student = Student.objects.get(student_id=student_id)
        course  = Course.objects.get(name = course_name)
        if cls.isValid(cls,student,course.unit):
            Course.students.add(student)
        # error
        else:
            pass
        
    @classmethod
    def remove_course(cls,student_id: int,course_name: str):
        student = Student.objects.get(student_id=student_id)
        Course.students.remove(student)
        
    @classmethod
    def get_courses(cls,student_id: int):
        student = Student.objects.get(student_id=student_id)
        return Course.objects.filter(students=student)
    
    @classmethod
    def get_all_courses(cls):
        return Course.objects.all()
    
    @classmethod
    def isValid(cls,student: Student,course_unit: int) -> bool:
        courses = Course.objects.filter(students=student)
        units = course_unit
        for course in courses:
            units += course.unit
        if units<=20:
            return True
        elif units>20 and student.gpa>17:
            return True
        return False