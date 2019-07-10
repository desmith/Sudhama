from src.pins import valve


def open():
    valve.off()


def close():
    valve.on()


def status():
    return 'stopped' if valve.value() else 'flowing'


close()
