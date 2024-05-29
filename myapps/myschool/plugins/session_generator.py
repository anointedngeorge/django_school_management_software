from datetime import datetime


def sessionGenerator(sessions=10):
    _container = []
    try:
        current_year = datetime.now().strftime("%Y")
        for x in range(1, sessions):
            session_str =  ""
            formatted =  int(current_year)
            formatted = formatted + x
            session_str += f"{formatted-1}-{formatted}"
            _container.append((session_str,session_str))
        return _container
    except Exception as e:
        pass