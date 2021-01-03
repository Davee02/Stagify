import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import UserModel from 'src/app/models/user.model';
import { AuthenticationService } from 'src/app/services/authentication/authentication/authentication.service';
import { UserService } from 'src/app/services/user/user.service';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.scss']
})
export class UserComponent implements OnInit {
  userModel:UserModel;
  isLoggedIn:boolean;
  isLoading:boolean = true;
  constructor(private authService:AuthenticationService,
    private router:Router,
    private userServie:UserService) { 
      if(authService.isLoggedIn()){
        this.userServie.getLoggedInUser()
        .then((value) => {
          this.userModel = value.body
          this.isLoading = false;
        })
      }else{
        router.navigate(['login'], {queryParams: {successfulLoginPath: 'user'}});
      }
      
  }

  ngOnInit(): void {
  }

  logout(){
    this.authService.logout()
    .then(value => this.router.navigate(["/home"])
    .catch(err => {}));
  }
}
