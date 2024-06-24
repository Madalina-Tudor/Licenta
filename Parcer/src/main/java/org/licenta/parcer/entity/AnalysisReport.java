package org.licenta.parcer.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;
@Getter
@Setter
@Entity
public class AnalysisReport {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String reportUrl;

    @ManyToOne
    @JoinColumn(name = "personal_data_id")
    private PersonalData personalData;

    // Getters and setters
}