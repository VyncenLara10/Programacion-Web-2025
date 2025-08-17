type PokemonListItem = { name: string; url: string };
type PokemonListResponse = { count: number; results: PokemonListItem[] };
type PokemonType = { slot: number; type: { name: string; url: string } };
type Pokemon = {
  id: number;
  name: string;
  sprites: {
    other?: {
      ['official-artwork']?: { front_default?: string | null }
    }
  };
  types: PokemonType[];
  height: number;
  weight: number;
  abilities: { ability: { name: string } }[];
};

const API_BASE = 'https://pokeapi.co/api/v2';
const GRID = document.querySelector<HTMLDivElement>('#grid')!;
const STATUS = document.querySelector<HTMLDivElement>('#status')!;

function titleCase(s: string) {
  return s.replace(/\b[a-z]/g, (c) => c.toUpperCase());
}

async function fetchPokemonPage(limit = 24, offset = 0): Promise<PokemonListItem[]> {
  const res = await fetch(`${API_BASE}/pokemon?limit=${limit}&offset=${offset}`);
  if (!res.ok) throw new Error('Failed to fetch pokemon list');
  const data = (await res.json()) as PokemonListResponse;
  return data.results;
}

async function fetchPokemon(url: string): Promise<Pokemon> {
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch pokemon detail');
  return res.json() as Promise<Pokemon>;
}

function renderCard(p: Pokemon) {
  const img = p.sprites?.other?.['official-artwork']?.front_default
           || `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${p.id}.png`;

  const types = p.types?.map(t => t.type.name) ?? [];
  const el = document.createElement('article');
  el.className = 'card';
  el.innerHTML = `
    <a class="thumb" href="https://pokeapi.co/api/v2/pokemon/${p.id}" target="_blank" rel="noreferrer">
      <img alt="${p.name}" src="${img}" loading="lazy" />
      <span class="sr-only">Open ${p.name} on PokeAPI</span>
    </a>
    <h2>${titleCase(p.name)} <small>#${p.id}</small></h2>
    <p class="meta">
      ${types.map(t => `<span class="type">${t}</span>`).join('')}
    </p>
  `;
  GRID.appendChild(el);
}

async function main() {
  try {
    STATUS.textContent = 'Loading Pokémon...';
    const list = await fetchPokemonPage(24, 0);
    const details = await Promise.all(list.map(item => fetchPokemon(item.url)));
    details.forEach(renderCard);
    STATUS.textContent = `Loaded ${details.length} Pokémon`;
  } catch (err) {
    console.error(err);
    STATUS.textContent = 'Failed to load Pokémon. Please try again.';
  }
}

main();
