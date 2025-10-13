## Components

### App.jsx
- Componente principal
- Maneja el estado del tab activo (hide/reveal)
- Renderiza HideTab o RevealTab según selección

### HideTab.jsx
- Formulario para ingresar secreto
- Llama a `POST /api/hide/`
- Muestra la key generada
- Botón para copiar link al portapapeles

### RevealTab.jsx
- Input para ingresar key
- Llama a `GET /api/reveal/{key}/`
- Muestra el secreto revelado
- Lee key de URL query params (`?key=xxx`)

## 🚀 Cómo Usar

### Con Docker  
```bash
# Desde la raíz del proyecto
docker compose up -d
Abre: http://localhost:3000

# Abre Redis Commander
open http://localhost:8081