import { HttpResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import ArtistModel from 'src/app/models/artist.model';
import ConcertModel from 'src/app/models/concert.model';
import { ArtistService } from 'src/app/services/artist/artist.service';
import { ConcertService } from 'src/app/services/concert/concert.service';

@Component({
  selector: 'app-artist-detail',
  templateUrl: './artist-detail.component.html',
  styleUrls: ['./artist-detail.component.scss']
})
export class ArtistDetailComponent implements OnInit {
  artistModel:ArtistModel = new ArtistModel();
  concerts:Array<ConcertModel> = new Array<ConcertModel>();
  isLoading:boolean = true;
  error:number;

  constructor(
    private artistService:ArtistService, 
    private router:Router,
    private route:ActivatedRoute) { 
      
  }

  ngOnInit(): void {
    this.route.params
    .subscribe(params => {
      this.artistModel.id = params.id;
      this.getArtistData();
    });
  }

  getArtistData(){
    this.artistService.getArtist(this.artistModel.id)
    .then(x =>  {
      this.artistModel = x.body;
      this.isLoading = false;
    })
    .catch((response:HttpResponse<any>) => {
      this.error = response.status;
      this.isLoading = false;
    }
    );
    
  }
}
