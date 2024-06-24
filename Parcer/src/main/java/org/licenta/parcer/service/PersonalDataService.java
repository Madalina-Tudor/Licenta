package org.licenta.parcer.service;

import org.licenta.parcer.entity.PersonalData;
import org.licenta.parcer.repository.PersonalDataRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class PersonalDataService {

    @Autowired
    private  PersonalDataRepository repository;

    public PersonalData saveOrUpdatePersonalData(PersonalData personalData) {
        PersonalData existingData = repository.findByName(personalData.getName());
        if (existingData != null) {
            // Update the existing entry
            personalData.setId(existingData.getId());
        }
        return repository.save(personalData);
    }
}
