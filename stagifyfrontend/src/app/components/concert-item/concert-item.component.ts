import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import ArtistModel from 'src/app/models/artist.model';
import ConcertModel from 'src/app/models/concert.model';
import { ArtistService } from 'src/app/services/artist/artist.service';
import { AuthenticationService } from 'src/app/services/authentication/authentication/authentication.service';
import { ConcertService } from 'src/app/services/concert/concert.service';

@Component({
  selector: 'app-concert-item',
  templateUrl: './concert-item.component.html',
  styleUrls: ['./concert-item.component.scss'],
})
export class ConcertItemComponent implements OnInit {
  @Input() concertModel: ConcertModel;
  @Input() showUser: boolean;
  isLoading: boolean = true;
  hasUserBoughtTickets: boolean = true;
  artistModel: ArtistModel;

  constructor(
    private artistService: ArtistService,
    private concertService: ConcertService,
    public authService: AuthenticationService,
    private router: Router
  ) {}

  ngOnInit(): void {
    if (!this.concertModel.artistId) {
      return;
    }

    this.artistService.getArtist(this.concertModel.artistId).then((value) => {
      this.artistModel = value.body;
      this.isLoading = false;
    });

    if (this.authService.isLoggedIn()) {
      this.concertService
        .getTicketsState(this.concertModel.id)
        .then((value) => {
          this.hasUserBoughtTickets = value.ticketCount > 0;
        });
    }
  }

  buyTicket(): void {
    this.router.navigate(['concerts', this.concertModel.id, 'tickets']);
  }
}
