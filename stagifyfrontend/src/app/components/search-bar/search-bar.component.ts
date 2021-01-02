import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.scss']
})
export class SearchBarComponent implements OnInit {

  constructor(private formBuilder: FormBuilder, private router:Router) {
    formBuilder.group({
      searchBar: new FormControl('')
    });
   }


  
  ngOnInit(): void {
  }

  search(value:string){
    this.router.navigate(['search', {value: value}], )
  }

}
