package org.licenta.parcer.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@Entity
public class Diagnostic {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String patientDisease;
    private String picture;

    @ManyToOne
    @JoinColumn(name = "personal_data_id")
    private PersonalData personalData;

}
