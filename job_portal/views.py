from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage

from .models import Job, Company, Application, UserProfile
from .utils import extract_text_from_pdf, clean_text, find_missing_skills


# ---------------- AUTH SELECTION PAGE ----------------
def auth(request):
    if request.method == "POST":
        account_type = request.POST.get("account_type")

        if account_type == "jobseeker":
            return redirect('jobseeker_auth')
        elif account_type == "employer":
            return redirect('employer_auth')

    return render(request, 'auth.html')


# ---------------- JOBSEEKER AUTH ----------------
def jobseeker_auth(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        action = request.POST.get("action")

        # LOGIN
        if action == "login":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user:
                if hasattr(user, "userprofile") and user.userprofile.role == "jobseeker":
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, "Not a Job Seeker account")
            else:
                messages.error(request, "Invalid username or password")

        # SIGNUP
        elif action == "signup":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )

                UserProfile.objects.create(user=user, role='jobseeker')

                messages.success(request, "Account created successfully")

    return render(request, "jobseeker_auth.html")


# ---------------- EMPLOYER AUTH ----------------
def employer_auth(request):

    if request.user.is_authenticated:
        return redirect('home2')

    if request.method == "POST":
        action = request.POST.get("action")

        # LOGIN
        if action == "login":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user:
                if hasattr(user, "userprofile") and user.userprofile.role == "employer":
                    login(request, user)
                    return redirect('home2')
                else:
                    messages.error(request, "Not an Employer account")
            else:
                messages.error(request, "Invalid username or password")

        # SIGNUP
        elif action == "signup":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )

                UserProfile.objects.create(user=user, role='employer')

                messages.success(request, "Employer account created successfully")

    return render(request, "employer_auth.html")


# ---------------- COMMON LOGOUT ----------------
def logout_user(request):
    logout(request)
    return redirect('auth')


# ---------------- JOBSEEKER PAGES ----------------
@login_required(login_url='/auth/')
def index(request):
    return render(request, 'index.html')


@login_required(login_url='/auth/')
def home(request):
    return render(request, 'home.html')


@login_required(login_url='/auth/')
def about(request):
    return render(request, 'index.html')


@login_required(login_url='/auth/')
def job(request):
    jobs = Job.objects.all()
    return render(request, 'jobs.html', {'jobs': jobs})


@login_required(login_url='/auth/')
def companies(request):
    companies = Company.objects.all()
    return render(request, 'companies.html', {'companies': companies})


@login_required(login_url='/auth/')
def recruiters(request):
    return render(request, 'recruiters.html')


@login_required(login_url='/auth/')
def apply_home(request):
    return render(request, 'apply_home.html')


@login_required(login_url='/auth/')
def apply(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")

        Application.objects.create(
            job=job,
            name=name,
            email=email,
            phone=request.POST.get("phone"),
            resume=request.FILES.get("resume")
        )

        email_sent = False

        try:
            send_mail(
                subject=f"Application Submitted - {job.job_title}",
                message=f"Hi {name}, your application was submitted successfully.",
                from_email=None,
                recipient_list=[email],
                fail_silently=False,
            )
            email_sent = True
        except:
            email_sent = False

        return render(request, "apply.html", {
            "job": job,
            "submitted": True,
            "email_sent": email_sent,
        })

    return render(request, "apply.html", {"job": job})


@login_required(login_url='/auth/')
def contact(request):
    return render(request, 'contact.html')


@login_required(login_url='/auth/')
def resume_analyzer(request):

    resume_url = request.session.get("resume_url")
    missing_skills = request.session.get("missing_skills", [])

    if request.method == "POST":

        try:
            resume = request.FILES.get("resume")
            job_description = request.POST.get("job_description", "")

            print("📄 FILE RECEIVED:", resume)
            print("📦 FILE SIZE:", resume.size if resume else "NO FILE")
            print("📝 JOB DESC LENGTH:", len(job_description))

            if resume and job_description:

                resume.seek(0)  # IMPORTANT FIX

                resume_text = extract_text_from_pdf(resume)
                job_text = clean_text(job_description)

                missing_skills = find_missing_skills(
                    resume_text,
                    job_text
                )

                print("✅ EXTRACTED TEXT LENGTH:", len(resume_text))
                print("🎯 MISSING SKILLS:", missing_skills)

                request.session["resume_url"] = resume.name
                request.session["missing_skills"] = missing_skills

        except Exception as e:
            print("🔥 RESUME ANALYZER ERROR:", str(e))

        return redirect("resume_analyzer")

    return render(request, "resume_analyzer.html", {
        "resume_url": resume_url,
        "missing_skills": missing_skills,
    })
    
# ---------------- EMPLOYER PAGES ----------------
@login_required(login_url='/auth/')
def home2(request):
    return render(request, 'home2.html')


@login_required(login_url='/auth/')
def contact2(request):
    return render(request, 'contact2.html')


@login_required(login_url='/auth/')
def add_job(request):

    if request.method == "POST":
        Job.objects.create(
            job_title=request.POST.get("job_title"),
            job_description=request.POST.get("job_description"),
            salary=request.POST.get("salary"),
            location=request.POST.get("location"),
            company=Company.objects.get(id=request.POST.get("company"))
        )
        return redirect("add_job")

    companies = Company.objects.all()
    return render(request, "add_job.html", {"companies": companies})


@login_required(login_url='/auth/')
def applications(request):
    applications = Application.objects.select_related('job', 'job__company')
    return render(request, 'applications.html', {
        'applications': applications
    })
