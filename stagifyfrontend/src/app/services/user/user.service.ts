import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import UserModel from 'src/app/models/user.model';
import UpdateUserViewModel from 'src/app/models/ViewModels/update-user.viewmodel';
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

  async updateUser(user: UpdateUserViewModel): Promise<HttpResponse<any>> {
    return this.httpClient
      .put(this.apiUrl + '/user/', JSON.stringify(user), {
        observe: 'response',
      })
      .toPromise();
  }
}
