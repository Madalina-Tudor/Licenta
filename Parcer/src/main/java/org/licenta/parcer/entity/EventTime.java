package org.licenta.parcer.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Entity
public class EventTime {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    //private String reportTime;
    private String minHeartRateTime;
    private String maxHeartRateTime;
    private String maxLongAsystoleTime;
    private String longestVentricularTachycardiaOccurTime;
    private String longestAtrialTachycardiaOccurTime;
    private String dataEndTime;
    private String dataStartTime;



    @ManyToOne
    @JoinColumn(name = "personal_data_id")
    private PersonalData personalData;

}