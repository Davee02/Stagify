import { Component, Input, OnInit } from '@angular/core';
import ArtistModel from 'src/app/models/artist.model';

@Component({
  selector: 'app-artist-item',
  templateUrl: './artist-item.component.html',
  styleUrls: ['./artist-item.component.scss'],
})
export class ArtistItemComponent implements OnInit {
  @Input() artistModel: ArtistModel;

  constructor() {}

  ngOnInit(): void {}
}
