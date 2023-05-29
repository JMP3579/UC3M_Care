"""Classs for the attribute age"""
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException

#pylint: disable=too-few-public-methods
class Reason(Attribute):
    """Classs for the attribute reason"""
    _validation_error_message = "reason is not valid"

    def _validate( self, attr_value: str ) -> str:
        """Validates the age according to the requirements"""
        if len(attr_value) < 2 or len(attr_value) > 100:
            raise VaccineManagementException(self._validation_error_message)
        return attr_value
