"""TESTS FOR CANCEL_APPOINTMENT METHOD"""
from unittest import TestCase
from freezegun import freeze_time
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException
from uc3m_care import JSON_FILES_RF2_PATH, JSON_FILES_PF_PATH
from uc3m_care import AppointmentsJsonStore
from uc3m_care import PatientsJsonStore
from uc3m_care import VaccinationJsonStore
from uc3m_care import CancellationJsonStore


param_list_nok = [("test_pf_node_1_duplication.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_1_deletion.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_2_duplication.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_2_deletion.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_3_duplication.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_3_deletion.json", "Bad label date_signature"),
                  ("test_pf_node_4_duplication.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_4_deletion.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_5_modification.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_6_duplication.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_6_deletion.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_7_duplication.json", "Bad label date_signature"),
                  ("test_pf_node_7_deletion.json", "Bad label date_signature"),
                  ("test_pf_node_8_duplication.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_8_deletion.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_9_duplication.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_9_deletion.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_10_duplication.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_10_deletion.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_11_duplication.json", "date_signature format is not valid"),
                  ("test_pf_node_11_deletion.json", "date_signature format is not valid"),
                  ("test_pf_node_12_duplication.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_12_deletion.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_13_duplication.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_13_deletion.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_14_duplication.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_14_deletion.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_15_duplication.json", "Bad label cancelation_type"),
                  ("test_pf_node_15_deletion.json", "Bad label cancelation_type"),
                  ("test_pf_node_16_duplication.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_16_deletion.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_17_duplication.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_17_deletion.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_18_duplication.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_18_deletion.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_19_duplication.json", "cancelation_type is not valid"),
                  ("test_pf_node_19_deletion.json", "cancelation_type is not valid"),
                  ("test_pf_node_20_duplication.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_20_deletion.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_21_duplication.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_21_deletion.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_22_duplication.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_22_deletion.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_23_duplication.json", "Bad label reason"),
                  ("test_pf_node_23_deletion.json", "Bad label reason"),
                  ("test_pf_node_24_duplication.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_24_deletion.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_25_duplication.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_25_deletion.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_26_duplication.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_26_deletion.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_27_deletion.json", "reason is not valid"),
                  ("test_pf_node_28_duplication.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_28_deletion.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_29_modification.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_30_modification.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_31_modification.json", "Bad label date_signature"),
                  ("test_pf_node_32_modification.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_33_modification.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_34_modification.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_35_modification.json", "date_signature format is not valid"),
                  ("test_pf_node_36_modification.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_37_modification.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_38_modification.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_39_modification.json", "Bad label cancelation_type"),
                  ("test_pf_node_40_modification.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_41_modification.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_42_modification.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_43_modification.json", "cancelation_type is not valid"),
                  ("test_pf_node_44_modification.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_45_modification.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_46_modification.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_47_modification.json", "Bad label reason"),
                  ("test_pf_node_48_modification.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_49_modification.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_50_modification.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_node_52_modification.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_pf_hagaya_pabaya.json", "File is not found"),
                  ("test_pf_invalid_appointment.json", "date_signature is not found"),
                  ("test_pf_cv_reason_1.json", "reason is not valid"),
                  ("test_pf_cv_reason_101.json", "reason is not valid"),
                  ("test_pf_cv_date_signature_63.json", "date_signature format is not valid"),
                  ("test_pf_cv_date_signature_65.json", "date_signature format is not valid")
                ]

class TestCancelAppointment(TestCase):
    """Tests for the cancel_appointment method"""
    @freeze_time("2022-03-08")
    def test_valid(self):
        """test 1"""
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        file_store_vaccine = VaccinationJsonStore()
        file_store_vaccine.delete_json_file()
        file_store_cancellation = CancellationJsonStore()
        file_store_cancellation.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        date = "2022-03-18"

        my_manager.get_vaccine_date(file_test, date)

        file_test = JSON_FILES_PF_PATH + "test_pf_valid.json"
        value = my_manager.cancel_appointment(file_test)
        self.assertEqual(value, "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")

    @freeze_time("2022-03-08")
    def test_valid2(self):
        """test 2"""
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        file_store = VaccinationJsonStore()
        file_store_date.delete_json_file()
        file_store_cancellation = CancellationJsonStore()
        file_store_cancellation.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        date = "2022-03-18"

        my_manager.get_vaccine_date(file_test, date)

        file_test = JSON_FILES_PF_PATH + "test_pf_node_27_duplication.json"
        value = my_manager.cancel_appointment(file_test)
        self.assertEqual(value, "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")

    @freeze_time("2022-03-08")
    def test_valid3(self):
        """test 3"""
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        file_store = VaccinationJsonStore()
        file_store_date.delete_json_file()
        file_store_cancellation = CancellationJsonStore()
        file_store_cancellation.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        date = "2022-03-18"

        my_manager.get_vaccine_date(file_test, date)

        file_test = JSON_FILES_PF_PATH + "test_pf_node_51_modification.json"
        value = my_manager.cancel_appointment(file_test)
        self.assertEqual(value, "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")

    @freeze_time("2022-03-08")
    def test_not_valid(self):
        """test 4"""
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        file_store_vaccine = VaccinationJsonStore()
        file_store_vaccine.delete_json_file()
        file_store_cancellation = CancellationJsonStore()
        file_store_cancellation.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        date = "2022-03-18"

        my_manager.get_vaccine_date(file_test, date)

        for file_name, expected_value in param_list_nok:
            with self.subTest(test=file_name):
                file_test = JSON_FILES_PF_PATH + file_name
                with self.assertRaises(VaccineManagementException) as context_manager:
                    my_manager.cancel_appointment(file_test)
                self.assertEqual(context_manager.exception.message, expected_value)
    @freeze_time("2022-03-08")
    def test_pf_already_vaccinated_setup(self):
        """test 5"""
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        file_store_vaccine = VaccinationJsonStore()
        file_store_vaccine.delete_json_file()
        file_store_cancellation = CancellationJsonStore()
        file_store_cancellation.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        date = "2022-03-18"

        my_manager.get_vaccine_date(file_test, date)
    @freeze_time("2022-03-18")
    def test_pf_already_vaccinated(self):
        """test 6"""
        my_manager = VaccineManager()
        my_manager.vaccine_patient("5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        file_test = JSON_FILES_PF_PATH + "test_pf_valid.json"
        with self.assertRaises(VaccineManagementException) as context_manager:
            my_manager.cancel_appointment(file_test)
        self.assertEqual(context_manager.exception.message, "Patient already vaccinated")



    @freeze_time("2022-03-19")
    def test_pf_invalid_date(self):
        """test 7"""
        file_store = VaccinationJsonStore()
        file_store.delete_json_file()
        my_manager = VaccineManager()
        file_test = JSON_FILES_PF_PATH + "test_pf_valid.json"
        with self.assertRaises(VaccineManagementException) as context_manager:
            my_manager.cancel_appointment(file_test)
        self.assertEqual(context_manager.exception.message, "Vaccination date has already passed")

    @freeze_time("2022-03-08")
    def test_pf_final_temporal(self):
        """test 8"""
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        file_store_vaccine = VaccinationJsonStore()
        file_store_vaccine.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        date = "2022-03-18"

        my_manager.get_vaccine_date(file_test, date)

        file_test = JSON_FILES_PF_PATH + "test_pf_valid.json"
        my_manager.cancel_appointment(file_test)
        file_test = JSON_FILES_PF_PATH + "test_pf_valid_2.json"
        with self.assertRaises(VaccineManagementException) as context_manager:
            my_manager.cancel_appointment(file_test)
        self.assertEqual(context_manager.exception.message, "Appointment is already cancelled")

    @freeze_time("2022-03-08")
    def test_pf_valid_2(self):
        """test 9"""
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        file_store_vaccine = VaccinationJsonStore()
        file_store_vaccine.delete_json_file()
        file_store_cancellation = CancellationJsonStore()
        file_store_cancellation.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        date = "2022-03-18"

        my_manager.get_vaccine_date(file_test, date)

        file_test = JSON_FILES_PF_PATH + "test_pf_valid_2.json"
        my_manager.cancel_appointment(file_test)
        file_test = JSON_FILES_PF_PATH + "test_pf_valid.json"
        value = my_manager.cancel_appointment(file_test)
        self.assertEqual(value, "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")

    @freeze_time("2022-03-08")
    def test_pf_cv_reason_2(self):
        """test 10"""
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        file_store_vaccine = VaccinationJsonStore()
        file_store_vaccine.delete_json_file()
        file_store_cancellation = CancellationJsonStore()
        file_store_cancellation.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        date = "2022-03-18"

        my_manager.get_vaccine_date(file_test, date)
        file_test = JSON_FILES_PF_PATH + "test_pf_cv_reason_2.json"
        value = my_manager.cancel_appointment(file_test)
        self.assertEqual(value, "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")

    @freeze_time("2022-03-08")
    def test_pf_cv_reason_3(self):
        """test 11"""
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        file_store_vaccine = VaccinationJsonStore()
        file_store_vaccine.delete_json_file()
        file_store_cancellation = CancellationJsonStore()
        file_store_cancellation.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        date = "2022-03-18"

        my_manager.get_vaccine_date(file_test, date)
        file_test = JSON_FILES_PF_PATH + "test_pf_cv_reason_3.json"
        value = my_manager.cancel_appointment(file_test)
        self.assertEqual(value, "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")

    @freeze_time("2022-03-08")
    def test_pf_cv_reason_99(self):
        """test 12"""
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        file_store_vaccine = VaccinationJsonStore()
        file_store_vaccine.delete_json_file()
        file_store_cancellation = CancellationJsonStore()
        file_store_cancellation.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        date = "2022-03-18"

        my_manager.get_vaccine_date(file_test, date)
        file_test = JSON_FILES_PF_PATH + "test_pf_cv_reason_99.json"
        value = my_manager.cancel_appointment(file_test)
        self.assertEqual(value, "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")

    @freeze_time("2022-03-08")
    def test_pf_cv_reason_100(self):
        """test 13"""
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        file_store_vaccine = VaccinationJsonStore()
        file_store_vaccine.delete_json_file()
        file_store_cancellation = CancellationJsonStore()
        file_store_cancellation.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        date = "2022-03-18"

        my_manager.get_vaccine_date(file_test, date)
        file_test = JSON_FILES_PF_PATH + "test_pf_cv_reason_100.json"
        value = my_manager.cancel_appointment(file_test)
        self.assertEqual(value, "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")

    @freeze_time("2022-03-08")
    def test_pf_cv_date_setup(self):
        """test 13"""
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        file_store_vaccine = VaccinationJsonStore()
        file_store_vaccine.delete_json_file()
        file_store_cancellation = CancellationJsonStore()
        file_store_cancellation.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        date = "2022-03-18"

        my_manager.get_vaccine_date(file_test, date)

    @freeze_time("2022-03-17")
    def test_pf_cv_date_1(self):
        """test_pf_cv_date_1 test"""
        my_manager = VaccineManager()
        file_test = JSON_FILES_PF_PATH + "test_pf_valid.json"
        value = my_manager.cancel_appointment(file_test)
        self.assertEqual(value, "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")

    @freeze_time("2022-03-18")
    def test_pf_cv_date_2(self):
        """test_pf_cv_date_2 test"""
        my_manager = VaccineManager()
        file_test = JSON_FILES_PF_PATH + "test_pf_valid.json"
        with self.assertRaises(VaccineManagementException) as context_manager:
            my_manager.cancel_appointment(file_test)
        self.assertEqual(context_manager.exception.message, "Vaccination date has already passed")

    @freeze_time("2022-03-19")
    def test_pf_cv_date_3(self):
        """test_pf_cv_date_3 test"""
        my_manager = VaccineManager()
        file_test = JSON_FILES_PF_PATH + "test_pf_valid.json"
        with self.assertRaises(VaccineManagementException) as context_manager:
            my_manager.cancel_appointment(file_test)
        self.assertEqual(context_manager.exception.message, "Vaccination date has already passed")

    @freeze_time("2022-03-08")
    def test_pf_ce_final_final(self):
        """test 8"""
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        file_store_vaccine = VaccinationJsonStore()
        file_store_vaccine.delete_json_file()
        file_store_cancellation = CancellationJsonStore()
        file_store_cancellation.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        date = "2022-03-18"

        my_manager.get_vaccine_date(file_test, date)

        file_test = JSON_FILES_PF_PATH + "test_pf_valid.json"
        my_manager.cancel_appointment(file_test)
        file_test = JSON_FILES_PF_PATH + "test_pf_valid.json"
        with self.assertRaises(VaccineManagementException) as context_manager:
            my_manager.cancel_appointment(file_test)
        self.assertEqual(context_manager.exception.message, "Appointment is already cancelled")

    @freeze_time("2022-03-08")
    def test_pf_ce_temporal_temporal(self):
        """test 8"""
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        file_store_vaccine = VaccinationJsonStore()
        file_store_vaccine.delete_json_file()
        file_store_cancellation = CancellationJsonStore()
        file_store_cancellation.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        date = "2022-03-18"

        my_manager.get_vaccine_date(file_test, date)

        file_test = JSON_FILES_PF_PATH + "test_pf_valid_2.json"
        my_manager.cancel_appointment(file_test)
        file_test = JSON_FILES_PF_PATH + "test_pf_valid_2.json"
        with self.assertRaises(VaccineManagementException) as context_manager:
            my_manager.cancel_appointment(file_test)
        self.assertEqual(context_manager.exception.message, "Appointment is already cancelled")
