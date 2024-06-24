import traceback

import tenseal as ts
import base64
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from models import source_engine, target_engine, PersonalData, Diagnostic, HealthEventOccurrence, EventTime, \
    AnalysisReport, PatientData

# Create TenSEAL context using BFV scheme
context = ts.context(
    ts.SCHEME_TYPE.BFV,
    poly_modulus_degree=32768,
    plain_modulus=786433,
    coeff_mod_bit_sizes=[60, 40, 40, 60]
)
context.generate_galois_keys()
context.generate_relin_keys()


def save_context(context, filename):
    with open(filename, 'wb') as f:
        f.write(context.serialize(save_secret_key=True))


def encrypt_data(data):
    try:
        if data is None or data == "":
            return None

        offset = 1000  # Use an offset to ensure characters are within a specific range
        if isinstance(data, str):
            vector = ts.bfv_vector(context, [ord(char) + offset for char in data])
        elif isinstance(data, (int, float)):
            vector = ts.bfv_vector(context, [int(data) + offset])
        elif isinstance(data, datetime):
            data_str = data.strftime('%Y-%m-%d %H:%M:%S')
            vector = ts.bfv_vector(context, [ord(char) + offset for char in data_str])
        else:
            raise ValueError("Data type not supported for encryption")

        encrypted_data = vector.serialize()
        return base64.b64encode(encrypted_data).decode('utf-8')
    except Exception as e:
        print(f"An error occurred while encrypting the data: {data}")
        raise e


def commit_in_batches(session, start, records, batch_size=10):
    count = start
    for i in range(0, len(records), batch_size):
        try:
            with session.begin():
                session.add_all(records[i:i + batch_size])
            count += batch_size
            print(f"Committed {count} records")
        except OperationalError as e:
            print(f"Error committing batch: {e}")
            session.rollback()
            retry_commit(session, records[i:i + batch_size])
            raise


def retry_commit(session, records):
    for record in records:
        try:
            with session.begin():
                session.add(record)
            print(f"Retry committed record {record.id}")
        except OperationalError as e:
            print(f"Retry error on record {record.id}: {e}")
            session.rollback()


def copy_and_encrypt_data():
    SourceSession = sessionmaker(bind=source_engine)
    TargetSession = sessionmaker(bind=target_engine)

    source_session = SourceSession()
    target_session = TargetSession()

    try:
        # PersonalData
        personal_data_records = source_session.query(PersonalData).all()
        encrypted_personal_data_records = []
        for record in personal_data_records:
            encrypted_name = encrypt_data(record.name)
            new_record = PersonalData(
                id=record.id,
                name=encrypted_name,
                gender=record.gender,
                age=record.age
            )
            encrypted_personal_data_records.append(new_record)
        commit_in_batches(target_session, 0, encrypted_personal_data_records)

        # Diagnostic
        diagnostic_records = source_session.query(Diagnostic).all()
        encrypted_diagnostic_records = []
        for record in diagnostic_records:
            encrypted_disease = encrypt_data(record.patient_disease)
            encrypted_picture = encrypt_data(record.picture)
            new_record = Diagnostic(
                id=record.id,
                patient_disease=encrypted_disease,
                picture=encrypted_picture,
                personal_data_id=record.personal_data_id
            )
            encrypted_diagnostic_records.append(new_record)
        commit_in_batches(target_session, len(encrypted_personal_data_records), encrypted_diagnostic_records)

        # HealthEventOccurrence
        event_records = source_session.query(HealthEventOccurrence).all()
        encrypted_event_records = []
        for record in event_records:
            encrypted_event_name = encrypt_data(record.event_name)
            encrypted_event_time = encrypt_data(record.event_time)
            new_record = HealthEventOccurrence(
                id=record.id,
                event_name=encrypted_event_name,
                event_time=encrypted_event_time,
                personal_data_id=record.personal_data_id
            )
            encrypted_event_records.append(new_record)
        commit_in_batches(target_session, len(encrypted_personal_data_records) + len(encrypted_diagnostic_records),
                          encrypted_event_records)

        # EventTime
        event_time_records = source_session.query(EventTime).all()
        encrypted_event_time_records = []
        for record in event_time_records:
            encrypted_min_heart_rate_time = encrypt_data(record.min_heart_rate_time)
            encrypted_max_heart_rate_time = encrypt_data(record.max_heart_rate_time)
            encrypted_max_long_asystole_time = encrypt_data(record.max_long_asystole_time)
            encrypted_longest_ventricular_tachycardia_occur_time = encrypt_data(
                record.longest_ventricular_tachycardia_occur_time)
            encrypted_longest_atrial_tachycardia_occur_time = encrypt_data(record.longest_atrial_tachycardia_occur_time)
            encrypted_data_end_time = encrypt_data(record.data_end_time)
            encrypted_data_start_time = encrypt_data(record.data_start_time)
            new_record = EventTime(
                id=record.id,
                min_heart_rate_time=encrypted_min_heart_rate_time,
                max_heart_rate_time=encrypted_max_heart_rate_time,
                max_long_asystole_time=encrypted_max_long_asystole_time,
                longest_ventricular_tachycardia_occur_time=encrypted_longest_ventricular_tachycardia_occur_time,
                longest_atrial_tachycardia_occur_time=encrypted_longest_atrial_tachycardia_occur_time,
                data_end_time=encrypted_data_end_time,
                data_start_time=encrypted_data_start_time,
                personal_data_id=record.personal_data_id
            )
            encrypted_event_time_records.append(new_record)
        commit_in_batches(target_session,
                          len(encrypted_personal_data_records) + len(encrypted_diagnostic_records) + len(
                              encrypted_event_records), encrypted_event_time_records)

        # AnalysisReport
        analysis_report_records = source_session.query(AnalysisReport).all()
        encrypted_analysis_report_records = []
        for record in analysis_report_records:
            encrypted_report_url = encrypt_data(record.report_url)
            new_record = AnalysisReport(
                id=record.id,
                report_url=encrypted_report_url,
                personal_data_id=record.personal_data_id
            )
            encrypted_analysis_report_records.append(new_record)
        commit_in_batches(target_session,
                          len(encrypted_personal_data_records) + len(encrypted_diagnostic_records) + len(
                              encrypted_event_records) + len(encrypted_event_time_records),
                          encrypted_analysis_report_records)

        # PatientData
        patient_data_records = source_session.query(PatientData).all()
        encrypted_patient_data_records = []
        for record in patient_data_records:
            encrypted_abnormal_beat_count = encrypt_data(record.abnormal_beat_count)
            new_record = PatientData(
                id=record.id,
                abnormal_beat_count=encrypted_abnormal_beat_count,
                abnormal_beat_percent=record.abnormal_beat_percent,
                af_beat_percent=record.af_beat_percent,
                asystole_rr_period_count=record.asystole_rr_period_count,
                atrial_beat_count=record.atrial_beat_count,
                atrial_bigeminy_count=record.atrial_bigeminy_count,
                atrial_permature_beat_count=record.atrial_permature_beat_count,
                atrial_tachycardia_count=record.atrial_tachycardia_count,
                atrial_trigeminy_count=record.atrial_trigeminy_count,
                average_heart_rate=record.average_heart_rate,
                beat_count=encrypt_data(record.beat_count),
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
            encrypted_patient_data_records.append(new_record)
        commit_in_batches(target_session,
                          len(encrypted_personal_data_records) + len(encrypted_diagnostic_records) + len(
                              encrypted_event_records) + len(encrypted_event_time_records) + len(
                              encrypted_analysis_report_records), encrypted_patient_data_records)

        # Save the TenSEAL context to a file
        save_context(context, 'tenseal_context.bin')

    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Exception type: {type(e).__name__}")
        traceback.print_exc()
        print(f"An error occurred: {e}")
        target_session.rollback()
    finally:
        source_session.close()
        target_session.close()


if __name__ == "__main__":
    copy_and_encrypt_data()
