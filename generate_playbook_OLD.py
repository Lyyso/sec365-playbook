from datetime import datetime
import re

class GeneratePlaybook:
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

    def __init__(self, id_rule, incident_identification, selected_tags,
                 attack_steps, mitigation_steps, containment_steps, conclusion):
        self.id_rule = id_rule
        self.incident_identification = incident_identification
        self.selected_tags = selected_tags or []
        self.attack_steps = attack_steps or []
        self.mitigation_steps = mitigation_steps or []
        self.containment_steps = containment_steps or []
        self.conclusion = conclusion or "Sem conclusão informada."
        self.date_generated = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")

    def clean_step_numbers(self, steps):
        """Remove qualquer numeração já existente na lista de passos"""
        cleaned = []
        for step in steps:
            # Remove padrões tipo "01. " ou "1. "
            step_clean = re.sub(r'^\s*\d{1,2}\.\s*', '', step)
            cleaned.append(step_clean)
        return cleaned

    def generate_steps_text(self, steps):
        """Numera automaticamente os passos (01, 02, ...) sem duplicar"""
        if not steps:
            return "Nenhuma informação disponível."
        steps_clean = self.clean_step_numbers(steps)
        return "\n".join([f"{i+1:02d}. {step}" for i, step in enumerate(steps_clean)])

    def generate_evaluation_text(self):
        lines = []
        for i, tag in enumerate(self.selected_tags):
            lines.append(f"[{i+1:02d}] - {tag}: {{{tag}}}")
        start_index = len(self.selected_tags)
        for i, (label, field) in enumerate(self.FIXED_FIELDS, start=start_index):
            lines.append(f"[{i+1:02d}] - {label}: {{{field}}}")
        return "\n".join(lines)

    def escape_json(self, text):
        return text.replace("\n", "\\n").replace('"', '\\"')

    def generate_playbook_text(self):
        identification_text = self.incident_identification or "Descrição padrão do incidente."

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

        return (
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

    def save_playbook_txt(self, directory="./"):
        filename = f"{directory}PLAYBOOK_{self.id_rule}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.generate_playbook_text())
        return filename
