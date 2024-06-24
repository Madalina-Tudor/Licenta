package org.licenta.parcer;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;

import java.util.Set;

@SpringBootApplication
@EntityScan("org.licenta.parcer.entity")

public class LicentaApplication {

    public static void main(String[] args) {
        SpringApplication.run(LicentaApplication.class, args);



    }

}
