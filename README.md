# Database app


Pakka kjøres ved å kjøre
```
python src\entrypoint.py
```

## Arkitektur

Prosjektet er delt opp i to moduler, data_access og entrypoint.
Entrypoint er det brukeren kjører, mens data_access inneholder all interaksjon med databasen.

``` plantuml
@startuml
database "database" {
}

[data_access] <-> sqlite3
sqlite3 <-> database
[entrypoint] <-> [data_access]
user <-> [entrypoint]


@enduml
```