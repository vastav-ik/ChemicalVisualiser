
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from analyzer.views import UploadView, HistoryView, AnalysisDataView, PDFReportView
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        "message": "Chemical Equipment Visualizer API is running",
        "endpoints": {
            "upload": "/api/upload/",
            "history": "/api/history/",
            "auth": "/api-token-auth/"
        }
    })

urlpatterns = [
    path('', api_root, name='api_root'),
    path('admin/', admin.site.urls),
    path('api/upload/', UploadView.as_view(), name='upload'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/history/', HistoryView.as_view(), name='history'),
    path('api/analysis/<int:pk>/data/', AnalysisDataView.as_view(), name='analysis_data'),
    path('api/analysis/<int:pk>/pdf/', PDFReportView.as_view(), name='analysis_pdf'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
