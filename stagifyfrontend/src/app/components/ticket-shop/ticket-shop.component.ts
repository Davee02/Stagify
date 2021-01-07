import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ConcertService } from '../../services/concert/concert.service';

@Component({
  selector: 'app-ticket-shop',
  templateUrl: './ticket-shop.component.html',
  styleUrls: ['./ticket-shop.component.scss'],
})
export class TicketShopComponent implements OnInit {
  concertId: number;
  alreadyBoughtTicketsCount: number;
  sendConfirmationEmail: boolean = false;

  constructor(
    route: ActivatedRoute,
    private router: Router,
    private concertService: ConcertService
  ) {
    this.concertId = Number(route.snapshot.paramMap.get('concertId'));
  }

  ngOnInit(): void {
    this.concertService.getTicketsState(this.concertId).then((value) => {
      this.alreadyBoughtTicketsCount = value.ticketCount;
    });
  }

  async buyTickets(): Promise<void> {
    await this.concertService.buyTickets(
      this.concertId,
      this.sendConfirmationEmail
    );

    this.router.navigate(['home']);
  }
}
