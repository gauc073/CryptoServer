import asyncio
import json
import time
import websockets
import socket
import sys
import traceback
from threading import Thread
from multiprocessing import Process, Array, Lock, Queue, Manager
from sockets.Currency import CurrencyView

btc_usd_symbol = "BTCUSD"
eth_btc_symbol = "ETHBTC"


async def subscribe_symbol(queue, given_symbol):
    currency_obj = CurrencyView()
    uri = "wss://api.hitbtc.com/api/2/ws"
    async with websockets.connect(uri) as websocket:
        query_symbol = {
            "method": "getSymbol",
            "params": {
                "symbol": given_symbol
            },
            "id": 123
        }
        await websocket.send(json.dumps(query_symbol))
        greeting = await websocket.recv()
        symbol = json.loads(greeting)["result"]
        currency_obj.set_symbol_details(symbol["id"], symbol["feeCurrency"])

        query_currency = {
            "method": "getCurrency",
            "params": {
                "currency": symbol["baseCurrency"]
            },
            "id": 123
        }
        await websocket.send(json.dumps(query_currency))
        greeting = await websocket.recv()
        cur_data = json.loads(greeting)["result"]
        currency_obj.set_currency_details(cur_data["fullName"])

        query = {
            "method": "subscribeTicker",
            "params": {
                "symbol": given_symbol
            },
            "id": 123
        }
        name = json.dumps(query)
        await websocket.send(name)

        while True:
            greeting = await websocket.recv()
            ticker_data = json.loads(greeting)
            if ticker_data.get("params"):
                ticker_data = ticker_data["params"]
                currency_obj.set_ticker_details(ticker_data["ask"], ticker_data["bid"], ticker_data["last"],
                                                ticker_data["open"], ticker_data["low"], ticker_data["high"])
            time.sleep(0.1)
            queue[given_symbol] = json.dumps(currency_obj.__dict__)


def run_btc_usd(array, symbol):
    print("start listening BTCUSD pricing")
    asyncio.get_event_loop().run_until_complete(subscribe_symbol(array, symbol))


def run_eth_btc(array, symbol):
    print("start listening ETHBTC pricing")
    asyncio.get_event_loop().run_until_complete(subscribe_symbol(array, symbol))


def main():
    d = Manager().dict()
    process_eth = Process(target=run_eth_btc, args=(d, "BTCUSD",))
    process_eth.start()
    process_btc = Process(target=run_btc_usd, args=(d, "ETHBTC",))
    process_btc.start()
    start_server(d)


def start_server(d):
    host = "127.0.0.1"
    port = 8000  # arbitrary non-privileged port
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket created")
    try:
        soc.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()
    soc.listen(6)  # queue up to 6 requests
    print("Socket now listening")
    # infinite loop- do not reset for every requests
    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)
        try:
            Thread(target=clientThread, args=(connection, ip, port, d)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()
    soc.close()


def clientThread(connection, ip, port, d, max_buffer_size=5120):
    is_active = True
    while is_active:
        client_input = receive_input(connection, max_buffer_size)
        if "QUIT" in client_input:
            print("Client is requesting to quit")
            connection.close()
            print("Connection " + ip + ":" + port + " closed")
            is_active = False
        else:
            if client_input == "ETHBTC":
                data = d.get(client_input, None)
                if data is None:
                    connection.sendall("please provide correct symbol".encode("utf8"))
                else:
                    json_dump = json.dumps(data)
                    connection.sendall(json_dump.encode("utf8"))
            elif client_input == "BTCUSD":
                data = d.get(client_input, None)
                if data is None:
                    connection.sendall("please provide correct symbol".encode("utf8"))
                else:
                    json_dump = json.dumps(data)
                    connection.sendall(json_dump.encode("utf8"))
            else:
                connection.sendall("please provide correct symbol".encode("utf8"))


def receive_input(connection, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)
    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}".format(client_input_size))
    decoded_input = client_input.decode("utf8").rstrip()
    result = process_input(decoded_input)
    return result


def process_input(input_str):
    print("Processing the input received from client")
    return str(input_str).upper()


if __name__ == "__main__":
    main()
