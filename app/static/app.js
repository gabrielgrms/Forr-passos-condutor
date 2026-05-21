const tabs = document.querySelectorAll('.tab');
const tabContents = document.querySelectorAll('.tab-content');
const stepForm = document.querySelector('#step-form');
const stepNameInput = document.querySelector('#step-name');
const startsLeftInput = document.querySelector('#starts-left');
const stepsList = document.querySelector('#steps-list');
const leftList = document.querySelector('#left-list');
const rightList = document.querySelector('#right-list');
const generateBtn = document.querySelector('#generate-btn');
const pairsList = document.querySelector('#pairs-list');
const leftoversList = document.querySelector('#leftovers-list');

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
  const steps = await response.json();

  const all = steps.map((step) => `${step.name} (${step.starts_with_left_free ? 'esquerda livre' : 'direita livre'})`);
  const left = steps.filter((step) => step.starts_with_left_free).map((step) => step.name);
  const right = steps.filter((step) => !step.starts_with_left_free).map((step) => step.name);

  renderList(stepsList, all, 'Nenhum passo cadastrado');
  renderList(leftList, left, 'Nenhum passo com esquerda livre');
  renderList(rightList, right, 'Nenhum passo com direita livre');
};

const createStep = async (event) => {
  event.preventDefault();

  const payload = {
    name: stepNameInput.value,
    starts_with_left_free: startsLeftInput.checked,
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
generateBtn.addEventListener('click', generateSequences);

fetchSteps();
