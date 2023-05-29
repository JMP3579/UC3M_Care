"""Class CancellationJsonStore"""
from uc3m_care.storage.json_store import JsonStore
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH

class CancellationJsonStore():
    """Implements the singleton pattern"""
    #pylint: disable=invalid-name
    class __CancellationJsonStore(JsonStore):
        """Subclass of JsonStore for managing the Appointments"""
        _FILE_PATH = JSON_FILES_PATH + "store_cancellation.json"
        _ID_FIELD = "_VaccinationAppointment__date_signature"
        ERROR_INVALID_APPOINTMENT_OBJECT = "Invalide appointment object"

        def add_item( self, item ):
            """Overrides the add_item method to verify the item to be stored"""
            #pylint: disable=import-outside-toplevel, cyclic-import
            self._data_list.append(item)
            self.save()

    instance = None
    def __new__ ( cls ):
        if not CancellationJsonStore.instance:
            CancellationJsonStore.instance = CancellationJsonStore.__CancellationJsonStore()
        return CancellationJsonStore.instance

    def __getattr__ ( self, nombre ):
        return getattr(self.instance, nombre)

    def __setattr__ ( self, nombre, valor ):
        return setattr(self.instance, nombre, valor)
