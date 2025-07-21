# Pokelib 🧬

Pokelib is a Django-based web application that displays Pokémon data using [PokeAPI](https://pokeapi.co/). Users can view random Pokémon on the homepage, filter Pokémon by type, or search by name. Each Pokémon has a detailed page showing species, types, abilities, forms, and (if available) evolution chains.

> ⚠️ Note: Only ~130 out of 1300 Pokémon have full evolution chain data loaded due to partial API fetching.

---

## 🚀 Features

- Random Pokémon display on homepage
- Full-text search by Pokémon name
- Filtering by Pokémon types in the navbar
- Detailed individual Pokémon pages with:
  - Base experience
  - Height and weight
  - Species
  - Types and abilities
  - Forms
  - Evolution chains (if available)
- Responsive design with Bootstrap 5
- Context processors for global filter access
- Clean class-based Django views

---

## 🛠️ Technologies Used

- Python 3.12
- Django 5.x
- Django REST Framework
- Django Filters
- Bootstrap 5
- Docker
- JSONField for complex nested data (abilities, types, species, etc.)
- Custom management commands to fetch data from PokeAPI

---

## 🐳 Quick Start (Docker)

1. Clone the repository:
   ```bash
   https://github.com/yalkun96/PokemonHouse
   cd pokelib
   
Build the Docker image:

docker build -t pokelib-app .
Run the container:

docker run -p 8000:8000 pokelib-app
Open in your browser:

http://localhost:8000


Local Development (no Docker)
Create and activate virtual environment:

python -m venv venv
source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Run migrations:
python manage.py migrate

Fetch Pokémon and chains (optional):
python manage.py fetch_pokemons
python manage.py fetch_chain

Start development server:

python manage.py runserver
