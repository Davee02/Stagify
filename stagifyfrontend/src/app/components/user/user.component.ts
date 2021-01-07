import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import ArtistModel from 'src/app/models/artist.model';
import UserModel from 'src/app/models/user.model';
import UpdateArtistViewModel from 'src/app/models/ViewModels/update-artist.viewmodel';
import { ArtistService } from 'src/app/services/artist/artist.service';
import { AuthenticationService } from 'src/app/services/authentication/authentication/authentication.service';
import { UserService } from 'src/app/services/user/user.service';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.scss'],
})
export class UserComponent implements OnInit {
  userModel: UserModel;
  artistModel: ArtistModel;
  isLoading: boolean = true;

  constructor(
    private authService: AuthenticationService,
    private router: Router,
    private userServie: UserService,
    private artistServie: ArtistService
  ) {}

  ngOnInit(): void {
    if (this.authService.isLoggedIn()) {
      this.fetchUserAndArtist();
    } else {
      this.router.navigate(['login'], {
        queryParams: { successfulLoginPath: 'user' },
      });
    }
  }

  fetchUserAndArtist() {
    this.isLoading = true;
    this.userServie.getLoggedInUser().then((value) => {
      this.userModel = value.body;
      if (this.userModel.artistId) {
        this.fetchArtist();
      }
      this.isLoading = false;
    });
  }

  fetchUser() {
    this.isLoading = true;
    this.userServie.getLoggedInUser().then((value) => {
      this.userModel = value.body;
      this.isLoading = false;
    });
  }

  fetchArtist() {
    this.isLoading = true;
    this.artistServie.getArtist(this.userModel.artistId).then((x) => {
      this.artistModel = x.body;
      this.isLoading = false;
    });
  }

  logout() {
    this.authService
      .logout()
      .then((value) => this.router.navigate(['/home']).catch((err) => {}));
  }
}
