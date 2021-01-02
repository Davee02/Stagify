import { HttpResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
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

  constructor(
    private authService:AuthenticationService, 
    private router:Router,
    private snackBar:MatSnackBar,
    private formBuilder:FormBuilder,) {
      this.loginForm = this.formBuilder.group({
        username: new FormControl(''),
        password: new FormControl('')
      });
    }

  ngOnInit(): void {
  }



  async login(loginData: LoginViewModel){
    var response = await this.authService.login(loginData);
    if(response.ok){
      this.snackBar.open('Login Succeeded');
      this.router.navigate(['home'])
    }
  }

}
