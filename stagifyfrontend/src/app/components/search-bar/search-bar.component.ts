import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.scss'],
})
export class SearchBarComponent implements OnInit {
  searchForm: FormGroup;
  constructor(private formBuilder: FormBuilder, private router: Router) {
    this.searchForm = formBuilder.group({
      searchBar: new FormControl(''),
    });
  }

  ngOnInit(): void {}

  search(value) {
    if (!(value == null || value == '')) {
      this.router.navigate(['artists/search'], {
        queryParams: { value: value.searchBar },
      });
    }
  }
}
