document.addEventListener('DOMContentLoaded', () => {
  const steps = Array.from(document.querySelectorAll('.wizard-step'));
  const stepList = document.getElementById('stepList');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const resetBtn = document.getElementById('resetBtn');
  const finishBtn = document.getElementById('finishBtn');
  const wizardForm = document.getElementById('wizardForm');
  const progressBar = document.getElementById('wizardProgressBar');
  let currentStep = 0;

  if (!steps.length || !stepList) {
    return;
  }

  function buildStepper() {
    stepList.innerHTML = '';
    steps.forEach((step, index) => {
      const item = document.createElement('div');
      item.className = 'd-flex align-items-center gap-2 text-nowrap';
      item.innerHTML = `<span class="step-pill">${index + 1}</span><span class="small text-muted">Etapa ${index + 1}</span>`;
      item.dataset.step = String(index);
      stepList.appendChild(item);
    });
  }

  function updateProgress() {
    if (!progressBar) {
      return;
    }
    const total = steps.length;
    const percent = total ? ((currentStep + 1) / total) * 100 : 0;
    progressBar.style.width = `${percent}%`;
    progressBar.setAttribute('aria-valuenow', String(Math.round(percent)));
    progressBar.textContent = `${Math.round(percent)}%`;
  }

  function syncStepper() {
    steps.forEach((step, index) => step.classList.toggle('active', index === currentStep));
    const items = Array.from(stepList.querySelectorAll('.step-pill'));
    items.forEach((pill, index) => {
      pill.classList.toggle('active', index === currentStep);
      pill.classList.toggle('done', index < currentStep);
    });

    if (prevBtn) {
      prevBtn.disabled = currentStep === 0;
    }
    if (nextBtn) {
      nextBtn.style.display = currentStep === steps.length - 1 ? 'none' : 'inline-flex';
    }
    if (finishBtn) {
      finishBtn.style.display = currentStep === steps.length - 1 ? 'inline-flex' : 'none';
    }

    updateProgress();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function goToStep(nextIndex) {
    if (nextIndex < 0 || nextIndex >= steps.length) {
      return;
    }
    currentStep = nextIndex;
    syncStepper();
  }

  if (prevBtn) prevBtn.addEventListener('click', () => goToStep(currentStep - 1));
  if (nextBtn) nextBtn.addEventListener('click', () => goToStep(currentStep + 1));
  if (resetBtn) resetBtn.addEventListener('click', () => wizardForm && wizardForm.reset());
  if (finishBtn && wizardForm) {
    finishBtn.addEventListener('click', () => wizardForm.requestSubmit());
  }

  function addPescadoRow() {
    const template = document.getElementById('pescadoRowTemplate');
    const body = document.getElementById('pescadoTableBody');
    if (!template || !body) {
      return;
    }
    body.appendChild(template.content.cloneNode(true));
    bindRemoveRowButtons();
  }

  function addDespesaRow(defaultName = '') {
    const template = document.getElementById('despesasRowTemplate');
    const body = document.getElementById('despesasTableBody');
    if (!template || !body) {
      return;
    }
    const fragment = template.content.cloneNode(true);
    const row = fragment.querySelector('tr');
    if (defaultName && row) {
      const input = row.querySelector('input[name="despesa_nome[]"]');
      if (input) {
        input.value = defaultName;
      }
    }
    body.appendChild(fragment);
    bindRemoveRowButtons();
  }

  function bindRemoveRowButtons() {
    document.querySelectorAll('.remove-row').forEach((btn) => {
      btn.onclick = () => btn.closest('tr')?.remove();
    });
  }

  const addPescadoRowBtn = document.getElementById('addPescadoRow');
  if (addPescadoRowBtn) {
    addPescadoRowBtn.addEventListener('click', addPescadoRow);
  }

  ['combustível', 'lubrificante', 'gelo', 'rancho', 'pagamento pescador', 'manutenção rede', 'manutenção barco', 'outros']
    .forEach((name) => addDespesaRow(name));

  const possuiCarteiraSelect = document.getElementById('possuiCarteiraSelect');
  if (possuiCarteiraSelect) {
    possuiCarteiraSelect.addEventListener('change', (event) => {
      const value = event.target.value;
      const grande = document.getElementById('carteiraGrandeWrap');
      const pequena = document.getElementById('carteiraPequenaWrap');
      if (grande) grande.style.display = value === 'sim' ? '' : 'none';
      if (pequena) pequena.style.display = value === 'sim' ? '' : 'none';
    });
  }

  const moradiaTipoSelect = document.getElementById('moradiaTipoSelect');
  if (moradiaTipoSelect) {
    moradiaTipoSelect.addEventListener('change', (event) => {
      const wrap = document.getElementById('moradiaOutroWrap');
      if (wrap) {
        wrap.style.display = event.target.value === 'outro' ? '' : 'none';
      }
    });
  }

  const tipoConstrucaoSelect = document.getElementById('tipoConstrucaoSelect');
  if (tipoConstrucaoSelect) {
    tipoConstrucaoSelect.addEventListener('change', (event) => {
      const wrap = document.getElementById('tipoConstrucaoOutroWrap');
      if (wrap) {
        wrap.style.display = event.target.value === 'outro' ? '' : 'none';
      }
    });
  }

  const registroColoniaInput = document.getElementById('registroColoniaInput');
  if (registroColoniaInput) {
    registroColoniaInput.addEventListener('input', (event) => {
      const wrap = document.getElementById('qualColoniaWrap');
      if (wrap) {
        wrap.style.display = event.target.value.trim() ? '' : 'none';
      }
    });
  }

  const registroAssociacaoInput = document.getElementById('registroAssociacaoInput');
  if (registroAssociacaoInput) {
    registroAssociacaoInput.addEventListener('input', (event) => {
      const wrap = document.getElementById('qualAssociacaoWrap');
      if (wrap) {
        wrap.style.display = event.target.value.trim() ? '' : 'none';
      }
    });
  }

  const saudeOutrosCheck = document.getElementById('saudeOutrosCheck');
  if (saudeOutrosCheck) {
    saudeOutrosCheck.addEventListener('change', (event) => {
      const wrap = document.getElementById('saudeOutrosWrap');
      if (wrap) {
        wrap.style.display = event.target.checked ? '' : 'none';
      }
    });
  }

  document.querySelectorAll('.health-check').forEach((checkbox) => {
    checkbox.addEventListener('change', () => {
      // Campos dinâmicos ligados aos itens da seção Saúde.
      // Futuras validações e regras de persistência podem ser adicionadas aqui.
    });
  });

  buildStepper();
  syncStepper();
  bindRemoveRowButtons();
});
