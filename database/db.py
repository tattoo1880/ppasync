import ssl
import motor.motor_asyncio


# uri = 'mongodb+srv://tattoo186225345941:Qwerty7788421@cluster0.cf73hmy.mongodb.net/?retryWrites=true&w=majority'
uri = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(uri)
db = client['asnum']
collection = db['asnum']