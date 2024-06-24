package org.licenta.parcer.service;

import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;
@Service
public class TranslationService {
    // Translation dictionary
    private static final Map<String, String> translationMap = new HashMap<>();

    static {
        translationMap.put("最大心率", "Max Heart Rate");
        translationMap.put("最小心率", "Min Heart Rate");
        translationMap.put("室上性早搏", "Supraventricular Premature Beat");
        translationMap.put("室上性早搏成对", "Couplet of Supraventricular Premature Beat");
        translationMap.put("室性早搏", "Ventricular Premature Beat");
        translationMap.put("室上性早搏二联律", "Supraventricular Bigeminy");
        translationMap.put("最长RR间期", "Longest RR Interval");
        translationMap.put("室上性早搏三联律", "Supraventricular Trigeminy");
        translationMap.put("室上性心动过速", "Supraventricular Tachycardia");
        translationMap.put("室性早搏成对", "Couplet of Ventricular Premature Beat");
        translationMap.put("室性心动过速", "Ventricular Tachycardia");
        translationMap.put("室性早搏二联律", "Premature Ventricular Bigeminy");


        // Add HERE IF NEEDED  NEW WORDS TO TRANSLATE
    }

    public String translate(String text) {
        return translationMap.getOrDefault(text, text);
    }
}
