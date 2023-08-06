import pdb
from typing import Optional, Type, Union

from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from edc_reference import site_reference_configs
from edc_visit_schedule import Crf, FormsCollection, Requisition, site_visit_schedules
from edc_visit_tracking.constants import MISSED_VISIT

from ..constants import KEYED, NOT_REQUIRED, REQUIRED
from ..stubs import CrfMetadataModelStub, RequisitionMetadataModelStub, VisitModel


class CreatesMetadataError(Exception):
    pass


class DeleteMetadataError(Exception):
    pass


class CrfCreator:
    metadata_model = "edc_metadata.crfmetadata"

    def __init__(
        self,
        visit_model_instance: VisitModel,
        update_keyed: bool,
        crf: Union[Crf, Requisition],
    ) -> None:
        self._metadata_obj: Optional[Model] = None
        self.update_keyed = update_keyed
        self.visit_model_instance = visit_model_instance
        self.crf = crf

    @property
    def metadata_model_cls(
        self,
    ) -> Union[Type[CrfMetadataModelStub], Type[RequisitionMetadataModelStub]]:
        return django_apps.get_model(self.metadata_model)

    @property
    def reference_model_cls(self) -> Type[Model]:
        reference_model = site_reference_configs.get_reference_model(name=self.crf.model)
        return django_apps.get_model(reference_model)

    @property
    def options(self) -> dict:
        options = self.visit_model_instance.metadata_query_options
        options.update(
            {
                "subject_identifier": self.visit_model_instance.subject_identifier,
                "model": self.crf.model,
            }
        )
        return options

    @property
    def metadata_obj(self) -> Union[CrfMetadataModelStub, RequisitionMetadataModelStub]:
        """Returns a metadata model instance.

        Creates the metadata model instance to represent a
        CRF, if it does not already exist.
        """
        if not self._metadata_obj:
            try:
                metadata_obj = self.metadata_model_cls.objects.get(**self.options)
            except ObjectDoesNotExist:
                metadata_obj = self.metadata_model_cls.objects.create(
                    entry_status=REQUIRED if self.crf.required else NOT_REQUIRED,
                    show_order=self.crf.show_order,
                    site=self.visit_model_instance.site,
                    **self.options,
                )
            else:
                if metadata_obj.entry_status in [REQUIRED, NOT_REQUIRED]:
                    if self.crf.required and metadata_obj.entry_status == NOT_REQUIRED:
                        metadata_obj.entry_status = REQUIRED
                        metadata_obj.save()
                    elif (not self.crf.required) and (metadata_obj.entry_status == REQUIRED):
                        metadata_obj.entry_status = NOT_REQUIRED
                        metadata_obj.save()
            self._metadata_obj = metadata_obj
        return self._metadata_obj

    def create(self) -> Union[CrfMetadataModelStub, RequisitionMetadataModelStub]:
        """Creates a metadata model instance to represent a
        CRF, if it does not already exist.
        """
        if self.update_keyed and self.metadata_obj.entry_status != KEYED:
            if self.is_keyed:
                self.metadata_obj.entry_status = KEYED
                self.metadata_obj.save()
        return self.metadata_obj

    @property
    def is_keyed(self) -> bool:
        """Returns True if CRF is keyed determined by
        querying the reference model.

        If model instance actually exists, warns then returns True
        regardless of `reference` data.

        See also edc_reference.
        """
        exists_instance = (
            django_apps.get_model(self.crf.model)
            .objects.filter(subject_visit=self.visit_model_instance)
            .exists()
        )
        exists_reference = self.reference_model_cls.objects.filter_crf_for_visit(
            name=self.crf.model, visit=self.visit_model_instance
        ).exists()
        if exists_reference != exists_instance:
            print(
                f"is_keyed mismatch: {self.crf.model}, {self.visit_model_instance}, "
                f"ref={exists_reference}, instance={exists_instance}. Fixed"
            )
        return (
            django_apps.get_model(self.crf.model)
            .objects.filter(subject_visit=self.visit_model_instance)
            .exists()
        )


class RequisitionCreator(CrfCreator):
    metadata_model: str = "edc_metadata.requisitionmetadata"

    def __init__(
        self,
        requisition: Requisition,
        update_keyed: bool,
        visit_model_instance: VisitModel,
    ) -> None:
        super().__init__(
            crf=requisition,
            update_keyed=update_keyed,
            visit_model_instance=visit_model_instance,
        )
        self.panel_name: str = f"{self.requisition.model}.{self.requisition.panel.name}"

    @property
    def reference_model_cls(self) -> Type[Model]:
        reference_model = site_reference_configs.get_reference_model(name=self.panel_name)
        return django_apps.get_model(reference_model)

    @property
    def requisition(self) -> Requisition:
        return self.crf

    @property
    def options(self) -> dict:
        options = super().options
        options.update({"panel_name": self.requisition.panel.name})
        return options

    @property
    def is_keyed(self) -> bool:
        """Returns True if requisition is keyed determined by
        getting the reference model instance for this
        requisition+panel_name .

        See also edc_reference.
        """
        return self.reference_model_cls.objects.get_requisition_for_visit(
            name=self.panel_name, visit=self.visit_model_instance
        )


class Creator:
    crf_creator_cls = CrfCreator
    requisition_creator_cls = RequisitionCreator

    def __init__(
        self,
        update_keyed: bool,
        visit_model_instance: VisitModel,
    ) -> None:
        self.visit_model_instance: VisitModel = visit_model_instance
        self.update_keyed = update_keyed
        self.visit_code_sequence = self.visit_model_instance.visit_code_sequence
        self.visit = (
            site_visit_schedules.get_visit_schedule(
                self.visit_model_instance.visit_schedule_name
            )
            .schedules.get(self.visit_model_instance.schedule_name)
            .visits.get(self.visit_model_instance.visit_code)
        )

    @property
    def crfs(self) -> FormsCollection:
        """Returns list of crfs for this visit based on
        values for visit_code_sequence and MISSED_VISIT.
        """
        if self.visit_model_instance.reason == MISSED_VISIT:
            return self.visit.crfs_missed
        elif self.visit_code_sequence != 0:
            return self.visit.crfs_unscheduled
        return self.visit.crfs

    @property
    def requisitions(self) -> FormsCollection:
        if self.visit_code_sequence != 0:
            return self.visit.requisitions_unscheduled
        elif self.visit_model_instance.reason == MISSED_VISIT:
            return FormsCollection()
        return self.visit.requisitions

    def create(self) -> None:
        """Creates metadata for all CRFs and requisitions for
        the scheduled or unscheduled visit instance.
        """
        for crf in self.crfs:
            self.create_crf(crf)
        for requisition in self.requisitions:
            self.create_requisition(requisition)

    def create_crf(self, crf) -> CrfMetadataModelStub:
        return self.crf_creator_cls(
            crf=crf,
            update_keyed=self.update_keyed,
            visit_model_instance=self.visit_model_instance,
        ).create()

    def create_requisition(self, requisition) -> RequisitionMetadataModelStub:
        return self.requisition_creator_cls(
            requisition=requisition,
            update_keyed=self.update_keyed,
            visit_model_instance=self.visit_model_instance,
        ).create()


class Destroyer:
    metadata_crf_model = "edc_metadata.crfmetadata"
    metadata_requisition_model = "edc_metadata.requisitionmetadata"

    def __init__(self, visit_model_instance: VisitModel) -> None:
        self.visit_model_instance: VisitModel = visit_model_instance

    @property
    def metadata_crf_model_cls(self) -> Type[CrfMetadataModelStub]:
        return django_apps.get_model(self.metadata_crf_model)

    @property
    def metadata_requisition_model_cls(self) -> Type[RequisitionMetadataModelStub]:
        return django_apps.get_model(self.metadata_requisition_model)

    def delete(self) -> int:
        """Deletes all CRF and requisition metadata for
        the visit instance (self.visit_model_instance) excluding where
        entry_status = KEYED.
        """
        qs = self.metadata_crf_model_cls.objects.filter(
            subject_identifier=self.visit_model_instance.subject_identifier,
            **self.visit_model_instance.metadata_query_options,
        ).exclude(entry_status=KEYED)
        deleted = qs.delete()
        qs = self.metadata_requisition_model_cls.objects.filter(
            subject_identifier=self.visit_model_instance.subject_identifier,
            **self.visit_model_instance.metadata_query_options,
        ).exclude(entry_status=KEYED)
        qs.delete()
        return deleted


class Metadata:
    creator_cls = Creator
    destroyer_cls = Destroyer

    def __init__(
        self,
        visit_model_instance: VisitModel,
        update_keyed: bool,
    ) -> None:
        self._reason = None
        self._reason_field = "reason"
        self.visit_model_instance = visit_model_instance
        self.creator = self.creator_cls(
            visit_model_instance=visit_model_instance, update_keyed=update_keyed
        )
        self.destroyer = self.destroyer_cls(visit_model_instance=visit_model_instance)

    def prepare(self) -> bool:
        """Creates or deletes metadata, depending on the visit reason,
        for the visit instance.
        """
        metadata_exists = False
        if self.reason in self.visit_model_instance.visit_schedule.delete_metadata_on_reasons:
            self.destroyer.delete()
        elif (
            self.reason in self.visit_model_instance.visit_schedule.create_metadata_on_reasons
        ):
            self.destroyer.delete()
            self.creator.create()
            metadata_exists = True
        else:
            visit = self.creator.visit
            raise CreatesMetadataError(
                f"Undefined 'reason'. Cannot create metadata. Got "
                f"reason='{self.reason}'. Visit='{visit}'. "
                "Check field value and/or edc_metadata.AppConfig."
                "create_on_reasons/delete_on_reasons."
            )
        return metadata_exists

    @property
    def reason(self):
        """Returns the `value` of the reason field on the
        subject visit model instance.

        For example: `schedule` or `unscheduled`
        """
        if not self._reason:
            reason_field = self.visit_model_instance.visit_schedule.visit_model_reason_field
            try:
                self._reason = getattr(self.visit_model_instance, reason_field)
            except AttributeError as e:
                raise CreatesMetadataError(
                    f"Invalid reason field. Expected attribute {reason_field}. "
                    f"{self.visit_model_instance._meta.label_lower}. Got {e}. "
                    f"visit schedule `{self.visit_model_instance.visit_schedule.name}` "
                    f"visit_model_reason_field = {reason_field}"
                ) from e
            if not self._reason:
                raise CreatesMetadataError(
                    f"Invalid reason from field '{reason_field}'. Got None. "
                    "Check field value and/or edc_metadata.AppConfig."
                    "create_on_reasons/delete_on_reasons."
                )
        return self._reason
