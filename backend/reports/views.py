"""Reports router - STUB: All endpoints need implementation."""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from reports.serializers import QualityReportSerializer
from checks.serializers import QualityScoreResponseSerializer


class DatasetReportView(APIView):
    """Get a full quality report for a dataset."""

    @extend_schema(
        responses={200: QualityReportSerializer},
        tags=["Reports"],
        summary="Get quality report for a dataset (TODO)",
    )
    def get(self, request, dataset_id):
        """Get a full quality report for a dataset.

        TODO: Implement using report_service.generate_report().

        Steps:
        1. Fetch dataset by ID (404 if not found)
        2. Fetch latest QualityScore for this dataset
        3. Fetch all CheckResults from latest check run
        4. Compose QualityReport with dataset info, score, results
        5. Return the report
        """
        return Response(
            {"detail": "GET /api/reports/{id} not implemented"},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )


class QualityTrendsView(APIView):
    """Get quality score trends over time."""

    @extend_schema(
        parameters=[
            OpenApiParameter("days", OpenApiTypes.INT, OpenApiParameter.QUERY, default=30),
        ],
        responses={200: QualityScoreResponseSerializer(many=True)},
        tags=["Reports"],
        summary="Get quality score trends (TODO)",
    )
    def get(self, request):
        """Get quality score trends over time.

        TODO: Implement using report_service.get_trend_data().

        Steps:
        1. Calculate start_date = now - days
        2. Query QualityScore after start_date
        3. Order by checked_at ascending
        4. Return scores showing quality trends
        """
        return Response(
            {"detail": "GET /api/reports/trends not implemented"},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )
