import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.scss']
})
export class SearchBarComponent implements OnInit {
  searchForm:FormGroup;
  constructor(formBuilder: FormBuilder, private router:Router) {
    this.searchForm = formBuilder.group({
      searchBar: new FormControl('')
    });
   }

  
  ngOnInit(): void {
  }

  search(value){
    this.router.navigate(['search', {value: value.value}], )
  }

}
