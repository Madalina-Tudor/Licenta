package com.licenta.userAuthentification.payload.request;

import java.util.Set;

import jakarta.validation.constraints.*;

public class SignupRequest {
  @NotBlank(message = "Username cannot be blank")
  @Size(min = 3, max = 20, message = "Username must be between 3 and 20 characters")
  private String username;

  @NotBlank(message = "Email cannot be blank")
  @Size(max = 50, message = "Email must be less than 50 characters")
  @Email(message = "Email should be valid")
  private String email;

  private Set<String> role;

  @NotBlank(message = "Password cannot be blank")
  @Size(min = 6, max = 40, message = "Password must be between 6 and 40 characters")
  private String password;

  public String getUsername() {
    return username;
  }

  public void setUsername(String username) {
    this.username = username;
  }

  public String getEmail() {
    return email;
  }

  public void setEmail(String email) {
    this.email = email;
  }

  public String getPassword() {
    return password;
  }

  public void setPassword(String password) {
    this.password = password;
  }

  public Set<String> getRole() {
    return this.role;
  }

  public void setRole(Set<String> role) {
    this.role = role;
  }
}