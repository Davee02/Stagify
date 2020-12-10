import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { env } from 'process';
import { Observable } from 'rxjs';
import LoginViewModel from 'src/app/models/ViewModels/login.viewmodel';
import RegisterViewModel from 'src/app/models/ViewModels/register.viewmodel';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl:string = environment.apiUrl;
  constructor(private httpClient:HttpClient) { }

  login(model:LoginViewModel):Observable<HttpResponse<any>>{
    return this.httpClient 
      .post<any>(
        this.apiUrl + '/user/login',
        JSON.stringify(model),
        {
          headers: new HttpHeaders().set('Content-Type', 'application/json'),
        });
  }

  register(model:RegisterViewModel):Observable<HttpResponse<any>>{
    return this.httpClient 
      .post<any>(
        this.apiUrl + '/user/login',
        JSON.stringify(model),
        {
          headers: new HttpHeaders().set('Content-Type', 'application/json'),
        });
  }
}
