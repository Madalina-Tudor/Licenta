from sqlalchemy import create_engine, Column, Integer, String, BigInteger, ForeignKey, Text, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Decrypted target database URL
DECRYPTED_TARGET_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/decryptedDB"

decrypted_target_engine = create_engine(DECRYPTED_TARGET_DATABASE_URL)
DecryptionBase = declarative_base()

# Decrypted target session
DecryptedTargetSession = sessionmaker(bind=decrypted_target_engine)
decrypted_target_session = DecryptedTargetSession()


# Decrypted Data Models
class DecryptedPersonalData(DecryptionBase):
    __tablename__ = 'decrypted_personal_data'
    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)


class DecryptedDiagnostic(DecryptionBase):
    __tablename__ = 'decrypted_diagnostic'
    id = Column(BigInteger, primary_key=True)
    patient_disease = Column(String)
    picture = Column(String)
    personal_data_id = Column(BigInteger, ForeignKey('decrypted_personal_data.id'))


class DecryptedHealthEventOccurrence(DecryptionBase):
    __tablename__ = 'decrypted_health_event_occurrence'
    id = Column(BigInteger, primary_key=True)
    event_name = Column(String)
    event_time = Column(DateTime)
    personal_data_id = Column(BigInteger, ForeignKey('decrypted_personal_data.id'))


class DecryptedEventTime(DecryptionBase):
    __tablename__ = 'decrypted_event_time'
    id = Column(BigInteger, primary_key=True)
    min_heart_rate_time = Column(DateTime)
    max_heart_rate_time = Column(DateTime)
    max_long_asystole_time = Column(DateTime)
    longest_ventricular_tachycardia_occur_time = Column(DateTime)
    longest_atrial_tachycardia_occur_time = Column(DateTime)
    data_end_time = Column(DateTime)
    data_start_time = Column(DateTime)
    personal_data_id = Column(BigInteger, ForeignKey('decrypted_personal_data.id'))


class DecryptedAnalysisReport(DecryptionBase):
    __tablename__ = 'decrypted_analysis_report'
    id = Column(BigInteger, primary_key=True)
    report_url = Column(String)
    personal_data_id = Column(BigInteger, ForeignKey('decrypted_personal_data.id'))


class DecryptedPatientData(DecryptionBase):
    __tablename__ = 'decrypted_patient_data'
    id = Column(BigInteger, primary_key=True)
    abnormal_beat_count = Column(Integer)
    abnormal_beat_percent = Column(Float)
    af_beat_percent = Column(Float)
    asystole_rr_period_count = Column(Integer)
    atrial_beat_count = Column(Integer)
    atrial_bigeminy_count = Column(Integer)
    atrial_permature_beat_count = Column(Integer)
    atrial_tachycardia_count = Column(Integer)
    atrial_trigeminy_count = Column(Integer)
    average_heart_rate = Column(Float)
    beat_count = Column(Integer)
    couple_atrial_permature_count = Column(Integer)
    couple_ventricular_permature_count = Column(Integer)
    long_rr_period_count = Column(Integer)
    longest_atrial_tachycardia_duration = Column(Float)
    longest_ventricular_tachycardia_duration = Column(Float)
    max_heart_rate = Column(Float)
    max_long_rr_period = Column(Float)
    min_heart_rate = Column(Float)
    total_duration = Column(Float)
    valid_duration = Column(Float)
    ventricular_beat_count = Column(Integer)
    ventricular_bigeminy_count = Column(Integer)
    ventricular_permature_beat_count = Column(Integer)
    ventricular_tachycardia_count = Column(Integer)
    ventricular_trigeminy_count = Column(Integer)
    personal_data_id = Column(BigInteger, ForeignKey('decrypted_personal_data.id'))


DecryptionBase.metadata.create_all(decrypted_target_engine)
#DecryptionBase.metadata.drop_all(decrypted_target_engine)  # Drop tables in the decrypted target database
