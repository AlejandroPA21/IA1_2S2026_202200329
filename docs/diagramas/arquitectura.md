# Diagramas de arquitectura — MediLogic (borrador, Entrega No. 1)

## 1. Arquitectura general (cliente-servidor)

```mermaid
flowchart LR
    subgraph Cliente["Navegador (cliente)"]
        UI[Interfaz web<br/>paciente / administrador]
    end

    subgraph Servidor["Servidor Python (Flask)"]
        Rutas[Rutas / Blueprints<br/>paciente y administrador]
        Motor[prolog_engine.py<br/>puente pyswip]
        RPA[admin_rpa.py<br/>RPA - PyAutoGUI]
        PDFGen[Generador de PDF<br/>ReportLab]
    end

    subgraph Logica["Motor logico"]
        PL[(knowledge_base.pl<br/>hechos + reglas)]
        SWI[SWI-Prolog]
    end

    UI <-->|HTTP| Rutas
    Rutas --> Motor
    Motor -->|consult / query| SWI
    SWI --> PL
    Rutas --> PDFGen
    Rutas -->|alta masiva de enfermedades| RPA
    RPA -->|reescribe| PL
    RPA -->|genera| Bitacora[(Bitacora .txt)]
    Motor -->|reload tras escritura| PL
```

**Nota de arquitectura:** toda la logica de decision (calculo de afinidad, contraindicaciones,
nivel de urgencia) vive exclusivamente en `knowledge_base.pl`. Python nunca reimplementa esa
logica: solo la invoca via `pyswip` y transforma el resultado para la interfaz web, cumpliendo
el requisito de la seccion 4.3 ("la logica de Prolog exclusivamente debe ser en Python" se
interpreta, y se documenta en `docs/decisiones_tecnicas.md`, como *"la unica logica de negocio
vive en Prolog; Python actua solo como puente/orquestador"*).

## 2. Flujo de un diagnostico (paciente)

```mermaid
sequenceDiagram
    participant P as Paciente (navegador)
    participant F as Flask (rutas paciente)
    participant E as prolog_engine.py
    participant PL as knowledge_base.pl

    P->>F: Envia sintomas+severidad, alergias, cronicas
    F->>E: informe(Sintomas, Alergias, Cronicas, Informe)
    E->>PL: query informe/4
    PL-->>E: lista resultado(Enfermedad, %, Urgencia, Recomendacion, Medicamento)
    E-->>F: Informe (estructura Python)
    F-->>P: Render de informe + opcion de descarga PDF
```

## 3. Flujo de actualizacion administrativa (incluye RPA)

```mermaid
sequenceDiagram
    participant A as Administrador
    participant F as Flask (rutas admin)
    participant RPA as admin_rpa.py
    participant PL as knowledge_base.pl
    participant E as prolog_engine.py

    A->>F: Sube archivo JSON de enfermedades
    F->>RPA: Ejecuta carga automatizada
    RPA->>RPA: Clasifica cada enfermedad (sistema del cuerpo / tipo)
    RPA->>PL: Reescribe hechos (enfermedad/4, enfermedad_sintoma/2, ...)
    RPA->>E: Solicita reload()
    E->>PL: consult/1 (recarga en caliente)
    RPA-->>A: Genera bitacora en texto plano
```

Ver también [docs/mockups/README.md](../mockups/README.md) para el diagrama de navegación
entre pantallas.

---
*Diagramas en borrador para la Entrega No. 1. Se ampliarán (diagrama de clases/módulos del
backend, diagrama entidad-relación del archivo .pl) para el Manual Técnico final.*
