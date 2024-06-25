import {HttpInterceptor, HttpRequest, HttpHandler, HttpEvent} from '@angular/common/http';
//import { TokenStorageService } from '../services/token-storage.service';
import { Injectable } from '@angular/core';
import {Observable} from "rxjs";

const TOKEN_HEADER_KEY = 'Authorization';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // @ts-ignore
    return undefined;
  }

  //constructor(private token: TokenStorageService) { }

  // intercept(req: HttpRequest<any>, next: HttpHandler) {
  //   let authReq = req;
  //  // const token = this.token.getToken();
  //  // if (token != null) {
  //     authReq = req.clone({ headers: req.headers.set(TOKEN_HEADER_KEY, 'Bearer ' + token) });
  //   }
  //   return next.handle(authReq);
  // }
}
