import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { ConcertService } from './concert.service';

describe('ConcertService', () => {
  let service: ConcertService;

  beforeEach(() => {
    TestBed.configureTestingModule({
        imports:[
            HttpClientTestingModule
        ]
    });
    service = TestBed.inject(ConcertService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
