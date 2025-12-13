# Loading POM Version Action

Esta action extrai a versão do arquivo `pom.xml` de um projeto Maven.

## ⚠️ Importante

Esta action **não exporta outputs no nível da action**. Você deve capturar o output através do **step id**.

## 📋 Uso Correto

```yaml
- name: Load POM Version
  id: load-version  # ← Defina um ID
  uses: Giustech/actions/.github/actions/loading-pom-version@main

- name: Use a versão
  run: echo "Version: ${{ steps.load-version.outputs.version }}"
  #                         ^^^^^^^^^^^^^ Use o ID do step
```

## 📚 Exemplos

### Exemplo 1: Uso Básico

```yaml
name: Build
on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Load POM Version
        id: load-version
        uses: Giustech/actions/.github/actions/loading-pom-version@main
      
      - name: Show version
        run: echo "Version: ${{ steps.load-version.outputs.version }}"
```

### Exemplo 2: Com Caminho Customizado

```yaml
- name: Load POM Version
  id: load-version
  uses: Giustech/actions/.github/actions/loading-pom-version@main
  with:
    pom_path: "submodule/pom.xml"
```

### Exemplo 3: Passando Entre Jobs (SEU CASO)

```yaml
jobs:
  loading-files:
    name: Loading files
    runs-on: ubuntu-latest
    outputs:
      # Exporte o output do step para outros jobs
      version: ${{ steps.load-version.outputs.version }}
      tag_exists: ${{ steps.extract_version.outputs.tag_exists }}
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Load version from POM
        id: load-version
        uses: Giustech/actions/.github/actions/loading-pom-version@main

      - name: Check if tag exists
        id: extract_version
        run: |       
          git fetch --tags --prune
          if git ls-remote --tags origin "refs/tags/v${{ steps.load-version.outputs.version }}" | grep -q .; then
            TAG_EXISTS=true
          else
            TAG_EXISTS=false
          fi
          
          echo "new_version=v${{ steps.load-version.outputs.version }}" >> $GITHUB_OUTPUT
          echo "tag_exists=${TAG_EXISTS}" >> $GITHUB_OUTPUT
          echo "Detected version: ${{ steps.load-version.outputs.version }}, tag_exists=${TAG_EXISTS}"

  next-job:
    needs: loading-files
    runs-on: ubuntu-latest
    steps:
      - name: Use version
        run: echo "Version: ${{ needs.loading-files.outputs.version }}"
```

### Exemplo 4: Build e Deploy Completo

```yaml
name: Build and Deploy
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
      
      - name: Load version
        id: version
        uses: Giustech/actions/.github/actions/loading-pom-version@main
      
      - name: Build
        run: mvn clean package
      
      - name: Create Docker image
        run: |
          docker build -t myapp:${{ steps.version.outputs.version }} .
          docker tag myapp:${{ steps.version.outputs.version }} myapp:latest
      
      - name: Push to registry
        run: |
          docker push myapp:${{ steps.version.outputs.version }}
          docker push myapp:latest
```

## 📥 Inputs

| Nome | Descrição | Obrigatório | Padrão |
|------|-----------|-------------|---------|
| `pom_path` | Caminho para o arquivo pom.xml | Não | `pom.xml` |

## 📤 Outputs

| Nome | Descrição | Como Acessar |
|------|-----------|--------------|
| `version` | Versão extraída do pom.xml | `${{ steps.SEU_ID.outputs.version }}` |

**Importante:** O output é acessado através do **step id**, não da action.

## 🔧 Requisitos

- Python 3 disponível no runner (já está por padrão no ubuntu-latest)
- Arquivo `pom.xml` válido com tag `<version>`

## 🐛 Troubleshooting

### Output está vazio
1. Certifique-se de fazer checkout do código antes: `uses: actions/checkout@v4`
2. Verifique se o caminho do `pom_path` está correto
3. Confirme que seu pom.xml tem uma tag `<version>` válida

### Não consigo acessar em outro job
Use o padrão de outputs no job:
```yaml
jobs:
  job1:
    outputs:
      version: ${{ steps.load-version.outputs.version }}
    steps:
      - id: load-version
        uses: Giustech/actions/.github/actions/loading-pom-version@main
  
  job2:
    needs: job1
    steps:
      - run: echo "${{ needs.job1.outputs.version }}"
```

## 📌 Versionamento

Recomendações para referenciar esta action:

```yaml
# Branch (desenvolvimento)
uses: Giustech/actions/.github/actions/loading-pom-version@main

# Tag específica (recomendado para produção)
uses: Giustech/actions/.github/actions/loading-pom-version@v1.0.0

# Commit específico (máxima segurança)
uses: Giustech/actions/.github/actions/loading-pom-version@a1b2c3d
```

