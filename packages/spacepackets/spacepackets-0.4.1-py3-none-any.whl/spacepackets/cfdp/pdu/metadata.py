from __future__ import annotations
import struct
from typing import List

from spacepackets.cfdp.pdu.file_directive import FileDirectivePduBase, DirectiveCodes
from spacepackets.cfdp.conf import PduConfig
from spacepackets.cfdp.tlv import CfdpTlv
from spacepackets.cfdp.lv import CfdpLv
from spacepackets.cfdp.definitions import ChecksumTypes
from spacepackets.cfdp.conf import check_packet_length
from spacepackets.log import get_console_logger


class MetadataPdu:
    """Encapsulates the Keep Alive file directive PDU, see CCSDS 727.0-B-5 p.83"""

    def __init__(
        self,
        closure_requested: bool,
        checksum_type: ChecksumTypes,
        file_size: int,
        source_file_name: str,
        dest_file_name: str,
        pdu_conf: PduConfig,
        options: List[CfdpTlv] = None,
    ):
        self.pdu_file_directive = FileDirectivePduBase(
            directive_code=DirectiveCodes.METADATA_PDU,
            pdu_conf=pdu_conf,
            directive_param_field_len=0
        )
        self.closure_requested = closure_requested
        self.checksum_type = checksum_type
        self.file_size = file_size
        source_file_name_as_bytes = source_file_name.encode('utf-8')
        self.source_file_name_lv = CfdpLv(
            value=source_file_name_as_bytes
        )
        dest_file_name_as_bytes = dest_file_name.encode('utf-8')
        self.dest_file_name_lv = CfdpLv(
            value=dest_file_name_as_bytes
        )
        if options is None:
            self.options = []
        else:
            self.options = options

    @classmethod
    def __empty(cls) -> MetadataPdu:
        empty_conf = PduConfig.empty()
        return cls(
            closure_requested=False,
            checksum_type=ChecksumTypes.MODULAR_LEGACY,
            file_size=0,
            source_file_name="",
            dest_file_name="",
            pdu_conf=empty_conf
        )

    def pack(self):
        if not self.pdu_file_directive.verify_file_len(self.file_size):
            raise ValueError
        packet = self.pdu_file_directive.pack()
        current_idx = self.pdu_file_directive.packet_len
        packet.append((self.closure_requested << 6) | self.checksum_type)
        if self.pdu_file_directive.pdu_header.large_file:
            packet.extend(struct.pack('!Q', self.file_size))
        else:
            packet.extend(struct.pack('!I', self.file_size))
        packet.extend(self.source_file_name_lv.pack())
        packet.extend(self.dest_file_name_lv.pack())
        for option in self.options:
            packet.extend(option.pack())

    @classmethod
    def unpack(cls, raw_packet: bytearray) -> MetadataPdu:
        metadata_pdu = cls.__empty()
        metadata_pdu.pdu_file_directive = FileDirectivePduBase.unpack(raw_packet=raw_packet)
        current_idx = metadata_pdu.pdu_file_directive.packet_len
        # Minimal length: 1 byte + FSS (4 byte) + 2 empty LV (1 byte)
        if not check_packet_length(len(raw_packet), current_idx + 7):
            raise ValueError
        metadata_pdu.closure_requested = raw_packet[current_idx] & 0x40
        metadata_pdu.checksum_type = raw_packet[current_idx] & 0x0f
        current_idx += 1
        current_idx, metadata_pdu.file_size = metadata_pdu.pdu_file_directive.parse_fss_field(
            raw_packet=raw_packet, current_idx=current_idx
        )
        metadata_pdu.source_file_name_lv.unpack(raw_bytes=raw_packet[current_idx:])
        current_idx += metadata_pdu.source_file_name_lv.get_total_len()
        metadata_pdu.dest_file_name_lv.unpack(raw_bytes=raw_packet[current_idx:])
        current_idx += metadata_pdu.dest_file_name_lv.get_total_len()
        if current_idx < len(raw_packet):
            metadata_pdu.parse_options(raw_packet=raw_packet, start_idx=current_idx)
        return metadata_pdu

    def parse_options(self, raw_packet: bytearray, start_idx: int):
        self.options = []
        current_idx = start_idx
        while True:
            current_tlv = CfdpTlv.unpack(raw_bytes=raw_packet[current_idx:])
            self.options.append(current_tlv)
            # This will always increment at least two, so we can't get stuck in the loop
            current_idx += current_tlv.get_total_length()
            if current_idx > len(raw_packet):
                logger = get_console_logger()
                logger.warning(
                    'Parser Error when parsing TLVs in Finished PDU. '
                    'Possibly invalid packet'
                )
                break
            elif current_idx == len(raw_packet):
                break
