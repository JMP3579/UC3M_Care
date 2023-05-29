"""Classs for the attribute DateSignature"""
import re
from datetime import datetime
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException

#pylint: disable=too-few-public-methods
class Date(Attribute):
    """Classs for the attribute DateSignature"""

    _validation_pattern = r"[0-9]{4}-[0-9]{2}-[0-9]{2}$"
    _validation_error_message = "date format is not valid"

    def _validate(self, attr_value):
        if type(attr_value) == str:
            registration_type_pattern = re.compile(self._validation_pattern)
            res = registration_type_pattern.fullmatch(attr_value)
            if not res:
                raise VaccineManagementException(self._validation_error_message)
            attr_value = datetime.strptime(attr_value, "%Y-%m-%d")
            attr_value = datetime.timestamp(attr_value)
        today_date = datetime.utcnow()
        today_date = datetime.timestamp(today_date)
        if attr_value <= today_date:
            raise VaccineManagementException("Appointment date is not valid")
        return attr_value
