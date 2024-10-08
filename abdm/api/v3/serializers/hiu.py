from datetime import datetime

from abdm.models.base import AccessMode, HealthInformationType, Purpose, Status
from rest_framework.serializers import (
    CharField,
    ChoiceField,
    DateTimeField,
    IntegerField,
    ListField,
    Serializer,
    UUIDField,
    ValidationError,
)


class IdentityAuthenticationSerializer(Serializer):
    abha_number = CharField(max_length=50, required=False)
    patient = UUIDField(required=False)

    def validate(self, data):
        abha_number = data.get("abha_number")
        patient = data.get("patient")

        if not abha_number and not patient:
            raise ValidationError(
                "At least one of 'abha_number' or 'patient' must be provided."
            )

        return data


class HiuConsentRequestOnInitSerializer(Serializer):

    class ConsentRequestSerializer(Serializer):
        id = UUIDField(required=True)

    class ResponseSerializer(Serializer):
        requestId = UUIDField(required=True)

    class ErrorSerializer(Serializer):
        code = CharField(max_length=50)
        message = CharField()

    consentRequest = ConsentRequestSerializer(required=False)
    error = ErrorSerializer(required=False, allow_null=True)
    response = ResponseSerializer(required=True)


class ConsentRequestStatusSerializer(Serializer):
    consent_request = UUIDField(required=True)


class HiuConsentRequestOnStatusSerializer(Serializer):
    class ConsentRequestSerializer(Serializer):
        class ConsentArtefactsSerializer(Serializer):
            id = UUIDField(required=True)

        id = UUIDField(required=True)
        status = ChoiceField(choices=Status.choices, required=True)
        consentArtefacts = ListField(child=ConsentArtefactsSerializer())

    class ResponseSerializer(Serializer):
        requestId = UUIDField(required=True)

    consentRequest = ConsentRequestSerializer(required=True)
    response = ResponseSerializer(required=True)


class HiuConsentRequestNotifySerializer(Serializer):
    class NotificationSerializer(Serializer):
        class ConsentArtefactSerializer(Serializer):
            id = UUIDField(required=True)

        consentRequestId = UUIDField(required=True)
        status = ChoiceField(choices=Status.choices, required=True)
        consentArtefacts = ListField(child=ConsentArtefactSerializer(), required=False)

    notification = NotificationSerializer(required=True)


class ConsentFetchSerializer(Serializer):
    consent_request = UUIDField(required=False)
    consent_artefact = UUIDField(required=False)

    def validate(self, data):
        consent_request = data.get("consent_request")
        consent_artefact = data.get("consent_artefact")

        if not consent_request and not consent_artefact:
            raise ValidationError(
                "At least one of 'consent_request' or 'consent_artefact' must be provided."
            )

        return data


class HiuConsentOnFetchSerializer(Serializer):
    class ConsentSerializer(Serializer):
        class ConsentDetailSerializer(Serializer):
            class PurposeSerializer(Serializer):
                text = CharField(max_length=50, required=False)
                code = ChoiceField(choices=Purpose.choices, required=True)
                refUri = CharField(max_length=100, allow_null=True)

            class PatientSerializer(Serializer):
                id = CharField(required=True, max_length=50)

            class HipSerializer(Serializer):
                id = CharField(required=False)

            class ConsentManagerSerializer(Serializer):
                id = CharField(required=False)

            class CareContextSerializer(Serializer):
                patientReference = CharField(required=True)
                careContextReference = CharField(required=True)

            class HiuSerializer(Serializer):
                id = CharField(required=False)

            class RequesterSerializer(Serializer):
                class IdentifierSerializer(Serializer):
                    type = CharField(required=True)
                    value = CharField(required=True)
                    system = CharField(required=True)

                name = CharField(required=True)
                identifier = IdentifierSerializer(required=True)

            class PermissionSerializer(Serializer):
                class DateRangeSerializer(Serializer):
                    fromTime = DateTimeField(source="from", required=True)
                    toTime = DateTimeField(source="to", required=True)

                    def to_internal_value(self, data):
                        return super().to_internal_value(
                            {
                                "fromTime": datetime.strptime(
                                    data.get("from"), "%Y-%m-%dT%H:%M:%S.%fZ"
                                ),
                                "toTime": datetime.strptime(
                                    data.get("to"), "%Y-%m-%dT%H:%M:%S.%fZ"
                                ),
                            }
                        )

                class FrequencySerializer(Serializer):
                    unit = CharField(required=True)
                    value = IntegerField(required=True)
                    repeats = IntegerField(required=True)

                accessMode = ChoiceField(choices=AccessMode.choices, required=True)
                dateRange = DateRangeSerializer(required=True)
                dataEraseAt = DateTimeField(required=True)
                frequency = FrequencySerializer(required=True)

            consentId = UUIDField(required=True)
            hip = HipSerializer(required=False)
            hiu = HiuSerializer(required=True)
            hiTypes = ListField(
                child=ChoiceField(choices=HealthInformationType.choices), required=True
            )
            patient = PatientSerializer(required=True)
            purpose = PurposeSerializer(required=True)
            requester = RequesterSerializer(required=True)
            permission = PermissionSerializer(required=True)
            careContexts = ListField(child=CareContextSerializer())
            consentManager = ConsentManagerSerializer(required=False)
            createdAt = DateTimeField(required=False)
            lastUpdated = DateTimeField(required=False)
            schemaVersion = CharField(required=False)

        status = ChoiceField(choices=Status.choices, required=True)
        consentDetail = ConsentDetailSerializer(required=True)
        signature = CharField(required=True)

    class ResponseSerializer(Serializer):
        requestId = UUIDField(required=True)

    consent = ConsentSerializer(required=True)
    response = ResponseSerializer(required=True)


class DataFlowHealthInformationRequestSerializer(Serializer):
    consent_artefact = UUIDField(required=True)


class HiuHealthInformationOnRequestSerializer(Serializer):
    class HiRequestSerializer(Serializer):
        transactionId = UUIDField(required=True)
        sessionStatus = ChoiceField(
            choices=["REQUESTED", "ACKNOWLEDGED"], required=True
        )

    class ErrorSerializer(Serializer):
        code = CharField(max_length=20)
        message = CharField(required=False)

    class ResponseSerializer(Serializer):
        requestId = UUIDField(required=True)

    hiRequest = HiRequestSerializer(required=False)
    error = ErrorSerializer(required=False, allow_null=True)
    response = ResponseSerializer(required=True)


class HiuHealthInformationTransferSerializer(Serializer):
    class KeyMaterialSerializer(Serializer):
        class DhPublicKeySerializer(Serializer):
            expiry = DateTimeField(required=True)
            parameters = CharField(max_length=50, required=False)
            keyValue = CharField(max_length=500, required=True)

        cryptoAlg = CharField(max_length=50, required=True)
        curve = CharField(max_length=50, required=True)
        dhPublicKey = DhPublicKeySerializer(required=True)
        nonce = CharField(max_length=50, required=True)

    class EntrySerializer(Serializer):
        content = CharField(required=False)
        link = CharField(required=False)
        media = CharField(required=False)
        checksum = CharField(required=False, allow_blank=True)
        careContextReference = CharField(required=True)

    transactionId = UUIDField(required=True)
    entries = ListField(child=EntrySerializer())
    keyMaterial = KeyMaterialSerializer(required=True)
    pageNumber = IntegerField(required=True)
    pageCount = IntegerField(required=True)
