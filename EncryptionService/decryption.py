import tenseal as ts
import base64
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from models_decryption import  decrypted_target_engine,  \
    DecryptedPersonalData, DecryptedDiagnostic, DecryptedHealthEventOccurrence, \
    DecryptedEventTime, DecryptedAnalysisReport, DecryptedPatientData
from models import target_engine, PersonalData, Diagnostic, HealthEventOccurrence, EventTime, \
    AnalysisReport, PatientData

def load_context(filename):
    with open(filename, 'rb') as f:
        return ts.context_from(f.read())


# Load the TenSEAL context from the file
context = load_context('tenseal_context.bin')
offset = 1000  # Offset to ensure characters are within a specific range


def decrypt_data(encrypted_data, data_type='str'):
    if encrypted_data is None or encrypted_data == "":
        return None

    encrypted_data = base64.b64decode(encrypted_data)
    encrypted_vector = ts.bfv_vector_from(context, encrypted_data)
    decrypted_vector = encrypted_vector.decrypt()
    decrypted_data = list(decrypted_vector)  # Ensure it's a list

    # Detailed debugging output
    print(f"Decrypted data (raw vector): {decrypted_data}")

    try:
        # Adjust for the offset
        adjusted_data = [i - offset for i in decrypted_data]

        if data_type == 'str':
            decoded_str = ''.join(chr(i) for i in adjusted_data)
            print(f"Decrypted data as ASCII: {decoded_str}")
            return decoded_str
        elif data_type == 'int':
            return adjusted_data[0]
        elif data_type == 'date':
            date_str = ''.join(chr(i) for i in adjusted_data if 0 <= i < 128)  # Filter to ASCII range for dates
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            print(f"Decrypted data as Date: {date}")
            return date
        else:
            raise ValueError(f"Unsupported data type: {data_type}")
    except Exception as e:
        print(f"Error processing decrypted data: {decrypted_data}, error: {e}")
        raise ValueError(f"Decrypted data type could not be determined: {decrypted_data}")


def decrypt_and_store_data():
    TargetSession = sessionmaker(bind=target_engine)
    DecryptedTargetSession = sessionmaker(bind=decrypted_target_engine)

    target_session = TargetSession()
    decrypted_target_session = DecryptedTargetSession()

    try:
        # PersonalData
        personal_data_records = target_session.query(PersonalData).all()
        decrypted_personal_data_records = []
        for record in personal_data_records:
            decrypted_name = decrypt_data(record.name)
            new_record = DecryptedPersonalData(
                id=record.id,
                name=decrypted_name,
                gender=record.gender,
                age=record.age
            )
            decrypted_personal_data_records.append(new_record)
        decrypted_target_session.bulk_save_objects(decrypted_personal_data_records)
        decrypted_target_session.commit()
        print(f"Decrypted and stored {len(decrypted_personal_data_records)} PersonalData records")

        # Diagnostic
        diagnostic_records = target_session.query(Diagnostic).all()
        decrypted_diagnostic_records = []
        for record in diagnostic_records:
            decrypted_disease = decrypt_data(record.patient_disease)
            decrypted_picture = decrypt_data(record.picture)
            new_record = DecryptedDiagnostic(
                id=record.id,
                patient_disease=decrypted_disease,
                picture=decrypted_picture,
                personal_data_id=record.personal_data_id
            )
            decrypted_diagnostic_records.append(new_record)
        decrypted_target_session.bulk_save_objects(decrypted_diagnostic_records)
        decrypted_target_session.commit()
        print(f"Decrypted and stored {len(decrypted_diagnostic_records)} Diagnostic records")

        # HealthEventOccurrence
        event_records = target_session.query(HealthEventOccurrence).all()
        decrypted_event_records = []
        for record in event_records:
            decrypted_event_name = decrypt_data(record.event_name)
            decrypted_event_time = decrypt_data(record.event_time)
            new_record = DecryptedHealthEventOccurrence(
                id=record.id,
                event_name=decrypted_event_name,
                event_time=decrypted_event_time,
                personal_data_id=record.personal_data_id
            )
            decrypted_event_records.append(new_record)
        decrypted_target_session.bulk_save_objects(decrypted_event_records)
        decrypted_target_session.commit()
        print(f"Decrypted and stored {len(decrypted_event_records)} HealthEventOccurrence records")

        # EventTime
        event_time_records = target_session.query(EventTime).all()
        decrypted_event_time_records = []
        for record in event_time_records:
            decrypted_min_heart_rate_time = decrypt_data(record.min_heart_rate_time)
            decrypted_max_heart_rate_time = decrypt_data(record.max_heart_rate_time)
            decrypted_max_long_asystole_time = decrypt_data(record.max_long_asystole_time)
            decrypted_longest_ventricular_tachycardia_occur_time = decrypt_data(
                record.longest_ventricular_tachycardia_occur_time)
            decrypted_longest_atrial_tachycardia_occur_time = decrypt_data(record.longest_atrial_tachycardia_occur_time)
            decrypted_data_end_time = decrypt_data(record.data_end_time)
            decrypted_data_start_time = decrypt_data(record.data_start_time)
            new_record = DecryptedEventTime(
                id=record.id,
                min_heart_rate_time=decrypted_min_heart_rate_time,
                max_heart_rate_time=decrypted_max_heart_rate_time,
                max_long_asystole_time=decrypted_max_long_asystole_time,
                longest_ventricular_tachycardia_occur_time=decrypted_longest_ventricular_tachycardia_occur_time,
                longest_atrial_tachycardia_occur_time=decrypted_longest_atrial_tachycardia_occur_time,
                data_end_time=decrypted_data_end_time,
                data_start_time=decrypted_data_start_time,
                personal_data_id=record.personal_data_id
            )
            decrypted_event_time_records.append(new_record)
        decrypted_target_session.bulk_save_objects(decrypted_event_time_records)
        decrypted_target_session.commit()
        print(f"Decrypted and stored {len(decrypted_event_time_records)} EventTime records")

        # AnalysisReport
        analysis_report_records = target_session.query(AnalysisReport).all()
        decrypted_analysis_report_records = []
        for record in analysis_report_records:
            decrypted_report_url = decrypt_data(record.report_url)
            new_record = DecryptedAnalysisReport(
                id=record.id,
                report_url=decrypted_report_url,
                personal_data_id=record.personal_data_id
            )
            decrypted_analysis_report_records.append(new_record)
        decrypted_target_session.bulk_save_objects(decrypted_analysis_report_records)
        decrypted_target_session.commit()
        print(f"Decrypted and stored {len(decrypted_analysis_report_records)} AnalysisReport records")

        # PatientData
        patient_data_records = target_session.query(PatientData).all()
        decrypted_patient_data_records = []
        for record in patient_data_records:
            decrypted_abnormal_beat_count = decrypt_data(record.abnormal_beat_count)
            decrypted_beat_count = decrypt_data(record.beat_count)
            new_record = DecryptedPatientData(
                id=record.id,
                abnormal_beat_count=decrypted_abnormal_beat_count,
                abnormal_beat_percent=record.abnormal_beat_percent,
                af_beat_percent=record.af_beat_percent,
                asystole_rr_period_count=record.asystole_rr_period_count,
                atrial_beat_count=record.atrial_beat_count,
                atrial_bigeminy_count=record.atrial_bigeminy_count,
                atrial_permature_beat_count=record.atrial_permature_beat_count,
                atrial_tachycardia_count=record.atrial_tachycardia_count,
                atrial_trigeminy_count=record.atrial_trigeminy_count,
                average_heart_rate=record.average_heart_rate,
                beat_count=decrypted_beat_count,
                couple_atrial_permature_count=record.couple_atrial_permature_count,
                couple_ventricular_permature_count=record.couple_ventricular_permature_count,
                long_rr_period_count=record.long_rr_period_count,
                longest_atrial_tachycardia_duration=record.longest_atrial_tachycardia_duration,
                longest_ventricular_tachycardia_duration=record.longest_ventricular_tachycardia_duration,
                max_heart_rate=record.max_heart_rate,
                max_long_rr_period=record.max_long_rr_period,
                min_heart_rate=record.min_heart_rate,
                total_duration=record.total_duration,
                valid_duration=record.valid_duration,
                ventricular_beat_count=record.ventricular_beat_count,
                ventricular_bigeminy_count=record.ventricular_bigeminy_count,
                ventricular_permature_beat_count=record.ventricular_permature_beat_count,
                ventricular_tachycardia_count=record.ventricular_tachycardia_count,
                ventricular_trigeminy_count=record.ventricular_trigeminy_count,
                personal_data_id=record.personal_data_id
            )
            decrypted_patient_data_records.append(new_record)
        decrypted_target_session.bulk_save_objects(decrypted_patient_data_records)
        decrypted_target_session.commit()
        print(f"Decrypted and stored {len(decrypted_patient_data_records)} PatientData records")

    except Exception as e:
        print(f"An error occurred: {e}")
        decrypted_target_session.rollback()
    finally:
        target_session.close()
        decrypted_target_session.close()


if __name__ == "__main__":
    decrypt_and_store_data()
