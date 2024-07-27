import datetime
from pyexpat.errors import messages
from re import template
from django.contrib import auth
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect

# Create your views here.
from django.shortcuts import render
from django.urls import reverse_lazy

from ap1.models import Project, Schedule, Student, Synopsis, Team, Weeklyreport
from django.contrib.auth import logout

def home(request):
  
    #user = request.user
    # Get user's team(s): use select_related or prefetch_related for efficiency
    #user_teams = user.Team.all().select_related('Team')  # Example using select_related
    name=request.COOKIES.get('name')
    email=request.COOKIES.get('email')
    phone=request.COOKIES.get('phone')
    usn=request.COOKIES.get('usn')
    context = {'name':name, 'email':email, 'phone':phone, 'usn':usn}
    return render(request, 'home.html', context)

def layout(request):
    return render(request,'layout.html')

def login(request):
    return render(request,'layout.html')

def register(request):
    return render(request,'register.html')

def teamcreation(request):
    return render(request,'teamcreation.html')

def uploadsynopsis(request):
    return render(request,'uploadsynopsis.html')

def reportupload(request):
    return render(request,'reportupload.html')

def viewprojectstatus(request):
    projects=Project.objects.all()
    return render(request,'viewprojectstatus.html',{'projects':projects})

def weeklyreport(request):
    w=Weeklyreport.objects.all()
    return render(request,'weeklyreport.html',{"w":w})


def weeklyprogress(request):
    usn=request.COOKIES.get('usn')
    from django.db.models import Q
    team=Team.objects.filter(Q(member1=usn)|Q(member2=usn)|Q(member3=usn)|Q(member4=usn)).values()
    l1=list()
    l2=list()
    for t in team:
        print(t)
        projects=Project.objects.filter(t_id_id=t['t_id'])
        l1.append(projects)
        for p in projects:
            submissions=Weeklyreport.objects.filter(p_id_id=p.p_id)
            l2.append(submissions)
        
    #pname=project.p_id
    #tid=project.t_id_id
    #submissions=Weeklyreport.objects.filter(p_id_id=l1[0]['pid'])
    print(l1)
    return render(request,'weeklyprogress.html',{'projects':l1, "submissions":l2})

def viewschedule(request):
    s=Schedule.objects.all()
    return render(request,'viewschedule.html',{"s":s})
    
def viewteam(request):
    return render(request,'viewteam.html')

def viewstudentlist(request):
    students=Student.objects.all()
    return render(request,'viewstudentlist.html',{'students':students})

def viewprojectteam(request):
    projects=Project.objects.all()
    teams=Team.objects.all()
    students=Student.objects.all()
    return render(request,'viewprojectteam.html',{'projects':projects,'teams':teams,'students':students})

def schedule(request):
    return render(request,'schedule.html')


def index(request):
    return render(request,'index.html')

def projectadmin(request):
    return render(request,'projectadmin.html')
    
def regstudent(request):
    if request.method== "POST":
        name=request.POST.get("name")
        usn=request.POST.get("usn")
        sem=request.POST.get("semester")
        sec=request.POST.get("section")
        gender=request.POST.get("gender")
        phone=request.POST.get("phone")
        email=request.POST.get("email")
        password=request.POST.get("password")
        s=Student(name=name, usn=usn, sem=sem, sec=sec, gender=gender,phone=phone,email=email, password=password)
        s.save()    
        return render(request,"index.html")

def loginpage(request):
    if request.method== "POST":
        usn=request.POST.get("uname")
        password=request.POST.get("psw")
        if usn=="admin" and password=="ppp":
            response = render(request, "projectadmin.html")
            response.set_cookie(key='name', value="admin")
            response.set_cookie(key='usn', value="admin")
            response.set_cookie(key='phone', value=" ")
            response.set_cookie(key='email', value="  ")
            return response
        l=Student.objects.filter(usn=usn,password=password).values()
        print(l)
        if l:
            #return "invalid credentials"
            role=request.POST.get("role")
            print(role)
            if role=="admin":
                return HttpResponse("You do not have admin priveleges")
            #     response.set_cookie(key='name', value=l[0]['name'])
            #     response.set_cookie(key='usn', value=l[0]['usn'])
            #     response.set_cookie(key='phone', value=l[0]['phone'])
            #     response.set_cookie(key='email', value=l[0]['email'])
            #     return response
            # #l.save() 
            response = render(request, "layout.html")  # django.http.HttpResponse
            response.set_cookie(key='name', value=l[0]['name'])
            response.set_cookie(key='usn', value=l[0]['usn'])
            response.set_cookie(key='phone', value=l[0]['phone'])
            response.set_cookie(key='email', value=l[0]['email'])
            return response
        else:
            return HttpResponse("invalid credentials")
        
def createteam(request):
    if request.method== "POST":
        member1=request.POST.get("usn1")
        member2=request.POST.get("usn2")
        member3=request.POST.get("usn3")
        member4=request.COOKIES.get("usn")
        title=request.POST.get("title")
        t=Team(title=title, member1=member1, member2=member2, member3=member3, member4=member4)
        t.save() 
        title=request.POST['title']   
        if not Team.objects.exists():  # Allow only one team creation
            team = Team.objects.create(name=title)
            return redirect("table_created")  # Redirect after successful creation
        else:
            return render(request, "teamcreation.html", {'error': 'Only one team can be created.'})
    else:
        return render(request,"uploadsynopsis.html")
    
def table_created(request):
    return render(request, 'table_created.html', {'message': 'Table is created!'})

def createproject(request):
    if request.method== "POST":
        tid=request.POST.get('tid')
        member4=request.COOKIES.get("usn")
        title=request.POST.get("title")
        domain=request.POST.get("domain")
        abstract=request.POST.get("abstract")
        t=Project(title=title,domain=domain,abstract=abstract,t_id_id=tid)
        t.save()    
        return render(request,"layout.html")
    else:
        usn=request.COOKIES.get('usn')
        from django.db.models import Q
        team=Team.objects.filter(Q(member1=usn)|Q(member2=usn)|Q(member3=usn)|Q(member4=usn))
        return render(request, 'projectcreation.html', {'teams': team})
        
        

def handle_uploaded_file(f):  
    with open('ap1/static/upload/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)   

def synopsis(request):
    if request.method=="POST": 
        student = Synopsis(request.POST, request.FILES)  
        handle_uploaded_file(request.FILES['synopsis'][0]) 
        tid=request.POST.get('tid')
        print(tid) 
        #c=Project.objects.get(id=cid)
        '''
        form=Synopsis(request.POST) 
        if form.is_valid(): 
            form.save() 
            return  HttpResponse("<h1>Record inserted successfully</h1>")
        '''
        return  HttpResponse("<h1>Record inserted successfully</h1>")
    else: 
        form=Synopsis() 
        return render(request,"uploadsynopsis.html",{"form":form})
    
def progress(request):
    if request.method== "POST":
        week=request.POST.get("week")
        summary=request.POST.get("summary")
        wdate=request.POST.get("eventDate")
        pid=request.POST.get("pid")
        print("pid",pid)
        tid=request.POST.get("tid")  # Get the team id from the form data
        submissions=Weeklyreport.objects.filter(p_id_id=pid)
        p=Weeklyreport(week_no=week,summary=summary,p_id_id=pid,date=wdate)
        p.save()  
        usn=request.COOKIES.get('usn')
        from django.db.models import Q
        team=Team.objects.filter(Q(member1=usn)|Q(member2=usn)|Q(member3=usn)|Q(member4=usn)).values()
        l1=list()
        l2=list()
        for t in team:
            print(t)
            projects=Project.objects.filter(t_id_id=t['t_id'])
            l1.append(projects)
            for p in projects:
                submissions=Weeklyreport.objects.filter(p_id_id=p.p_id)
                l2.append(submissions)
            
        #pname=project.p_id
        #tid=project.t_id_id
        #submissions=Weeklyreport.objects.filter(p_id_id=l1[0]['pid'])
        print(l1)
        return render(request,'weeklyprogress.html',{'projects':l1, "submissions":l2})
def date(request):
    now = datetime.date.now()
    html = "<html><body><h3>Date %s.</h3></body></html>" % now
    return HttpResponse(html,request,'weeklyprogress.html')

        #return render(request,"weeklyprogress.html",{"pname":pid,"tid":tid,"submissions":submissions})
    
    
def report(request):
    if request.method== "POST":
        report_file=request.POST.get("report_file")
        r=Project(report=report_file)
        r.save()  
        return HttpResponse(request)

def eventschedule(request):
    if request.method== "POST":
        eventDate=request.POST.get("eventDate")
        eventName=request.POST.get("eventName")
        eventInstructions=request.POST.get("eventInstructions")
        deadline=request.POST.get("deadline")
        e=Schedule(event=eventName,date=eventDate,instrution=eventInstructions, deadline=deadline)
        e.save()  
        return render(request,"projectadmin.html")

def studentlist(request):
  students = studentlist.objects.all()  # Retrieve all students
  context = {'students': students}
  return render(request, 'viewstudentlist.html', context)

def uploadsyn(request):
    from django.core.files.storage import FileSystemStorage
    
    if request.method == 'POST':
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            tid=request.POST.get('tid')
            fs = FileSystemStorage(location="ap1/synopsis")
            filename = fs.save(myfile.name, myfile)
            #team=Team.objects.all()
            usn=request.COOKIES.get('usn')
            from django.db.models import Q
            team=Team.objects.filter(Q(member1=usn)|Q(member2=usn)|Q(member3=usn)|Q(member4=usn)).values()
            uploaded_file_url = fs.url(filename)
            p=Project.objects.filter(t_id_id=tid)
            #print("hereich")
            if p:
                p.update(synopsis=uploaded_file_url)
            else:
                p=Project(t_id_id=tid,synopsis=uploaded_file_url)
                p.save()
            return render(request, 'upload.html', {
                'uploaded_file_url': uploaded_file_url,
                'teams': team
            })

            #return HttpResponseRedirect('upload_success.html') 
    else:
        
        usn=request.COOKIES.get('usn')
        from django.db.models import Q
        team=Team.objects.filter(Q(member1=usn)|Q(member2=usn)|Q(member3=usn)|Q(member4=usn))

    return render(request, 'upload.html', {'teams': team})

def uploadreport(request):
    from django.core.files.storage import FileSystemStorage
    
    if request.method == 'POST':
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            tid=request.POST.get('tid')
            fs = FileSystemStorage(location="ap1/reports")
            filename = fs.save(myfile.name, myfile)
            usn=request.COOKIES.get('usn')
            from django.db.models import Q
            team=Team.objects.filter(Q(member1=usn)|Q(member2=usn)|Q(member3=usn)|Q(member4=usn)).values()
            uploaded_file_url = "/reports/"+filename
           # print(filename)
            p=Project.objects.filter(t_id_id=tid)
            #print("hereich")
            if p:
                p.update(report=uploaded_file_url)
            else:
                p=Project(t_id_id=tid,report=uploaded_file_url)
                p.save()
            return render(request, 'rupload.html', {
                'uploaded_file_url': uploaded_file_url,
                'teams': team
            })

            #return HttpResponseRedirect('upload_success.html') 
    else:

        usn=request.COOKIES.get('usn')
        from django.db.models import Q
        team=Team.objects.filter(Q(member1=usn)|Q(member2=usn)|Q(member3=usn)|Q(member4=usn))

    return render(request, 'rupload.html', {'teams': team})

def logout(request):
    html = render(request,"index.html")
    html.delete_cookie('usn') 
    html.delete_cookie('name')
    html.delete_cookie('email')
    html.delete_cookie('phone')
     
    return html  
def logout_view(request):
        try:
            del(request.session['latitude'])
            del(request.session['longitude'])
            del(request.session['current_url'])
        except KeyError:
            pass
        auth.logout(request)        
        return redirect('loginpage')

