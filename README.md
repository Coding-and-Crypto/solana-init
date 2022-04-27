# Solana Init

Get off the ground fast with auto-generated Solana workspaces.

### Standard

```shell
python -m solana_init my-project
```

```shell
--- my-project
      |--- scripts
      |     |--- cicd.sh
      |--- src
      |     |--- clients
      |     |     |--- main.ts
      |     |--- programs
      |--- .gitignore
      |--- README.md
      |--- package.json
```

### With Docker

```shell
python -m solana_init my-project --docker
```

```shell
--- my-project
      |--- scripts
      |     |--- cicd.sh
      |--- src
      |     |--- clients
      |     |     |--- main.ts
      |     |--- programs
      |--- .gitignore
      |--- README.md
      |--- Dockerfile
      |--- package.json
```

### Including Rust Programs

```shell
python -m solana_init my-project --program prog1 --program prog2 
```

```shell
--- my-project
      |--- scripts
      |     |--- cicd.sh
      |--- src
      |     |--- clients
      |     |     |--- main.ts
      |     |--- programs
      |     |     |--- prog1
      |     |     |     |--- src
      |     |     |     |     |--- lib.rs
      |     |     |     |--- Cargo.toml
      |     |     |--- prog2
      |     |     |     |--- src
      |     |     |     |     |--- lib.rs
      |     |     |     |--- Cargo.toml
      |--- .gitignore
      |--- README.md
      |--- package.json
```