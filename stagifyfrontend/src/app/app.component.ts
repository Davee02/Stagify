import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from './../environments/environment';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  constructor(private httpClient: HttpClient) {
  }

  async ngOnInit(): Promise<void> {
    const res = await this.httpClient.get(`${environment.apiUrl}/`).toPromise();
  }


  title = 'Stagify';
}
