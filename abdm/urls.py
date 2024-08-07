from django.urls import path
from rest_framework.routers import SimpleRouter

from abdm.api.viewsets.abha_number import AbhaNumberViewSet
from abdm.api.viewsets.auth import (
    AuthNotifyView,
    DiscoverView,
    LinkConfirmView,
    LinkInitView,
    NotifyView,
    OnAddContextsView,
    OnConfirmView,
    OnFetchView,
    OnInitView,
    RequestDataView,
)
from abdm.api.viewsets.consent import ConsentCallbackViewSet, ConsentViewSet
from abdm.api.viewsets.health_facility import HealthFacilityViewSet
from abdm.api.viewsets.health_information import (
    HealthInformationCallbackViewSet,
    HealthInformationViewSet,
)
from abdm.api.viewsets.healthid import ABDMHealthIDViewSet
from abdm.api.viewsets.hip import HipViewSet
from abdm.api.viewsets.monitoring import HeartbeatView
from abdm.api.viewsets.patients import PatientsCallbackViewSet, PatientsViewSet
from abdm.api.viewsets.status import NotifyView as PatientStatusNotifyView
from abdm.api.viewsets.status import SMSOnNotifyView


class OptionalSlashRouter(SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = "/?"


router = OptionalSlashRouter()


router.register("healthid", ABDMHealthIDViewSet, basename="abdm-healthid")
router.register("consent", ConsentViewSet, basename="abdm-consent")
router.register(
    "health_information",
    HealthInformationViewSet,
    basename="abdm-healthinformation",
)
router.register("patients", PatientsViewSet, basename="abdm-patients")
router.register("abha_numbers", AbhaNumberViewSet, basename="abdm-abhanumber")
router.register(
    "health_facility", HealthFacilityViewSet, basename="abdm-healthfacility"
)


router.register("profile/v1.0/patients/", HipViewSet, basename="hip")

urlpatterns = [
    *router.urls,
    path(
        "v0.5/consent-requests/on-init",
        ConsentCallbackViewSet.as_view({"post": "consent_request__on_init"}),
        name="abdm__consent_request__on_init",
    ),
    path(
        "v0.5/consent-requests/on-status",
        ConsentCallbackViewSet.as_view({"post": "consent_request__on_status"}),
        name="abdm__consent_request__on_status",
    ),
    path(
        "v0.5/consents/hiu/notify",
        ConsentCallbackViewSet.as_view({"post": "consents__hiu__notify"}),
        name="abdm__consents__hiu__notify",
    ),
    path(
        "v0.5/consents/on-fetch",
        ConsentCallbackViewSet.as_view({"post": "consents__on_fetch"}),
        name="abdm__consents__on_fetch",
    ),
    path(
        "v0.5/health-information/hiu/on-request",
        HealthInformationCallbackViewSet.as_view(
            {"post": "health_information__hiu__on_request"}
        ),
        name="abdm__health_information__hiu__on_request",
    ),
    path(
        "v0.5/health-information/transfer",
        HealthInformationCallbackViewSet.as_view(
            {"post": "health_information__transfer"}
        ),
        name="abdm__health_information__transfer",
    ),
    path(
        "v0.5/patients/on-find",
        PatientsCallbackViewSet.as_view({"post": "patients__on_find"}),
        name="abdm__patients__on_find",
    ),
    path(
        "v0.5/users/auth/on-fetch-modes",
        OnFetchView.as_view(),
        name="abdm_on_fetch_modes_view",
    ),
    path(
        "v0.5/users/auth/on-init",
        OnInitView.as_view(),
        name="abdm_on_init_view",
    ),
    path(
        "v0.5/users/auth/on-confirm",
        OnConfirmView.as_view(),
        name="abdm_on_confirm_view",
    ),
    path(
        "v0.5/users/auth/notify",
        AuthNotifyView.as_view(),
        name="abdm_auth_notify_view",
    ),
    path(
        "v0.5/links/link/on-add-contexts",
        OnAddContextsView.as_view(),
        name="abdm_on_add_context_view",
    ),
    path(
        "v0.5/care-contexts/discover",
        DiscoverView.as_view(),
        name="abdm_discover_view",
    ),
    path(
        "v0.5/links/link/init",
        LinkInitView.as_view(),
        name="abdm_link_init_view",
    ),
    path(
        "v0.5/links/link/confirm",
        LinkConfirmView.as_view(),
        name="abdm_link_confirm_view",
    ),
    path(
        "v0.5/consents/hip/notify",
        NotifyView.as_view(),
        name="abdm_notify_view",
    ),
    path(
        "v0.5/health-information/hip/request",
        RequestDataView.as_view(),
        name="abdm_request_data_view",
    ),
    path(
        "v0.5/patients/status/notify",
        PatientStatusNotifyView.as_view(),
        name="abdm_patient_status_notify_view",
    ),
    path(
        "v0.5/patients/sms/on-notify",
        SMSOnNotifyView.as_view(),
        name="abdm_patient_status_notify_view",
    ),
    path(
        "v0.5/heartbeat",
        HeartbeatView.as_view(),
        name="abdm_monitoring_heartbeat_view",
    ),
]
