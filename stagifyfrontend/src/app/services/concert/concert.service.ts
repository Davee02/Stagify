import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import ConcertTicketsState from 'src/app/models/concertTicketsState.model';
import { environment } from 'src/environments/environment';
import ConcertModel from '../../models/concert.model';
import CreateConcertViewModel from '../../models/ViewModels/create-concert.viewmodel';

@Injectable({
  providedIn: 'root',
})
export class ConcertService {
  apiUrl: string = environment.apiUrl;
  constructor(private httpClient: HttpClient) {}

  async getUpcomingConcerts(
    numberOfSuggestions: number
  ): Promise<Array<ConcertModel>> {
    return this.httpClient
      .get<Array<ConcertModel>>(
        this.apiUrl + '/concerts/suggestions?count=' + numberOfSuggestions
      )
      .toPromise();
  }

  createConcert(concert: CreateConcertViewModel) {
    return this.httpClient.post(
      this.apiUrl + '/concerts',
      JSON.stringify(concert),
      {
        headers: new HttpHeaders().set('Content-Type', 'application/json'),
      }
    );
  }

  getLoggedInUsersConcerts(): Observable<ConcertModel> {
    return this.httpClient.get<ConcertModel>(this.apiUrl + '/concerts');
  }

  getOwnedConcerts() {}

  async getTicketsState(concertId: number): Promise<ConcertTicketsState> {
    return this.httpClient
      .get<ConcertTicketsState>(this.apiUrl + `/concerts/${concertId}/tickets`)
      .toPromise();
  }

  async buyTickets(
    concertId: number,
    sendConfirmationEmail: boolean
  ): Promise<any> {
    return this.httpClient
      .post<any>(this.apiUrl + `/concerts/${concertId}/tickets/`, {
        sendConfirmationEmail: sendConfirmationEmail,
      })
      .toPromise();
  }
}
