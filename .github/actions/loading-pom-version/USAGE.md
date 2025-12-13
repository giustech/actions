# Como Usar a Action Loading POM Version

## ⚠️ Importante: Forma Correta de Uso

Devido a limitações de compatibilidade do GitHub Actions, esta action **NÃO exporta outputs diretamente**. Você precisa capturar o output do step que executa a action.

## ✅ Uso Correto

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      # Capture o output do step, não da action
      version: ${{ steps.load-version.outputs.version }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Load POM Version
        id: load-version
        uses: Giustech/actions/.github/actions/loading-pom-version@main
      
      - name: Use the version no mesmo job
        run: |
          echo "Version: ${{ steps.load-version.outputs.version }}"
```

## 📋 Exemplo Completo do Seu Caso

```yaml
name: Release

on:
  workflow_dispatch:
  push:
    branches:
      - master

permissions:
  contents: write
  pull-requests: write

jobs:
  loading-files:
    name: Loading files
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.load-version.outputs.version }}
      tag_exists: ${{ steps.extract_version.outputs.tag_exists }}
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Load version from POM
        id: load-version
        uses: Giustech/actions/.github/actions/loading-pom-version@main

      - name: Extract version from pom.xml
        id: extract_version
        run: |       
          # Ensure tags are fetched and check remote for the exact tag
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
      - name: Use version from previous job
        run: |
          echo "Version from previous job: ${{ needs.loading-files.outputs.version }}"
```

## 🔑 Pontos-Chave

1. **Sempre use `id`** no step que chama a action
2. **Referencie pelo step id**: `${{ steps.SEU_ID.outputs.version }}`
3. **Para passar entre jobs**: Defina no `outputs` do job e use `needs.JOB_NAME.outputs.version`

## 📝 Inputs

| Nome | Descrição | Obrigatório | Padrão |
|------|-----------|-------------|---------|
| `pom_path` | Caminho para o arquivo pom.xml | Não | `pom.xml` |

### Exemplo com caminho customizado:

```yaml
- name: Load POM Version
  id: load-version
  uses: Giustech/actions/.github/actions/loading-pom-version@main
  with:
    pom_path: "submodule/pom.xml"
```

## 📤 Outputs

| Nome | Descrição | Como Acessar |
|------|-----------|--------------|
| `version` | Versão extraída do pom.xml | `${{ steps.SEU_ID.outputs.version }}` |

## 🐛 Troubleshooting

### Output está vazio
1. Verifique se você fez checkout do código antes
2. Verifique se o caminho do pom.xml está correto
3. Certifique-se de estar usando o `id` do step correto

### Erro "Unexpected value 'outputs'"
Este erro foi corrigido. Faça commit e push das mudanças e tente novamente.

