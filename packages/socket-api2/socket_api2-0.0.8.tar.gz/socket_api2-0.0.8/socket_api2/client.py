__name__ = "socket_api2"
__version__ = "0.0.8"

__author__ = "Da4ndo"
__discord__ = "Da4ndo#0934"
__youtube__ = "https://www.youtube.com/channel/UCdhZa-JISiqwd913nhB8cAw?"
__github__ = "https://github.com/Mesteri05"

import socket
from pyngrok import ngrok
import _thread, threading, time

class SEND_METHOD:
    default_send = 0
    just_send = 1

def outstr(mode, text, start=""):
    """
    MODE = ["INFO", "DEBUG", "ERROR", "ACCESS"]
    """

    ct = time.localtime()
    t = time.strftime("%Y.%m.%d %H:%M:%S", ct)

    try:
        import colorama
        colorama.init()

        red = colorama.Fore.RED
        red2 = colorama.Fore.LIGHTRED_EX
        blue = colorama.Fore.BLUE
        blue2 = colorama.Fore.LIGHTBLUE_EX
        green = colorama.Fore.GREEN
        gray = colorama.Fore.LIGHTBLACK_EX
        gray2 = colorama.Fore.LIGHTWHITE_EX
        magenta = colorama.Fore.MAGENTA
        reset = colorama.Fore.RESET

        if mode.lower() == "info":
            print(f"{start}[{t}]{reset} {blue}<{mode}>{reset}: {blue2}{text}{reset}")
        elif mode.lower() == "debug":
            print(f"{start}[{t}]{reset} {gray}<{mode}>{reset}: {gray2}{text}{reset}")
        elif mode.lower() == "error":
            print(f"{start}[{t}]{reset} {red}<{mode}>{reset}: {red2}{text}{reset}")
        elif mode.lower() == "access":
            print(f"{start}[{t}]{reset} {green}<INFO>{reset}: {green}{text}{reset}")
        else:
            raise Exception(f"Wrong mode. Valid modes are INFO, DEBUG, ERROR, ACCESS not {mode}")
    except Exception as e:
        if mode.lower() == "info":
            print(f"{start}[{t}] <{mode}>: {text}")
        elif mode.lower() == "debug":
            print(f"{start}[{t}] <{mode}>: {text}")
        elif mode.lower() == "error":
            print(f"{start}[{t}] <{mode}>: {text}")
        elif mode.lower() == "access":
            print(f"{start}[{t}] <INFO>: {text}")
        else:
            raise Exception(f"Wrong mode. Valid modes are INFO, DEBUG, ERROR, ACCESS not {mode}")

class Client():
    def  __init__(self, target_ip:str, target_port:int, console_output:bool=True, timeout:int=None, reconnect:bool=True):
        self.ip, self.port = target_ip, target_port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.console_output = console_output
        
        self.running = True
        self.reconnect_counter = 0
        self.try_reconnect = reconnect
        self.timeout = timeout

        self.client.settimeout(timeout)
    
    @property
    def socket_object(self):
        return self.client

    def connect(self):
        try:
            self.client.connect((self.ip, self.port))
            if self.console_output: outstr("INFO", f"Connected to {self.ip}:{self.port}")
            return 200
        except Exception as e:
            return e, 500

    def _reconnect(self):
        try:
            self.reconnect_counter += 1
            self.client.close()
            del self.client
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connect()
            self.reconnect_counter = 0
            return True
        except:
            return False
    
    def disconnect(self):
        self.client.close()
        if self.console_output: outstr("INFO", f"Disconnected from {self.ip}:{self.port}")

    def close(self):
        self.client.close()
        if self.console_output: outstr("INFO", f"Disconnected from {self.ip}:{self.port}")

    def send(self, msg, method:SEND_METHOD=SEND_METHOD.default_send):
        self.check_connection()

        time.sleep(0.2)
        def _send(msg, method):
            if isinstance(msg, str):
                msg = msg.encode()
            elif isinstance(msg, bytes):
                pass
            else:
                msg = str(msg).encode()
            
            if self.console_output: outstr("DEBUG", f"Send: {msg}")

            self.check_connection()

            if method == 0:
                self.client.send(str(len(msg)).encode())
                time.sleep(0.5)
                self.client.send(msg)
            elif method == 1:
                self.client.send(msg)
            else:
                raise Exception(f"Unknown method -> {method}")
        
        try:
            _send(msg, method)
            return 200
        except ConnectionResetError as e:
            return e, 500
        except socket.timeout as e:
            return e, 500
        except Exception:
            raise Exception
    
    def sendfile(self, file, offset=0, count=None):
        self.client.sendfile(file, offset, count)
    
    def recv(self, buffer:int):
        self.check_connection()

        def _recv():
            received = self.client.recv(buffer).decode()
            if str(received) == "exit":
                self.client.close()
                if self.console_output: outstr("DEBUG", "Server forced to disconnect.")
                time.sleep(1)
                return None

            try:
                bfsize = int(received)
            except Exception as e:
                if self.console_output: outstr("DEBUG", f"Recv: {received}")

                return str(received)

            received_chunks = []
            remaining = bfsize
            while remaining > 0:
                if remaining > 10000:
                    received = self.client.recv(10000).decode()
                else:
                    received = self.client.recv(remaining).decode()
                if not received:
                    raise Exception(f'{self.ip} Error: unexpected EOF')
                received_chunks.append(received)
                remaining -= len(received)

            outp = ''.join(received_chunks)
            if str(outp) == "exit":
                self.client.close()
                if self.console_output: outstr("DEBUG",  "Server forced to disconnect.")
                time.sleep(1)
                return None

            if self.console_output: outstr("DEBUG", f"Recv: {outp}")
            return str(outp)

        try:
            return _recv()
        except ConnectionResetError as e:
            return e, 500
        except socket.timeout as e:
            return e, 500
        except Exception:
            raise Exception

    @property
    def is_connected(self):
        resp = self._check_connection()
        try:
            self.client.settimeout(self.timeout)
        except OSError:
            self.client.close()
            return False
        return resp
    
    def check_connection(self):
        connected = False
        while not connected:
            if not self._check_connection():
                try:
                    self.client.settimeout(self.timeout)
                except OSError:
                    self.client.close()
                if self.console_output: outstr("ERROR", f"Connection lost.")
                while not connected:
                    time.sleep(0.3)
                    if self.console_output: outstr("INFO", f"Reconnect... Counter: {self.reconnect_counter}")
                    if self._reconnect():
                        connected = True
                    
            else:
                try:
                    self.client.settimeout(self.timeout)
                    connected = True 
                except OSError:
                    self.client.close()
                    connected = False

    def _check_connection(self):
        try:
            self.client.settimeout(1.4)
            data = self.client.recv(16, socket.MSG_PEEK)

            if len(data) == 0:
                return False
            return True
        except BlockingIOError:

            return True 
        except ConnectionResetError:

            return False
            
        except socket.timeout:

            return True
        
        except WindowsError:
            return False
        
        except OSError:
            return False

        except Exception as e:
            outstr("ERROR", str(e))