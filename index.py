from asyncio.events import get_event_loop
from asyncio import sleep
from reswarm import Reswarm

async def main():
    rw = Reswarm()

    # Publishes sample data every 2 seconds to the 're.hello.world' topic
    while True:
        data = {"temperature": 20}
        await rw.publish('re.hello.world', data)

        print(f'Published {data} to topic re.hello.world')

        await sleep(2)



if __name__ == "__main__":
    get_event_loop().run_until_complete(main())