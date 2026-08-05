
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Attendance.views import AttendanceViewSet

from Fitness.views import FitnessLogViewSet
from Fees.views import AdminPaymentStatusView, GuardianPaymentView
from Schedule.views import ScheduleViewSet
from Teams.views import TeamViewSet
from academy.views import AcademyViewSet
from players.views import PlayerViewSet
from scouting.views import ScoutReportViewSet
from communications.views import AnnouncementViewSet
from chat.views import ChatMessageView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


router = DefaultRouter()
router.register(r'academies', AcademyViewSet, basename='academy')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'players', PlayerViewSet, basename='player')
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'fitness', FitnessLogViewSet, basename='fitness')
router.register(r'schedules', ScheduleViewSet, basename='schedule')
router.register(r'scout-reports', ScoutReportViewSet, basename='scout-report')
router.register(r'announcements', AnnouncementViewSet, basename='announcement')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/accounts/', include('accounts.urls')),
    path ('api/schema', SpectacularAPIView.as_view(), name='schema'),
    path ('api/docs', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/fees/', GuardianPaymentView.as_view(), name='payments'),
    path('api/chat/', ChatMessageView.as_view(), name='chat-room'),
    path('api/payments/', GuardianPaymentView.as_view(), name='payments-list'),
    path('api/payments/<int:pk>/status/', AdminPaymentStatusView.as_view(), name='payment-status-update'),
]


