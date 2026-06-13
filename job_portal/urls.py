from django.urls import path,include
from .import views
from .views import resume_analyzer


urlpatterns = [
    path('',views.auth,name='auth'),
    path('index',views.index,name='index'),
    path('about/',views.home,name='about'),
    path('home/',views.home,name='home'),
    path('job/',views.job,name='job'),
    path('companies/',views.companies,name='companies'),
    path('recruiters/',views.recruiters,name='recruiters'),
    path('apply/<int:job_id>/', views.apply, name='apply'),
    path('contact/',views.contact,name='contact'),
    path("resume-analyzer/",resume_analyzer,name="resume_analyzer"),
    path('add-job/', views.add_job, name='add_job'),
    path('home2/',views.home2,name='home2'),
    path('contact2/', views.contact2, name='contact2'),

    path('jobseeker/', views.jobseeker_auth, name='jobseeker_auth'),
    path('employer/', views.employer_auth, name='employer_auth'),
path('logout/', views.logout_user, name='logout'),

path(
    'applications/',
    views.applications,
    name='applications'
),
]

