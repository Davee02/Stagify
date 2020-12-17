import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { env } from 'process';
import { Observable } from 'rxjs';
import LoginViewModel from '../../models/ViewModels/login.viewmodel';
import RegisterViewModel from 'src/app/models/ViewModels/register.viewmodel';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl:string = environment.apiUrl;
  constructor(private httpClient:HttpClient) { }

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

  async getLoggedInUser(): Promise<HttpResponse<any>>{
    return this.httpClient
      .get(
        this.apiUrl + '/user',
        {
          observe:'response'
        }
      ).toPromise();
  }
}
