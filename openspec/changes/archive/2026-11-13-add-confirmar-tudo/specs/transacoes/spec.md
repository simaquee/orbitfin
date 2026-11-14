## ADDED Requirements

### Requirement: Confirmar todos os lançamentos
Na revisão da importação, o sistema SHALL exibir o botão "Confirmar tudo", que confirma de uma vez todos os cards pendentes com a descrição e o valor que estão nos campos. Cards com valor zero MUST continuar pendentes, com o aviso "O valor deve ser diferente de zero. Corrija os cards que continuam pendentes.". O botão fica desabilitado quando não há card pendente.

#### Scenario: Confirmar tudo
- **WHEN** a revisão tem 129 cards pendentes e o usuário clica em "Confirmar tudo"
- **THEN** os 129 cards passam a "Confirmado" e "Confirmar importação" é habilitado

#### Scenario: Card com valor zero
- **WHEN** um dos cards pendentes está com valor R$ 0,00 e o usuário clica em "Confirmar tudo"
- **THEN** os demais são confirmados, esse card continua pendente e "Confirmar importação" continua desabilitado
