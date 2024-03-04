package com.PASN;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;

@SpringBootApplication()
public class PasnApplication {

	public static void main(String[] args) {
		SpringApplication.run(PasnApplication.class, args);
	}

	@GetMapping("/")
	public String apiRoot(){
		return "Hello, World!";
	}

}
