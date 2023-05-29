"""Class VaccinationAppointmentCancel"""
from datetime import datetime
from uc3m_care.data.attribute.attribute_date_signature import DateSignature
from uc3m_care.data.attribute.attribute_cancelation_type import CancelationType
from uc3m_care.data.attribute.attribute_reason import Reason
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.storage.appointments_json_store import AppointmentsJsonStore
from uc3m_care.storage.vaccination_json_store import VaccinationJsonStore
from uc3m_care.storage.cancellation_json_store import CancellationJsonStore
from uc3m_care.parser.cancelation_json_parser import CancelationJsonParser

class VaccinationAppointmentCancel():
    """Class representing an appointment  for the vaccination of a patient"""

    def __init__( self, date_signature, cancelation_type, reason):
        self._date_signature = DateSignature(date_signature).value
        self._cancelation_type = CancelationType(cancelation_type).value
        self._reason = Reason(reason).value
        vaccination_appointment = self.get_appointment_from_date_signature(self._date_signature)
        self.check_date(vaccination_appointment['_VaccinationAppointment__appointment_date'])
        self.modify_appointment(vaccination_appointment, self._cancelation_type)


    def get_appointment_from_date_signature(self, date_signature):
        """returns the vaccination appointment object for the date_signature received"""
        appointments_store = AppointmentsJsonStore()
        appointment_record = appointments_store.find_item(date_signature)
        if appointment_record is None:
            raise VaccineManagementException("date_signature is not found")
        vaccination_store = VaccinationJsonStore()
        vaccination_record = vaccination_store.find_item(date_signature)
        if vaccination_record is not None:
            raise VaccineManagementException("Patient already vaccinated")
        return appointment_record


    @property
    def date_signature(self):
        """porperty date_signature"""
        return self._date_signature
    @date_signature.setter
    def date_signature(self, value):
        """setter date_signature"""
        self._date_signature = DateSignature(value).value

    @property
    def cancelation_type(self):
        """property cancelation_type"""
        return self._cancelation_type

    @cancelation_type.setter
    def cancelation_type(self, value):
        """Setter cancelation_type"""
        self._cancelation_type = CancelationType(value).value

    @property
    def reason(self):
        """property reason"""
        return self._reason

    @reason.setter
    def reason(self, value):
        """setter reason"""
        self._reason = Reason(value).value
    @classmethod
    def create_appointment_cancelation_request_from_json_file(cls, json_file):
        """returns the vaccination appointment for the received input json file"""
        cancelation_parser = CancelationJsonParser(json_file)
        new_appointment = cls(
            cancelation_parser.json_content[cancelation_parser.DATE_SIGNATURE_KEY],
            cancelation_parser.json_content[cancelation_parser.CANCELATION_TYPE_KEY],
            cancelation_parser.json_content[cancelation_parser.REASON_KEY])
        return new_appointment


    def check_date(self, date):
        """check_date method"""
        today_date = datetime.today()
        today_date_timestamp = datetime.timestamp(today_date)
        if date <= today_date_timestamp:
            raise VaccineManagementException("Vaccination date has already passed")

    def modify_appointment(self, item, type):
        """modify_appointment method"""
        appointment = AppointmentsJsonStore()
        appointment.appointment_state_modify(item, type)
        if type == "Final":
            cancellation = CancellationJsonStore()
            cancellation.add_item(item)
