class Course():

    def __init__(self,course="",prof="",classroom="",type=""):
        self.course = course
        self.prof = prof
        self.classroom = classroom
        self.type = type
        self.set_color()

    
    @property 
    def course(self):
        return self._course
    
    @course.setter
    def course(self,course):
        if not course or course.isspace():
            raise ValueError("Invalid course name ")
        self._course = course
    
    @property
    def prof(self):
        return self._prof
    
    @prof.setter
    def prof(self,prof):
        if not prof or prof.isspace():
            raise ValueError("Invalid professor name")
        self._prof = prof
    
    @property
    def classroom(self):
        return self._classroom
    
    @classroom.setter
    def classroom(self,classroom):
        if not classroom or classroom.isspace():
            raise ValueError("Invalid classroom")
        self._classroom = classroom
    
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self,type):
        if type not in ["C","TD","TP","CI"]:
            raise ValueError("Invalid Course type")
        self._type = type
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self,color):
        if not color or color.isspace():
            ValueError("Invalid color value")
        self._color = color

    def set_color(self):
        if self._type == "C":
            self._color = "FB6266"
        elif self._type == "TD":
            self._color = "80FF80"
        elif self._type =="TP":
            self._color = "7D7DFF"
        elif self._type =="CI":
            self._color = "868686"
        else:
            self._color = "F0F0F0"
    
    def __eq__(self,other):
        if isinstance(other,Course):
            return self.course == other.course and self.prof == other.prof and self.classroom == other.classroom and self.type == other.type
        return False
        
    def __str__(self):
        return f"course: {self.course} professor: {self.prof} classroom: {self.classroom} course type: {self.type}"

