# Tauri + React

Proyecto creado con Tauri y React en Vite.

## Recommended IDE Setup

- [VS Code](https://code.visualstudio.com/) + [Tauri](https://marketplace.visualstudio.com/items?itemName=tauri-apps.tauri-vscode) + [rust-analyzer](https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer)

# Tutorial: Inicializando el Proyecto

Los siguientes son los pasos para poder poner en marcha el proyecto [TractorScript].

## Paso 0: Instalar los prerequisitos
Ve a la pagina oficial de [Tauri](https://tauri.app/v1/guides/getting-started/prerequisites) y sigue los pasos para instalar los prerequisitos.
> Nota: Solo con instalar Rust se descarga e instala lo necesario.

## Paso 1: Descarga el repositorio 

Primero, necesitamos instalar las dependencias necesarias. Para ello ve a la carpeta raíz del proyecto y ejecuta:

```bash
npm install
```
## Paso 2: Descarga los modulos necesarios para Python

Debido a que el analisis se lleva a cabo a modo de servidor que recibe peticiones HTTP, es necesario instalar algunas librerias de Python para lograr esto, asi como la librería necesaria para el analisis.

```bash
pip install flask flask_cors ply
```
## Paso 3: Ejecutar el proyecto
Dirígete a la carpeta raíz del proyecto y ejecuta:
```bash
npm run compilador
```

## Paso 4: ¡Listo para Empezar!
¡Felicidades! Has inicializado con éxito el proyecto [TractorScript]. Ahora puedes comenzar a explorar o editar el código si lo requieres.
