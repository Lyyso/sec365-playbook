import streamlit as st
from json_parser import JsonParser
from generate_playbook import GeneratePlaybook
import json
import pandas as pd

# --- Função para filtrar JSON ---
def filtrar_json(firewall_options, json_input):
    try:
        json_string_to_dict = json.loads(json_input)
    except json.JSONDecodeError:
        st.error("O JSON inserido é inválido")
        return None, None
    
    filtro = JsonParser(firewall_options, json_string_to_dict)
    identifiers, tags = filtro.select_firewall()
    return identifiers, tags

# --- Configuração da página ---
st.set_page_config(page_title="Sec365 - Playbook", layout="wide")
st.title("Sec365 - Playbook")

# --- Seleção de Firewall ---
st.subheader("Selecione o Firewall")
firewall_options = st.multiselect(
    "Selecione o Firewall",
    ["Paloalto", "Trellix", "Fortigate"],
    max_selections=1
)

# --- Inserção do Log ---
st.subheader("Insira o Log")
json_input = st.text_area("Cole aqui o JSON do log", height=300)
if st.button("Enviar Log Para Análise") and firewall_options:
    ids, tags = filtrar_json(firewall_options, json_input)
    if ids and tags:
        st.session_state["ids"] = ids
        st.session_state["tags"] = tags
        st.session_state["selected_tags"] = []

# --- Identificação do Incidente ---
st.subheader("INCIDENTE")
incident_identification = st.text_input("Insira a Identificação do Incidente.")

# --- Colunas ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("Campos filtrados do JSON")
    if "ids" in st.session_state and st.session_state["ids"]:
        df = pd.DataFrame(list(st.session_state["ids"].items()), columns=["Campo", "Valor"])
        st.dataframe(df, width="stretch", height=800)
    else:
        st.info("Nenhum JSON processado ainda.")

with col2:
    st.subheader("Id da Regra")
    id_rule = st.text_area("Cole aqui o ID do log")

    st.subheader("Campos para adicionar no Playbook")
    if "selected_tags" not in st.session_state:
        st.session_state["selected_tags"] = []

    if "tags" in st.session_state and st.session_state["tags"]:
        for tag in st.session_state["tags"]:
            checked = st.checkbox(tag, key=f"chk_{tag}")
            if checked and tag not in st.session_state["selected_tags"]:
                st.session_state["selected_tags"].append(tag)
            elif not checked and tag in st.session_state["selected_tags"]:
                st.session_state["selected_tags"].remove(tag)

        if st.session_state["selected_tags"]:
            st.success("Campos selecionados:")
            st.write(st.session_state["selected_tags"])
        else:
            st.info("Nenhum campo selecionado.")
    else:
        st.info("Nenhum campo disponível para seleção.")

# --- Etapas do Ataque ---
st.subheader("ETAPAS DO ATAQUE")
attack_steps = []
amount_attack_types = st.number_input("Quantas etapas de ataque deseja inserir?", 1, 10)
for i in range(int(amount_attack_types)):
    attack_text_value = st.text_input(f"Texto da etapa {i + 1}", key=f"attack_text_{i}")
    attack_steps.append(attack_text_value)

# --- Mitigação ---
st.subheader("MITIGAÇÃO")
mitigation_steps = []
amount_mitigation_steps = st.number_input("Quantas etapas de mitigação deseja inserir?", 1, 10)
for i in range(int(amount_mitigation_steps)):
    mitigation_text_value = st.text_input(f"Sequência de Mitigação {i + 1}", key=f"mitigation_text_{i}")
    mitigation_steps.append(mitigation_text_value)

# --- Contenção ---
st.subheader("CONTENÇÃO")
containment_steps = []
amount_containment_steps = st.number_input("Quantas etapas de contenção deseja inserir?", 1, 10)
for i in range(int(amount_containment_steps)):
    containment_text_value = st.text_input(f"Sequência de Contenção {i + 1}", key=f"containment_text_{i}")
    containment_steps.append(containment_text_value)

# --- Conclusão ---
st.subheader("CONCLUSÃO")
conclusion = st.text_input("Insira a conclusão sobre o incidente.")

# --- Gerar Playbook ---
gp = GeneratePlaybook(
    id_rule=id_rule,
    incident_identification=incident_identification,
    selected_tags=st.session_state.get("selected_tags", []),
    attack_steps=attack_steps,
    mitigation_steps=mitigation_steps,
    containment_steps=containment_steps,
    conclusion=conclusion
)

# --- Mostrar Playbook TXT ---
st.markdown("### Visualizar Playbook")
playbook_text = gp.generate_playbook_text()
st.code(playbook_text, language="text")

# --- Download direto do Playbook TXT ---
st.download_button(
    label="Baixar Playbook TXT",
    data=playbook_text.encode("utf-8"),
    file_name=f"PLAYBOOK_{id_rule}.txt",
    mime="text/plain"
)
