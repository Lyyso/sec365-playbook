#  Playbook Generator

Este projeto é uma ferramenta para gerar **playbooks de incidentes de segurança** a partir de logs de firewalls (como Paloalto, Trellix e Fortigate). Ele permite filtrar campos do JSON, selecionar quais informações incluir e gerar o playbook em **TXT** ou **HTML**.(futuramente)

---

## Funcionalidades

- Filtragem automática de campos do log do firewall.
- Seleção de campos dinâmicos para incluir no playbook.
- Adição de etapas de ataque, mitigação e contenção.
- Conclusão do incidente.
- Geração de playbook em **TXT** ou **HTML**.
- Download direto dos arquivos gerados.

---

## Pré-requisitos

- Python 3.10 ou superior.
- pip instalado.
- Um terminal/console para rodar comandos.

---

## Instalação

1. Clone este repositório:

```bash
git clone https://github.com/Lyyso/sec365-playbook.git
cd sec365-playbook

2. Instale os requisitos do projeto
```bash
pip install -r requirements.txt

3. Execute o Projeto
```bash
streamlit run main.py

