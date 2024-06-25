import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { AuthService } from '../auth.service';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, HttpClientModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  loginForm: FormGroup;
  successMessage: string | null = null;
  errorMessage: string | null = null;
  validationErrors: any = {};

  constructor(private fb: FormBuilder, private authService: AuthService) {
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  onSubmit(): void {
    this.successMessage = null;
    this.errorMessage = null;
    this.validationErrors = {};
    if (this.loginForm.valid) {
      this.authService.login(this.loginForm.value).subscribe(
        response => {
          this.successMessage = 'Login successful!';
          console.log('Login successful', response);
          // Handle successful login, e.g., store token, redirect, etc.
        },
        error => {
          if (error.details) {
            this.validationErrors = error.details;
            this.errorMessage = null;
          } else {
            this.errorMessage = error.message;
          }
          console.error('Login error', error);
        }
      );
    }
  }
}
