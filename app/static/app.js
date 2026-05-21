const tabs = document.querySelectorAll('.tab');
const tabContents = document.querySelectorAll('.tab-content');
const stepForm = document.querySelector('#step-form');
const stepNameInput = document.querySelector('#step-name');
const startsLeftInput = document.querySelector('#starts-left');
const isCompositeInput = document.querySelector('#is-composite');
const componentsBuilder = document.querySelector('#components-builder');
const componentStepSelect = document.querySelector('#component-step-select');
const addComponentBtn = document.querySelector('#add-component-btn');
const selectedComponentsList = document.querySelector('#selected-components-list');
const stepsList = document.querySelector('#steps-list');
const leftList = document.querySelector('#left-list');
const rightList = document.querySelector('#right-list');
const generateBtn = document.querySelector('#generate-btn');
const pairsList = document.querySelector('#pairs-list');
const leftoversList = document.querySelector('#leftovers-list');

let cachedSteps = [];
let selectedComponentIds = [];

const notify = (message) => {
  window.alert(message);
};

const renderList = (element, items, emptyMessage) => {
  element.innerHTML = '';
  if (!items.length) {
    const li = document.createElement('li');
    li.textContent = emptyMessage;
    element.appendChild(li);
    return;
  }
  items.forEach((item) => {
    const li = document.createElement('li');
    li.textContent = item;
    element.appendChild(li);
  });
};

const fetchSteps = async () => {
  const response = await fetch('/api/steps');
  cachedSteps = await response.json();

  const all = cachedSteps.map((step) => {
    if (!step.is_composite) {
      return `${step.name} (${step.starts_with_left_free ? 'esquerda livre' : 'direita livre'})`;
    }
    const decomposition = step.components.map((component) => component.name).join(' -> ');
    return `${step.name} [composto: ${decomposition}] (${step.starts_with_left_free ? 'esquerda livre' : 'direita livre'})`;
  });
  const left = cachedSteps.filter((step) => step.starts_with_left_free).map((step) => step.name);
  const right = cachedSteps.filter((step) => !step.starts_with_left_free).map((step) => step.name);

  renderList(stepsList, all, 'Nenhum passo cadastrado');
  renderList(leftList, left, 'Nenhum passo com esquerda livre');
  renderList(rightList, right, 'Nenhum passo com direita livre');
  renderComponentOptions();
};

const renderComponentOptions = () => {
  componentStepSelect.innerHTML = '';
  cachedSteps.forEach((step) => {
    const option = document.createElement('option');
    option.value = step.id;
    option.textContent = `${step.name} (${step.starts_with_left_free ? 'esquerda livre' : 'direita livre'})`;
    componentStepSelect.appendChild(option);
  });
};

const renderSelectedComponents = () => {
  selectedComponentsList.innerHTML = '';
  if (!selectedComponentIds.length) {
    const li = document.createElement('li');
    li.textContent = 'Nenhum componente selecionado';
    selectedComponentsList.appendChild(li);
    return;
  }

  selectedComponentIds.forEach((stepId, index) => {
    const component = cachedSteps.find((step) => step.id === stepId);
    const li = document.createElement('li');
    li.classList.add('component-item');
    li.textContent = `${index + 1}. ${component.name}`;

    const actions = document.createElement('div');
    actions.classList.add('component-actions');

    const moveUpBtn = document.createElement('button');
    moveUpBtn.type = 'button';
    moveUpBtn.textContent = '↑';
    moveUpBtn.disabled = index === 0;
    moveUpBtn.addEventListener('click', () => {
      const temp = selectedComponentIds[index - 1];
      selectedComponentIds[index - 1] = selectedComponentIds[index];
      selectedComponentIds[index] = temp;
      renderSelectedComponents();
    });

    const moveDownBtn = document.createElement('button');
    moveDownBtn.type = 'button';
    moveDownBtn.textContent = '↓';
    moveDownBtn.disabled = index === selectedComponentIds.length - 1;
    moveDownBtn.addEventListener('click', () => {
      const temp = selectedComponentIds[index + 1];
      selectedComponentIds[index + 1] = selectedComponentIds[index];
      selectedComponentIds[index] = temp;
      renderSelectedComponents();
    });

    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.textContent = 'Remover';
    removeBtn.addEventListener('click', () => {
      selectedComponentIds = selectedComponentIds.filter((id) => id !== stepId);
      renderSelectedComponents();
    });

    actions.appendChild(moveUpBtn);
    actions.appendChild(moveDownBtn);
    actions.appendChild(removeBtn);
    li.appendChild(actions);
    selectedComponentsList.appendChild(li);
  });
};

const toggleCompositeMode = () => {
  const isComposite = isCompositeInput.checked;
  componentsBuilder.classList.toggle('hidden', !isComposite);
  startsLeftInput.disabled = isComposite;
};

const addComponent = () => {
  const selectedId = Number(componentStepSelect.value);
  if (!selectedId) {
    return;
  }
  if (selectedComponentIds.includes(selectedId)) {
    notify('Esse componente já foi selecionado');
    return;
  }
  selectedComponentIds.push(selectedId);
  renderSelectedComponents();
};

const createStep = async (event) => {
  event.preventDefault();
  const isComposite = isCompositeInput.checked;

  if (isComposite && selectedComponentIds.length < 2) {
    notify('Passo composto precisa ter pelo menos 2 componentes');
    return;
  }

  const payload = {
    name: stepNameInput.value,
    starts_with_left_free: isComposite ? null : startsLeftInput.checked,
    is_composite: isComposite,
    component_step_ids: isComposite ? selectedComponentIds : [],
  };

  const response = await fetch('/api/steps', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorData = await response.json();
    notify(errorData.detail || 'Erro ao cadastrar passo');
    return;
  }

  stepForm.reset();
  selectedComponentIds = [];
  toggleCompositeMode();
  renderSelectedComponents();
  await fetchSteps();
};

const generateSequences = async () => {
  const response = await fetch('/api/randomize', { method: 'POST' });
  const data = await response.json();

  const pairs = data.pairs.map((pair, index) => `${index + 1}. ${pair.first.name} -> ${pair.second.name}`);
  const leftovers = data.leftovers.map((step) => `${step.name} (${step.starts_with_left_free ? 'esquerda livre' : 'direita livre'})`);

  renderList(pairsList, pairs, 'Nenhuma sequência possível');
  renderList(leftoversList, leftovers, 'Sem sobras');
};

tabs.forEach((tab) => {
  tab.addEventListener('click', () => {
    tabs.forEach((item) => item.classList.remove('active'));
    tabContents.forEach((content) => content.classList.remove('active'));

    tab.classList.add('active');
    document.querySelector(`#${tab.dataset.tab}`).classList.add('active');
  });
});

stepForm.addEventListener('submit', createStep);
isCompositeInput.addEventListener('change', toggleCompositeMode);
addComponentBtn.addEventListener('click', addComponent);
generateBtn.addEventListener('click', generateSequences);

fetchSteps();
toggleCompositeMode();
renderSelectedComponents();
