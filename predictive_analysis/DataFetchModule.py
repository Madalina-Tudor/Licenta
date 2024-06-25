from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import pandas as pd

Base = declarative_base()


class DecryptedPatientData(Base):
    __tablename__ = 'decrypted_patient_data'
    id = Column(Integer, primary_key=True)
    abnormal_beat_percent = Column(Float)
    af_beat_percent = Column(Float)
    asystole_rr_period_count = Column(Integer)
    atrial_beat_count = Column(Integer)
    atrial_bigeminy_count = Column(Integer)
    atrial_permature_beat_count = Column(Integer)
    atrial_tachycardia_count = Column(Integer)
    atrial_trigeminy_count = Column(Integer)
    average_heart_rate = Column(Float)
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
    personal_data_id = Column(Integer)
    abnormal_beat_count = Column(Integer)
    beat_count = Column(Integer)
    events = relationship("DecryptedHealthEventOccurrence", back_populates="patient_data")


class DecryptedHealthEventOccurrence(Base):
    __tablename__ = 'decrypted_health_event_occurrence'
    id = Column(Integer, primary_key=True)
    personal_data_id = Column(Integer, ForeignKey('decrypted_patient_data.id'))
    event_name = Column(String)
    event_time = Column(DateTime)
    patient_data = relationship("DecryptedPatientData", back_populates="events")


engine = create_engine('postgresql://postgres:postgres@localhost:5432/decryptedDB')
Session = sessionmaker(bind=engine)
session = Session()


def fetch_data(session, getPersonalID=False):
    query = session.query(
        DecryptedPatientData,
        DecryptedHealthEventOccurrence.event_name,
        DecryptedHealthEventOccurrence.event_time
    ).join(DecryptedHealthEventOccurrence, DecryptedPatientData.personal_data_id == DecryptedHealthEventOccurrence.personal_data_id)

    data = query.all()

    df = pd.DataFrame([
        {
            **{column.name: getattr(record[0], column.name) for column in DecryptedPatientData.__table__.columns if
               column.name not in ['id',None if getPersonalID else "personal_data_id" ]},
            'event_name': record[1],
            'event_time': record[2]
        }
        for record in data
    ])

    return df


# data = fetch_data(session)
# # with open('decrypted_data.csv', 'w') as f:
# #     data.to_csv(f, index=False,encoding='utf-8')
# print(data[:1])
