package org.licenta.parcer.service;

import org.licenta.parcer.entity.PatientData;
import org.licenta.parcer.entity.PersonalData;
import org.licenta.parcer.repository.PatientDataRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class PatientDataService {


    @Autowired
    private PatientDataRepository repository;

    @Autowired
    private PersonalDataService personalDataService;



    public PatientData savePatientData(PatientData patientData, PersonalData personalData) {
        PersonalData managedPersonalData = personalDataService.saveOrUpdatePersonalData(personalData);
        if (managedPersonalData == null || managedPersonalData.getId() == null) {
            throw new IllegalStateException("Failed to manage personal data correctly.");
        }
        patientData.setPersonalData(managedPersonalData);  // Links the personal data to the patient data
      //  return repository.save(patientData);


        PatientData savedPatientData = repository.save(patientData);

        // Verify that saved data matches the expected input data
        if (!savedPatientData.equals(patientData)) {
            throw new IllegalStateException("There was an error saving the patient data, data mismatch.");
        }
        return savedPatientData;
    }



}
