import { HttpResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from 'src/app/services/user/user.service';
import {MatSnackBar} from '@angular/material/snack-bar'
import LoginViewModel from 'src/app/models/ViewModels/login.viewmodel';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  username:string;
  password:string;
  constructor(
    private userService:UserService, 
    private router:Router,
    private snackBar:MatSnackBar) { }

  ngOnInit(): void {
  }

  login(){
    this.userService.login({username:this.username, password:this.password})
      .subscribe(
        (value:HttpResponse<any>)=>{
          if(value.ok){
            this.snackBar.open('Login erfolgreich')
            this.router.navigate(['/home'])
          }
        },
        error=>{
          this.snackBar.open('Login fehlgeschlagen')
        }
      )
  }

}
