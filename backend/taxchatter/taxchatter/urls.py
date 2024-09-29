"""
URL configuration for taxchatter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from chat import views as chat_views
from chat.views import AdminConversationsView
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin", admin.site.urls),
    path("chat", chat_views.chat_page, name="chat"),
    path("api/upload", chat_views.FileUploadView.as_view(), name="upload"),
    path("api/xml_schema", chat_views.XmlSchemaView.as_view(), name="xml_schema"),
    path("api/xml_schema_sdz2", chat_views.XmlSchemaSdzView.as_view(), name="xml_schema_sdz2"),
    path("api/validate_user_data", chat_views.ValidateUserDataView.as_view(), name="validate_user_data"),
    path("api/generate_xml", chat_views.GenerateXmlView.as_view(), name="generate_xml"),
    path("api/generate_sdz2", chat_views.GenerateSdzView.as_view(), name="generate_sdz2"),
    path("api/closestUrzad", chat_views.LocationView.as_view(), name="closest_urzad"),
    path("api/initialize_conversation", chat_views.InitializeConversationView.as_view(), name="initialize_conversation"),
    path("api/validate_infer", chat_views.ValidateAndInferView.as_view(), name="validate_infer"),
    path("api/admin/conversations", AdminConversationsView.as_view(), name="admin-conversations"),
]
