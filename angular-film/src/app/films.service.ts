import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { Films } from './films';

@Injectable({
  providedIn: 'root'
})
export class FilmsService {

  private baseUrl: string = 'http://127.0.0.1:5000'

  constructor(
    private http: HttpClient
  ) { }

  searchFilms (value: string): Observable<Films[]> {
    return this.http.get<Films[]>(`${this.baseUrl}/api/v1/search/${value}`)
  }
  getFilm (id: string): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/api/v1/films/${id}`)
  }
  getSimilar (title: string): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/api/v1/similar/${title}`)
  }
}