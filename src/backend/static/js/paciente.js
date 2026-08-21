// MediLogic - Formulario de paciente
// Habilita/deshabilita el selector de severidad segun si el sintoma
// correspondiente esta marcado, tal como se veia en el mockup estatico
// (docs/mockups/02_paciente_formulario.html), pero ahora con comportamiento
// real en el navegador.
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".sintoma-check").forEach((checkbox) => {
    const select = document.getElementById(checkbox.dataset.target);
    if (!select) return;

    const sincronizar = () => {
      select.disabled = !checkbox.checked;
    };
    sincronizar();
    checkbox.addEventListener("change", sincronizar);
  });
});
