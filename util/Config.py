import ConfigParser

parser = ConfigParser.SafeConfigParser()
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
    add_default_plant = parser.getboolean("Startup", "add_default_plant")
    clean_start = parser.getboolean("Startup", "clean_start")
    return {"add_default_plant": add_default_plant, "clean_start": clean_start}
