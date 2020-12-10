import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-concert-item',
  templateUrl: './concert-item.component.html',
  styleUrls: ['./concert-item.component.scss']
})
export class ConcertItemComponent implements OnInit {

  @Input() concertImagePath: string;
  @Input() artistImagePath: string;
  @Input() artistName: string;
  @Input() concertName:string;
  @Input() concertDate: Date;

  constructor() { }

  ngOnInit(): void {
  }

}
