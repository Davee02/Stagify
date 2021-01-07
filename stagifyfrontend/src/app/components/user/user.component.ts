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
  userForm: FormGroup;
  artistForm: FormGroup;
  isLoading: boolean = true;

  constructor(
    private authService: AuthenticationService,
    private router: Router,
    private userServie: UserService,
    private artistServie: ArtistService,
    private snackBar: MatSnackBar,
    private formBuilder: FormBuilder
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

  initializeForms() {
    this.userForm = this.formBuilder.group({
      username: new FormControl(this.userModel.username),
      firstname: new FormControl(this.userModel.firstname),
      lastname: new FormControl(this.userModel.lastname),
    });
    this.artistForm = this.formBuilder.group({
      artistName: new FormControl(this.artistModel.displayname),
      artistDescription: new FormControl(this.artistModel.description),
    });
  }

  fetchUserAndArtist() {
    this.isLoading = true;
    this.userServie.getLoggedInUser().then((value) => {
      this.userModel = value.body;
      if (this.userModel.artistId) {
        this.fetchArtist();
      } else {
        this.initializeForms();
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

  updateUser(value: UserModel) {
    this.isLoading = true;
    var updatedUser = this.userModel;
    updatedUser.username = value.username;
    updatedUser.firstname = value.firstname;
    updatedUser.lastname = value.lastname;
    this.userServie
      .updateUser(updatedUser)
      .then((response) => {
        this.snackBar.open('Benutzer aktualisiert');
        this.isLoading = false;
        this.fetchUser();
      })
      .catch((err) => {
        this.snackBar.open(
          'Benutzer konnte nicht aktualisiert werden. Versuchen Sie es erneut.'
        );
        this.isLoading = false;
      });
  }

  fetchArtist() {
    this.isLoading = true;
    this.artistServie.getArtist(this.userModel.artistId).then((x) => {
      this.artistModel = x.body;
      this.initializeForms();
      this.isLoading = false;
    });
  }

  updateArtist(value: ArtistModel) {
    this.isLoading = true;
    var updatedArtist = new UpdateArtistViewModel();
    updatedArtist.description = value.description;
    updatedArtist.displayname = value.displayname;
    this.artistServie
      .updateArtist(updatedArtist)
      .then((response) => {
        this.snackBar.open('Künstler Profil aktualisiert');
        this.fetchArtist();
        this.isLoading = false;
      })
      .catch((err) => {
        this.snackBar.open(
          'Künstler Profil konnte nicht aktualisiert werden. Versuchen Sie es erneut.'
        );
        this.isLoading = false;
      });
  }

  logout() {
    this.authService
      .logout()
      .then((value) => this.router.navigate(['/home']).catch((err) => {}));
  }
}
