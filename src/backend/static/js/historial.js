// MediLogic - Historial de diagnosticos de la sesion activa (seccion 4.2 del
// enunciado: "mantener un historial local temporal de diagnosticos durante
// la sesion activa en el navegador"). Se guarda en sessionStorage: nunca se
// envia al servidor y se pierde al cerrar la pestana/navegador.
(() => {
  const CLAVE = "medilogic_historial";

  function leerHistorial() {
    try {
      return JSON.parse(sessionStorage.getItem(CLAVE)) || [];
    } catch (err) {
      return [];
    }
  }

  function guardarHistorial(historial) {
    sessionStorage.setItem(CLAVE, JSON.stringify(historial));
  }

  function etiqueta(atomo) {
    if (!atomo) return "";
    return atomo
      .replace(/_/g, " ")
      .replace(/\b\w/g, (c) => c.toUpperCase());
  }

  function registrarDiagnosticoActual() {
    const nodo = document.getElementById("resultado-actual");
    if (!nodo) return;
    const datos = JSON.parse(nodo.textContent);
    if (!datos.principal) return;

    const historial = leerHistorial();
    historial.unshift({
      hora: new Date().toLocaleTimeString("es-GT", { hour: "2-digit", minute: "2-digit" }),
      principal: datos.principal,
      afinidad: datos.afinidad,
    });
    guardarHistorial(historial.slice(0, 20));
  }

  function pintarHistorial() {
    const cuerpo = document.getElementById("historial-cuerpo");
    if (!cuerpo) return;
    const historial = leerHistorial();

    if (historial.length === 0) {
      cuerpo.innerHTML =
        '<tr><td colspan="3" class="empty-state">Sin diagnósticos previos en esta sesión.</td></tr>';
      return;
    }

    cuerpo.innerHTML = historial
      .map(
        (item) =>
          `<tr><td>${item.hora}</td><td>${etiqueta(item.principal)}</td><td>${item.afinidad}%</td></tr>`
      )
      .join("");
  }

  document.addEventListener("DOMContentLoaded", () => {
    registrarDiagnosticoActual();
    pintarHistorial();
  });
})();
