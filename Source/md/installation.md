# Installation

**Package Manager**

- This project using [rye](https://rye.astral.sh/) as package manager.

## Development

**Create the project**

```bash
rye init ares --license MIT --private --script
```

**Install dependencies**

```bash
rye sync
```

**Running the Project**

```bash
rye run dev
```

**Testing**

```bash
rye test
```

**Auto-generated `requirements.txt`**

```bash
rye list > requirements.txt
```
