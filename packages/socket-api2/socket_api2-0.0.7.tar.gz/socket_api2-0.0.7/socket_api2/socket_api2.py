__name__ = "socket_api2"
__version__ = "0.0.7"

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


class ClientObject():
    def __init__(self, ip, conn, console_output:bool=True, **kwargs):
        self._ip = ip
        self.conn = conn

        self._data = kwargs.get("data", {})
        self.timeout = kwargs.get("timeout", None)

        self.console_output = console_output

        self.conn.settimeout(self.timeout)
    
    @property
    def ip(self):
        return self._ip
    
    @property
    def data(self):
        return self._data
    
    @property
    def manager(self):
        return self.conn

    @property
    def is_connected(self):
        return self.check_connection()

    def set(self, var_before:str, var_after:str):
        eval(f"{var_before} = {var_after}")

    def send(self, msg, method:SEND_METHOD=SEND_METHOD.default_send):
        self.check_connection()

        time.sleep(0.2)
        def _send(msg ,method):
            if isinstance(msg, str):
                msg = msg.encode()
            elif isinstance(msg, bytes):
                pass
            else:
                msg = str(msg).encode()

            if self.console_output: outstr("DEBUG", f"Send to {self.ip}: {msg}")

            if method == 0:
                self.conn.send(str(len(msg)).encode())
                time.sleep(0.5)
                self.conn.send(msg)
            elif method == 1:
                self.conn.send(msg)
            else:
                raise Exception(f"Unknown method -> {method}")
        
        try:
            _send(msg, method)
        except ConnectionAbortedError:
            pass

        except socket.timeout:
            pass

        except ConnectionResetError:
            pass
    
        except OSError:
            pass
    
        except WindowsError:
            pass

        except Exception as e:
            raise e
    
    def recv(self, buffer:int=2048):
        self.check_connection()

        def _recv(buffer):
            received = self.conn.recv(buffer).decode()

            try:
                bfsize = int(received)
            except Exception as e:
                msg = str(received)
                if self.console_output: outstr("DEBUG", f"Recv from {self.ip}: {received}")
                return msg

            received_chunks = []
            remaining = bfsize
            while remaining > 0:
                if remaining > 10000:
                    received = self.conn.recv(10000).decode()
                else:
                    received = self.conn.recv(remaining).decode()
                if not received:
                    raise Exception(f'{self.ip} Error: unexpected EOF')
                received_chunks.append(received)
                remaining -= len(received)

            outp = ''.join(received_chunks)
            if self.console_output: outstr("DEBUG", f"Recv from {self.ip}: {outp}")
            return str(outp)

        try:
            return _recv(buffer)

        except ConnectionAbortedError:
            pass

        except ConnectionResetError:
            pass
    
        except OSError:
            pass
    
        except WindowsError:
            pass

        except socket.timeout:
            return None

        except Exception as e:
            raise e
    
    def check_connection(self):
        if not self._check_connection():
            try:
                self.conn.settimeout(self.timeout)
            except OSError:
                self.conn.close()
                return False
            self.conn.close()
            return False

        try:
            self.conn.settimeout(self.timeout)
        except OSError:
            self.conn.close()
            return False
        return True
    
    def _check_connection(self):
        try:
            self.conn.settimeout(1.4)
            self.conn.recv(16, socket.MSG_PEEK)
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

class Server():
    def __init__(
        self,
        ip,
        port:int, 
        console_output:bool=True,
        client_timeout:int=None,
        use_pyngrok:bool = False,
        pyngrok_options:dict = None
    ):
        self.use_pyngrok = use_pyngrok
        if not None:
            self.pyngrok_options = pyngrok_options
        else: 
            raise Exception("If use_pyngrok is true then pyngrok_options is a required argument. If you don't know what options are valid, heres and example: pyngrok_options={\"mode\": \"tcp\"}")

        if ip == "auto":
            self.IP = socket.gethostbyname(socket.gethostname()) 
        else:
            self.IP = ip

        self.PORT = port
        self.console_output = console_output
        self.client_timeout = client_timeout

        self.decorator_functions_call = []
        self.decorator_client_disconnect = []

        self.clients = []

    def start(self):
        if self.console_output: outstr("INFO", "Starting server...")
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.server.bind((self.IP, self.PORT))
        self.server.listen(1)
        
        if self.use_pyngrok: self.PUBLIC_URL = ngrok.connect(self.PORT, self.pyngrok_options.get("mode", "tcp"), options={"remote_addr": "{}:{}".format(self.IP, self.PORT)})

        if self.console_output:
            try:
                if self.console_output: outstr("INFO", "Server Address: " + str(self.PUBLIC_URL).split("")[1])
            except:
                if self.console_output: outstr("INFO", f"Server Address: {self.IP}:{self.PORT}")

            if self.console_output: outstr("INFO", "Listening for incoming connections...")
        
        threading.Thread(target=self.check_clients).start()

        while True:
            try:
                conn, addr = self.server.accept()
                if self.console_output: outstr("ACCESS", f"Connection from {addr} has been established!", start="\n")

                new_client = ClientObject(ip=addr, conn=conn, console_output=self.console_output, tiemout=self.client_timeout)
                self.clients.append(new_client)

                for func in self.decorator_functions_call:
                    _thread.start_new_thread(func, (new_client,))

            except Exception:
                raise Exception
    
    def check_clients(self):
        def _check(client):
            if not client.check_connection():
                self.clients.remove(client)
                if self.console_output: outstr("DEBUG", f"{client.ip} is no longer connected. (Disconnect)")
                for func in self.decorator_functions_call:
                    _thread.start_new_thread(func, (client,))

        while True:
            time.sleep(10)
            for client in self.clients:
                _thread.start_new_thread(_check, (client,))

    @property
    def ip(self):
        return self.IP
    
    @property
    def connected_clients(self):
        return self.clients
    
    @property
    def socket_object(self):
        return self.server

    def sendall(self, msg):
        if isinstance(msg, str):
            msg = msg.encode()
        elif isinstance(msg, bytes):
            pass
        else:
            msg = str(msg).encode()

        self.server.sendall(msg)
    
    def on_client_connect(self, *args, **kwargs):
        def decorator(func):
            if func not in self.decorator_functions_call:
                self.decorator_functions_call.append(func)
            return func

        return decorator
    
    def on_client_disconnect(self, *args, **kwargs):
        def decorator(func):
            if func not in self.decorator_client_disconnect:
                self.decorator_client_disconnect.append(func)
            return func

        return decorator

class MultiClient():
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
        self.client.connect((self.ip, self.port))
        if self.console_output: outstr("INFO", f"Connected to {self.ip}:{self.port}")

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
        except ConnectionResetError:
            pass
        except socket.timeout:
            pass
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
        except ConnectionResetError:
            pass
        except socket.timeout:
            return ""
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