# Curso intensivo de Prolog — aplicado a MediLogic

Guía rápida para entender **el Prolog que realmente usa este proyecto** (no un curso
genérico de Prolog). Cada concepto se explica con código real de
`src/prolog/knowledge_base.pl`. Para practicar: instala SWI-Prolog, y desde la raíz del
repo corre `swipl src/prolog/knowledge_base.pl` — te deja en la consola `?-` con la base ya
cargada, lista para escribir las consultas de ejemplo de cada sección.

## 1. Hechos: la base de datos de Prolog

Un **hecho** afirma algo que siempre es verdadero, sin condiciones. Es la unidad más básica:

```prolog
sintoma(dolor_cabeza).
medicamento(losartan).
enfermedad(hipertension, 'Presion arterial alta...', circulatorio, cronico).
```

Cada uno es un *predicado* con un nombre y unos *argumentos* entre paréntesis
(`enfermedad/4` significa "el predicado `enfermedad` con 4 argumentos" — verás esta
notación `nombre/aridad` en todo el manual técnico). Puedes tener muchos hechos con el
mismo predicado — juntos forman una tabla, como una fila por hecho:

```prolog
enfermedad_sintoma(hipertension, dolor_cabeza).
enfermedad_sintoma(hipertension, mareo).
enfermedad_sintoma(hipertension, vision_borrosa).
```

Prueba: `?- sintoma(dolor_cabeza).` → `true.` (existe ese hecho). `?- sintoma(gripe).` →
`false.` (no existe).

## 2. Variables y consultas: hacerle preguntas a la base

Una variable empieza con **mayúscula**. Preguntar `?- enfermedad_sintoma(hipertension, S).`
le pide a Prolog: "encuentra un valor de `S` que haga verdadero este hecho". Prolog busca
entre todos los `enfermedad_sintoma(hipertension, _)` y responde uno por uno (con `;` pides
la siguiente respuesta):

```
?- enfermedad_sintoma(hipertension, S).
S = dolor_cabeza ;
S = mareo ;
S = vision_borrosa.
```

Esto es **unificación**: Prolog intenta hacer que la variable `S` "encaje" con cada hecho
que tenga esa forma. Es el mecanismo detrás de todo lo demás en este lenguaje.

## 3. Reglas: hechos condicionales (`:-`)

Una **regla** dice "esto es verdad SI esto otro también lo es". El símbolo `:-` se lee "si".
Ejemplo real, simplificado (`knowledge_base.pl`, sección 7):

```prolog
enfermedad_cronica(Nombre) :-
    enfermedad(Nombre, _Descripcion, _SistemaCuerpo, cronico).
```

Se lee: "`Nombre` es una enfermedad crónica SI existe un hecho `enfermedad(Nombre, _, _,
cronico)`". Los guiones bajos (`_Descripcion`, `_SistemaCuerpo`) son variables que no nos
importa qué valor tomen — es la forma de decir "lo que sea, no lo voy a usar". Esta regla
**deriva** un catálogo (enfermedades crónicas) a partir de otro (todas las enfermedades),
sin duplicar datos — así el administrador solo mantiene un catálogo de enfermedades, y
"cuáles son crónicas" se calcula solo.

## 4. Listas y `member/2`

Una lista se escribe entre corchetes: `[dolor_cabeza-moderado, mareo-severo]`. El `-` entre
`dolor_cabeza` y `moderado` no es resta: es el functor `-/2`, una forma común en Prolog de
empaquetar un par de valores juntos (aquí: síntoma-severidad). `member(X, Lista)` es
verdadero si `X` está en `Lista` — y, con `X` como variable, va entregando cada elemento uno
por uno (igual que unificar contra hechos, sección 2).

```prolog
puntos_enfermedad(Enfermedad, SintomasPaciente, Puntos) :-
    findall(Peso,
        ( enfermedad_sintoma(Enfermedad, Sintoma),
          member(Sintoma-Severidad, SintomasPaciente),
          peso_severidad(Severidad, Peso)
        ),
        Pesos),
    sum_list(Pesos, Puntos).
```

Esta es la regla que calcula cuántos puntos suma un paciente para una enfermedad
(`knowledge_base.pl`, sección 8). Léela como una receta paso a paso:

1. `enfermedad_sintoma(Enfermedad, Sintoma)` — recorre cada síntoma catalogado de la
   enfermedad (uno a la vez, por unificación).
2. `member(Sintoma-Severidad, SintomasPaciente)` — ¿el paciente reportó ese mismo síntoma?
   Si sí, `Severidad` queda unificada con la severidad que indicó.
3. `peso_severidad(Severidad, Peso)` — traduce esa severidad a un número (leve=1,
   moderado=2, severo=3).
4. `findall(Peso, (...), Pesos)` — repite los 3 pasos anteriores para **todas** las
   combinaciones posibles, y junta cada `Peso` obtenido en una lista `Pesos`.
5. `sum_list(Pesos, Puntos)` — suma esa lista.

`findall/3` es probablemente el predicado que más vas a usar al leer este proyecto: es el
"para cada X que cumpla esta condición, dame una lista con el resultado" de Prolog —
equivalente conceptual a un list comprehension o a un `.filter().map()`.

## 5. Aritmética: `is/2` y comparaciones

Prolog no evalúa `2 + 3` automáticamente: `X = 2 + 3` deja a `X` unificado con el *término*
`2+3`, no con `5`. Para calcular de verdad se usa `is/2`:

```prolog
Maximo is Cantidad * PesoMaximo.
Porcentaje is round((Puntos * 100) / Maximo).
```

`>`, `<`, `>=`, `=<` sí comparan valores numéricos directamente (evaluando ambos lados),
como en `nivel_urgencia/3`:

```prolog
nivel_urgencia(Porcentaje, alta, 'Consulta medica inmediata sugerida') :-
    Porcentaje >= 60.
nivel_urgencia(Porcentaje, media, 'Posible automanejo') :-
    Porcentaje >= 20, Porcentaje < 60.
```

La coma `,` entre `Porcentaje >= 20` y `Porcentaje < 60` significa **Y** (ambas condiciones
deben cumplirse). Al consultar `nivel_urgencia(56, Nivel, Recomendacion)`, Prolog prueba las
3 cláusulas de `nivel_urgencia/3` en orden y usa la primera que unifique con éxito.

## 6. Negación: `\+`

`\+ Objetivo` es verdadero si `Objetivo` **falla** (no se puede probar). Es "negación por
fallo", no negación lógica estricta: Prolog no dice "sé que esto es falso", dice "no pude
demostrar que sea verdadero". Ejemplo (`knowledge_base.pl`, sección 10):

```prolog
medicamento_seguro(Medicamento, Alergias, EnfermedadesCronicas) :-
    \+ contraindicado_por_alergia(Medicamento, Alergias),
    \+ contraindicado_por_cronica(Medicamento, EnfermedadesCronicas).
```

"Un medicamento es seguro SI NO está contraindicado por alergia Y NO está contraindicado por
una enfermedad crónica del paciente." Esta es la regla que implementa los dos niveles de
seguridad de medicamentos que pide el enunciado del proyecto.

## 7. El corte (`!`) — probablemente lo más confuso al principio

`!` le dice a Prolog "ya encontraste lo que buscabas en este punto, no sigas probando otras
alternativas". Se usa en `medicamento_sugerido/4`:

```prolog
medicamento_sugerido(Enfermedad, Alergias, EnfermedadesCronicas, Medicamento) :-
    medicamento_para(Medicamento, Enfermedad),
    \+ contraindicacion_enfermedad(Medicamento, Enfermedad),
    medicamento_seguro(Medicamento, Alergias, EnfermedadesCronicas),
    !.
```

Sin el `!`, si le pidieras a Prolog "dame otra respuesta" (con `;`), seguiría probando el
siguiente `medicamento_para(Medicamento, Enfermedad)` de la lista y te devolvería *todos*
los medicamentos seguros, uno por uno. Con `!`, en cuanto encuentra el **primer**
medicamento que pasa las dos validaciones de seguridad, se detiene ahí — que es justo el
comportamiento que se quiere: "dame el primer candidato seguro, no la lista completa de
opciones". Si ese primer candidato falla alguna validación, Prolog automáticamente
retrocede (*backtracking*) y prueba el siguiente `medicamento_para` — así es como el motor
"sustituye" un medicamento contraindicado por el siguiente disponible, sin que el código
tenga que escribir un `if/else` explícito para eso: es backtracking normal de Prolog,
cortado apenas encuentra una respuesta válida.

## 8. Ordenar resultados: `sort/4`

```prolog
sort(2, @>=, Diagnosticos, DiagnosticosOrdenados).
```

Ordena la lista `Diagnosticos` (términos `diagnostico(Enfermedad, Porcentaje)`) usando el
**2do argumento** de cada término (`Porcentaje`) como clave, de mayor a menor (`@>=`). Se
usó `sort/4` en vez de `predsort/3` deliberadamente: `@>=` conserva empates (dos
enfermedades con la misma afinidad aparecen ambas), mientras que `predsort/3` los eliminaría
por considerarlos "duplicados".

## 9. De extremo a extremo: `informe/4`

Con todo lo anterior ya puedes leer la regla más importante del archivo:

```prolog
informe(SintomasPaciente, Alergias, EnfermedadesCronicas, Informe) :-
    diagnosticar(SintomasPaciente, Diagnosticos),
    findall(
        resultado(Enfermedad, Porcentaje, Urgencia, Recomendacion, Medicamento),
        ( member(diagnostico(Enfermedad, Porcentaje), Diagnosticos),
          nivel_urgencia(Porcentaje, Urgencia, Recomendacion),
          ( medicamento_sugerido(Enfermedad, Alergias, EnfermedadesCronicas, Medicamento)
          -> true
          ; Medicamento = ninguno_disponible
          )
        ),
        Informe).
```

Traducido: "calcula todos los diagnósticos ordenados; luego, para cada uno, calcula su nivel
de urgencia y su medicamento sugerido — y si `medicamento_sugerido` no encuentra ningún
candidato seguro (falla), usa el átomo `ninguno_disponible` en su lugar". El `->` es un
if-then-else: `Condicion -> SiVerdadera ; SiFalsa`.

## 10. Cómo lo consume Python (`pyswip`)

`src/backend/prolog_engine.py` abre el motor y hace las mismas consultas que harías tú a
mano en la consola `swipl`, solo que armando el texto de la consulta con f-strings de Python:

```python
consulta = (
    f"informe({lista_sintomas}, {lista_alergias}, {lista_cronicas}, Informe), "
    "member(resultado(Enf, Pct, Urg, Rec, Med), Informe)"
)
filas = self._query(consulta)
```

Nota el `member(resultado(...), Informe)` al final: `pyswip` no reconstruye bien términos
compuestos anidados dentro de listas (los devuelve como texto), así que en vez de pedirle a
Python que interprete cada `resultado(...)` de la lista `Informe`, se le pide a **Prolog**
que los recorra uno a uno con `member/2` — cada uno llega a Python como una fila con
variables simples (átomos/números), que sí se convierten bien. Es el mismo patrón de "para
cada X, dame una fila" de `findall/3`, aplicado para cruzar la frontera Python↔Prolog.

## 11. Practica tú mismo

Con `swipl src/prolog/knowledge_base.pl` abierto, prueba en orden (son las mismas consultas
de referencia de `scripts/demo_prolog.pl`):

```prolog
?- afinidad(hipertension, [dolor_cabeza-moderado, mareo-severo], P).
?- nivel_urgencia(56, Nivel, Recomendacion).
?- medicamento_sugerido(hipertension, [losartan], [], Medicamento).
?- diagnosticar([dolor_cabeza-moderado, mareo-severo, dolor_abdominal-leve], D).
?- informe([dolor_cabeza-moderado, mareo-severo], [ibuprofeno], [], Informe).
```

Después edita un hecho (por ejemplo agrega `sintoma(tos_seca_prueba).`), guarda, y en la
misma consola corre `?- consult('src/prolog/knowledge_base.pl').` para recargar sin salir —
es exactamente lo que hace `PrologEngine.reload()` cuando el administrador guarda un cambio
desde el panel web.

## 12. Para profundizar más

Este curso cubre solo lo que usa `knowledge_base.pl`. Para ir más allá (recursión sobre
listas propias, aridad múltiple del mismo predicado, `assert`/`retract` dinámicos, DCGs,
etc.), el tutorial oficial de SWI-Prolog es la referencia más directa:
<https://www.swi-prolog.org/pldoc/man?section=quickstart>.
