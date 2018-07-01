from flask import jsonify

class JsonValue:

    @staticmethod
    def success(node=None,
                process_name="",
                event_name="",
                status="Success",
                code=80):

        return jsonify(status=status,
                       code=code,
                       message = f"{node.name} {process_name} {event_name} event succesfully",
                       nodename = node.name,
                       processname = process_name,
                       data = node.get_process(process_name).serialize())

    @staticmethod
    def error(node=None,
            process_name="",
            event_name="",
            status="Error",
            code=0,
            payload=""):

        return jsonify(status=status,
                       code=code,
                       message = f"{node.name} {process_name} {event_name} event unsuccesfully",
                       nodename = node.name,
                       payload=payload)