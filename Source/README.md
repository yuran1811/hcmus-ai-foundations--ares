<h1 align="center">Ares</h1>
<p align="center" style="font-size:16px"><strong></strong></p>
<p align="center">  
  <img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/palette/macchiato.png" width="400" />
</p>

<p align="center">
  <img alt="Stars" src="https://badgen.net/github/stars/yuran1811/hcmus-ai-foundations">
  <img alt="Forks" src="https://badgen.net/github/forks/yuran1811/hcmus-ai-foundations">
  <img alt="Issues" src="https://badgen.net/github/issues/yuran1811/hcmus-ai-foundations">
  <img alt="Commits" src="https://badgen.net/github/commits/yuran1811/hcmus-ai-foundations">
  <img alt="Code Size" src="https://img.shields.io/github/languages/code-size/yuran1811/hcmus-ai-foundations">
</p>

## Screenshots

<div style="display:flex;gap:12px;justify-content:center">
	<img src="./public/screenshots/home.png" style="width:45%;max-width:380px">
	<img src="./public/screenshots/game.png" style="width:45%;max-width:380px">
</div>
<div style="display:flex;gap:12px;justify-content:center">
	<img src="./public/screenshots/pick-algo.png" style="width:45%;max-width:380px">
	<img src="./public/screenshots/pick-map.png" style="width:45%;max-width:380px">
</div>
<div style="display:flex;gap:12px;justify-content:center">
	<img src="./public/screenshots/setting.png" style="width:45%;max-width:380px">
	<img src="./public/screenshots/import-map.png" style="width:45%;max-width:380px">
</div>

## Quick Start

- This project using [rye](https://rye.astral.sh/) as package manager.

**Install dependencies**

```bash
rye sync
```

or

```bash
pip install -r requirements.txt
```

**Running the Project**

```bash
rye run solve
```

or

```bash
rye run dev
```

or

```bash
rye run ares
```

or

```bash
rye run ares [OPTIONS]

Options:
	-v,	--version	Print the version
		--gui		Using GUI
```

**Testing**

```bash
rye test
```

**Linting**

```bash
rye lint
```

**Formatting**

```bash
rye fmt
```
