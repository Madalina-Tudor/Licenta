package org.licenta.parcer.repository;

import org.licenta.parcer.entity.EventTime;
import org.springframework.data.jpa.repository.JpaRepository;

public interface EventTimeRepository extends JpaRepository<EventTime, Long> {
}