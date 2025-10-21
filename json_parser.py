

class JsonParser:
    def __init__(self,firewall_options,json_input):
        self.firewall_options = firewall_options
        self.json_input = json_input

        self.paloalto_data = ["src_ip","dst_ip","nat_source_ip","nat_destination_ip","application","dst_port","nat_source_port",
                              "nat_destination_port","ip_protocol","category","source_location","destination_location",
                              "virtual_system_name","device_name","application_category","application_technology",
                              "application_characteristics","tunneled_application"]



    def select_firewall(self):
        if self.firewall_options[0] == "Paloalto":
            filtered = self.identifiers_paloalto(self.json_input)
            info_group = self.tag_paloalto(self.json_input)
            return filtered,info_group
    
    def identifiers_paloalto(self,json_input):
        """Apresenta os valores associados as tags do firewall"""
        data_values = json_input.get("data",{}) # Retorna os dados se houver, se não retona um dic vazio {}
        filtered = {key: value for key, value in data_values.items() if key in self.paloalto_data}
        return filtered

    def tag_paloalto(self,json_input):
      """Apresenta as tags do Firewall e o"""
      formated_tags = []
      data_values = json_input.get("data", {})
      tags = [key for key in data_values.keys() if key in self.paloalto_data]
      for tag in tags:
          add_data_name = "data:" + str(tag)
          formated_tags.append(add_data_name)
      return formated_tags

f = ["Paloalto"]
i = {
        "decoder": {
            "name": "paloalto"
        },
        "data": {
            "action": "allow",
            "device_name": "PA-5220-1",
            "serial_number": "013201006880",
            "generated_time": "2025/10/02 15:00:19",
            "src_ip": "10.163.44.22",
            "dst_ip": "8.8.8.8",
            "src_port": "0",
            "dst_port": "0",
            "application": "ping",
            "action_flags": "0x8000000000000000",
            "action_source": "from-policy",
            "application_category": "general-internet",
            "application_characteristics": "has-known-vulnerability,tunnel-other-application,pervasive-use",
            "application_level_link_changes": "0",
            "application_risk": "2",
            "application_sanctioned_state": "no",
            "application_subcategory": "internet-utility",
            "application_technology": "network-protocol",
            "bytes": "124",
            "bytes_received": "60",
            "bytes_sent": "64",
            "category": "any",
            "config_version": "2562",
            "destination_location": "United States",
            "destination_zone": "WAN",
            "device_group_hierarchy_level_1": "0",
            "device_group_hierarchy_level_2": "0",
            "device_group_hierarchy_level_3": "0",
            "device_group_hierarchy_level_4": "0",
            "elapsed_time_in_seconds": "0",
            "flags": "0x8000000000000000",
            "high_resolution_timestamp": "2025-10-02T15:00:20.593-03:00",
            "http_2_connection": "0",
            "inbound_interface": "ae1.1000",
            "ip_protocol": "icmp",
            "is_saas_app": "no",
            "log_action": "PANORAMA-TRAFFIC_ONLY",
            "log_number": "1",
            "nat_destination_ip": "8.8.8.8",
            "nat_destination_port": "0",
            "nat_source_ip": "177.74.63.59",
            "nat_source_port": "0",
            "offloaded": "0",
            "outbound_interface": "ethernet1/20",
            "packets": "2",
            "packets_received": "1",
            "packets_sent": "1",
            "parent_session_id": "0",
            "receive_time": "2025/10/02 15:00:19",
            "repeat_count": "1",
            "rule_name": "PROJETO_WIFI_NAS_ESCOLAS",
            "sctp_association_id": "0",
            "sctp_chunks": "0",
            "sctp_chunks_received": "0",
            "sctp_chunks_sent": "0",
            "sequence_number": "7359924323149928155",
            "session_end_reason": "aged-out",
            "session_id": "0",
            "source_location": "10.0.0.0-10.255.255.255",
            "source_zone": "CHEGADA",
            "start_time": "2025/10/02 15:00:05",
            "threat_content_type": "end",
            "time_logged": "2025/10/02 15:00:19",
            "tunnel_id_imsi": "0",
            "tunnel_type": "N/A",
            "tunneled_application": "untunneled",
            "type": "TRAFFIC",
            "uuid_for_rule": "5a0834eb-2d81-4885-8b45-564a47e5aa76",
            "virtual_system": "vsys1",
            "virtual_system_name": "FW_ESTADO"
        }
}

#p1 = JsonParser(f,i)
#print(p1.select_firewall()[0])
#print(p1.select_firewall()[1])
    