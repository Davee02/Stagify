import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import ArtistModel from 'src/app/models/artist.model';
import ConcertModel from 'src/app/models/concert.model';
import { ConcertService } from 'src/app/services/concert/concert.service';
import { SearchService } from 'src/app/services/search/search.service';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {
  artists: Array<ArtistModel>
  isLoading:boolean = true;
  searchValue:string;

  constructor(private searchService:SearchService,
    private route:ActivatedRoute) { 
  }

  search(){
    if(this.searchValue == '' || this.search == null){
      this.isLoading = false;
    }else{
      this.searchService.searchArtists(this.searchValue)
      .then(resultValue => {
        this.artists = resultValue;
         this.isLoading = false
        })
      .catch(() => this.isLoading = false);
    }


  }

  ngOnInit(): void {
    this.route.queryParams
    .subscribe(params => {
      this.searchValue = params.value;
      this.search()
    }
  );
  }

  

}
