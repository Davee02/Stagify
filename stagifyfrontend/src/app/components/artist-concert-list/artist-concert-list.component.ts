import { Component, Input, OnInit } from '@angular/core';
import ConcertModel from 'src/app/models/concert.model';
import { ConcertService } from 'src/app/services/concert/concert.service';

@Component({
  selector: 'app-artist-concert-list',
  templateUrl: './artist-concert-list.component.html',
  styleUrls: ['./artist-concert-list.component.scss'],
})
export class ArtistConcertListComponent implements OnInit {
  @Input() artistId: number;
  concerts: Array<ConcertModel>;
  isLoading: boolean = true;
  error: boolean = false;

  constructor(private concertService: ConcertService) {}

  ngOnInit(): void {
    this.concertService.getArtistsConcerts(this.artistId).then((x) => {
      if (x.ok) {
        this.concerts = x.body;
        this.isLoading = false;
      } else {
        this.error = true;
        this.isLoading = false;
      }
    });
  }
}
