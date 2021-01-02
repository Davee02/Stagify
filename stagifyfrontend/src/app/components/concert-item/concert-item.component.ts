import { Component, Input, OnInit } from '@angular/core';
import ConcertModel from 'src/app/models/concert.model';

@Component({
  selector: 'app-concert-item',
  templateUrl: './concert-item.component.html',
  styleUrls: ['./concert-item.component.scss']
})
export class ConcertItemComponent implements OnInit {

  @Input() concertModel: ConcertModel;


  constructor() { }

  ngOnInit(): void {
  }

}
