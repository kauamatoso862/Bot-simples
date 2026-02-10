# Bot-simples
Bot de Discord completo para gerenciamento de Facções/Polícias em servidores de FiveM (RP). Possui sistema de registro com formulário, controle de hierarquia (promoção/rebaixamento), logs automáticos e sistema de punição progressiva (ADV 1, 2, 3 + PD automático). Desenvolvido em Python.

# 🤖 Bot FiveM Manager - Facções & Corporações

Este é um bot desenvolvido em **Python** (`discord.py`) focado na automação e gerenciamento de grupos (Facções, Polícias, Organizações) dentro de servidores de **GTA V Roleplay (FiveM)**.

O objetivo é substituir o trabalho manual da liderança, automatizando desde a entrada do membro (registro) até a saída (PD), passando por promoções e advertências com lógica acumulativa.

## ✨ Funcionalidades Principais

### 📝 Sistema de Registro (Whitelist)
- Botão interativo para iniciar o registro.
- **Formulário (Modal):** Solicita Nome, ID (Passaporte) e Recrutador.
- **Aprovação via Embed:** A Staff aprova ou reprova com um clique.
- **Automação:** Ao aprovar, o bot altera o apelido do usuário para o padrão `Nome | ID` e entrega o cargo de membro automaticamente.

### 📈 Gerenciamento de Hierarquia
- **/promover:** Adiciona um novo cargo ao membro.
  - *Diferencial:* O cargo é acumulativo (não remove os anteriores).
  - Envia log técnico para a Staff e anúncia para a cidade.
- **/rebaixar:** Troca de cargo (Remove o atual e insere o inferior).
- **Proteção Hierárquica:** Impede que membros com cargos baixos tentem gerenciar superiores.

### ⚖️ Sistema de Punição (PD & ADV)
- **/pd (Perda de Direitos):** - Expulsa (Kick) o membro do Discord.
  - Envia o motivo na DM do usuário antes de remover.
  - Registra em dois canais: Log Técnico (Staff) e Anúncio Público (Cidade).
  
- **/adv (Advertências Progressivas):**
  - **Lógica Automática:** O bot verifica os cargos do usuário.
  - **Escalada:** - Se não tem nada -> Ganha **ADV 1**.
    - Se tem ADV 1 -> Ganha **ADV 2**.
    - Se tem ADV 2 -> Ganha **ADV 3** e é **removido automaticamente (PD)**.
  - Registra tudo nos logs para controle.

---

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior.
- Conta no Discord Developer Portal (com **Intents** de Membros e Conteúdo ativadas).

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/kauamatoso862/Bot-simples.git]([https://github.com/kauamatoso862/Bot-simples.git)

2. **Instale as dependências:**
    ```bash
    pip install discord.py

3. **Configure o Bot:**

- Abra o arquivo bot_fivem.py.
- Insira seu TOKEN do bot.
- Substitua os IDs dos Cargos (Verificado, ADV1, ADV2, ADV3).
- Substitua os IDs dos Canais (Logs Staff/Público, Registro, etc).

4. **Inicie o Bot:**
  ```bash
  python bot_fivem.py
```

## 🛠️ Lista de Comandos

| Comando | Descrição | Permissão Necessária |
| :--- | :--- | :--- |
| `/comecar` | Envia o painel interativo de registro no canal. | Administrador |
| `/promover` | Promove um membro (adiciona o cargo, cumulativo). | Administrador |
| `/rebaixar` | Rebaixa um membro (remove o cargo atual e adiciona o novo). | Administrador |
| `/adv` | Aplica advertência progressiva (1 -> 2 -> 3 + Expulsão). | Administrador |
| `/pd` | Aplica Perda de Direitos (PD) e expulsa o membro do servidor. | Administrador |

