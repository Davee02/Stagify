import { Component, OnInit } from '@angular/core';
import ArtistModel from 'src/app/models/artist.model';

@Component({
  selector: 'app-artist-test-host',
  templateUrl: './artist-test-host.component.html',
  styleUrls: ['./artist-test-host.component.scss'],
})
export class ArtistTestHostComponent implements OnInit {
  artistModel: ArtistModel = new ArtistModel();
  constructor() {}

  ngOnInit(): void {}
}
