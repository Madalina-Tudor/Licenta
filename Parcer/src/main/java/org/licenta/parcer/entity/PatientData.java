package org.licenta.parcer.entity;

import jakarta.persistence.*;

import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;

@Getter
@Setter
@Entity
@Table(name = "patient_data")

public class PatientData {
    @jakarta.persistence.Id


    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "abnormal_beat_count")
    private String abnormalBeatCount;

    @Column(name = "abnormal_beat_percent")
    private Integer abnormalBeatPercent;

    @Column(name = "af_beat_percent")
    private Integer afBeatPercent;

    @Column(name = "asystole_RR_period_count")
    private Integer asystoleRRPeriodCount;

    @Column(name = "atrial_beat_count")
    private Integer atrialBeatCount;

    @Column(name = "atrial_bigeminy_count")
    private Integer atrialBigeminyCount;

    @Column(name = "atrial_permature_beat_count")
    private Integer atrialPermatureBeatCount;

    @Column(name = "atrial_tachycardia_count")
    private Integer atrialTachycardiaCount;

    @Column(name = "atrial_trigeminy_count")
    private Integer atrialTrigeminyCount;

    @Column(name = "average_heart_rate")
    private Integer averageHeartRate;

    @Column(name = "beat_count")
    private String beatCount;

    @Column(name = "couple_atrial_permature_count")
    private Integer coupleAtrialPermatureCount;

    @Column(name = "couple_ventricular_permature_count")
    private Integer coupleVentricularPermatureCount;

    @Column(name = "long_rr_period_count")
    private Integer longRRPeriodCount;

    @Column(name = "longest_atrial_tachycardia_duration")
    private Integer longestAtrialTachycardiaDuration;

    @Column(name = "longest_ventricular_tachycardia_duration")
    private Integer longestVentricularTachycardiaDuration;

    @Column(name = "max_heart_rate")
    private Integer maxHeartRate;

    @Column(name = "max_long_rr_period")
    private Integer maxLongRRPeriod;

    @Column(name = "min_heart_rate")
    private Integer minHeartRate;

    @Column(name = "total_duration")
    private Integer totalDuration;

    @Column(name = "valid_duration")
    private Integer validDuration;

    @Column(name = "ventricular_beat_count")
    private Integer ventricularBeatCount;

    @Column(name = "ventricular_bigeminy_count")
    private Integer ventricularBigeminyCount;

    @Column(name = "ventricular_permature_beat_count")
    private Integer ventricularPermatureBeatCount;

    @Column(name = "ventricular_tachycardia_count")
    private Integer ventricularTachycardiaCount;

    @Column(name = "ventricular_trigeminy_count")
    private Integer ventricularTrigeminyCount;

    @ManyToOne
    @JoinColumn(name = "personal_data_id")
    private PersonalData personalData;


}
