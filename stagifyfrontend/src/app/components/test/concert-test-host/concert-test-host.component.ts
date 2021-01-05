import { Component, OnInit } from '@angular/core';
import ConcertModel from 'src/app/models/concert.model';

@Component({
  selector: 'app-concert-test-host',
  templateUrl: './concert-test-host.component.html',
  styleUrls: ['./concert-test-host.component.scss'],
})
export class ConcertTestHostComponent implements OnInit {
  concertModel: ConcertModel = new ConcertModel();
  constructor() {}

  ngOnInit(): void {}
}
