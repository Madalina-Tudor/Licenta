package org.licenta.parcer.service;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.licenta.parcer.entity.PersonalData;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.net.URL;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Service
public class PDFExtractorService {
    Logger logger = LoggerFactory.getLogger(PDFExtractorService.class);

    public PersonalData extractPersonalData(String url)
            throws IOException {
        logger.info("Start extracting personal data from the following URL: {}", url);
        String text = extractTextFromPDF(url);

        logger.info("Extracted text from PDF:\n{}", text);
        PersonalData personalData = parsePersonalData(text);
        logger.info("Parsed personal data: {}", personalData);
        return parsePersonalData(text);
    }

    private String extractTextFromPDF(String url) throws IOException {
        try (PDDocument document = PDDocument.load(new URL(url).openStream())) {
            PDFTextStripper stripper = new PDFTextStripper();
            return stripper.getText(document);
        }
    }

    private PersonalData parsePersonalData(String text) {
        PersonalData personalData = new PersonalData();
        Pattern pattern = Pattern.compile("Name\\s*:\\s*(.*?)\\s+Gender\\s*:\\s*(.*?)\\s+Age\\s*:\\s*(\\d+)");
        Matcher matcher = pattern.matcher(text);
        if (matcher.find()) {
            personalData.setName(matcher.group(1));
         //   System.out.println("Name: " + matcher.group(1));
            personalData.setGender(matcher.group(2));
          //  System.out.println("Gender: " + matcher.group(2));
            personalData.setAge(Integer.parseInt(matcher.group(3)));
         //   System.out.println("Age: " + matcher.group(3));
        }
        if (personalData.getName() == null || personalData.getGender() == null || personalData.getAge() == 0) {
            throw new IllegalArgumentException("Invalid data extracted from the PDF file.");
        }


        return personalData;
    }
}
