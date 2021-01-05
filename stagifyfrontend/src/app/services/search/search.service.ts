import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import ArtistModel from 'src/app/models/artist.model';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class SearchService {
  private apiUrl = environment.apiUrl;
  constructor(private httpClient: HttpClient) {}

  async searchArtists(value: string): Promise<Array<ArtistModel>> {
    return this.httpClient
      .get<Array<ArtistModel>>(this.apiUrl + '/artists/search/' + value)
      .toPromise();
  }
}
