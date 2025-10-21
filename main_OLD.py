import streamlit as st
from json_parser import JsonParser
from generate_playbook_OLD import GeneratePlaybook
import json
import pandas as pd

#Json com Características retun[0]
def filtrar_json(firewall_options,json_input):
    #Converter a String para Dict
    try:
        json_string_to_dict = json.loads(json_input)
    except json.JSONDecodeError:
        st.error("O Json Inserido é invalido")
    
    filter = JsonParser(firewall_options,json_string_to_dict)
    identifiers = filter.select_firewall()[0]
    tags = filter.select_firewall()[1]
    return identifiers,tags

# ---------------------- Title ----------------------
st.set_page_config(page_title="Sec365 - Playbook", layout="wide")
st.title("Sec365 - Playbook")
# ---------------------- Firewall Selection ----------------------
st.subheader("Selecione o Firewall")
firewall_options = st.multiselect(
    "Selecione o Firewall",
    ["Paloalto", "Trellix", "Fortigate"],
    max_selections=1
)

# ---------------------- Firewall Enviromennt  ----------------------
st.subheader("Insira o Log")
json_input = st.text_area("Cole aqui o JSON do log", height=300)
if st.button("Enviar Log Para Análise") and firewall_options:
    ids, tags = filtrar_json(firewall_options, json_input)
    if ids and tags:
        st.session_state["ids"] = ids
        st.session_state["tags"] = tags
        st.session_state["selected_tags"] = []  # limpa a seleção anterior

# ---------------------- Declaração do Incidente ----------------------
st.subheader("INCIDENTE")
incident_identification = st.text_input("Insira a Identificação do Incidente.")


# ---------------------- Columns Json ----------------------
col1, col2 = st.columns(2)
with col1:
    st.subheader("Campos filtrados do JSON")

    if "ids" in st.session_state and st.session_state["ids"]:
        df = pd.DataFrame(
            list(st.session_state["ids"].items()), columns=["Campo", "Valor"]
        )
        st.dataframe(df, width="stretch", height=800)
    else:
        st.info("Nenhum JSON processado ainda.")

# ---------------------- COLUNA 2 ----------------------
with col2:
    st.subheader("Id da Regra")
    id_rule = st.text_area("Cole aqui o ID do log") #Field

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


# ---------------------- ETAPAS DO ATAQUE ----------------------
attack_steps = []
st.subheader("ETAPAS DO ATAQUE")
amount_attack_types = st.number_input("Insira as Etapas de ataque que deseja inserir no Playbook", 1, 10) 
for i in range(int(amount_attack_types)):
    attack_text_value = st.text_input(f"Insira o texto da etapa {i + 1}", key=f"attack_text_{i}")
    attack_steps.append(f"0{i+1}. {attack_text_value}")

# ---------------------- MITIGAÇÃO ----------------------
mitigation_steps = []
st.subheader("MITIGAÇÃO")
amount_mitigation_steps = st.number_input("Insira as etapas de Mitigação.", 1, 10)  
for i in range(int(amount_mitigation_steps)):
    mitigation_text_value = st.text_input(f"Insira a sequência de Mitigação {i + 1}", key=f"mitigation_text_{i}")
    mitigation_steps.append(f"0{i+1}. {mitigation_text_value}")

# ---------------------- CONTENÇÃO ----------------------
containment_steps = []
st.subheader("CONTENÇÃO")
amount_containment_steps = st.number_input("Insira as etapas de Contenção.", 1, 10)  
for i in range(int(amount_containment_steps)):
    containment_text_value = st.text_input(f"Insira a sequência de Contenção {i + 1}", key=f"containment_text_{i}")
    containment_steps.append(f"0{i+1}. {containment_text_value}")

# ---------------------- CONCLUSÃO ----------------------
st.subheader("CONCLUSÃO")
conclusion = st.text_input("Insira a conclusão sobre o incidente.")



if st.button("Gerar Playbook TXT"):
    if "ids" in st.session_state and st.session_state["ids"]:
        playbook = GeneratePlaybook(
            id_rule=id_rule,
            incident_identification=incident_identification,
            selected_tags=st.session_state["selected_tags"],
            attack_steps=attack_steps,
            mitigation_steps=mitigation_steps,
            containment_steps=containment_steps,
            conclusion=conclusion
        )
        arquivo = playbook.save_playbook_txt()
        st.success(f"Playbook gerado com sucesso: {arquivo}")
