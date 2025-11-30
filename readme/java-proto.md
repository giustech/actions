# [Nome da Aplicação] - Protobuf Connector

Este repositório contém as classes Java geradas (stubs) a partir das definições Protobuf (`.proto`) da **[Sua Aplicação Principal]**.

Esta biblioteca atua como um conector oficial, garantindo que serviços consumidores utilizem os contratos de dados e clientes gRPC corretos e atualizados.

---

## 📦 Instalação

Configure o seu gerenciador de dependências conforme abaixo.

### 🐘 Gradle (build.gradle)

Adicione o repositório e a dependência no seu arquivo `build.gradle`:

```groovy
repositories {
    mavenCentral()
    // Exemplo para GitHub Packages ou Nexus Privado
    maven {
        url = uri("https://maven.pkg.github.com/[SEU_USUARIO]/[SEU_REPOSITORIO]")
        credentials {
            username = System.getenv("GITHUB_ACTOR") ?: "SEU_USUARIO"
            password = System.getenv("GITHUB_TOKEN") ?: "SEU_TOKEN"
        }
    }
}

dependencies {
    // Conector da Aplicação
    implementation 'com.giustech:[SEU_ARTIFACT_ID]:[VERSAO_ATUAL]'

    // Dependências transitivas do gRPC (caso necessário)
    implementation 'io.grpc:grpc-protobuf:1.58.0'
    implementation 'io.grpc:grpc-stub:1.58.0'
}