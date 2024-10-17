let chips; // Declarar a variável fora da função

function gerarChips(selectedDay, startTime, endTime) {
    const chipContainer = document.getElementById('chipContainer');
        const chipValue = `${selectedDay}:${startTime}-${endTime}`; // Formato do chip

        // Verificar se o chip já existe no Set
        if (!chips.has(chipValue)) {
            const chip = document.createElement('div');
            chip.className = 'chip';
            chip.textContent = chipValue; // Definindo o texto do chip

            // Criar botão de exclusão
            const removeButton = document.createElement('button');
            removeButton.textContent = 'x'; // Texto do botão
            removeButton.className = 'btn btn-danger btn-sm'; // Estilo do botão
            removeButton.style.marginLeft = '10px'; // Espaçamento
            removeButton.addEventListener('click', function() {
                chipContainer.removeChild(chip); // Remove o chip
                chips.delete(chipValue); // Remove do Set
                updateHiddenField(); // Atualiza o campo oculto
            });

            // Adicionar o botão de exclusão ao chip
            chip.appendChild(removeButton);
            chipContainer.appendChild(chip);

            // Adicionar o valor ao Set
            chips.add(chipValue);
            updateHiddenField(); // Atualiza o campo oculto
        } else {
            alert('Este dia e horário já foi adicionado.');
        }
}

// Função para inicializar o Set
function initializeChips() {
    chips = new Set(); // Reinicia o Set
    const hiddenField = document.getElementById('id_dias_horas_preferidas');
    chips_string = hiddenField.value
    if(chips_string) {
        chips_string = chips_string.split(',')
        if(chips_string.length > 0) {
            chips_string.forEach(chip => {
                const [day, startTime, endTime] = chip.replace(':','-').split('-');
                gerarChips(day, startTime, endTime);
            }); 
        }
    }
}

// Inicializa os chips quando a página carrega
window.onload = initializeChips;

document.getElementById('addChip').addEventListener('click', function() {
    const select = document.getElementById('diasSelect');
    const startTime = document.getElementById('startTime').value;
    const endTime = document.getElementById('endTime').value;
    const selectedDay = select.value; // Pegando o valor

    // Verifica se os horários estão preenchidos
    if (startTime && endTime) {
        // Verifica se o horário final é menor que o inicial
        if (endTime < startTime) {
            alert('O horário final não pode ser menor que o horário inicial.');
            return; // Interrompe a execução
        }

        gerarChips(selectedDay, startTime, endTime);
        
    } else {
        alert('Por favor, preencha os horários.');
    }
});

// Função para atualizar o campo oculto com a string concatenada
function updateHiddenField() {
    const hiddenField = document.getElementById('id_dias_horas_preferidas');
    hiddenField.value = Array.from(chips).join(','); // Juntando os chips em uma string
}

// Atualiza o campo oculto quando o formulário é enviado
document.getElementById('submitButton').addEventListener('click', function(event) {
    if (chips.size === 0) { // Verifica se não há chips
        alert('Você deve adicionar pelo menos um horário.');
        event.preventDefault(); // Impede o envio do formulário
    } else {
        updateHiddenField();
    }
});
