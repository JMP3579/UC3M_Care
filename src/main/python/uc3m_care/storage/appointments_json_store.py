"""Subclass of JsonStore for managing the Appointments"""

from uc3m_care.storage.json_store import JsonStore
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


class AppointmentsJsonStore():
    """Implements the singleton pattern"""
    #pylint: disable=invalid-name
    class __AppointmentsJsonStore(JsonStore):
        """Subclass of JsonStore for managing the Appointments"""
        _FILE_PATH = JSON_FILES_PATH + "store_date.json"
        _ID_FIELD = "_VaccinationAppointment__date_signature"
        ERROR_INVALID_APPOINTMENT_OBJECT = "Invalide appointment object"

        def add_item( self, item ):
            """Overrides the add_item method to verify the item to be stored"""
            #pylint: disable=import-outside-toplevel, cyclic-import
            from uc3m_care.data.vaccination_appointment import VaccinationAppointment
            if not isinstance(item, VaccinationAppointment):
                raise VaccineManagementException(self.ERROR_INVALID_APPOINTMENT_OBJECT)
            super().add_item(item)

        def appointment_state_modify(self, item, new_state):
            """appointment_state_modify method"""
            #self.load()
            appointment = self._data_list.index(item)
            state = self._data_list[appointment]["_VaccinationAppointment__appointment_state"]
            if state == "Not cancelled" or (state == "Temporal" and new_state == "Final"):
                self._data_list[appointment]["_VaccinationAppointment__appointment_state"] = new_state
                self.save()
            else:
                raise VaccineManagementException("Appointment is already cancelled")



    instance = None
    def __new__ ( cls ):
        if not AppointmentsJsonStore.instance:
            AppointmentsJsonStore.instance = AppointmentsJsonStore.__AppointmentsJsonStore()
        return AppointmentsJsonStore.instance

    def __getattr__ ( self, nombre ):
        return getattr(self.instance, nombre)

    def __setattr__ ( self, nombre, valor ):
        return setattr(self.instance, nombre, valor)
