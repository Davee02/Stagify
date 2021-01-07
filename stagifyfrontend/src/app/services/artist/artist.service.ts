import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import ArtistModel from 'src/app/models/artist.model';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class ArtistService {
  apiUrl: string = environment.apiUrl;

  constructor(private httpClient: HttpClient) {}

  async allArtists(): Promise<Array<ArtistModel>> {
    return this.httpClient
      .get<Array<ArtistModel>>(this.apiUrl + '/artists')
      .toPromise();
  }

  async getArtist(id: number): Promise<HttpResponse<ArtistModel>> {
    return this.httpClient
      .get<ArtistModel>(this.apiUrl + '/artists/' + id, {
        observe: 'response',
      })
      .toPromise();
  }
}
