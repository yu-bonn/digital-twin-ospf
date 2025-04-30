from pysnmp.hlapi import *
import os
from collections import defaultdict
import ipaddress

# 各OIDプレフィックス（LSDBエントリごとの属性）
OIDS = {
    'type': '1.3.6.1.2.1.14.4.1.2',
    'lsid': '1.3.6.1.2.1.14.4.1.3',
    'adv_router': '1.3.6.1.2.1.14.4.1.4',
    'seq': '1.3.6.1.2.1.14.4.1.6',
    'age': '1.3.6.1.2.1.14.4.1.7'
}

# バイナリを IPv4 アドレス形式に変換
def to_ip(val):
    try:
        return str(ipaddress.IPv4Address(bytes(val)))
    except Exception:
        return str(val)

# SNMP walkでOIDのデータ収集
def snmp_bulk_walk(community, host, oid):
    results = {}
    for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=1),
        UdpTransportTarget((host, 161), timeout=1, retries=3),
        ContextData(),
        ObjectType(ObjectIdentity(oid)),
        lexicographicMode=False
    ):
        if errorIndication:
            print("[ERROR]", errorIndication)
            break
        elif errorStatus:
            print("[ERROR]", errorStatus.prettyPrint())
            break
        else:
            for oid, val in varBinds:
                results[str(oid)] = val
    return results

# LSDBエントリの統合
def collect_lsdb(community, host):
    data = {key: snmp_bulk_walk(community, host, oid) for key, oid in OIDS.items()}
    entries = defaultdict(dict)

    for key, oid_dict in data.items():
        for oid, val in oid_dict.items():
            index = '.'.join(oid.split('.')[-4:])
            entries[index][key] = val

    result = []
    for index, entry in entries.items():
        if all(k in entry for k in OIDS):
            result.append(entry)
    return result

# 出力ファイルへの書き出し（IP表記で）
def write_to_file(entries, filepath):
    with open(filepath, 'w') as f:
        for e in entries:
            f.write(f"{e['type']} {to_ip(e['lsid'])} {to_ip(e['adv_router'])} {e['seq']} {e['age']}\n")

# 実行部
if __name__ == "__main__":
    COMMUNITY = "nishimuuuu"
    HOST = "203.178.136.25"
    OUTPUT = os.path.join(os.path.dirname(__file__), "lsdb_input.txt")

    print("[INFO] Collecting OSPF LSDB entries...")
    entries = collect_lsdb(COMMUNITY, HOST)
    print(f"[INFO] Retrieved {len(entries)} valid LSA entries.")
    write_to_file(entries, OUTPUT)
    print(f"[INFO] Saved to {OUTPUT}")
