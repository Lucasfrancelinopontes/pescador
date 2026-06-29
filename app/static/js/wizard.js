document.addEventListener('DOMContentLoaded', () => {
  const steps = Array.from(document.querySelectorAll('.wizard-step'));
  const stepList = document.getElementById('stepList');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const resetBtn = document.getElementById('resetBtn');
  const finishBtn = document.getElementById('finishBtn');
  const wizardForm = document.getElementById('wizardForm');
  const progressBar = document.getElementById('wizardProgressBar');
  const codigoColetaHidden = document.getElementById('codigoColetaHidden');
  const codigoColetaParts = Array.from(document.querySelectorAll('.codigo-coleta-part'));
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

    if (prevBtn) prevBtn.disabled = currentStep === 0;
    if (nextBtn) nextBtn.style.display = currentStep === steps.length - 1 ? 'none' : 'inline-flex';
    if (finishBtn) finishBtn.style.display = currentStep === steps.length - 1 ? 'inline-flex' : 'none';

    updateProgress();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function goToStep(nextIndex) {
    if (nextIndex < 0 || nextIndex >= steps.length) return;
    currentStep = nextIndex;
    syncStepper();
  }

  if (prevBtn) prevBtn.addEventListener('click', () => goToStep(currentStep - 1));
  if (nextBtn) nextBtn.addEventListener('click', () => goToStep(currentStep + 1));
  if (resetBtn) resetBtn.addEventListener('click', () => wizardForm && wizardForm.reset());
  if (finishBtn && wizardForm) finishBtn.addEventListener('click', () => wizardForm.requestSubmit());

  function syncCodigoColeta() {
    if (!codigoColetaHidden || !codigoColetaParts.length) {
      return;
    }
    codigoColetaHidden.value = codigoColetaParts.map((input) => input.value.trim()).join('');
  }

  codigoColetaParts.forEach((input, index) => {
    input.addEventListener('input', (event) => {
      const value = event.target.value.replace(/\s+/g, '').slice(0, 1);
      event.target.value = value;
      if (value && index < codigoColetaParts.length - 1) {
        codigoColetaParts[index + 1].focus();
      }
      syncCodigoColeta();
    });
    input.addEventListener('keydown', (event) => {
      if (event.key === 'Backspace' && !input.value && index > 0) {
        codigoColetaParts[index - 1].focus();
      }
    });
  });

  if (wizardForm) {
    wizardForm.addEventListener('submit', syncCodigoColeta);
  }

  function addPescadoRow() {
    const template = document.getElementById('pescadoRowTemplate');
    const body = document.getElementById('pescadoTableBody');
    if (!template || !body) return;
    const fragment = template.content.cloneNode(true);
    const row = fragment.querySelector('tr');
    body.appendChild(fragment);
    if (row) bindEspeciesAutocomplete(body.lastElementChild);
    bindRemoveRowButtons();
  }

  function addDespesaRow(defaultName = '') {
    const template = document.getElementById('despesasRowTemplate');
    const body = document.getElementById('despesasTableBody');
    if (!template || !body) return;
    const fragment = template.content.cloneNode(true);
    const row = fragment.querySelector('tr');
    if (defaultName && row) {
      const input = row.querySelector('input[name="despesa_nome[]"]');
      if (input) input.value = defaultName;
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
  if (addPescadoRowBtn) addPescadoRowBtn.addEventListener('click', addPescadoRow);

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
      if (wrap) wrap.style.display = event.target.value === 'outro' ? '' : 'none';
    });
  }

  const tipoConstrucaoSelect = document.getElementById('tipoConstrucaoSelect');
  if (tipoConstrucaoSelect) {
    tipoConstrucaoSelect.addEventListener('change', (event) => {
      const wrap = document.getElementById('tipoConstrucaoOutroWrap');
      if (wrap) wrap.style.display = event.target.value === 'outro' ? '' : 'none';
    });
  }

  const registroColoniaSelect = document.getElementById('registroColoniaSelect');
  if (registroColoniaSelect) {
    registroColoniaSelect.addEventListener('change', (event) => {
      const wrap = document.getElementById('qualColoniaWrap');
      if (wrap) wrap.style.display = event.target.value === 'sim' ? '' : 'none';
    });
  }

  const registroAssociacaoSelect = document.getElementById('registroAssociacaoSelect');
  if (registroAssociacaoSelect) {
    registroAssociacaoSelect.addEventListener('change', (event) => {
      const wrap = document.getElementById('qualAssociacaoWrap');
      if (wrap) wrap.style.display = event.target.value === 'sim' ? '' : 'none';
    });
  }

  const saudeOutrosCheck = document.getElementById('saudeOutrosCheck');
  if (saudeOutrosCheck) {
    saudeOutrosCheck.addEventListener('change', (event) => {
      const wrap = document.getElementById('saudeOutrosWrap');
      if (wrap) wrap.style.display = event.target.checked ? '' : 'none';
    });
  }

  document.querySelectorAll('.health-check').forEach((checkbox) => {
    checkbox.addEventListener('change', () => {
      // Campos dinâmicos ligados aos itens da seção Saúde.
      // Futuras validações e regras de persistência podem ser adicionadas aqui.
    });
  });

  // ── Autocomplete de espécies na tabela de pescado ────────────────────────
  let especiesCache = null;   // null = não carregado ainda, [] = carregado vazio
  let especiesLoading = false;

  function loadAllEspecies() {
    if (especiesCache !== null || especiesLoading) return Promise.resolve(especiesCache || []);
    especiesLoading = true;
    return fetch('/especies?q=', { credentials: 'same-origin' })
      .then(res => res.ok ? res.json() : [])
      .catch(() => [])
      .then(data => { especiesCache = data; especiesLoading = false; return data; });
  }

  function filterEspecies(items, q) {
    if (!q) return items;
    const lower = q.toLowerCase();
    const asNum = parseInt(q, 10);
    return items.filter(item =>
      (!isNaN(asNum) && item.id === asNum) ||
      (item.nome_comum && item.nome_comum.toLowerCase().includes(lower)) ||
      (item.nome_cientifico && item.nome_cientifico.toLowerCase().includes(lower))
    );
  }

  function bindEspeciesAutocomplete(row) {
    const idInput  = row.querySelector('.pescado-id-input');
    const nomeInput = row.querySelector('.pescado-nome-input');
    const list     = row.querySelector('.autocomplete-list');
    if (!idInput || !nomeInput || !list) return;

    let highlighted = -1;
    let debounceTimer = null;

    function renderList(items) {
      list.innerHTML = '';
      highlighted = -1;

      if (!items.length) {
        const li = document.createElement('li');
        li.className = 'px-3 py-2 text-muted';
        li.style.fontSize = '0.82rem';
        li.textContent = 'Nenhuma espécie encontrada';
        list.appendChild(li);
        list.style.display = 'block';
        return;
      }

      items.forEach((item, idx) => {
        const li = document.createElement('li');
        li.className = 'autocomplete-item px-3 py-1';
        li.dataset.idx = idx;
        li.innerHTML =
          `<span class="autocomplete-id">#${item.id}</span> ` +
          `<span class="autocomplete-nome">${item.nome_comum}</span>` +
          (item.nome_cientifico
            ? ` <em class="autocomplete-cientifico">${item.nome_cientifico}</em>`
            : '');
        li.addEventListener('mousedown', (e) => {
          e.preventDefault();
          selectItem(item);
        });
        list.appendChild(li);
      });
      list.style.display = 'block';
    }

    function selectItem(item) {
      idInput.value   = item.id;
      nomeInput.value = item.nome_comum;
      list.style.display = 'none';
      highlighted = -1;
    }

    function openDropdown() {
      loadAllEspecies().then(all => {
        const q = idInput.value.trim();
        renderList(filterEspecies(all, q));
      });
    }

    idInput.addEventListener('focus', openDropdown);

    idInput.addEventListener('input', () => {
      clearTimeout(debounceTimer);
      if (!idInput.value.trim()) nomeInput.value = '';
      debounceTimer = setTimeout(() => {
        if (especiesCache !== null) {
          renderList(filterEspecies(especiesCache, idInput.value.trim()));
        } else {
          openDropdown();
        }
      }, 150);
    });

    idInput.addEventListener('keydown', (e) => {
      const items = list.querySelectorAll('.autocomplete-item');
      if (!items.length || list.style.display === 'none') return;
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        highlighted = Math.min(highlighted + 1, items.length - 1);
        items.forEach((el, i) => el.classList.toggle('autocomplete-item--active', i === highlighted));
        items[highlighted]?.scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        highlighted = Math.max(highlighted - 1, 0);
        items.forEach((el, i) => el.classList.toggle('autocomplete-item--active', i === highlighted));
        items[highlighted]?.scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'Enter' && highlighted >= 0) {
        e.preventDefault();
        items[highlighted].dispatchEvent(new MouseEvent('mousedown'));
      } else if (e.key === 'Escape') {
        list.style.display = 'none';
      }
    });

    idInput.addEventListener('blur', () => {
      setTimeout(() => { list.style.display = 'none'; highlighted = -1; }, 200);
    });
  }

  // ─────────────────────────────────────────────────────────────────────────

  buildStepper();
  syncStepper();
  syncCodigoColeta();
  bindRemoveRowButtons();
});