import { Component, Input, OnInit } from '@angular/core';
import ArtistModel from 'src/app/models/artist.model';
import ConcertModel from 'src/app/models/concert.model';
import { ArtistService } from 'src/app/services/artist/artist.service';

@Component({
  selector: 'app-concert-item',
  templateUrl: './concert-item.component.html',
  styleUrls: ['./concert-item.component.scss']
})
export class ConcertItemComponent implements OnInit {

  @Input() concertModel: ConcertModel;
  isLoading:boolean = true;
  artistModel:ArtistModel;

  constructor(private artistService:ArtistService) { }

  ngOnInit(): void {
    this.artistService.getArtist(this.concertModel.artist)
    .then(value => {
      this.artistModel = value;
      this.isLoading = false;
    } ) 
  }

}
