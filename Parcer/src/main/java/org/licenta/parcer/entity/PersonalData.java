package org.licenta.parcer.entity;


import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.util.List;
import java.util.Set;

@Setter
@Getter
@Entity
@Table(name = "personal_data")
public class PersonalData {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private String gender;
    private int age;

    @OneToMany(mappedBy = "personalData", cascade = CascadeType.ALL)
    private List<PatientData> patientData;

    @OneToMany(mappedBy = "personalData")
    private Set<Diagnostic> Diagnostic;

    @OneToMany(mappedBy = "personalData")
    private Set<EventTime> eventTimes;

    @OneToMany(mappedBy = "personalData")
    private Set<HealthEventsOccurrences> events;

}
