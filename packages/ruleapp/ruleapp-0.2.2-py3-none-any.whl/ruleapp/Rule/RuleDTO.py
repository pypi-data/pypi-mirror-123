class Rule(object):
    def __init__(self):
        self.id = ""
        self.name = ""
        self.last_time_on = ""
        self.last_time_off = ""
        self.last_date_on = ""
        self.last_date_off = ""
        self.device_antecedents = []
        self.device_consequents = []
        self.antecedents = []
        self.consequents = []
        self.evaluation = "false"

    def json_mapping(self, rule_json):
        if "id" in rule_json.keys():
            self.id = rule_json["id"]
        if "name" in rule_json.keys():
            self.name = rule_json["name"]
        if "device_antecedents" in rule_json.keys():
            self.device_antecedents = rule_json["device_antecedents"]
        if "device_consequents" in rule_json.keys():
            self.device_consequents = rule_json["device_consequents"]
        if "antecedents" in rule_json.keys():
            self.antecedents = rule_json["antecedents"]
        if "consequents" in rule_json.keys():
            self.consequents = rule_json["consequents"]
