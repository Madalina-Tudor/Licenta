
package org.licenta.parcer.service;


import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.licenta.parcer.entity.*;
import org.licenta.parcer.repository.*;
import org.springframework.core.env.Environment;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@Service
public class DatabaseService {

    @Autowired
    private PDFExtractorService pdfExtractorService;

    @Autowired
    private Environment environment;


    @Autowired
    private PatientDataService patientDataService;

    @Autowired
    private PersonalDataRepository personalDataRepository;

    @Autowired
    private DiagnosticRepository diagnosticRepository;

    @Autowired
    private EventTimeRepository eventTimeRepository;

    @Autowired
    private HeathEventsOccurrencesRepository heathEventsOccurrencesRepository;

    @Autowired
    private AnalysisReportRepository analysisReportRepository;


    @Autowired
    private TranslationService translationService;

    private static final DateTimeFormatter DATE_TIME_FORMATTER =  DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");;




    public void processAllJsonFilesFromDirectory() throws IOException {
        String directoryPath = environment.getProperty("json.files.directory");
        File folder = new File(directoryPath);
        File[] listOfFiles = folder.listFiles();

        if (listOfFiles != null) {
            for (File file : listOfFiles) {
                if (file.isFile() && file.getName().endsWith(".json")) {
                    String jsonInput = new String(Files.readAllBytes(file.toPath()));
                    processAndStorePatientDataAndPersonalData(jsonInput);
                }
            }
        }
    }

    public void processAndStorePatientDataAndPersonalData(String jsonInput) throws IOException {
        PatientData patientData = convertJsonToPatientData(jsonInput);
        String pdfUrl = getPdfUrlFromJson(jsonInput);
        PersonalData personalData = pdfExtractorService.extractPersonalData(pdfUrl);

        patientDataService.savePatientData(patientData, personalData);


        // Save AnalysisReport
        AnalysisReport analysisReport = new AnalysisReport();
        analysisReport.setReportUrl(pdfUrl);
        analysisReport.setPersonalData(personalData);
        analysisReportRepository.save(analysisReport);

        // Save or update the personalData entity
        personalDataRepository.save(personalData);

        patientDataService.savePatientData(patientData, personalData);

        saveDiagnosticsFromJson(jsonInput, personalData);
        saveEventsFromJson(jsonInput, personalData);
        saveEventTimesFromJson(jsonInput, personalData);
    }

    private String getPdfUrlFromJson(String json) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        JsonNode rootNode = mapper.readTree(json);
        return rootNode.path("data").path("analysisReport").asText();
    }


    private void saveDiagnosticsFromJson(String json, PersonalData personalData) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        JsonNode jsonNode = mapper.readTree(json);
        JsonNode diagnoseListNode = jsonNode.path("data").path("diagnoseList");

        if (diagnoseListNode.isArray()) {
            for (JsonNode diagnoseNode : diagnoseListNode) {
                Diagnostic diagnostic = new Diagnostic();
                diagnostic.setPatientDisease(diagnoseNode.path("diagnoseInfo").asText());
                diagnostic.setPersonalData(personalData);
                diagnosticRepository.save(diagnostic);
            }
        }
    }

    private void saveEventsFromJson(String json, PersonalData personalData) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        JsonNode jsonNode = mapper.readTree(json);
        JsonNode allEventListNode = jsonNode.path("data").path("allEventList");

        if (allEventListNode.isArray()) {
            for (JsonNode eventNode : allEventListNode) {
                HealthEventsOccurrences event = new HealthEventsOccurrences();
                String eventName = eventNode.path("eventName").asText();
                String translatedEventName = translationService.translate(eventName); // Traducere
                event.setEventName(translatedEventName);

                String eventTimeStr = eventNode.path("eventTime").asText();
                LocalDateTime eventTime = LocalDateTime.parse(eventTimeStr, DATE_TIME_FORMATTER);
                event.setEventTime(eventTime);

               // event.setEventTime(eventNode.path("eventTime").asText());
                event.setPersonalData(personalData);
                heathEventsOccurrencesRepository.save(event);
            }
        }
    }

    private void saveEventTimesFromJson(String json, PersonalData personalData) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        JsonNode jsonNode = mapper.readTree(json);

        EventTime eventTime = new EventTime();
       // eventTime.setReportTime(jsonNode.path("data").path("reportTime").asText());
        eventTime.setMinHeartRateTime(jsonNode.path("data").path("minHeartRateTime").asText());
        eventTime.setMaxHeartRateTime(jsonNode.path("data").path("maxHeartRateTime").asText());
        eventTime.setMaxLongAsystoleTime(jsonNode.path("data").path("maxLongAsystoleTime").asText());
        eventTime.setLongestVentricularTachycardiaOccurTime(jsonNode.path("data").path("longestVentricularTachycardiaOccurTime").asText());
        eventTime.setLongestAtrialTachycardiaOccurTime(jsonNode.path("data").path("longestAtrialTachycardiaOccurTime").asText());
        eventTime.setDataEndTime(jsonNode.path("data").path("dataEndTime").asText());
        eventTime.setDataStartTime(jsonNode.path("data").path("dataStartTime").asText());
        eventTime.setPersonalData(personalData);
        eventTimeRepository.save(eventTime);
    }


    private PatientData convertJsonToPatientData(String json) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        JsonNode jsonNode = mapper.readTree(json);
        PatientData patientData = new PatientData();

        patientData.setAbnormalBeatCount(jsonNode.path("data").path("abnormalBeatCount").asText());
        patientData.setAbnormalBeatPercent(jsonNode.path("data").path("abnormalBeatPercent").asInt());
        patientData.setAfBeatPercent(jsonNode.path("data").path("afBeatPercent").asInt());
        patientData.setAsystoleRRPeriodCount(jsonNode.path("data").path("asystoleRRPeriodCount").asInt());
        patientData.setAtrialBeatCount(jsonNode.path("data").path("atrialBeatCount").asInt());
        patientData.setAtrialBigeminyCount(jsonNode.path("data").path("atrialBigeminyCount").asInt());
        patientData.setAtrialPermatureBeatCount(jsonNode.path("data").path("atrialPermatureBeatCount").asInt());
        patientData.setAtrialTachycardiaCount(jsonNode.path("data").path("atrialTachycardiaCount").asInt());
        patientData.setAtrialTrigeminyCount(jsonNode.path("data").path("atrialTrigeminyCount").asInt());
        patientData.setAverageHeartRate(jsonNode.path("data").path("averageHeartRate").asInt());
        patientData.setBeatCount(jsonNode.path("data").path("beatCount").asText());
        patientData.setCoupleAtrialPermatureCount(jsonNode.path("data").path("coupleAtrialPermatureCount").asInt());
        patientData.setCoupleVentricularPermatureCount(jsonNode.path("data").path("coupleVentricularPermatureCount").asInt());
        patientData.setLongRRPeriodCount(jsonNode.path("data").path("longRRPeriodCount").asInt());
        patientData.setLongestAtrialTachycardiaDuration(jsonNode.path("data").path("longestAtrialTachycardiaDuration").asInt());
        patientData.setLongestVentricularTachycardiaDuration(jsonNode.path("data").path("longestVentricularTachycardiaDuration").asInt());
        patientData.setMaxHeartRate(jsonNode.path("data").path("maxHeartRate").asInt());
        patientData.setMaxLongRRPeriod(jsonNode.path("data").path("maxLongRRPeriod").asInt());
        patientData.setMinHeartRate(jsonNode.path("data").path("minHeartRate").asInt());
        patientData.setTotalDuration(jsonNode.path("data").path("totalDuration").asInt());
        patientData.setValidDuration(jsonNode.path("data").path("validDuration").asInt());
        patientData.setVentricularBeatCount(jsonNode.path("data").path("ventricularBeatCount").asInt());
        patientData.setVentricularBigeminyCount(jsonNode.path("data").path("ventricularBigeminyCount").asInt());
        patientData.setVentricularPermatureBeatCount(jsonNode.path("data").path("ventricularPermatureBeatCount").asInt());
        patientData.setVentricularTachycardiaCount(jsonNode.path("data").path("ventricularTachycardiaCount").asInt());
        patientData.setVentricularTrigeminyCount(jsonNode.path("data").path("ventricularTrigeminyCount").asInt());

        return patientData;
    }
}