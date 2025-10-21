import streamlit as st
from generatePlaybook_OLD import Playbook 
import os
import json

# Layout das primeiras colunas para IDENTIFICADOR e INCIDENTE
col1, col2 = st.columns(2)
with col1:
    st.subheader("IDENTIFICADOR - REGRA")
    identification = st.text_input("Insira o Id da Regra que representa o incidente.")
with col2:
    st.subheader("INCIDENTE")
    incident_identification = st.text_input("Insira a Identificação do Incidente.") 

st.subheader("Carregar JSON")
json_input = st.text_area("Cole aqui o JSON do log", height=300)

# Função recursiva para listar todos os caminhos possíveis
def listar_campos(d, prefixo=""):
    campos = []
    if isinstance(d, dict):
        for k, v in d.items():
            novo_prefixo = f"{prefixo}.{k}" if prefixo else k
            campos.append(novo_prefixo)
            campos.extend(listar_campos(v, novo_prefixo))
    elif isinstance(d, list):
        for i, item in enumerate(d):
            novo_prefixo = f"{prefixo}[{i}]"
            campos.append(novo_prefixo)
            campos.extend(listar_campos(item, novo_prefixo))
    return campos

# Função para pegar valor pelo caminho
def pegar_valor(d, caminho):
    partes = caminho.split(".")
    for p in partes:
        if "[" in p and "]" in p:  # lidar com listas
            nome, idx = p[:-1].split("[")
            d = d[nome][int(idx)]
        else:
            d = d[p]
    return d

if json_input:
    try:
        data = json.loads(json_input)  
        st.success("✅ JSON carregado com sucesso!")

        # Gerar lista completa de campos
        todos_campos = listar_campos(data)

        # Mostrar todos os campos possíveis
        with st.expander("📋 Ver todos os campos disponíveis"):
            for campo in todos_campos:
                st.write(campo)

        # Seleção múltipla de campos
        selected_fields = st.multiselect(
            "Selecione os campos que deseja visualizar",
            options=todos_campos,
        )

        # Mostrar JSON filtrado
        if selected_fields:
            resumo = {}
            for campo in selected_fields:
                try:
                    resumo[campo] = pegar_valor(data, campo)
                except Exception as e:
                    resumo[campo] = f"Erro ao acessar: {e}"

            st.write("### JSON Filtrado")
            st.json(resumo)

    except Exception as e:
        st.error(f"❌ Erro ao carregar JSON: {e}")



# ETAPAS DO ATAQUE
attack_steps = []
st.subheader("ETAPAS DO ATAQUE")
amount_attack_types = st.number_input("Insira as Etapas de ataque que deseja inserir no Playbook", 1, 10) 
for i in range(int(amount_attack_types)):
    attack_text_value = st.text_input(f"Insira o texto da etapa {i + 1}", key=f"attack_text_{i}")
    attack_steps.append(f"0{i+1}. {attack_text_value}")

# AVALIAÇÃO
data_steps = []
st.subheader("AVALIAÇÃO")
amount_data_steps = st.number_input("Insira os Dados que foram Avaliados.", 1, 100)  
for i in range(int(amount_data_steps)):
    avaliation_text_value = st.text_input(f"Insira o dado Avaliado {i + 1}", key=f"avaliation_text_{i}")
    prefix = f"[0{i+1}]" if i < 9 else f"[{i+1}]"
    data_steps.append(f"{prefix} - {avaliation_text_value}")

# Separando MITIGAÇÃO e CONTENÇÃO em 2 colunas
col1, col2 = st.columns(2)

with col1:
    # MITIGAÇÃO
    mitigation_steps = []
    st.subheader("MITIGAÇÃO")
    amount_mitigation_steps = st.number_input("Insira as etapas de Mitigação.", 1, 10)  
    for i in range(int(amount_mitigation_steps)):
        mitigation_text_value = st.text_input(f"Insira a sequência de Mitigação {i + 1}", key=f"mitigation_text_{i}")
        mitigation_steps.append(f"0{i+1}. {mitigation_text_value}")

with col2:
    # CONTENÇÃO
    containment_steps = []
    st.subheader("CONTENÇÃO")
    amount_containment_steps = st.number_input("Insira as etapas de Contenção.", 1, 10)  
    for i in range(int(amount_containment_steps)):
        containment_text_value = st.text_input(f"Insira a sequência de Contenção {i + 1}", key=f"containment_text_{i}")
        containment_steps.append(f"0{i+1}. {containment_text_value}")

# CONCLUSÃO
st.subheader("CONCLUSÃO")
conclusion = st.text_input("Insira a conclusão sobre o incidente.")

# Visualização do que foi criado até agora
st.markdown("<br><hr><br>", unsafe_allow_html=True)
st.subheader("Resumo do Playbook - {}".format(identification))

with st.container():
    st.write("###### IDENTIFICAÇÃO")
    st.write(incident_identification)

    st.write("###### ETAPAS DO ATAQUE")
    for step in attack_steps:
        st.write(step)

    st.write("###### AVALIAÇÃO")
    for step in data_steps:
        st.write(step)

    st.write("###### MITIGAÇÃO")
    for step in mitigation_steps:
        st.write(step)

    st.write("###### CONTENÇÃO")
    for step in containment_steps:
        st.write(step)

    st.write(f"###### CONCLUSÃO: \n{conclusion}")

# Colocando os botões no centro
st.markdown("<br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    click_html = st.button("Gerar Playbook HTML")

with col2:
    click_txt = st.button("Gerar Arquivo TXT")

with col3:
    click_formatted = st.button("Gerar Formato String")

if click_html:
    # Criando a instância do Playbook com os dados inseridos
    playbook = Playbook(
        identification=identification,
        incident_identification=incident_identification,
        attack_steps=attack_steps,
        data_steps=data_steps,
        mitigation_steps=mitigation_steps,
        containment_steps=containment_steps,
        conclusion=conclusion
    )

    # Gerando o playbook no formato HTML
    formatted_playbook = playbook.generate_playbook()

    # Exibindo o resultado formatado
    st.markdown(formatted_playbook, unsafe_allow_html=True)

elif click_txt:
    # Validação básica antes de gerar o arquivo
    if not identification or not incident_identification or not conclusion:
        st.error("Por favor, preencha pelo menos os campos obrigatórios: Identificador, Incidente e Conclusão.")
    else:
        # Criando a instância do Playbook
        playbook = Playbook(
            identification=identification,
            incident_identification=incident_identification,
            attack_steps=attack_steps,
            data_steps=data_steps,
            mitigation_steps=mitigation_steps,
            containment_steps=containment_steps,
            conclusion=conclusion
        )

        # Gerando o arquivo TXT
        filename, success, message = playbook.generate_txt_file()
        
        if success:
            st.success(f"Suceeso : {message}")
            st.info(f" Arquivo gerado: {filename}")
            
            # Opção para baixar o arquivo
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as file:
                    txt_content = file.read()
                
                st.download_button(
                    label=" Baixar Arquivo TXT",
                    data=txt_content,
                    file_name=filename,
                    mime="text/plain"
                )
        else:
            st.error(f"Falha: {message}")

elif click_formatted:
    # Criando a instância do Playbook
    playbook = Playbook(
        identification=identification,
        incident_identification=incident_identification,
        attack_steps=attack_steps,
        data_steps=data_steps,
        mitigation_steps=mitigation_steps,
        containment_steps=containment_steps,
        conclusion=conclusion
    )

    # Gerando o formato string
    formatted_string = playbook.generate_formatted_string()
    
    st.subheader("Formato String Gerado:")
    st.code(formatted_string, language="text")
    
    # Opção para copiar
    st.text_area("Copie o conteúdo abaixo:", formatted_string, height=200)