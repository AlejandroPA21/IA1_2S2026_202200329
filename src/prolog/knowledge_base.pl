% =============================================================================
% MediLogic - Base de conocimiento en Prolog
% =============================================================================
% Contiene los hechos y reglas del motor de diagnostico preliminar. Se carga
% mediante consult/1 desde src/backend/prolog_engine.py (pyswip) y se vuelve a
% cargar cada vez que el administrador modifica un registro (seccion 4.2 del
% enunciado: actualizacion dinamica del archivo .pl).
%
% Representacion de la entrada del paciente usada por las reglas de este
% archivo:
%   SintomasPaciente     -> lista de pares Sintoma-Severidad,
%                            ej. [dolor_cabeza-moderado, mareo-severo]
%   Alergias              -> lista de atomos de medicamentos,
%                            ej. [ibuprofeno]
%   EnfermedadesCronicas  -> lista de atomos de enfermedades preexistentes,
%                            ej. [hipertension]
%
% Este es un entregable inicial (Entrega No. 1 - Tarea 1): incluye hechos
% basicos y reglas ya funcionales para las 4 enfermedades de ejemplo de
% EjemploRPA.json. El catalogo completo, el CRUD administrativo y las
% pruebas exhaustivas se amplian en la Entrega No. 2.
% =============================================================================


% =============================================================================
% 1. CATALOGO DE SINTOMAS (hechos)
% =============================================================================

sintoma(dolor_cabeza).
sintoma(mareo).
sintoma(vision_borrosa).
sintoma(dificultad_respiratoria).
sintoma(silbido_pecho).
sintoma(tos_seca).
sintoma(sed_excesiva).
sintoma(fatiga).
sintoma(dolor_abdominal).
sintoma(nauseas).
sintoma(diarrea).
sintoma(fiebre_leve).


% =============================================================================
% 2. CATALOGO DE MEDICAMENTOS (hechos)
% =============================================================================
% Un solo catalogo de medicamentos: sirve tanto para sugerir tratamientos
% como para poblar dinamicamente el checklist de alergias del paciente (ver
% alergia/1 en la seccion 7), tal como pide la seccion 4.2 del enunciado
% ("este catalogo debe cargarse de forma dinamica consultando los
% medicamentos registrados previamente por el administrador").

medicamento(losartan).
medicamento(enalapril).
medicamento(salbutamol).
medicamento(metformina).
medicamento(suero_oral).
medicamento(loperamida).
medicamento(ibuprofeno).
medicamento(aspirina).
medicamento(corticosteroides).
medicamento(descongestivos).
medicamento(betabloqueantes).
medicamento(anti_inflamatorios_no_esteroideos).


% =============================================================================
% 3. ENFERMEDADES (hechos)
% =============================================================================
% enfermedad(Nombre, Descripcion, SistemaCuerpo, Tipo)
% Datos de ejemplo tomados de EjemploRPA.json.

enfermedad(hipertension,
    'Presion arterial alta cronica que afecta el sistema circulatorio.',
    circulatorio, cronico).

enfermedad(asma_bronquial,
    'Enfermedad respiratoria cronica caracterizada por la inflamacion de las vias aereas.',
    respiratorio, cronico).

enfermedad(diabetes_tipo_2,
    'Trastorno metabolico caracterizado por niveles elevados de glucosa en sangre.',
    endocrino, cronico).

enfermedad(gastroenteritis_aguda,
    'Inflamacion de la membrana interna del intestino causada por infecciones.',
    digestivo, viral).


% =============================================================================
% 4. RELACION ENFERMEDAD - SINTOMA (hechos)
% =============================================================================

enfermedad_sintoma(hipertension, dolor_cabeza).
enfermedad_sintoma(hipertension, mareo).
enfermedad_sintoma(hipertension, vision_borrosa).

enfermedad_sintoma(asma_bronquial, dificultad_respiratoria).
enfermedad_sintoma(asma_bronquial, silbido_pecho).
enfermedad_sintoma(asma_bronquial, tos_seca).

enfermedad_sintoma(diabetes_tipo_2, sed_excesiva).
enfermedad_sintoma(diabetes_tipo_2, fatiga).
enfermedad_sintoma(diabetes_tipo_2, vision_borrosa).

enfermedad_sintoma(gastroenteritis_aguda, dolor_abdominal).
enfermedad_sintoma(gastroenteritis_aguda, nauseas).
enfermedad_sintoma(gastroenteritis_aguda, diarrea).
enfermedad_sintoma(gastroenteritis_aguda, fiebre_leve).


% =============================================================================
% 5. RELACION ENFERMEDAD - MEDICAMENTO QUE LA TRATA (hechos)
% =============================================================================
% medicamento_para(Medicamento, Enfermedad). Puede haber mas de un
% medicamento por enfermedad: si el primero resulta contraindicado, la regla
% medicamento_sugerido/4 (seccion 9) prueba el siguiente automaticamente.

medicamento_para(losartan, hipertension).
medicamento_para(enalapril, hipertension).

medicamento_para(salbutamol, asma_bronquial).

medicamento_para(metformina, diabetes_tipo_2).

medicamento_para(suero_oral, gastroenteritis_aguda).
medicamento_para(loperamida, gastroenteritis_aguda).


% =============================================================================
% 6. CONTRAINDICACIONES FARMACO <-> PATOLOGIA (hechos)
% =============================================================================
% contraindicacion_enfermedad(Medicamento, Enfermedad).
% Esta unica relacion cubre los DOS niveles de contraindicacion exigidos en
% la seccion 4.2 del enunciado:
%   - Nivel "farmaco-patologia": se usa contra la enfermedad que se esta
%     diagnosticando (ver medicamento_sugerido/4).
%   - Nivel "condiciones del paciente": se usa contra cada enfermedad
%     cronica que el paciente marco como antecedente (ver
%     contraindicado_por_cronica/2), reutilizando los mismos hechos porque
%     una enfermedad cronica del paciente es, precisamente, una enfermedad
%     de este mismo catalogo (seccion 3).

contraindicacion_enfermedad(ibuprofeno, hipertension).
contraindicacion_enfermedad(descongestivos, hipertension).

contraindicacion_enfermedad(aspirina, asma_bronquial).
contraindicacion_enfermedad(betabloqueantes, asma_bronquial).

contraindicacion_enfermedad(corticosteroides, diabetes_tipo_2).

contraindicacion_enfermedad(anti_inflamatorios_no_esteroideos, gastroenteritis_aguda).


% =============================================================================
% 7. CATALOGOS DERIVADOS (reglas)
% =============================================================================

% alergia(-Medicamento)
% El catalogo de alergias que se le muestra al paciente es, por definicion,
% el catalogo completo de medicamentos registrados (cualquier medicamento se
% puede marcar como alergia).
alergia(Medicamento) :-
    medicamento(Medicamento).

% enfermedad_cronica(-Nombre)
% El catalogo de antecedentes cronicos que se le muestra al paciente se
% deriva de las enfermedades ya clasificadas por el administrador como tipo
% "cronico", evitando mantener una lista duplicada.
enfermedad_cronica(Nombre) :-
    enfermedad(Nombre, _Descripcion, _SistemaCuerpo, cronico).


% =============================================================================
% 8. PONDERACION DE SEVERIDAD Y CALCULO DE AFINIDAD (hechos + reglas)
% =============================================================================
% Criterio estandar de la seccion 4.2 del enunciado.

peso_severidad(leve, 1).
peso_severidad(moderado, 2).
peso_severidad(severo, 3).

% puntos_enfermedad(+Enfermedad, +SintomasPaciente, -Puntos)
% Suma la ponderacion de severidad de los sintomas del paciente que SI
% pertenecen al conjunto de sintomas definidos para la enfermedad evaluada.
puntos_enfermedad(Enfermedad, SintomasPaciente, Puntos) :-
    findall(Peso,
        ( enfermedad_sintoma(Enfermedad, Sintoma),
          member(Sintoma-Severidad, SintomasPaciente),
          peso_severidad(Severidad, Peso)
        ),
        Pesos),
    sum_list(Pesos, Puntos).

% puntos_maximos_enfermedad(+Enfermedad, -Maximo)
% Total maximo posible para la enfermedad: el escenario en el que el
% paciente presentara TODOS los sintomas definidos para esa enfermedad en su
% grado mas severo (peso 3 cada uno). Es el criterio que da sentido a la
% "proporcion entre puntos acumulados y total maximo posible" que pide el
% enunciado.
puntos_maximos_enfermedad(Enfermedad, Maximo) :-
    findall(Sintoma, enfermedad_sintoma(Enfermedad, Sintoma), Sintomas),
    length(Sintomas, Cantidad),
    peso_severidad(severo, PesoMaximo),
    Maximo is Cantidad * PesoMaximo.

% afinidad(+Enfermedad, +SintomasPaciente, -Porcentaje)
% Solo tiene exito si el paciente coincide con al menos un sintoma de la
% enfermedad (Puntos > 0); de lo contrario esa enfermedad no debe aparecer
% en el informe.
afinidad(Enfermedad, SintomasPaciente, Porcentaje) :-
    puntos_enfermedad(Enfermedad, SintomasPaciente, Puntos),
    Puntos > 0,
    puntos_maximos_enfermedad(Enfermedad, Maximo),
    Maximo > 0,
    Porcentaje is round((Puntos * 100) / Maximo).


% =============================================================================
% 9. NIVEL DE URGENCIA (reglas)
% =============================================================================
% nivel_urgencia(+Porcentaje, -Nivel, -Recomendacion)
% Umbrales definidos como criterio propio del proyecto (documentados en
% docs/decisiones_tecnicas.md): >=60% urgencia alta, 20-59% media, <20% baja.

nivel_urgencia(Porcentaje, alta, 'Consulta medica inmediata sugerida') :-
    Porcentaje >= 60.
nivel_urgencia(Porcentaje, media, 'Posible automanejo') :-
    Porcentaje >= 20, Porcentaje < 60.
nivel_urgencia(Porcentaje, baja, 'Observacion recomendada') :-
    Porcentaje < 20.


% =============================================================================
% 10. SEGURIDAD DE MEDICAMENTOS (reglas)
% =============================================================================

% contraindicado_por_alergia(+Medicamento, +Alergias)
contraindicado_por_alergia(Medicamento, Alergias) :-
    member(Medicamento, Alergias).

% contraindicado_por_cronica(+Medicamento, +EnfermedadesCronicas)
contraindicado_por_cronica(Medicamento, EnfermedadesCronicas) :-
    member(Cronica, EnfermedadesCronicas),
    contraindicacion_enfermedad(Medicamento, Cronica).

% medicamento_seguro(+Medicamento, +Alergias, +EnfermedadesCronicas)
% Un medicamento es seguro si no cae en ninguno de los dos niveles de
% contraindicacion del paciente (alergia directa o enfermedad cronica).
medicamento_seguro(Medicamento, Alergias, EnfermedadesCronicas) :-
    \+ contraindicado_por_alergia(Medicamento, Alergias),
    \+ contraindicado_por_cronica(Medicamento, EnfermedadesCronicas).

% medicamento_sugerido(+Enfermedad, +Alergias, +EnfermedadesCronicas, -Medicamento)
% Recorre los medicamentos registrados para la enfermedad diagnosticada, en
% orden, y devuelve el PRIMERO que sea seguro: no contraindicado contra la
% enfermedad que se esta tratando (nivel farmaco-patologia) ni contra las
% alergias/cronicas del paciente (nivel condiciones del paciente). Si el
% primer candidato esta contraindicado, prueba automaticamente el siguiente
% (seccion 4.2: "sugiriendo otro posible medicamento con el mismo fin").
medicamento_sugerido(Enfermedad, Alergias, EnfermedadesCronicas, Medicamento) :-
    medicamento_para(Medicamento, Enfermedad),
    \+ contraindicacion_enfermedad(Medicamento, Enfermedad),
    medicamento_seguro(Medicamento, Alergias, EnfermedadesCronicas),
    !.


% =============================================================================
% 11. DIAGNOSTICO E INFORME COMPLETO (reglas)
% =============================================================================

% diagnosticar(+SintomasPaciente, -Diagnosticos)
% Diagnosticos: lista de terminos diagnostico(Enfermedad, Porcentaje) para
% toda enfermedad con al menos un sintoma coincidente, ordenada de mayor a
% menor afinidad (seccion 4.2: "deberan ordenarse por porcentaje de
% coincidencia"). Se usa sort/4 con clave en el 2do argumento y orden @>=
% para ordenar de forma descendente SIN perder enfermedades que empaten en
% porcentaje (@>= conserva duplicados; @> los eliminaria).
diagnosticar(SintomasPaciente, DiagnosticosOrdenados) :-
    findall(diagnostico(Enfermedad, Porcentaje),
        ( enfermedad(Enfermedad, _, _, _),
          afinidad(Enfermedad, SintomasPaciente, Porcentaje)
        ),
        Diagnosticos),
    sort(2, @>=, Diagnosticos, DiagnosticosOrdenados).

% informe(+SintomasPaciente, +Alergias, +EnfermedadesCronicas, -Informe)
% Junta afinidad + urgencia + medicamento seguro para cada enfermedad
% coincidente, en el formato final que consumira la capa web:
%   resultado(Enfermedad, Porcentaje, Urgencia, Recomendacion, Medicamento)
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


% =============================================================================
% 12. EJEMPLOS DE CONSULTA (queries de referencia, ver Manual Tecnico / PDF
%     de evidencia para el detalle y la salida esperada de cada una)
% =============================================================================
% ?- afinidad(hipertension, [dolor_cabeza-moderado, mareo-severo], P).
% ?- nivel_urgencia(56, Nivel, Recomendacion).
% ?- medicamento_sugerido(hipertension, [ibuprofeno], [], Medicamento).
% ?- diagnosticar([dolor_cabeza-moderado, mareo-severo, dolor_abdominal-leve], D).
% ?- informe([dolor_cabeza-moderado, mareo-severo], [ibuprofeno], [], Informe).
% =============================================================================
