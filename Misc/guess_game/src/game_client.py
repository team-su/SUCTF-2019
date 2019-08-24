import asyncio
import pickle
from guess_game.Ticket import Ticket
from guess_game import banner
from struct import pack


def pack_length(obj):
    return pack('>I', obj)


async def start_client(host, port):
    reader, writer = await asyncio.open_connection(host, port)
    print(banner)

    for _ in range(10):
        number = ''
        while number == '':
            try:
                number = input('Input the number you guess\n> ')
                number = int(number)
            except ValueError:
                number = ''
                pass

        ticket = Ticket(number)
        ticket = pickle.dumps(ticket)

        writer.write(pack_length(len(ticket)))
        writer.write(ticket)

        response = await reader.readline()
        print(response.decode())

    response = await reader.readline()
    print(response.decode())

loop = asyncio.get_event_loop()
loop.run_until_complete(start_client('172.17.0.2', 9999))
