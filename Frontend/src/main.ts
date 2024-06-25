import { bootstrapApplication } from '@angular/platform-browser';
import { ReactiveFormsModule } from '@angular/forms';
import { provideHttpClient, HTTP_INTERCEPTORS } from '@angular/common/http';
import { AppComponent } from './app/app.component';
import { AppRoutingModule } from './app/app-routing.module';
 import {importProvidersFrom} from "@angular/core";
import {AppModule} from "./app/app.module";

bootstrapApplication(AppComponent, {
  providers: [
    importProvidersFrom(AppModule)  // This imports all providers from AppModule
  ]
}).catch(err => console.error(err));
