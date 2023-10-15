from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.homepage,name="homepage"),
    path('home', views.homepage,name="homepage"),
    path('about', views.aboutpage,name="aboutpage"),
    path('about/', views.aboutpage,name="aboutpage"),
    path('contact', views.contactpage,name="contactpage"),
    path('contact/', views.contactpage,name="contactpage"),
    path('user', views.user_log_sign_page,name="userloginpage"),
    path('user/login', views.user_log_sign_page,name="userloginpage"),
    path('user/bookings', views.user_bookings,name="dashboard"),
    path('user/book-room', views.book_room_page,name="bookroompage"),
    path('user/book-room/book', views.book_room,name="bookroom"),
    path('user/signup', views.user_sign_up,name="usersignup"),
    path('staff/', views.staff_log_sign_page,name="staffloginpage"),
    path('staff/login', views.staff_log_sign_page,name="staffloginpage"),
    path('staff/signup', views.staff_sign_up,name="staffsignup"),
    path('logout', views.logoutuser,name="logout"),
    path('staff/panel', views.panel,name="staffpanel"),
    path('staff/allbookings', views.all_bookings,name="allbookigs"),
    path('send-email/', views.send_email, name='send_email'),
    path('send-email', views.send_email, name='send_email'),
    path('feedback/', views.feedback_form, name='feedback_form'),
    path('feedback', views.feedback_form, name='feedback_form'),
    path('user/send_invite_email', views.send_invite_email, name='send_invite_email'),
    path('user/send_invite_email', views.send_invite_email, name='send_invite_email'),


    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('staff/panel/add-new-location', views.add_new_location,name="addnewlocation"),
    path('staff/panel/edit-room', views.edit_room),
    path('staff/panel/add-new-room', views.add_new_room,name="addroom"),
    path('staff/panel/edit-room/edit', views.edit_room),
    path('staff/panel/view-room', views.view_room),
    path('available-students/', views.available_students, name='available_students'),
    path('available-students', views.available_students, name='available_students'),
    

    path('admin/', admin.site.urls),
    

]