import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ArtistTestHostComponent } from './artist-test-host.component';

describe('ArtistTestHostComponent', () => {
  let component: ArtistTestHostComponent;
  let fixture: ComponentFixture<ArtistTestHostComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ArtistTestHostComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ArtistTestHostComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
