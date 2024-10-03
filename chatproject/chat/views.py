from django.shortcuts import render , redirect
from django.views import View
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User
from . import models
from django.db.models import Q



# Create your views here.



class Main(View):
    def get(self, request):

        if request.user.is_authenticated:
            return redirect("home")

        return render(request=request , template_name="chat/main.html")



class Login(View):
    def get(self, request):
        return render(request=request , template_name="chat/login.html")
    
    def post(self, request):

        data = request.POST.dict()
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request=request , username=username , password=password)
        if user != None:
            login(request=request , user=user)
            return redirect("home")


        context = {"error":"there is something wrong"}
        return render(request=request , template_name="chat/login.html" , context=context)



class Register(View):
    def get(self, request):
        return render(request=request , template_name="chat/register.html")
    
    def post(self, request):

        context = {}
        
        data = request.POST.dict()
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        try:
            new_user = User()
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.username = username
            new_user.email = email
            new_user.set_password(password)
            new_user.save()
        

            user = authenticate(request=request , username=username , password=password)
            if user != None:
                login(request=request , user=user)
                return redirect("home")
        except:
            context.update({"error":"the data is wrong"})

        return render(request=request , template_name="chat/register.html" , context=context)
    


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("main")



class Home(View):
    def get(self, request):

        if request.user.is_authenticated:

            users = User.objects.all()

            print(users)

            context = {"user":request.user,
                       "users":users}
            return render(request=request , template_name="chat/home.html", context=context)
        
        return redirect("main")



class ChatPerson(View):
    def get(self, request, id):

        person = User.objects.get(id=id)
        me = request.user
        messages = models.Message.objects.filter(Q(from_who=me , to_who=person) | Q(to_who=me , from_who=person)).order_by("date" , "time")



        user_channel_name = models.UserChannel.objects.get(user=person)
        data = {"type":"recevier_function",
                "type_of_data":"the_messages_have_been_seen_from_the_other"}
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)(user_channel_name.channel_name, data)



        messages_have_not_been_seen = models.Message.objects.filter(from_who=person, to_who=me)
        messages_have_not_been_seen.update(has_been_seen=True)



        context = {"person":person,
                   "me":me,
                   "messages":messages}
        return render(request=request , template_name="chat/chat_person.html", context=context)











