"""Classs for the attribute cancelation_type"""
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException

#pylint: disable=too-few-public-methods
class CancelationType(Attribute):
    """Classs for the attribute cancelation_type"""
    _validation_error_message = "cancelation_type is not valid"

    def _validate( self, attr_value: str ) -> str:
        """Validates the cancelation_type according to the requirements"""
        if attr_value == "Temporal" or attr_value == "Final":
            return attr_value
        else:
            raise VaccineManagementException(self._validation_error_message)
