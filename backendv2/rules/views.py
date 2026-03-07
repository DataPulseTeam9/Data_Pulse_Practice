"""Validation rules router - PARTIAL implementation."""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from rules.models import ValidationRule
from rules.serializers import RuleCreateSerializer, RuleResponseSerializer, RuleUpdateSerializer
from datapulse.exceptions import InvalidRuleException

VALID_TYPES = {"NOT_NULL", "DATA_TYPE", "RANGE", "UNIQUE", "REGEX"}
VALID_SEVERITIES = {"HIGH", "MEDIUM", "LOW"}


class RuleListCreateView(APIView):
    """Handle POST (create) and GET (list) for rules."""

    @extend_schema(
        request=RuleCreateSerializer,
        responses={201: RuleResponseSerializer},
        tags=["Rules"],
        summary="Create a new validation rule",
    )
    def post(self, request):
        """Create a new validation rule - IMPLEMENTED."""
        serializer = RuleCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if data["rule_type"] not in VALID_TYPES:
            raise InvalidRuleException(f"Invalid rule_type: {VALID_TYPES}")
        
        if data["severity"] not in VALID_SEVERITIES:
            raise InvalidRuleException(f"Invalid severity: {VALID_SEVERITIES}")

        rule = ValidationRule.objects.create(**data)
        return Response(
            RuleResponseSerializer(rule).data, status=status.HTTP_201_CREATED
        )

    @extend_schema(
        parameters=[
            OpenApiParameter("dataset_type", OpenApiTypes.STR, OpenApiParameter.QUERY, required=False),
        ],
        responses={200: RuleResponseSerializer(many=True)},
        tags=["Rules"],
        summary="List validation rules",
    )
    def get(self, request):
        """List validation rules - IMPLEMENTED."""
        dataset_type = request.query_params.get("dataset_type")
        queryset = ValidationRule.objects.filter(is_active=True)
        if dataset_type:
            queryset = queryset.filter(dataset_type=dataset_type)
        return Response(
            RuleResponseSerializer(queryset, many=True).data, status=status.HTTP_200_OK
        )


class RuleDetailView(APIView):
    """Handle PUT (update) and DELETE for a specific rule."""

    @extend_schema(
        request=RuleUpdateSerializer,
        responses={200: RuleResponseSerializer},
        tags=["Rules"],
        summary="Update a validation rule (TODO)",
    )
    def put(self, request, rule_id):
        """Update a validation rule - TODO: Implement.

        Steps:
        1. Fetch rule by ID (404 if not found)
        2. Update non-None fields from rule_data
        3. Validate rule_type and severity if changed
        4. Commit and return updated rule
        """
        return Response(
            {"detail": "PUT /api/rules/{id} not implemented"},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )

    @extend_schema(
        responses={204: None},
        tags=["Rules"],
        summary="Delete a validation rule (TODO)",
    )
    def delete(self, request, rule_id):
        """Soft-delete a validation rule - TODO: Implement.

        Steps:
        1. Fetch rule by ID (404 if not found)
        2. Set is_active = False
        3. Save, return 204
        """
        return Response(
            {"detail": "DELETE /api/rules/{id} not implemented"},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )
