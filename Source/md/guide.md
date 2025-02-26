# Installation

**Package Manager**

- This project using [rye](https://rye.astral.sh/) as package manager.

# Development

**Create the project**

```bash
rye init ares --license MIT --private --script
```

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

**Generate `requirements.txt`**

```bash
rye list > requirements.txt
```
