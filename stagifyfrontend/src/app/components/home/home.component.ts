import { Component, OnInit } from '@angular/core';
import ConcertModel from 'src/app/models/concert.model';
import {ConcertService} from '../../services/concert/concert.service'


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  concerts: Array<ConcertModel>;
  constructor(private concertService:ConcertService) { }

  ngOnInit(): void {
    this.getConcerts();
  }

  getConcerts():void{
    this.concertService
      .getUpcomingConcerts()
      .subscribe((data: Array<ConcertModel>) => this.concerts = data);
  }
}
