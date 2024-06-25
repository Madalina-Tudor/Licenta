import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { API_ENDPOINTS } from './api-endpoints';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  constructor(private http: HttpClient) { }

  login(credentials: { username: string, password: string }): Observable<any> {
    return this.http.post(API_ENDPOINTS.AUTH.LOGIN, {
      username: credentials.username,
      password: credentials.password
    }, httpOptions).pipe(
      catchError(this.handleError)
    );
  }

  register(user: { username: string, email: string, password: string }): Observable<any> {
    return this.http.post(API_ENDPOINTS.AUTH.REGISTER, {
      username: user.username,
      email: user.email,
      password: user.password
    }, httpOptions).pipe(
      catchError(this.handleError)
    );
  }

  getUserProfile(): Observable<any> {
    return this.http.get(API_ENDPOINTS.AUTH.PROFILE, httpOptions).pipe(
      catchError(this.handleError)
    );
  }

  private handleError(error: HttpErrorResponse) {
    console.error('Backend returned code', error.status, 'body was:', error.error);
    let errorMessage = '';
    let errorDetails = {};

    if (error.error instanceof ErrorEvent) {
      // A client-side or network error occurred.
      console.error('An error occurred:', error.error.message);
      errorMessage = error.error.message;
    } else {
      // The backend returned an unsuccessful response code.
      if (error.status === 400 && error.error) {
        // Validation error
        errorMessage = 'Validation error occurred';
        errorDetails = error.error;
      } else if (error.error.message) {
        // Custom backend error message
        errorMessage = error.error.message;
      } else {
        // Generic backend error
        errorMessage = 'Something went wrong. Please try again later.';
      }
    }

    return throwError(() => ({ message: errorMessage, details: errorDetails }));
  }
}
