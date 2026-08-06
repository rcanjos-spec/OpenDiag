from opendiag.bus.mock import MockCANBus
from opendiag.core.can_frame import CANFrame
from opendiag.logger import Logger
from opendiag.tools.sniffer import Sniffer

bus = MockCANBus()

bus.send(CANFrame(0x7E0, b"\x02\x10\x03", 0.0))
bus.send(CANFrame(0x7E8, b"\x50\x03\x00\x32\x01", 0.0))

logger = Logger()

sniffer = Sniffer(bus, logger)
sniffer.run(max_frames=2)
