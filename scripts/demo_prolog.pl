% =============================================================================
% MediLogic - Demostracion de consultas sobre knowledge_base.pl
% =============================================================================
% Uso (desde la raiz del repositorio):
%   swipl scripts/demo_prolog.pl
%
% Imprime, una por una, las 5 consultas de referencia documentadas en
% docs/manual_tecnico/borrador_manual_tecnico.md (seccion 5), con una breve
% explicacion antes de cada resultado. Pensado para capturarse con CodeSnap
% (o cualquier herramienta de captura) para el informe en PDF.
% =============================================================================

:- prolog_load_context(directory, ScriptDir),
   directory_file_path(ScriptDir, '../src/prolog/knowledge_base.pl', KBPath),
   consult(KBPath).

demo :-
    format("~n~`=t~60|~n"),
    format("Consulta 1: afinidad/3~n"),
    format("~`=t~60|~n"),
    format("Paciente con dolor_cabeza-moderado y mareo-severo.~n"),
    format("Se espera el porcentaje de afinidad con hipertension.~n~n"),
    afinidad(hipertension, [dolor_cabeza-moderado, mareo-severo], P1),
    format("?- afinidad(hipertension, [dolor_cabeza-moderado, mareo-severo], P).~n"),
    format("P = ~w.~n", [P1]),

    format("~n~`=t~60|~n"),
    format("Consulta 2: nivel_urgencia/3~n"),
    format("~`=t~60|~n"),
    format("Se traduce el ~w% de afinidad anterior a un nivel de urgencia.~n~n", [P1]),
    nivel_urgencia(P1, Nivel, Recomendacion),
    format("?- nivel_urgencia(~w, Nivel, Recomendacion).~n", [P1]),
    format("Nivel = ~w, Recomendacion = '~w'.~n", [Nivel, Recomendacion]),

    format("~n~`=t~60|~n"),
    format("Consulta 3: medicamento_sugerido/4 (sustitucion por alergia)~n"),
    format("~`=t~60|~n"),
    format("El paciente es alergico a losartan (primera opcion para hipertension);~n"),
    format("se espera que el motor sugiera automaticamente el siguiente candidato seguro.~n~n"),
    medicamento_sugerido(hipertension, [losartan], [], Med),
    format("?- medicamento_sugerido(hipertension, [losartan], [], Medicamento).~n"),
    format("Medicamento = ~w.~n", [Med]),

    format("~n~`=t~60|~n"),
    format("Consulta 4: diagnosticar/2 (varias enfermedades, ordenadas)~n"),
    format("~`=t~60|~n"),
    format("Paciente con sintomas de mas de una enfermedad; se espera la lista~n"),
    format("ordenada de mayor a menor afinidad.~n~n"),
    diagnosticar([dolor_cabeza-moderado, mareo-severo, dolor_abdominal-leve], Diags),
    format("?- diagnosticar([dolor_cabeza-moderado, mareo-severo, dolor_abdominal-leve], D).~n"),
    format("D = ~w.~n", [Diags]),

    format("~n~`=t~60|~n"),
    format("Consulta 5: informe/4 (consulta integral)~n"),
    format("~`=t~60|~n"),
    format("Junta afinidad + urgencia + medicamento seguro para un paciente~n"),
    format("alergico a ibuprofeno.~n~n"),
    informe([dolor_cabeza-moderado, mareo-severo], [ibuprofeno], [], Informe),
    format("?- informe([dolor_cabeza-moderado, mareo-severo], [ibuprofeno], [], Informe).~n"),
    forall(member(R, Informe), format("  ~w~n", [R])),
    format("~n~`=t~60|~n").

:- initialization(demo, main).
