import time

from library_nsxt.services.nsxt_api_client import *
from library_nsxt.services.nsxt_policy_api_client import *
from library_nsxt.exceptions.nsxt_errors import *
import argparse

class NSG_Cluster:
    def __init__(self, url, user, password, group_name, policy=False):
        """
        Client used to auto create NSX groups in couchbase or mongodb and apply their rules.
        :param str url: Host/URL to access to specific NSX-T cluster.
        :param str user: User to access to NSX-T clsuter with API.
        :param str password: Password to access to NSX-T clsuter with API.
        :param str group_name: Group name for NSX group.
        """
        self.url = url.replace("http://", "").replace("https://", "")
        self.spplited_url = self.url.split(".")
        self.user = user
        self.password = password
        self.group_name = group_name
        self.section_name = "Reglas automatizadas"
        self.policy_id = self.section_name.replace(" ", "_")
        self.policy = policy
        self._api = NSXTAPIClient(self.url, self.user, self.password)
        self._api_policy = NSXTPolicyAPIClient(self.url, self.user, self.password)

        ### If Arteixo PRE...
        if self.spplited_url[0] == "axprensxtmgr":
            ### If Couchbase...
            if "cbs" in group_name:
                self.complete_group_name = "nsg-preec-cbs-cl-" + group_name
                self.complete_rule_name = "rl-preec-cbs-cl-" + group_name
                self.spplited_group_name = self.complete_group_name.split("-")
                self.master_group_name = self.spplited_group_name[0] + "-" + self.spplited_group_name[1] + "-" + self.spplited_group_name[2] + "-all"
            ### If MongoDB...
            if "mng" in group_name:
                self.complete_group_name = "nsg-preec-mng-cl-" + group_name
                self.complete_rule_name = "rl-preec-mng-cl-" + group_name
                self.spplited_group_name = self.complete_group_name.split("-")
                self.master_group_name = self.spplited_group_name[0] + "-" + self.spplited_group_name[1] + "-" + self.spplited_group_name[2] + "-all"
        ### If Arteixo PRO...
        elif self.spplited_url[0] == "axinecnsxmgr":
            ### If Couchbase...
            if "cbs" in group_name:
                self.complete_group_name = "nsg-axec-cbs-cl-" + group_name
                self.complete_rule_name = "rl-axec-cbs-cl-" + group_name
                self.spplited_group_name = self.complete_group_name.split("-")
                self.master_group_name = self.spplited_group_name[0] + "-" + self.spplited_group_name[1] + "-" + self.spplited_group_name[2] + "-all"
            ### If MongoDB...
            if "mng" in group_name:
                self.complete_group_name = "nsg-axec-mng-cl-" + group_name
                self.complete_rule_name = "rl-axec-mng-cl-" + group_name
                self.spplited_group_name = self.complete_group_name.split("-")
                self.master_group_name = self.spplited_group_name[0] + "-" + self.spplited_group_name[1] + "-" + self.spplited_group_name[2] + "-all"
        ### If any other NSX system...
        else:
            self.spplited_url[0] = self.spplited_url[0].replace("nsxtmgr", "")
            ### If Couchbase...
            if "cbs" in group_name:
                self.complete_group_name = "nsg-" + self.spplited_url[0] + "-cbs-cl-" + group_name
                self.complete_rule_name = "rl-" + self.spplited_url[0] + "-cbs-cl-" + group_name
                self.spplited_group_name = self.complete_group_name.split("-")
                self.master_group_name = self.spplited_group_name[0] + "-" + self.spplited_group_name[1] + "-" + self.spplited_group_name[2] + "-all"
            ### If MongoDB...
            if "mng" in group_name:
                self.complete_group_name = "nsg-" + self.spplited_url[0] + "-mng-cl-" + group_name
                self.complete_rule_name = "rl-" + self.spplited_url[0] + "-mng-cl-" + group_name
                self.spplited_group_name = self.complete_group_name.split("-")
                self.master_group_name = self.spplited_group_name[0] + "-" + self.spplited_group_name[1] + "-" + self.spplited_group_name[2] + "-all"

        if not hasattr(self, "complete_group_name"):
            raise NSXTError("Group name not contain any string wich match with couchbase or mongoDB.", "Bad group name")



    def create_group_cluster_and_rules(self):
        # region Create Group cluster and rules in imperative API.
        if self.policy == False:
            ### Create group cluster and put it into master group.
            if self._api.check_if_nsgroup_exist(self.master_group_name):
                self._api.post_nsx_group(self.complete_group_name)
                self._api.put_nsx_member_group(self.master_group_name, self.complete_group_name)
            else:
                raise APIError("The NSX master group name \"" + self.master_group_name + "\" not match with any other in NSX cluster.", None, "Bad master NSX group name")

            ### Create rules for specific group cluster and put it into specific firewall section.
            if self._api.check_if_firewall_inventory_section_exist(self.section_name):
                section_id = self._api.get_id_from_firewall_inventory_section(self.section_name)

                group_id = self._api.get_nsx_group_id(self.complete_group_name)
                revision = self._api.get_firewall_inventory_sections(section_id)["_revision"]
                rules = self._api.get_firewallsection_rules(section_id)["results"]
                rules.append(
                    {
                        "display_name": self.complete_rule_name,
                        "notes": "",
                        "destinations_excluded": False,
                        "sources": [
                            {
                                "target_display_name": self.complete_group_name,
                                "is_valid": True,
                                "target_type": "NSGroup",
                                "target_id": group_id
                            }
                        ],
                        "destinations": [
                            {
                                "target_display_name": self.complete_group_name,
                                "is_valid": True,
                                "target_type": "NSGroup",
                                "target_id": group_id
                            }
                        ],
                        "applied_tos": [
                            {
                                "target_display_name": self.complete_group_name,
                                "is_valid": True,
                                "target_type": "NSGroup",
                                "target_id": group_id
                            }
                        ],
                        "ip_protocol": "IPV4_IPV6",
                        "rule_tag": "",
                        "logged": False,
                        "action": "ALLOW",
                        "sources_excluded": False,
                        "disabled": False,
                        "direction": "IN_OUT"
                    }
                )
                self._api.post_firewallsection_rules(self.section_name, section_id, rules, revision)
            else:
                self._api.post_firewall_inventory_section(self.section_name)
                time.sleep(1.5)
                section_id = self._api.get_id_from_firewall_inventory_section(self.section_name)
                group_id = self._api.get_nsx_group_id(self.complete_group_name)
                revision = self._api.get_firewall_inventory_sections(section_id)["_revision"]
                rules = self._api.get_firewallsection_rules(section_id)["results"]
                rules.append(
                    {
                        "display_name": self.complete_rule_name,
                        "notes": "",
                        "destinations_excluded": False,
                        "sources": [
                            {
                                "target_display_name": self.complete_group_name,
                                "is_valid": True,
                                "target_type": "NSGroup",
                                "target_id": group_id
                            }
                        ],
                        "destinations": [
                            {
                                "target_display_name": self.complete_group_name,
                                "is_valid": True,
                                "target_type": "NSGroup",
                                "target_id": group_id
                            }
                        ],
                        "applied_tos": [
                            {
                                "target_display_name": self.complete_group_name,
                                "is_valid": True,
                                "target_type": "NSGroup",
                                "target_id": group_id
                            }
                        ],
                        "ip_protocol": "IPV4_IPV6",
                        "rule_tag": "",
                        "logged": False,
                        "action": "ALLOW",
                        "sources_excluded": False,
                        "disabled": False,
                        "direction": "IN_OUT"
                    }
                )
                self._api.post_firewallsection_rules(self.section_name, section_id, rules, revision)
        # endregion

        # region Create group cluster and rules in declarative API.
        if self.policy == True:
            ### Create group cluster and put it into master group.
            if self._api_policy.check_if_nsgroup_exist(self.master_group_name):
                self._api_policy.post_nsx_group(self.complete_group_name)
                self._api_policy.put_nsx_member_group(self.master_group_name, self.complete_group_name)
            else:
                raise APIError(
                    "The NSX master group name \"" + self.master_group_name + "\" not match with any other in NSX cluster.",
                    None, "Bad master NSX group name")

            ### Create rules for specific group cluster and put it into specific firewall policy section.
            sources = []
            sources.append(self.complete_group_name)
            destinations = []
            destinations.append(self.complete_group_name)
            if self._api_policy.check_if_firewall_policy_section_exist(self.policy_id):
                self._api_policy.put_firewall_rule(self.complete_rule_name, self.complete_rule_name, self.policy_id, "default", sources, destinations)
            else:
                self._api_policy.put_firewall_policy_section(self.policy_id, self.section_name)
                self._api_policy.put_firewall_rule(self.complete_rule_name, self.complete_rule_name, self.policy_id, "default", sources, destinations)
        # endregion

        ### Send email if section has more than 10 rules.
        # if len(rules) > 10:
        #     pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, required=True, help="NSX-T URL to API access.")
    parser.add_argument("--user", type=str, required=True, help="NSX-T user to API access.")
    parser.add_argument("--pass", type=str, required=True, help="NSX-T password to API access.")
    parser.add_argument("--cluster", type=str, required=True, help="NSX-T cluster name.")
    parser.add_argument("--policy", action="store_true", required=False,
                        help="NSX-T API mode. (Optional: if set, API mode is \"POLICY\". Default is \"Imperative API\").")

    args = parser.parse_args()

    if args.policy:
        NSG_Cluster(args.url, args.user, args.__getattribute__("pass"), args.cluster,
                    True).create_group_cluster_and_rules()
    else:
        NSG_Cluster(args.url, args.user, args.__getattribute__("pass"), args.cluster).create_group_cluster_and_rules()

if __name__ == "__main__":
    main()