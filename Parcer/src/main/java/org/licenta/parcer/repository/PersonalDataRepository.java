package org.licenta.parcer.repository;

import org.licenta.parcer.entity.PersonalData;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PersonalDataRepository extends JpaRepository<PersonalData, Long>{
    PersonalData findByName(String name);


}
