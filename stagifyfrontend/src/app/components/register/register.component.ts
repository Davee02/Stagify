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
    this.registerForm = this.formBuilder.group(RegisterViewModel);
  }

  ngOnInit(): void {
  }

  register(registerData:RegisterViewModel){
    this.userService.register(registerData)
    .subscribe(
      (data:HttpResponse<any>) => {
          if(data.ok){
            this.snackBar.open('Registered Successfully');
            this.router.navigate(['/home'])
          }
      },
      (error)=>{
        this.snackBar.open('Beim regisitrieren ist ein Fehler aufgetreten. Bitte versuche es erneut.')
        this.registerForm.reset();
      }
    )
  }
}
