"""
URL configuration for jobportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from recruiter_app.views import recruiter_signup,recruiter_login,recruiter_dashboard,recruiter_profile,recruiter_logout,homepage,recruiter_profile_update,job_details,applied_job,approve
from candidate_app.views import candidate_dashboard,candidate_login,candidate_logout,candidate_profile,candidate_signup,candidate_profile_update,view_detail,apply_job,scheduled
from django.conf.urls import handler404
from recruiter_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",homepage,name="homepage"),
    path("r_signup/",recruiter_signup,name="recruiter_signup"),
    path("r_login/",recruiter_login,name="recruiter_login"),
    path("r_dashboard/",recruiter_dashboard,name="recruiter_dashboard"),
    path("r_profile/",recruiter_profile, name="recruiter_profile"),
    path("r_logout/",recruiter_logout,name="recruiter_logout"),
    path("r_profile_update/",recruiter_profile_update,name="recruiter_profile_update"),
    path("job_details/",job_details,name="job_details"),
    path("applied_job/",applied_job,name="applied_job"),
    path("approve/<int:id>",approve,name="approve"),

    path("c_signup/",candidate_signup,name="candidate_signup"),
    path("c_login/",candidate_login,name="candidate_login"),
    path("c_dashboard/",candidate_dashboard,name="candidate_dashboard"),
    path("c_profile/",candidate_profile,name="candidate_profile"),
    path("c_logout/",candidate_logout,name="candidate_logout"),
    path('c_profile_update/',candidate_profile_update,name="candidate_profile_update"),
    path("view_detail/<int:id>",view_detail,name="view_detail"),
    path("apply_job/<int:id>",apply_job,name="apply_job"),
    path("result/",scheduled,name="result"),
]

# Media files
urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# Catch wrong URL (must be LAST)
urlpatterns += [
    path('<path:invalid_path>', views.page_not_found),
]
