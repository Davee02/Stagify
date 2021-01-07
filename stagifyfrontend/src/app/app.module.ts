import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './components/home/home.component';
import { SearchComponent } from './components/search/search.component';
import { SearchBarComponent } from './components/search-bar/search-bar.component';
import { ConcertItemComponent } from './components/concert-item/concert-item.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormBuilder, FormsModule, ReactiveFormsModule } from '@angular/forms';
import {
  MatSnackBar,
  MAT_SNACK_BAR_DEFAULT_OPTIONS,
} from '@angular/material/snack-bar';
import { OverlayModule } from '@angular/cdk/overlay';
import { UserComponent } from './components/user/user.component';
import { CookieService } from 'ngx-cookie-service';
import { ArtistItemComponent } from './components/artist-item/artist-item.component';
import { WithCredentialsInterceptor } from './services/authentication/authentication/authentication.withcredentials.interceptor';
import { TicketShopComponent } from './components/ticket-shop/ticket-shop.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    SearchComponent,
    SearchBarComponent,
    ConcertItemComponent,
    LoginComponent,
    RegisterComponent,
    UserComponent,
    ArtistItemComponent,
    TicketShopComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    OverlayModule,
  ],
  providers: [
    FormBuilder,
    MatSnackBar,
    { provide: MAT_SNACK_BAR_DEFAULT_OPTIONS, useValue: { duration: 2500 } },
    CookieService,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: WithCredentialsInterceptor,
      multi: true,
    },
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
