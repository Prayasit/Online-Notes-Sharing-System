from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from nssapp.models import CustomUser,UserReg,Notes
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import re
User = get_user_model()

def Index(request):
       return render(request,'index.html')

@login_required(login_url = '/')


def BASE(request):
    return render(request, 'base.html')

def DASHBOARD(request):
    user_admin = request.user
    try:
        user_reg = UserReg.objects.get(admin=user_admin)
    except UserReg.DoesNotExist:
        messages.error(request, "User registration details not found.")
        return render(request, 'dashboard.html')

    uploadedsub_count = Notes.objects.filter(nsuser=user_reg).count()
    user_notes = Notes.objects.filter(nsuser=user_reg)

    # Initialize file count
    total_files = 0

    # Count files for each note
    for note in user_notes:
        if note.file1:
            total_files += 1
        if note.file2:
            total_files += 1
        if note.file3:
            total_files += 1
        if note.file4:
            total_files += 1

    context = {
        'uploadedsub_count': uploadedsub_count,
        'total_files': total_files,
    }

    return render(request, 'dashboard.html', context)


def LOGIN(request):
    return render(request,'login.html')


def doLogout(request):
    logout(request)
    request.session.flush()  # Clear the session including CSRF token
    return redirect('login')

def doLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
       

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('dashboard')
            elif user_type == '2':
                return redirect('dashboard')
        else:
            messages.error(request, 'Email or Password is not valid')
            return redirect('login')  # Redirect back to the login page with an error message
    else:
        # If the request method is not POST, redirect to the login page with an error message
        messages.error(request, 'Invalid request method')
        return redirect('login')


def USERSIGNUP(request):

    if request.method == "POST":
        pic        = request.FILES.get('pic')
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        username   = request.POST.get('username', '').strip()
        email      = request.POST.get('email', '').strip()
        mobno      = request.POST.get('mobno', '').strip()
        password   = request.POST.get('password', '')

        # ---------- BASIC REQUIRED FIELDS ----------
        if not all([first_name, last_name, username, email, mobno, password]):
            messages.warning(request, 'All fields are required.')
            return redirect('usersignup')

        # ---------- MOBILE VALIDATION (10 DIGITS ONLY) ----------
        if not mobno.isdigit() or len(mobno) != 10:
            messages.warning(request, 'Mobile number must be exactly 10 digits.')
            return redirect('usersignup')

        # ---------- PASSWORD STRENGTH VALIDATION ----------
        # Rules: at least 8 chars, one uppercase, one lowercase, one digit, one special char
        if len(password) < 8:
            messages.warning(request, 'Password must be at least 8 characters long.')
            return redirect('usersignup')

        if not re.search(r'[A-Z]', password):
            messages.warning(request, 'Password must contain at least one uppercase letter.')
            return redirect('usersignup')

        if not re.search(r'[a-z]', password):
            messages.warning(request, 'Password must contain at least one lowercase letter.')
            return redirect('usersignup')

        if not re.search(r'\d', password):
            messages.warning(request, 'Password must contain at least one digit.')
            return redirect('usersignup')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            messages.warning(request, 'Password must contain at least one special character.')
            return redirect('usersignup')

        # ---------- UNIQUE EMAIL / USERNAME CHECK ----------
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exist')
            return redirect('usersignup')

        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username already exist')
            return redirect('usersignup')

        # ---------- CREATE USER ----------
        user = CustomUser(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            user_type=2,
            profile_pic=pic,
        )
        user.set_password(password)
        user.save()

        nsuser = UserReg(
            admin=user,
            mobilenumber=mobno,
        )
        nsuser.save()

        messages.success(request, 'Signup Successfully')
        return redirect('usersignup')

    # GET request
    return render(request, 'signup.html')   # or your template name


@login_required(login_url='/')
def PROFILE(request):
    if request.method == "POST":
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            userreg = UserReg.objects.get(admin_id=request.user.id)

            # Update user data
            customuser.first_name = request.POST.get('first_name', customuser.first_name)
            customuser.last_name = request.POST.get('last_name', customuser.last_name)
            
            if 'profile_pic' in request.FILES:
                customuser.profile_pic = request.FILES['profile_pic']
            customuser.save()

            messages.success(request, "Your profile has been updated successfully")
            return redirect('profile')
        except ObjectDoesNotExist:
            messages.error(request, "User profile not found")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    else:
        try:
            user = CustomUser.objects.get(id=request.user.id)
            nsuser = UserReg.objects.get(admin_id=request.user.id)
        except CustomUser.DoesNotExist:
            user = None
        except UserReg.DoesNotExist:
            nsuser = None

        context = {
            "user": user,
            "nsuser": nsuser,
        }
        return render(request, 'profile.html', context)


def CHANGE_PASSWORD(request):
     context ={}
     ch = User.objects.filter(id = request.user.id)
     
     if len(ch)>0:
            data = User.objects.get(id = request.user.id)
            context["data"] = data            
     if request.method == "POST":        
        current = request.POST["cpwd"]
        new_pas = request.POST['npwd']
        user = User.objects.get(id = request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
          user.set_password(new_pas)
          user.save()
          messages.success(request,'Password Change  Succeesfully!!!')
          user = User.objects.get(username=un)
          login(request,user)
        else:
          messages.success(request,'Current Password wrong!!!')
          return redirect("change_password")
     return render(request,'change-password.html')


def ADD_NOTES(request):
    if request.method == "POST":
        title = request.POST.get('notestitle')
        subject = request.POST.get('subject')
        description = request.POST.get('notesdesc')
        file1 = request.FILES.get('file1')
        file2 = request.FILES.get('file2')
        file3 = request.FILES.get('file3')
        file4 = request.FILES.get('file4')

        userreg = UserReg.objects.get(admin_id=request.user.id)

        notes = Notes(
            notestitle=title,
            subject = subject,
            notesdesc = description,
            file1 = file1,
            file2 = file2,
            file3 = file3,
            file4 = file4,
            nsuser = userreg,
        )
        notes.save()
        messages.success(request, 'Notes Added Successfully')
        return redirect("add_notes")
    return render(request, 'add-notes.html')

login_required(login_url='/')
def MANAGE_NOTES(request):
    userreg = UserReg.objects.get(admin_id=request.user.id)
    data_list = Notes.objects.filter(nsuser = userreg)
    paginator = Paginator(data_list, 10)  # Show 10 data per page

    page_number = request.GET.get('page')
    try:
        data_list = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        data_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        data_list = paginator.page(paginator.num_pages)

    context = {'data_list': data_list,
   }
    return render(request, 'manage-notes.html', context)

login_required(login_url='/')
def DELETE_NOTES(request,id):
       del_data = Notes.objects.get(id = id)
       del_data.delete()
       messages.success(request,'Record Delete Succeesfully!!!')
       return redirect('manage_notes')


login_required(login_url='/')
def VIEW_NOTES(request,id):    
    data_notes = Notes.objects.get(id =id)    
    context = {
        
        "data_notes":data_notes,
    }
    return render(request,'update_notes.html',context)

@login_required(login_url='/')
def EDIT_NOTES(request):
    if request.method == "POST":
        data_id = request.POST.get('notes_id')
        try:
            data_edit = Notes.objects.get(id=data_id)
        except Notes.DoesNotExist:
            messages.error(request, "Data does not exist")
            return redirect('manage_data')

        # Create a dictionary with updated data
        updated_data = {
            'notestitle': request.POST.get('notestitle'),
            'subject': request.POST.get('subject'),
            'notesdesc': request.POST.get('notesdesc'),
        }

        # Update the data_edit object with the updated data
        for field, value in updated_data.items():
            if value:
                setattr(data_edit, field, value)

        # Handle file uploads separately
        for i in range(1, 5):
            file_field = f'file{i}'
            if file_field in request.FILES:
                setattr(data_edit, file_field, request.FILES[file_field])

        data_edit.save()
        messages.success(request, "Data has been updated successfully")
        return redirect('manage_notes')

    return render(request, 'manage-notes.html')


def SEARCH_NOTES(request):
    if request.method == "GET":
        # Clear existing messages
        storage = messages.get_messages(request)
        list(storage)  # Access the messages to clear them

        userreg = UserReg.objects.get(admin_id=request.user.id)
        query = request.GET.get('query', '')

        if query:
            searchdata = Notes.objects.filter(
                Q(notestitle__icontains=query) |
                Q(subject__icontains=query),
                nsuser=userreg
            )

            if searchdata.exists():
                messages.info(request, f"Search results for '{query}'")
            else:
                messages.info(request, f"No results found for '{query}'")

            return render(request, 'search.html', {'searchdata': searchdata, 'query': query})
        else:
            
            return render(request, 'search.html', {'searchdata': [], 'query': query})

    return render(request, 'search.html', {'searchdata': [], 'query': ''})


login_required(login_url='/')
def NOTES_DETAILS(request):    
    data_list = Notes.objects.all()
    paginator = Paginator(data_list, 10)  # Show 10 data per page

    page_number = request.GET.get('page')
    try:
        data_list = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        data_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        data_list = paginator.page(paginator.num_pages)  
    context = {
        
        "data_list":data_list,
    }
    return render(request,'notes.html',context)


