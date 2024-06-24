package org.licenta.parcer.controller;

import org.licenta.parcer.service.DatabaseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;

@RestController
@RequestMapping("/data")
public class DataController {
    @Autowired
    private DatabaseService databaseService;

    @PostMapping("/testProcess")
    public ResponseEntity<String> processData(@RequestBody String jsonData) {
        try {
            databaseService.processAndStorePatientDataAndPersonalData(jsonData);
            return ResponseEntity.ok("Data processed successfully");
        } catch (IOException e) {
            return ResponseEntity.badRequest().body("Failed to process data: " + e.getMessage());
        }
    }


    @GetMapping("/processAll")
    public ResponseEntity<String> processAllData() {
        try {
            databaseService.processAllJsonFilesFromDirectory();
            return ResponseEntity.ok("All data processed successfully");
        } catch (IOException e) {
            return ResponseEntity.badRequest().body("Failed to process all data: " + e.getMessage());
        }
    }


}
