package org.licenta.parcer.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import lombok.Getter;
import lombok.Setter;


@Setter
@Getter
@Entity
public class HealthEventsOccurrences {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String eventName;
    private LocalDateTime eventTime;

    @ManyToOne
    @JoinColumn(name = "personal_data_id")
    private PersonalData personalData;
}
