# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2020 Deutsches Elektronen-Synchrotron DESY.
# See LICENSE.txt for license details.
#
# Terminal for the custom "serial over IPMB" protocol used by DESY MMC
# 
# Based on pyserial miniterm, https://github.com/pyserial/pyserial/blob/master/serial/tools/miniterm.py
# (C)2002-2020 Chris Liechti <cliechti@gmx.net>

import os
import sys
import threading
import pyipmi
import pyipmi.interfaces
import argparse
import logging
import time
from enum import Enum
from .__init__ import __version__

class IpmiCode(Enum):
    SOI_CHANNEL_INFO = 0xf0
    SOI_SESSION_CTRL = 0xf1
    SOI_POLL_XCHG = 0xf2

class IpmiConn():
    def __init__(self, mmc_addr, mch_url, ipmitool_mode=False):
        if ipmitool_mode:
            self.interface = pyipmi.interfaces.create_interface('ipmitool', interface_type='lan')
        else:
            self.interface = pyipmi.interfaces.create_interface('rmcp', keep_alive_interval=0)
        self.conn = self.mtca_mch_bridge_amc(mch_url, mmc_addr)

    '''
        From https://github.com/kontron/python-ipmi/blob/master/pyipmi/__init__.py#L111

        Example #2: access to an AMC in a uTCA chassis
            slave = 0x81, target = 0x72
            routing = [(0x81,0x20,0),(0x20,0x82,7),(0x20,0x72,None)]

                        uTCA - MCH                        AMC
                    .-------------------.             .--------.
                    |       .-----------|             |        |
                    | ShMC  | CM        |             | MMC    |
         channel=0  |       |           |  channel=7  |        |
     81 ------------| 0x20  |0x82  0x20 |-------------| 0x72   |
                    |       |           |             |        |
                    |       |           |             |        |
                    |       `-----------|             |        |
                    `-------------------´             `--------´
        `------------´     `---´        `---------------´
    '''
    def mtca_mch_bridge_amc(self, mch_url: str, amc_mmc_addr: int):
        '''
        Create a "double bridge" IPMI connection to talk directly to a AMC
        '''
        mtca_amc_double_bridge = [(0x81, 0x20, 0),
                                 (0x20, 0x82, 7),
                                 (0x20, amc_mmc_addr, None)]

        conn = pyipmi.create_connection(self.interface)
        conn.session.set_session_type_rmcp(mch_url)
        conn.session.set_auth_type_user('', '')
        conn.session.establish()
        conn.target = pyipmi.Target(
            ipmb_address=amc_mmc_addr,
            routing=mtca_amc_double_bridge
        )
        return conn

    def raw_cmd(self, cmd_code, cmd_data=None):
        '''
        Send IPMI raw command to the MMC
        '''
        data = int.to_bytes(cmd_code.value, 1, byteorder='big')
        if cmd_data is not None:
            if isinstance(cmd_data, int):
                data += int.to_bytes(cmd_data, 1, byteorder='big')
            else:
                data += cmd_data

        raw_reply = self.conn.raw_command(0, 0x30, data)
        return raw_reply[0], raw_reply[1:]
    
    def channel_list(self):
        '''
        Retrieve list of available "serial over IPMB" channels
        '''
        channels = []
        ch_idx = 0
        while True:
            try:
                status, reply = self.raw_cmd(IpmiCode.SOI_CHANNEL_INFO, ch_idx)
            except Exception:
                # "out of range" error makes ipmitool backend throw an exception
                break
            if status != 0:
                break
            reply = reply.decode('utf-8')
            channels.append((ch_idx, reply))
            ch_idx += 1
        return channels

    def session_ctrl(self, channel, enable):
        '''
        Open / close "serial over IPMB" session
        '''
        channel = int.to_bytes(channel, 1, byteorder='big')
        enable = b'\x01' if enable else b'\x00'
        status, _ = self.raw_cmd(IpmiCode.SOI_SESSION_CTRL, channel + enable)
        if status != 0:
            print(f'session_ctrl returned 0x{status:02x}')
        return status == 0
    
    def poll_xchg(self, tx_data):
        '''
        Poll / exchange "serial over IPMB" data
        '''
        # Assuming tx_data is not longer than one max. TX packet (if that happens, we have to implement splitting)
        return self.raw_cmd(IpmiCode.SOI_POLL_XCHG, tx_data)

'''
Console code based on pyserial/miniterm
'''
class ConsoleBase(object):
    """OS abstraction for console (input/output codec, no echo)"""

    def __init__(self):
        self.byte_output = sys.stdout.buffer
        self.output = sys.stdout

    def setup(self):
        """Set console to read single characters, no echo"""

    def cleanup(self):
        """Restore default console settings"""

    def getkey(self):
        """Read a single key from the console"""
        return None

    def write_bytes(self, byte_string):
        """Write bytes (already encoded)"""
        self.byte_output.write(byte_string)
        self.byte_output.flush()

    def write(self, text):
        """Write string"""
        self.output.write(text)
        self.output.flush()

    def cancel(self):
        """Cancel getkey operation"""

    # context manager:
    # switch terminal temporary to normal mode (e.g. to get user input)

    def __enter__(self):
        self.cleanup()
        return self

    def __exit__(self, *args, **kwargs):
        self.setup()


if os.name == 'nt':  # noqa
    import msvcrt
    import ctypes
    import platform

    class Out(object):
        """file-like wrapper that uses os.write"""

        def __init__(self, fd):
            self.fd = fd

        def flush(self):
            pass

        def write(self, s):
            os.write(self.fd, s)

    class Console(ConsoleBase):
        fncodes = {
            ';': '\1bOP',  # F1
            '<': '\1bOQ',  # F2
            '=': '\1bOR',  # F3
            '>': '\1bOS',  # F4
            '?': '\1b[15~',  # F5
            '@': '\1b[17~',  # F6
            'A': '\1b[18~',  # F7
            'B': '\1b[19~',  # F8
            'C': '\1b[20~',  # F9
            'D': '\1b[21~',  # F10
        }
        navcodes = {
            'H': '\x1b[A',  # UP
            'P': '\x1b[B',  # DOWN
            'K': '\x1b[D',  # LEFT
            'M': '\x1b[C',  # RIGHT
            'G': '\x1b[H',  # HOME
            'O': '\x1b[F',  # END
            'R': '\x1b[2~',  # INSERT
            'S': '\x1b[3~',  # DELETE
            'I': '\x1b[5~',  # PGUP
            'Q': '\x1b[6~',  # PGDN        
        }
        
        def __init__(self):
            super(Console, self).__init__()
            self._saved_ocp = ctypes.windll.kernel32.GetConsoleOutputCP()
            self._saved_icp = ctypes.windll.kernel32.GetConsoleCP()
            ctypes.windll.kernel32.SetConsoleOutputCP(65001)
            ctypes.windll.kernel32.SetConsoleCP(65001)
            # ANSI handling available through SetConsoleMode since Windows 10 v1511 
            # https://en.wikipedia.org/wiki/ANSI_escape_code#cite_note-win10th2-1
            if platform.release() == '10' and int(platform.version().split('.')[2]) > 10586:
                ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
                import ctypes.wintypes as wintypes
                if not hasattr(wintypes, 'LPDWORD'): # PY2
                    wintypes.LPDWORD = ctypes.POINTER(wintypes.DWORD)
                SetConsoleMode = ctypes.windll.kernel32.SetConsoleMode
                GetConsoleMode = ctypes.windll.kernel32.GetConsoleMode
                GetStdHandle = ctypes.windll.kernel32.GetStdHandle
                mode = wintypes.DWORD()
                GetConsoleMode(GetStdHandle(-11), ctypes.byref(mode))
                if (mode.value & ENABLE_VIRTUAL_TERMINAL_PROCESSING) == 0:
                    SetConsoleMode(GetStdHandle(-11), mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)
                    self._saved_cm = mode
            self.output = Out(sys.stdout.fileno()) # codecs.getwriter('UTF-8')(Out(sys.stdout.fileno()), 'replace')
            # the change of the code page is not propagated to Python, manually fix it
            sys.stderr = Out(sys.stderr.fileno()) # codecs.getwriter('UTF-8')(Out(sys.stderr.fileno()), 'replace')
            sys.stdout = self.output
            self.output.encoding = 'UTF-8'  # needed for input

        def __del__(self):
            ctypes.windll.kernel32.SetConsoleOutputCP(self._saved_ocp)
            ctypes.windll.kernel32.SetConsoleCP(self._saved_icp)
            try:
                ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), self._saved_cm)
            except AttributeError: # in case no _saved_cm
                pass

        def getkey(self):
            while True:
                z = msvcrt.getwch()
                if z == chr(13):
                    return chr(10)
                elif z is chr(0) or z is chr(0xe0):
                    try:
                        code = msvcrt.getwch()
                        if z is chr(0):
                            return self.fncodes[code]
                        else:
                            return self.navcodes[code]
                    except KeyError:
                        pass
                else:
                    return z

        def cancel(self):
            # CancelIo, CancelSynchronousIo do not seem to work when using
            # getwch, so instead, send a key to the window with the console
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            ctypes.windll.user32.PostMessageA(hwnd, 0x100, 0x0d, 0)

elif os.name == 'posix':
    import atexit
    import termios
    import fcntl

    class Console(ConsoleBase):
        def __init__(self):
            super(Console, self).__init__()
            self.fd = sys.stdin.fileno()
            self.old = termios.tcgetattr(self.fd)
            atexit.register(self.cleanup)
            self.enc_stdin = sys.stdin

        def setup(self):
            new = termios.tcgetattr(self.fd)
            new[3] = new[3] & ~termios.ICANON & ~termios.ECHO & ~termios.ISIG
            new[6][termios.VMIN] = 1
            new[6][termios.VTIME] = 0
            termios.tcsetattr(self.fd, termios.TCSANOW, new)

        def getkey(self):
            c = self.enc_stdin.read(1)
            if c == chr(0x7f):
                c = chr(8)    # map the BS key (which yields DEL) to backspace
            return c

        def cancel(self):
            fcntl.ioctl(self.fd, termios.TIOCSTI, b'\0')

        def cleanup(self):
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old)

else:
    raise NotImplementedError(
        'Sorry no implementation for your platform ({}) available.'.format(sys.platform))

class MMCterm(object):
    def __init__(self, ipmi_conn):
        self.console = Console()
        self.ipmi = ipmi_conn
        self.exit_character = chr(0x18)  # ctrl-x
        self.alive = None
        self._reader_alive = None
        self.receiver_thread = None
        self.console_queue = []
        self.queue_lock = threading.Lock()

    def _start_reader(self):
        """Start reader thread"""
        self._reader_alive = True
        self.receiver_thread = threading.Thread(target=self.reader, name='rx')
        self.receiver_thread.daemon = True
        self.receiver_thread.start()

    def _stop_reader(self):
        """Stop reader thread only, wait for clean exit of thread"""
        self._reader_alive = False
        self.receiver_thread.join()

    def start(self):
        """start worker threads"""
        self.alive = True
        self._start_reader()
        self.transmitter_thread = threading.Thread(target=self.writer, name='tx')
        self.transmitter_thread.daemon = True
        self.transmitter_thread.start()
        self.console.setup()

    def stop(self):
        """set flag to stop worker threads"""
        self.alive = False

    def join(self, transmit_only=False):
        """wait for worker threads to terminate"""
        self.transmitter_thread.join()
        self.receiver_thread.join()

    def reader_abort(self, msg):
        self.console.write(msg)
        self.alive = False
        self.console.cancel()

    def reader(self):
        '''
        IPMI communication thread
        send input from console to MMC "stdin", return MMC "stdout" data to print on the console
        '''
        rx_data = b''
        while self.alive and self._reader_alive:
            tx_data = b''

            # Check for user input from console
            with self.queue_lock:
                if len(self.console_queue):
                    tx_data = self.console_queue
                    self.console_queue = []

            if len(tx_data) == 0 and len(rx_data) == 0:
                # Don't flood the MCH with polling, if there's probably no data to exchange
                time.sleep(0.01)

            # write user input to MMC, fetch MMC output to print
            try:
                status, rx_data = self.ipmi.poll_xchg(bytearray(tx_data))
            except Exception as e:
                self.reader_abort(f'pyipmi exception: {e}')
                return

            if len(rx_data):
                self.console.write_bytes(rx_data)
            if status != 0:
                self.reader_abort(f'Status error: {status:02x}')

    def writer(self):
        '''
        Console thread
        Append console data to the queue, exit if exit_character key is pressed
        '''
        try:
            while self.alive:
                try:
                    c = self.console.getkey()
                except KeyboardInterrupt:
                    c = '\x03'
                if not self.alive:
                    break
                elif c == self.exit_character:
                    self.stop()
                    break
                else:
                    with self.queue_lock:
                        self.console_queue += c.replace('\n', '\r').encode('utf-8')
        except:
            self.alive = False
            raise


def main():
# example: ./mmcterm.py 0x74 -m 192.168.1.252
    parser = argparse.ArgumentParser(
        description='DESY MMC Serial over IPMB console'
    )
    parser.add_argument('mch_addr',
                        type=str,
                        help='IP address or hostname of MCH'
    )
    parser.add_argument('mmc_addr',
                        type=lambda x: int(x,0),
                        help='IPMB-L address of MMC'
    )
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s ' + __version__
    )
    parser.add_argument('-c', '--channel',
                        type=int,
                        default=0,
                        help='console channel (default 0)'
    )
    parser.add_argument('-l', '--list',
                        action='store_true',
                        help='list available channels'
    )
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='pyipmi debug mode'
    )
    parser.add_argument('-i', '--ipmitool',
                        action='store_true',
                        help='make pyipmi use ipmitool instead of native rmcp'
    )
    args = parser.parse_args()

    if args.debug:
        pyipmi.logger.set_log_level(logging.DEBUG)
        pyipmi.logger.add_log_handler(logging.StreamHandler())
    
    conn = IpmiConn(args.mmc_addr, args.mch_addr, ipmitool_mode=args.ipmitool)

    if args.list:
        lst = conn.channel_list()
        if not len(lst):
            print('Could not read channel list')
            sys.exit(-1)

        for l in lst:
            print(f'channel {l[0]}: {l[1]}')
        sys.exit(0)

    if not conn.session_ctrl(args.channel, True):
        print(f'Could not open session for channel {args.channel}')
        sys.exit(-1)

    mmcterm = MMCterm(conn)

    print("Press Ctrl-x to exit")
    mmcterm.start()
    try:
        mmcterm.join(True)
    except KeyboardInterrupt:
        pass
    mmcterm.join()

    conn.session_ctrl(args.channel, False)

if __name__ == '__main__':
    main()
