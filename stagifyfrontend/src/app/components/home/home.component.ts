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
  isLoading:Boolean = true;

  constructor(private concertService:ConcertService) { }

  ngOnInit(): void {
    this.getConcerts();
  }

  async getConcerts(){
    this.concertService.getUpcomingConcerts(10)
    .then(value => {
      this.concerts = value; 
      this.isLoading = false;
    })
    .catch(error => {});
  }

}
