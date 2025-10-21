from datetime import datetime
import re

class GeneratePlaybook:
    # Campos fixos do abuseipdb
    FIXED_FIELDS = [
        ("Má Reputação de IP Origem (Indicador)", "abuseipdb:found"),
        ("Má Reputação de IP Origem (Nível)", "abuseipdb:abuseConfidenceScore"),
        ("Má Reputação de IP Origem (Domínio)", "abuseipdb:domain"),
        ("Má Reputação de IP Origem (Ocorrências)", "abuseipdb:totalReports"),
        ("Má Reputação de IP Origem (Última ocorrência)", "abuseipdb:lastReportedAt"),
        ("Tipo de IP Origem", "abuseipdb:usageType"),
        ("ISP de Origem", "abuseipdb:isp"),
        ("Código de País do IP de Origem", "abuseipdb:countryCode")
    ]

    # Tradução dos campos do Paloalto
    PALOALTO_FIELD_NAMES = {
        "data:device_name": "Nome Dispositivo",
        "data:src_ip": "Endereço Origem",
        "data:dst_ip": "Endereço Destino",
        "data:nat_source_ip": "Ip do NAT Origem",
        "data:nat_destination_ip": "Ip do NAT destino",
        "data:application": "Aplicação",
        "data:dst_port": "Porta de Destino dos Dados",
        "data:nat_source_port": "Porta de Origem do NAT dos Dados",
        "data:nat_destination_port": "Porta de Destino do NAT dos Dados",
        "data:ip_protocol": "Protocolo de Rede",
        "data:category": "Verificação",
        "data:source_location": "País de Origem dos Dados",
        "data:destination_location": "País de Destino dos Dados",
        "data:virtual_system_name": "Nome da Máquina Virtual",
        "data:application_category": "Categoria da Aplicação",
        "data:application_technology": "Tecnologia da Aplicação",
        "data:application_characteristics": "Características da Aplicação",
        "data:tunneled_application": "Dados da Aplicação Encapsulada"
    }

    def __init__(self, id_rule, incident_identification, selected_tags,
                 attack_steps, mitigation_steps, containment_steps, conclusion):
        self.id_rule = id_rule
        self.incident_identification = incident_identification or ""
        self.selected_tags = selected_tags or []
        self.attack_steps = attack_steps or []
        self.mitigation_steps = mitigation_steps or []
        self.containment_steps = containment_steps or []
        self.conclusion = conclusion or "Sem conclusão informada."
        self.date_generated = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")

    def clean_step_numbers(self, steps):
        """Remove qualquer numeração já existente no começo dos passos"""
        cleaned = []
        for step in steps:
            if step is None:
                continue
            step_clean = re.sub(r'^\s*\d{1,2}\.\s*', '', str(step).strip())
            cleaned.append(step_clean)
        return cleaned

    def generate_steps_text(self, steps):
        """Numera automaticamente os passos (01, 02, ...)"""
        if not steps:
            return "Nenhuma informação disponível."
        steps_clean = self.clean_step_numbers(steps)
        return "\n".join([f"{i+1:02d}. {step}" for i, step in enumerate(steps_clean)])

    def generate_evaluation_text(self):
        """Gera avaliação com campos traduzidos + campos fixos abuseipdb"""
        lines = []
        # Campos selecionados pelo usuário (dinâmicos)
        for i, tag in enumerate(self.selected_tags):
            label = self.PALOALTO_FIELD_NAMES.get(tag, tag)
            lines.append(f"[{i+1:02d}] - {label}: {{{tag}}}")
        start_index = len(self.selected_tags)
        # Campos fixos
        for i, (label, field) in enumerate(self.FIXED_FIELDS, start=start_index):
            lines.append(f"[{i+1:02d}] - {label}: {{{field}}}")
        return "\n".join(lines)

    def escape_json(self, text):
        if text is None:
            return ""
        return str(text).replace("\n", "\\n").replace('"', '\\"')

    def generate_playbook_text(self):
        """Gera o playbook em formato TXT"""
        identification_text = self.incident_identification or (
            "O incidente de segurança identificado envolve uma conexão pervasiva permitida através do firewall, "
            "que utiliza uma aplicação. Essa conexão apresenta uma vulnerabilidade conhecida e pode ser explorada por malware."
        )

        attack_text = self.generate_steps_text(self.attack_steps)
        mitigation_text = self.generate_steps_text(self.mitigation_steps)
        containment_text = self.generate_steps_text(self.containment_steps)
        evaluation_text = self.generate_evaluation_text()

        json_text = (
            f"<p align=justify>"
            f"<b>IDENTIFICAÇÃO:</b>\\n{self.escape_json(identification_text)}"
            f"\\n\\n<b>ETAPAS DO ATAQUE:</b>\\n{self.escape_json(attack_text)}"
            f"\\n\\n<b>AVALIAÇÃO:</b>\\n{self.escape_json(evaluation_text)}"
            f"\\n\\n<b>MITIGAÇÃO:</b>\\n{self.escape_json(mitigation_text)}"
            f"\\n\\n<b>CONTENÇÃO:</b>\\n{self.escape_json(containment_text)}"
            f"\\n\\n<b>CONCLUSÃO:</b> {self.escape_json(self.conclusion)}</p>"
        )

        playbook_text = (
            f"PLAYBOOK - {self.id_rule}\n"
            f"{'='*50}\n\n"
            f"IDENTIFICAÇÃO:\n{identification_text}\n\n"
            f"ETAPAS DO ATAQUE:\n{attack_text}\n\n"
            f"AVALIAÇÃO:\n{evaluation_text}\n\n"
            f"MITIGAÇÃO:\n{mitigation_text}\n\n"
            f"CONTENÇÃO:\n{containment_text}\n\n"
            f"CONCLUSÃO:\n{self.conclusion}\n\n"
            f"(JSON) : \"{self.id_rule}\":\"{json_text}\",\n\n"
            f"{'='*50}\n"
            f"Playbook gerado em: {self.date_generated}"
        )
        return playbook_text

    def generate_playbook_html(self):
        """Gera HTML completo do playbook"""
        def html_block(title, body):
            return f"<h3>{title}</h3><div style='white-space:pre-wrap;'>{body}</div>"

        body = (
            html_block("IDENTIFICAÇÃO:", self.incident_identification) +
            html_block("ETAPAS DO ATAQUE:", self.generate_steps_text(self.attack_steps)) +
            html_block("AVALIAÇÃO:", self.generate_evaluation_text()) +
            html_block("MITIGAÇÃO:", self.generate_steps_text(self.mitigation_steps)) +
            html_block("CONTENÇÃO:", self.generate_steps_text(self.containment_steps)) +
            html_block("CONCLUSÃO:", self.conclusion) +
            f"<p><small>Playbook gerado em: {self.date_generated}</small></p>"
        )

        return (
            "<!doctype html>\n"
            "<html lang='pt-br'>\n"
            "<head>\n"
            "  <meta charset='utf-8'/>\n"
            f"  <title>PLAYBOOK - {self.id_rule}</title>\n"
            "  <style>body{font-family:Arial,Helvetica,sans-serif;padding:18px} h3{margin-bottom:6px;} div{margin-bottom:12px;}</style>\n"
            "</head>\n"
            "<body>\n"
            f"<h1>PLAYBOOK - {self.id_rule}</h1>\n"
            f"{body}\n"
            "</body>\n"
            "</html>"
        )

    def save_playbook_txt(self, directory="./"):
        filename = f"{directory}PLAYBOOK_{self.id_rule}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.generate_playbook_text())
        return filename

    def save_playbook_html(self, directory="./"):
        filename = f"{directory}PLAYBOOK_{self.id_rule}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.generate_playbook_html())
        return filename
