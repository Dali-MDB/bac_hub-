from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

#fields enum
class Field(models.TextChoices):
    EXPERIMENTAL_SCIENCES = 'علوم تجريبية', 'علوم تجريبية'
    MATHEMATICS = 'رياضيات', 'رياضيات'
    TECHNICAL_MATHEMATICS = 'تقني رياضي', 'تقني رياضي'
    MANAGEMENT_ECONOMICS = 'تسيير و اقتصاد', 'تسيير و اقتصاد'
    LITERATURE_PHILOSOPHY = 'آداب و فلسفة', 'آداب و فلسفة'
    FOREIGN_LANGUAGES = 'لغات أجنبية', 'لغات أجنبية'



#profile
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    field = models.CharField(max_length=21,choices=Field.choices)
    city = models.CharField(max_length=30,null=True,blank=True)
    school_name = models.CharField(max_length=30,null=True,blank=True)
    xp = models.IntegerField(default=0)

    def __str__(self):
        return self.user.email



#subject model
class Subject(models.Model):
    name = models.CharField(max_length=30)
    field = MultiSelectField(max_length=100,choices=Field.choices)
    coefficient = models.IntegerField()

    def __str__(self):
        return f'{self.name} - {self.field}'
    

#resource type enum
class ResourceType(models.TextChoices):
    TEXT_BOOKS = 'TEXT_BOOKS','TEXT_BOOKS'
    NOTES = 'NOTES','NOTES'
    VIDEO = 'VIDEO','VIDEO'
    SUMMARY = 'SUMMARY','SUMMARY'
    EXAM = 'EXAM','EXAM'


#resources model
class Resource(models.Model):
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='resources')
    name = models.CharField(max_length=100)
    description = models.TextField()
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='resources')
    type = models.CharField(max_length=20,choices=ResourceType.choices)
    labels = models.CharField(max_length=100)
    link = models.URLField(unique=True)
    additional_link = models.URLField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reports = models.IntegerField(default=0)


    def add_report(self):   #reporting an unwanted content
        self.reports+=1
        if self.reports > 5:
            self.delete()
            return 0
        return self.reports

    def __str__(self):
        return f'{self.name} - {self.subject} - {self.created_at}'
    
    

#question model
class Question(models.Model):
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='questions')
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='questions')
    content = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    reports = models.IntegerField(default=0)


    def add_report(self):   #reporting an unwanted content
        self.reports+=1
        if self.reports > 5:
            self.delete()
            return 0
        return self.reports

    def __str__(self):
        return f'question by : {self.author} - {self.subject} - {self.date_posted}'
    

#images of a question
class ImageQuestion(models.Model):
    img = models.ImageField(upload_to='images/')
    question = models.ForeignKey(Question,on_delete=models.CASCADE)



#reply model
class Reply(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='question')
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='replies')
    content = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    reports = models.IntegerField(default=0)

    def add_report(self):   #reporting an unwanted content
        self.reports+=1
        if self.reports > 5:
            self.delete()
            return 0
        return self.reports
    
    def __str__(self):
        return f'Reply by {self.author} - {self.date_posted}'
    
    class Meta:
        verbose_name_plural = 'Replies'



#images of a reply
class ImageReply(models.Model):
    img = models.ImageField(upload_to='images/')
    reply = models.ForeignKey(Reply,on_delete=models.CASCADE)
    

