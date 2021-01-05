import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  private apiUrl: string = environment.apiUrl;
  constructor(private httpClient: HttpClient) {}

  async getLoggedInUser(): Promise<HttpResponse<any>> {
    return this.httpClient
      .get(this.apiUrl + '/user', {
        observe: 'response',
      })
      .toPromise();
  }
}
