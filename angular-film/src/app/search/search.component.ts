import { Component, OnInit } from '@angular/core';
import { FilmsService } from '../films.service'
import { Films } from '../films';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {
  
  data: Films[];
  film: Films;
  similarFilms: any;
  showSuggestion: boolean = false;
  showSimilarContainer: boolean = false;
  showFilm: boolean = false;
  showCast: boolean = false;
  showCrew: boolean = false;

  constructor(
    private filmService: FilmsService,
  ) { }

  ngOnInit() {
  }

  getFilms (searchValue: string): void {
    this.showSuggestion = true;
    this.showSimilarContainer = false;
    this.filmService.searchFilms(searchValue)
      .subscribe(data => {
        this.data = data;
      });
  }

  fetchOneFilm (id: string): void {
    this.showSuggestion = false;
    this.showFilm = true;
    this.showCast = false;
    this.showCrew = false;
    this.filmService.getFilm(id)
      .subscribe(item => {
        this.film = item;
    })
  }

  showSimilar (title: string): void {
    this.showSimilarContainer = true;
    this.filmService.getSimilar(title)
    .subscribe(suggestion => {
      this.similarFilms = suggestion;
    })
  }
  hideSuggestion (): void {
    this.showSuggestion = false;
  }

  showCastInfo (): void {
    this.showFilm = false;
    this.showCast = true;
    this.showCrew = false;
  }

  showOverview (): void {
    this.showFilm = true;
    this.showCast = false;
    this.showCrew = false;
  }
  
  showCrewInfo (): void {
    this.showCrew = true;
    this.showFilm = false;
    this.showCast = false;
  }
}
