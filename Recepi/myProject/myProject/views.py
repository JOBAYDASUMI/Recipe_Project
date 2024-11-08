from django.shortcuts import render,redirect

from myApp.models import *
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def signupPage(request):
    
    if request.method=='POST':
        
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        Confirm_password=request.POST.get("Confirm_password")
        user_type=request.POST.get("user_type")
        Profile_Pic=request.FILES.get("Profile_Pic")
    
        
        if password==Confirm_password:
            
            
            user=customUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                user_type=user_type,
                Profile_Pic=Profile_Pic,
            )
            if user_type=='viewers':
                viewersProfileModel.objects.create(user=user)
                
            elif user_type=='creator':
                creatorProfileModel.objects.create(user=user)
            
            return redirect("signInPage")
            
    return render(request,"signupPage.html")


def signInPage(request):
    if request.method == 'POST':
        
        user_name=request.POST.get("username")
        pass_word=request.POST.get("password")

        try:
            user = authenticate(request, username=user_name, password=pass_word)

            if user is not None:
                login(request, user)
                return redirect('homePage') 
            else:
                return redirect('signInPage')

        except customUser.DoesNotExist:
            return redirect('signInPage')

    return render(request, 'signInPage.html')

@login_required
def homePage(request):
    
    
    return render(request,"homePage.html")


def logoutPage(request):
    
    logout(request)
    
    return redirect('signInPage')

@login_required
def profilePage(request):
    
    return render(request,"profilePage.html")

def editprofilePage(request):
    
    current_user=request.user
    
    if request.method=='POST':
        username=request.POST.get("username")
        email=request.POST.get("email")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        profile_pic=request.FILES.get("profile_pic")
        
        specialties=request.POST.get("specialties")
        Followers=request.POST.get("Followers")
        Achievements=request.POST.get("Achievements")
        Bio=request.POST.get("Bio")
        interests=request.POST.get("interests")
        
        current_user.username=username
        current_user.email=email
        current_user.first_name=first_name
        current_user.last_name=last_name
        current_user.Profile_Pic=profile_pic
        current_user.save()
        
        
        try:
            creatorProfile=creatorProfileModel.objects.get(user=current_user)
            creatorProfile.Specialties=specialties
            creatorProfile.Followers=Followers
            creatorProfile.Achievements=Achievements
            creatorProfile.Bio=Bio
            creatorProfile.save()
            current_user.save()
            
            return redirect("profilePage")
            
        except creatorProfileModel.DoesNotExist:
            creatorProfile=None
            
        try:
            viewersProfile=viewersProfileModel.objects.get(user=current_user)
            viewersProfile.Interests=interests
            viewersProfile.save()
            current_user.save()
            
            return redirect("profilePage")
            
        except viewersProfileModel.DoesNotExist:
            viewersProfile=None
    
    return render(request,"editprofilePage.html")


def addRacipe(request):
    if request.method=='POST':
        current_user=request.user
        Title=request.POST.get("title")
        Ingredients=request.POST.get("ingredients")
        Instruction=request.POST.get("instruction")
        Prep_time=request.POST.get("prep_time")
        Cook_time=request.POST.get("cook_time")
        Total_time=request.POST.get("total_time")
        Difficulty=request.POST.get("difficulty")
        Nutrition=request.POST.get("nutrition")
        Image=request.FILES.get("image")
        Category=request.POST.get("category")
        Tag=request.POST.get("tag")
        Calories=request.POST.get("calories")
        
        recipe=RecipeModel(
            user=current_user,
            Category=Category,
            Difficulty=Difficulty,
            Tag=Tag,
            title=Title,
            ingredients=Ingredients,
            instructions=Instruction,
            prep_time=Prep_time,
            cooking_time=Cook_time,
            total_time=Total_time,
            nutrition=Nutrition,
            image=Image,
            calories=Calories,
        )
        recipe.save()
        
        return redirect("createdRecipe")
    return render(request,"addRacipe.html")


def createdRecipe(request):
    current_user=request.user
    
    recipe=RecipeModel.objects.filter(user=current_user)
    
    
    context={
        'recipe':recipe
    }
    
    return render(request, 'createdRecipe.html',context)

def editRecipe(request,id):
    if request.method=='POST':
        current_user=request.user
        
        Id=request.POST.get("id")
        Title=request.POST.get("title")
        Ingredients=request.POST.get("ingredients")
        Instruction=request.POST.get("instruction")
        Prep_time=request.POST.get("prep_time")
        Cook_time=request.POST.get("cook_time")
        Total_time=request.POST.get("total_time")
        Difficulty=request.POST.get("difficulty")
        Nutrition=request.POST.get("nutrition")
        Image=request.FILES.get("image")
        Category=request.POST.get("category")
        Tag=request.POST.get("tag")
        Calories=request.POST.get("calories")
        
        recipe=RecipeModel(
            user=current_user,
            id=Id,
            Category=Category,
            Difficulty=Difficulty,
            Tag=Tag,
            title=Title,
            ingredients=Ingredients,
            instructions=Instruction,
            prep_time=Prep_time,
            cooking_time=Cook_time,
            total_time=Total_time,
            nutrition=Nutrition,
            image=Image,
            calories=Calories,
        )
        recipe.save()
        
        return redirect("createdRecipe")
    
    
    recipe=RecipeModel.objects.get(id=id)
    context={
        'recipe':recipe
    }
    
    return render(request,"editRecipe.html",context)

def viewRecipe(request,id):
    recipe=RecipeModel.objects.get(id=id)
    
    context={
        'recipe':recipe
    }
    
    return render(request,"viewRecipe.html",context)
def deleteRecipe(request,id):
    
    recipe=RecipeModel.objects.get(id=id).delete()
    
    return redirect("createdRecipe")

def RecipeFeed(request):
    recipe=RecipeModel.objects.all()
    
    context={
        'recipe':recipe
    }
    return render(request,"RecipeFeed.html",context)

def recipe_search(request):
    
    query=request.GET.get("query")
    
    if query:
        recipes=RecipeModel.objects.filter(
            Q(title__icontains=query) |
            Q(Category__icontains=query) |
            Q(Tag__icontains=query)|
            Q(user__username__icontains=query)
            )
    else:
        recipes=RecipeModel.objects.none()
        
    context={
        'recipes':recipes,
        'query':query
    }
    
    return render(request,"recipe_search.html",context)
    
    
