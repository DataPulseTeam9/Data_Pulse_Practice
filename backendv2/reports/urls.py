"""Reports URL configuration."""

from django.urls import path
from reports.views import QualityTrendsView, DatasetReportView

urlpatterns = [
    path("trends", QualityTrendsView.as_view(), name="reports-trends"),
    path("<int:dataset_id>", DatasetReportView.as_view(), name="reports-detail"),
]
