import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import ConcertModel from '../../models/concert.model';
import CreateConcertViewModel from '../../models/ViewModels/create-concert.viewmodel';

@Injectable({
  providedIn: 'root'
})
export class ConcertService {
  apiUrl:string = environment.apiUrl;
  constructor(private httpClient:HttpClient, private router:Router) { }
  
  async getUpcomingConcerts(numberOfSuggestions:number): Promise< Array<ConcertModel>>{
    return this.httpClient
        .get< Array<ConcertModel>>(this.apiUrl+'/concerts/suggestions?count='+numberOfSuggestions)
        .toPromise();
  }

  createConcert(concert:CreateConcertViewModel){
    return this.httpClient.post(this.apiUrl+ '/concerts',
      JSON.stringify(concert),
      {
        headers: new HttpHeaders().set('Content-Type', 'application/json'),
      });
  }

  getLoggedInUsersConcerts(): Observable<ConcertModel>{
    return this.httpClient
      .get<ConcertModel>(this.apiUrl+'/concerts');
  }

  getOwnedConcerts(){

  }
}
