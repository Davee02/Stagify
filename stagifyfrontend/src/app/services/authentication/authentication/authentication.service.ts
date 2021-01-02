import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import LoginViewModel from 'src/app/models/ViewModels/login.viewmodel';
import RegisterViewModel from 'src/app/models/ViewModels/register.viewmodel';
import {environment} from 'src/environments/environment'

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  private apiUrl = environment.apiUrl;
  constructor(private httpClient:HttpClient, private cookieService:CookieService) { }

  isLoggedIn():boolean{
      return this.cookieService.check('sessionid');
  }

  async login(model:LoginViewModel):Promise<HttpResponse<any>>{
    return await this.httpClient 
      .post<any>(
        this.apiUrl + '/user/login',
        JSON.stringify(model),
        {
          headers: new HttpHeaders().set('Content-Type', 'application/json'),
          observe: 'response'
        }).toPromise();
  }

  async register(model:RegisterViewModel):Promise<HttpResponse<any>>{
    return this.httpClient 
      .post<any>(
        this.apiUrl + '/user/register',
        JSON.stringify(model),
        {
          headers: new HttpHeaders().set('Content-Type', 'application/json'),
          observe: 'response'
        }).toPromise();
  }

  async logout():Promise<HttpResponse<any>>{
    return this.httpClient
      .post<any>(
        this.apiUrl + '/user/logout',
        {
          observe:'response'
        }
      ).toPromise();
  }
}


