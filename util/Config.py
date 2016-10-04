from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('conf/config.local.ini')


def get_kafka_config():
    server = parser.get("Kafka", "bootstrap_server")
    port = parser.get("Kafka", "bootstrap_port")
    topic = parser.get("Kafka", "topic")
    enabled = parser.getboolean("Kafka", "enabled")
    return {"server": server, "port": port, "topic": topic, "enabled": enabled}


def get_history_config():
    enabled = parser.getboolean("History", "enabled")
    filename = parser.get("History", "filename")
    return {"enabled": enabled, "filename": filename}


def get_startup_config():
    add_plants = parser.getboolean("Startup", "add_plants")
    clean_start = parser.getboolean("Startup", "clean_start")
    return {"add_plants": add_plants, "clean_start": clean_start}
