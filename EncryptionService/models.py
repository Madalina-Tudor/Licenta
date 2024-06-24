from sqlalchemy import create_engine, Column, Integer, String, BigInteger, ForeignKey, Text, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Source database URL
SOURCE_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/allPatientData"
# Target database URL
TARGET_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/encryptionDB"
# Decrypted target database URL
DECRYPTED_TARGET_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/decryptedDB"

source_engine = create_engine(SOURCE_DATABASE_URL)
target_engine = create_engine(TARGET_DATABASE_URL)
decrypted_target_engine = create_engine(DECRYPTED_TARGET_DATABASE_URL)

Base = declarative_base()

# Source session
SourceSession = sessionmaker(bind=source_engine)
source_session = SourceSession()

# Target session
TargetSession = sessionmaker(bind=target_engine)
target_session = TargetSession()

# Decrypted target session
DecryptedTargetSession = sessionmaker(bind=decrypted_target_engine)
decrypted_target_session = DecryptedTargetSession()


class PersonalData(Base):
    __tablename__ = 'personal_data'
    id = Column(BigInteger, primary_key=True)
    name = Column(Text)  # Changed to Text
    gender = Column(String(255))
    age = Column(Integer)
    diagnostics = relationship("Diagnostic", back_populates="personal_data")
    events = relationship("HealthEventOccurrence", back_populates="personal_data")
    event_times = relationship("EventTime", back_populates="personal_data")
    analysis_reports = relationship("AnalysisReport", back_populates="personal_data")
    patient_data = relationship("PatientData", back_populates="personal_data")


class Diagnostic(Base):
    __tablename__ = 'diagnostic'
    id = Column(BigInteger, primary_key=True)
    patient_disease = Column(Text)  # Changed to Text
    picture = Column(Text)  # Changed to Text
    personal_data_id = Column(BigInteger, ForeignKey('personal_data.id'))
    personal_data = relationship("PersonalData", back_populates="diagnostics")


class HealthEventOccurrence(Base):
    __tablename__ = 'health_events_occurrences'
    id = Column(BigInteger, primary_key=True)
    event_name = Column(Text)
    event_time = Column(Text)
    personal_data_id = Column(BigInteger, ForeignKey('personal_data.id'))
    personal_data = relationship("PersonalData", back_populates="events")


class EventTime(Base):
    __tablename__ = 'event_time'
    id = Column(BigInteger, primary_key=True)
    min_heart_rate_time = Column(Text)
    max_heart_rate_time = Column(Text)
    max_long_asystole_time = Column(Text)
    longest_ventricular_tachycardia_occur_time = Column(Text)
    longest_atrial_tachycardia_occur_time = Column(Text)
    data_end_time = Column(Text)
    data_start_time = Column(Text)
    personal_data_id = Column(BigInteger, ForeignKey('personal_data.id'))
    personal_data = relationship("PersonalData", back_populates="event_times")


class AnalysisReport(Base):
    __tablename__ = 'analysis_report'
    id = Column(BigInteger, primary_key=True)
    report_url = Column(Text)  # Changed to Text
    personal_data_id = Column(BigInteger, ForeignKey('personal_data.id'))
    personal_data = relationship("PersonalData", back_populates="analysis_reports")


class PatientData(Base):
    __tablename__ = 'patient_data'
    id = Column(BigInteger, primary_key=True)
    abnormal_beat_count = Column(Text)
    abnormal_beat_percent = Column(Integer)
    af_beat_percent = Column(Integer)
    asystole_rr_period_count = Column(Integer)  # Corrected column name
    atrial_beat_count = Column(Integer)
    atrial_bigeminy_count = Column(Integer)
    atrial_permature_beat_count = Column(Integer)
    atrial_tachycardia_count = Column(Integer)
    atrial_trigeminy_count = Column(Integer)
    average_heart_rate = Column(Integer)
    beat_count = Column(Text)
    couple_atrial_permature_count = Column(Integer)
    couple_ventricular_permature_count = Column(Integer)
    long_rr_period_count = Column(Integer)
    longest_atrial_tachycardia_duration = Column(Integer)
    longest_ventricular_tachycardia_duration = Column(Integer)
    max_heart_rate = Column(Integer)
    max_long_rr_period = Column(Integer)
    min_heart_rate = Column(Integer)
    total_duration = Column(Integer)
    valid_duration = Column(Integer)
    ventricular_beat_count = Column(Integer)
    ventricular_bigeminy_count = Column(Integer)
    ventricular_permature_beat_count = Column(Integer)
    ventricular_tachycardia_count = Column(Integer)
    ventricular_trigeminy_count = Column(Integer)
    personal_data_id = Column(BigInteger, ForeignKey('personal_data.id'))
    personal_data = relationship("PersonalData", back_populates="patient_data")


class EncryptedData(Base):
    __tablename__ = 'encrypted_data'
    id = Column(BigInteger, primary_key=True)
    data = Column(Text)  # Changed to Text


# Create tables in the target and decrypted target databases
Base.metadata.create_all(target_engine)
#Base.metadata.drop_all(target_engine)  # Drop tables in the target database
