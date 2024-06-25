//
// import { Injectable } from '@angular/core';
// import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpErrorResponse } from '@angular/common/http';
// import { Observable, throwError } from 'rxjs';
// import { catchError } from 'rxjs/operators';
// import { TokenStorageService } from '../services/token-storage.service';
// import { AuthService } from '../services/auth.service';
// import { switchMap } from 'rxjs/operators';
// import { JwtResponse } from '../Model/jwt-response';
// import {Router} from "@angular/router";
//
// @Injectable()
// export class TokenInterceptor implements HttpInterceptor {
//
//   private refreshTokenRetryCount = 0;
//
//   constructor(
//     private tokenStorageService: TokenStorageService,
//     private authService: AuthService,
//     private router: Router
//
//   ) {}
//
//   intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
//     return next.handle(request).pipe(
//       catchError((error: HttpErrorResponse) => {
//
//         // If it's a login request and there's a 401, it's bad credentials.
//         if (request.url.includes('/signin') && error.status === 401) {
//           console.error("Invalid credentials.");
//           return throwError("Invalid credentials");
//         }
//
//         if (error.status === 401 && this.tokenStorageService.getRefreshToken()) {
//           console.log('Unauthorized error detected. Attempting token refresh...');
//
//           // Check if we've already retried 3 times
//           if (this.refreshTokenRetryCount >= 3) {
//             console.error("Tried to refresh token 3 times without success. Redirecting to login.");
//             this.refreshTokenRetryCount = 0;  //  Reset retry count
//             this.router.navigate(['/login']);  // Redirect to login
//             return throwError("Too many refresh attempts");
//           }
//
//
//
//           const refreshToken = this.tokenStorageService.getRefreshToken();
//           if (!refreshToken) {
//             console.error("No refresh token available");
//             return throwError("No refresh token available");
//           }
//           this.refreshTokenRetryCount++;
//
//           return this.authService.refreshToken({ refreshToken }).pipe(
//             switchMap((refreshedTokens: JwtResponse) => {
//               console.log("Successfully refreshed the token.");
//               console.log("Refreshed Token: ", refreshedTokens.accessToken);
//
//               if (this.authService.isValidJWT(refreshedTokens.accessToken)) {
//                 this.tokenStorageService.setAccessToken(refreshedTokens.accessToken);
//                 this.tokenStorageService.setRefreshToken(refreshedTokens.refreshToken);
//
//                 const authReq = request.clone({
//                   headers: request.headers.set('Authorization', 'Bearer ' + refreshedTokens.accessToken)
//                 });
//                 return next.handle(authReq);
//               } else {
//                 console.error("Invalid JWT format after refresh.");
//                 return throwError("Invalid JWT format");
//               }
//             }),
//             catchError(refreshError => {
//               //TO DO  Don't navigate here, handle the navigation in components/services
//               return throwError(refreshError);
//             })
//           );
//         } else {
//           console.error("Error while making API request: ", error);
//           //TO DO: Don't navigate here, handle the navigation in components/services
//           return throwError(error);
//         }
//       })
//     );
//   }
// }
