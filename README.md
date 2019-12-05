# KemenyRanking
Using simmulated annealing to create Kemeny ranking of 1984 F1 competitors

Run using `python3 kemenyranking.py Formula_One_1984.wmg` to create a potential ranking using the .wmg file provided.
This will attempt to use simmulated annealing to produce a global optima for the ranking order of the competitors, based on edges and weights provided in the Formula_One_1984.wmg file. 

Rankings will be based on reducing the discrepancy of competitors ranks, and victories/losses contradicting the order of these ranks, and this method is based upon the [Kemeny method](https://en.wikipedia.org/wiki/Kemeny%E2%80%93Young_method).

Example ranking result when running the algorithm:

| Rank | ID | Name               |
| ---- |:--:| ------------------:|
| 1    | 10 | Alain Prost        |
| 2    | 9  | Niki Lauda         |
| 3    | 2  | Rene Arnoux        |
| 4    | 3  | Elio de Angelis    |
| 5    | 13 | Michele Alboreto   |
| 6    | 22 | Derek Warwick      |
| 7    | 16 | Nelson Piquet      |
| 8    | 7  | Corrado Fabi       |
| 9    | 18 | Patrick Tambay     |
| 10   | 20 | Andrea de Cesaris  |
| 11   | 33 | Mauro Baldi        | 
| 12   | 31 | Teo Fabi           |
| 13   | 21 | Riccardo Patrese   |
| 14   | 6  | Nigel Mansell      |
| 15   | 28 | Stefan Johansson   |
| 16   | 29 | Jo Gartner         |
| 17   | 1  | Keke Rosberg       |
| 18   | 11 | Thierry Bousten    |
| 19   | 14 | Ayrton Senna       |
| 20   | 30 | Gerhard Berger     |
| 21   | 24 | Eddie Cheever      |
| 22   | 35 | Philippe Streiff   |
| 23   | 12 | Marc Surer         |
| 24   | 15 | Jonathan Palmer    |
| 25   | 26 | Martin Brundle     |
| 26   | 19 | Huub Rothengatter  |
| 27   | 4  | Jacques Laffite    |
| 28   | 23 | Stefan Bellof      |
| 29   | 5  | Piercarlo Ghinzani |
| 30   | 25 | Francois Hesnault  |
| 31   | 8  | Manfred Winkelhock |
| 32   | 17 | Johnny Cecotto     |
| 33   | 27 | Philippe Alliot    |
| 34   | 34 | Mike Thackwell     |
| 35   | 32 | Pierluigi Martini  |

