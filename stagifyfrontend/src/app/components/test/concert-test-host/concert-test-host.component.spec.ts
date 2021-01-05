import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConcertTestHostComponent } from './concert-test-host.component';

describe('ConcertTestHostComponent', () => {
  let component: ConcertTestHostComponent;
  let fixture: ComponentFixture<ConcertTestHostComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ConcertTestHostComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ConcertTestHostComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
