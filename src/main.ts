const API_BASE = 'https://pokeapi.co/api/v2';
const GRID = document.querySelector<HTMLDivElement>('#grid')!;
const STATUS = document.querySelector<HTMLDivElement>('#status')!;
const SHUFFLE_BTN = document.querySelector<HTMLButtonElement>('#shuffle')!;

type PokemonListItem = { name: string; url: string };
type PokemonListResponse = { count: number; results: PokemonListItem[] };
type PokemonType = { slot: number; type: { name: string; url: string } };
type Pokemon = {
  id: number;
  name: string;
  sprites: { other?: { ['official-artwork']?: { front_default?: string | null } } };
  types: PokemonType[];
  height: number;
  weight: number;
  abilities: { ability: { name: string } }[];
};

function titleCase(s: string) { return s.replace(/\b[a-z]/g, c => c.toUpperCase()); }

async function fetchPokemonList(): Promise<PokemonListItem[]> {
  const res = await fetch(`${API_BASE}/pokemon?limit=100000&offset=0`);
  const data = (await res.json()) as PokemonListResponse;
  return data.results;
}

async function fetchPokemon(url: string): Promise<Pokemon> {
  const res = await fetch(url);
  return res.json() as Promise<Pokemon>;
}

function renderCard(p: Pokemon) {
  const img = p.sprites?.other?.['official-artwork']?.front_default
           || `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${p.id}.png`;

  const types = p.types?.map(t => t.type.name) ?? [];
  const displayName = titleCase(p.name);

  const altura = (p.height * 0.1).toFixed(1);
  const peso = (p.weight * 0.1).toFixed(1);

  const el = document.createElement('article');
  el.className = 'card';
  el.innerHTML = `
    <a class="thumb" href="https://pokeapi.co/api/v2/pokemon/${p.id}" target="_blank" rel="noreferrer">
      <img alt="${displayName}" src="${img}" loading="lazy" />
      <span class="sr-only">Abrir ${displayName} en PokeAPI</span>
    </a>
    <h2>${displayName} <small>#${p.id}</small></h2>
    <p class="meta">${types.map(t => `<span class="type">${t}</span>`).join('')}</p>
    <p class="meta">Altura: ${altura} m | Peso: ${peso} kg</p>
  `;
  GRID.appendChild(el);
}

async function loadRandomPokemons(allList: PokemonListItem[]) {
  GRID.innerHTML = '';
  STATUS.textContent = 'Cargando pokemones';

  const randomItems: PokemonListItem[] = [];
  const usedIndexes = new Set<number>();
  while (randomItems.length < 25) {
    const idx = Math.floor(Math.random() * allList.length);
    if (!usedIndexes.has(idx)) {
      usedIndexes.add(idx);
      randomItems.push(allList[idx]);
    }
  }

  const details = await Promise.all(randomItems.map(item => fetchPokemon(item.url)));
  details.forEach(renderCard);
  STATUS.textContent = `Se han cargado 25 Pokemones`;
}

async function main() {
  try {
    const allList = await fetchPokemonList();
    await loadRandomPokemons(allList);

    SHUFFLE_BTN.addEventListener('click', async () => {
      await loadRandomPokemons(allList);
    });
  } catch (err) {
    console.error(err);
    STATUS.textContent = 'Error cargando Pokemones. Intenta de nuevo.';
  }
}

main();
