# Pokémon Gallery (Vite + PokeAPI + AWS + GitHub Actions)

Runtime data from [PokeAPI](https://pokeapi.co/).

## Tech Stack
- Vite (vanilla TS)
- GitHub Actions
- AWS S3 + CloudFront
- Doppler (secrets & GitHub Config Sync)

## Public URL (CloudFront)
- http://d2qtw570o1hscj.cloudfront.net

## Screenshots (required)
- Doppler → **Config Syncs** 
![Captura](docs/dopler.png)
- Doppler → **Variables** (values redacted)
![Captura](docs/bucket.png)
![Captura](docs/cloudfront.png)
- GitHub → **Settings → Secrets and variables → Actions**
![Captura](docs/git.png)

## How to run locally
```bash
npm install
npm run dev
