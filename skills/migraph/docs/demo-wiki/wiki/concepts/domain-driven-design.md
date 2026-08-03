---
title: Domain-Driven Design
type: concept
category: Architecture
domain: ddd
created: 2026-08-03
updated: 2026-08-03
tags:
  - ddd
  - architecture
  - bounded-context
  - domain-model
status: active
id: ddd.concept.domain-driven-design
version: "1.0.0"
confidence: high
source: https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf
inputs: []
outputs: []
dependencies: []
quality_score: 0
aliases: [ddd]
summary: Domain-Driven Design é uma abordagem de modelagem de software onde o domínio do negócio é o coração do sistema — via ubiquitous language, bounded contexts e context mapping no nível estratégico, e entities/value objects/aggregates no nível tático.
---

# Domain-Driven Design

## 🧠 Definition

**Domain-Driven Design (DDD)** é uma abordagem para modelar software complexo colocando o **domínio do negócio** no centro. Proposto por Eric Evans (Blue Book), foca em colaboração entre *domain practitioners* e *software practitioners* para construir um modelo de domínio que reflita a realidade do negócio — usando **ubiquitous language**, **bounded contexts** e **context mapping** (estratégico) e **entities, value objects, aggregates** (tático).

## 📚 Explanation

### Nível Estratégico

**Bounded Context**: fronteira explícita onde um modelo de domínio se aplica. Cada contexto tem sua própria ubiquitous language e modelo — o mesmo termo pode significar coisas diferentes em contextos diferentes.

**Ubiquitous Language**: vocabulário comum entre domínio e código — termos do negócio usados consistentemente em conversas, documentação e código.

**Core Domain vs Subdomains**: o Core Domain é onde a empresa diferencia-se (maior investimento); os demais são *Generic Subdomains* (supporting/generic, frequentemente comprados ou terceirizados).

### Context Mapping

Padrões de integração entre bounded contexts:

| Padrão | Quando usar |
|--------|-------------|
| **Partnership** | duas equipes coordenam juntas para atingir objetivos compartilhados |
| **Shared Kernel** | parte do modelo compartilhada entre contextos (com cuidado) |
| **Customer/Supplier** | upstream define o contrato; downstream consome |
| **Conformist** | downstream aceita o modelo do upstream sem tradução |
| **Anticorruption Layer (ACL)** | downstream protege seu modelo com uma camada de tradução |
| **Open-host Service** | upstream publica uma API formal para downstreams |
| **Published Language** | formato/documentação bem definido do contrato |
| **Separate Ways** | contextos operam isolados, sem integração |
| **Big Ball of Mud** | anti-padrão: modelo único sem fronteiras claras |

### Nível Tático

- **Entity**: objeto com identidade contínua (id) e ciclo de vida (ex.: Order).
- **Value Object**: objeto imutável descrito por atributos, sem identidade (ex.: Money).
- **Aggregate**: cluster de entidades com consistência transacional; uma **Aggregate Root** é a única porta de entrada.
- **Repository**: abstração de persistência para aggregates.
- **Domain Service**: lógica de negócio que não pertence naturalmente a uma entity/value object.
- **Domain Event**: fato do domínio ocorrido (OrderPlaced) para integração/efeitos colaterais.
- **Factory**: criação de objetos complexos mantendo invariantes.

## 🔗 Related

- [[Kubernetes]]
- [[ArgoCD]]

## 🧩 Key Insights

- Bounded contexts = fronteiras de modelo; sem eles, o modelo vira Big Ball of Mud.
- Anticorruption Layer permite que sistemas legados coexistam sem contaminar o domínio.
- Core Domain justifica investimento; subdomínios genéricos devem ser comprados/reusados.
- DDD é colaborativo: requer *domain practitioners* + *software practitioners* no mesmo processo.

## ⚠️ Trade-offs

- Alto custo de modelagem inicial e comunicação contínua com especialistas de domínio.
- Overkill para sistemas CRUD simples sem complexidade de negócio.
- Tático sem estratégico (ou vice-versa) gera resultados incompletos.

## 📊 Observability

- **SLIs**: bounded contexts mapeados, cobertura de tests por aggregate
- **SLOs**: invariantes de aggregate sempre válidos
- **Metrics**: event stream por domain event, error rate por bounded context

## 🔐 Security Considerations

- ACL isola e protege dados entre contextos.
- Domain events podem expor dados sensíveis — anonimização no event stream.
- Validação de autorização por contexto (multi-tenant).

## 🏗️ Usage Context

- Quando usar: domínio de negócio complexo, equipes grandes, microsserviços por bounded context, legacy com novas fronteiras.
- Quando NÃO usar: CRUD simples, protótipos, domínio sem regras de negócio complexas.
- Pré-requisitos: acesso a especialistas de domínio, cultura colaborativa.

## 📚 References

- [DDD Reference (Eric Evans)](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)
- [Domain Language — Eric Evans](https://www.domainlanguage.com/)
- [Microsoft — DDD patterns](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/ddd-oriented-microservice)
