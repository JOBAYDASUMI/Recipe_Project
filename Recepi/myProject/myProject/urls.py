from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from myProject.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('signupPage/',signupPage,name="signupPage"),
    path("", signInPage, name="signInPage"),
    path("homePage/", homePage, name="homePage"),
    path("logoutPage/", logoutPage, name="logoutPage"),
    path("ProfilePage/", profilePage, name="profilePage"),
    
    path("addRacipe/", addRacipe, name="addRacipe"),
    path("createdRecipe/", createdRecipe, name="createdRecipe"),
    path("RecipeFeed/", RecipeFeed, name="RecipeFeed"),
    
    path("recipe_search/", recipe_search, name="recipe_search"),
    
    path("editprofilePage/", editprofilePage, name="editprofilePage"),
    
    path("viewRecipe/<str:id>", viewRecipe, name="viewRecipe"),
    path("deleteRecipe/<str:id>", deleteRecipe, name="deleteRecipe"),
    path("editRecipe/<str:id>", editRecipe, name="editRecipe"),
    
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
