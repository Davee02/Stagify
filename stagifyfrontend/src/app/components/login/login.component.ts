import { HttpResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from 'src/app/services/user/user.service';
import {MatSnackBar} from '@angular/material/snack-bar'
import LoginViewModel from 'src/app/models/ViewModels/login.viewmodel';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { AuthenticationService } from 'src/app/services/authentication/authentication/authentication.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  loginForm:FormGroup;
  afterSuccessfulLoginPath:string;
  constructor(
    private authService:AuthenticationService, 
    private router:Router,
    private snackBar:MatSnackBar,
    private formBuilder:FormBuilder,
    private route:ActivatedRoute) {
      this.loginForm = this.formBuilder.group({
        username: new FormControl(''),
        password: new FormControl('')
      });
    }

  ngOnInit(): void {
    this.getSuccessfulLoginPath();
  }

  getSuccessfulLoginPath(){
    this.route.queryParams
    .subscribe(params => {
      debugger;
      this.afterSuccessfulLoginPath = params.successfulLoginPath;
    });
  }

  async login(loginData: LoginViewModel){
    var response = await this.authService.login(loginData);
    if(response.ok){
      this.snackBar.open('Login Succeeded');
      if(this.afterSuccessfulLoginPath && this.afterSuccessfulLoginPath != ''){
        this.router.navigate([this.afterSuccessfulLoginPath])
      }else{
        this.router.navigate(['home'])
      }
    }
  }

}
