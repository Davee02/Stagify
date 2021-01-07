import { Component, Input, OnInit } from '@angular/core';
import ArtistModel from 'src/app/models/artist.model';
import ConcertModel from 'src/app/models/concert.model';
import { ArtistService } from 'src/app/services/artist/artist.service';
import { ConcertService } from 'src/app/services/concert/concert.service';

@Component({
  selector: 'app-concert-item',
  templateUrl: './concert-item.component.html',
  styleUrls: ['./concert-item.component.scss']
})
export class ConcertItemComponent implements OnInit {

  @Input() concertModel: ConcertModel;
  @Input() showUser:boolean;
  isLoading:boolean = true;
  constructor() {
   }

  ngOnInit(): void {
  }

}
