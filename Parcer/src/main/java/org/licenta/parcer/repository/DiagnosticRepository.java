package org.licenta.parcer.repository;

import org.licenta.parcer.entity.Diagnostic;
import org.springframework.data.jpa.repository.JpaRepository;

public interface DiagnosticRepository extends JpaRepository<Diagnostic, Long> {
}