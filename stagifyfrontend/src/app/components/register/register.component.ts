import { HttpResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import RegisterViewModel from 'src/app/models/ViewModels/register.viewmodel';
import { UserService } from 'src/app/services/user/user.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {  
  registerForm:FormGroup;

  constructor(
    private userService:UserService, 
    private formBuilder:FormBuilder,
    private snackBar:MatSnackBar,
    private router:Router
    ) { 
    this.registerForm = this.formBuilder.group({
      username: new FormControl(''),
      email: new FormControl(''),
      password: new FormControl('')
    });
  }

  ngOnInit(): void {
  }

  async register(registerData){
    var response = await this.userService.register(registerData);
    if(response.ok){
      this.snackBar.open('Register Succeeded');
      this.router.navigate(['login']);
    }else{
      this.snackBar.open('Register failed something must be wrong, please try again');
    }
  }
}
