import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { AuthService } from '../auth.service';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, HttpClientModule],
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent {
  registerForm: FormGroup;
  successMessage: string | null = null;
  errorMessage: string | null = null;
  validationErrors: any = {};

  constructor(private fb: FormBuilder, private authService: AuthService) {
    this.registerForm = this.fb.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });
  }

  onSubmit(): void {
    this.successMessage = null;
    this.errorMessage = null;
    this.validationErrors = {};
    if (this.registerForm.valid) {
      this.authService.register(this.registerForm.value).subscribe(
        response => {
          this.successMessage = 'User registered successfully. Please log in.';
          console.log('Registration successful', response);
          this.registerForm.reset();
        },
        error => {
          if (error.details) {
            this.validationErrors = error.details;
            this.errorMessage = null;
          } else {
            this.errorMessage = error.message;
          }
          console.error('Registration error', error);
        }
      );
    }
  }
}
