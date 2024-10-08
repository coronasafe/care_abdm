import json
import logging

from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from care.facility.models.file_upload import FileUpload

logger = logging.getLogger(__name__)


class HealthInformationViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk):
        files = FileUpload.objects.filter(
            Q(internal_name__contains=f"{pk}.json") | Q(associating_id=pk),
            file_type=FileUpload.FileType.ABDM_HEALTH_INFORMATION.value,
            upload_completed=True,
        )

        if files.count() == 0:
            return Response(
                {"detail": "No Health Information found for the given id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if files.count() == 1 and files.first().is_archived:
            return Response(
                {
                    "is_archived": True,
                    "archived_reason": files.first().archive_reason,
                    "archived_time": files.first().archived_datetime,
                    "detail": f"This file has been archived as { files.first().archive_reason} at { files.first().archived_datetime}",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        files = files.filter(is_archived=False)

        contents = []
        for file in files:
            if file.upload_completed:
                _, content = file.file_contents()
                contents.extend(content)

        return Response({"data": json.loads(content)}, status=status.HTTP_200_OK)
