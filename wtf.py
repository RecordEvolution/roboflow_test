from asyncio import sleep, get_event_loop
from reswarm import Reswarm

async def main():
    rw = Reswarm(serial_number="aa4ef0de-9800-482b-8205-d7ca22388dd1")

    # Publishes sample data every 2 seconds to the 're.hello.world' topic
    while True:
        data = {"temperature": 20}
        await rw.publish('re.hello.world', data)

        print(f'Published {data} to topic re.hello.world')

        await sleep(2)

if __name__ == "__main__":
    get_event_loop().run_until_complete(main())