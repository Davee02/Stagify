import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import ConcertModel from 'src/app/models/concert.model';
import { ConcertService } from 'src/app/services/concert/concert.service';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {
  concerts: Array<ConcertModel>
  constructor(private concertService:ConcertService,
    private route:ActivatedRoute) { 
    
  }

  search(value:string){
  }

  ngOnInit(): void {
    this.route.params.toPromise().then((value:Params) => this.search(value.get('value')));
  }

  

}
