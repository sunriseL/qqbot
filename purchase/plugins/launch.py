from os import stat
from nonebot import on_command, CommandSession
import logging

User = tuple[int, str]
delim = "--------"

class Car:
	def __init__(self, ID: int, description: str, price, driver: User):
		self.ID = ID
		self.price = price
		self.description: str = description
		self.members: list[User] = [driver]
		self.driver: User = driver
		self.payed_members: list[User] = []
		self.stop = False
		pass

	def partipate(self, user_id: int, username: str) -> str:
		if self.stop:
			raise Exception("车 {} 已经锁车，无法上车".format(self.description))

		for member in self.members:
			if member[0] == user_id:
				raise Exception("您已经上车，无法重复上车")


		self.members.append((user_id, username))
	
	def stop(self):
		self.stop = True

	def __str__(self) -> str:
		result = "ID: {}\n描述: {}\n价格: {}\n发起人: {}\n成员: {}\n人均价格: {}\n".format(
			self.ID,
			self.description,
			self.price,
			self.driver[1],
			",".join([member[1] for member in self.members]),
			self.price / len(self.members) if len(self.members) > 0 else 0 
		)
		if self.stop:
			result += "目前已锁车\n"
			result += "已付款成员: {}".format(
				",".join([member[1] for member in self.members]),
			)
		else:
			result += "目前还可以上车"
		return result

class Station:
	def __init__(self):
		self.cars: list[Car] = []
		self.ID: int = 1
	def launch(self, description, price, sender: User) -> Car:
		car = Car(self.ID, description, price, sender)
		self.ID += 1
		self.cars.append(car)
		return car

	def _printCar(self, print_stop = True, print_active = True):
		result = ""
		for car in self.cars:
			if (not car.stop and not print_active) or (car.stop and not print_stop):
				continue
			result += "{}\n{}\n".format(delim, car)
		return result
	
	def printAllCar(self):
		result = "所有正在进行的车:\n"
		result += self._printCar()
		return result
	
	def printActiveCar(self):
		result = "还没关车门的车:\n"
		result += self._printCar(print_stop = False)
		return result

	def printStopCar(self):
		result = "关了车门的车:\n"
		result += self._printCar(print_active = False)
		return result
	
	def getCars(self, title = None, ID = None):
		result = []
		if ID:
			for car in self.cars:
				if car.ID == ID:
					result.append(car)
					return result
		else:
			for car in self.cars:
				if title in car.description:
					result.append(car)
		return result
	
			
station = Station()
logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)
fh = logging.FileHandler("car.log", encoding = "utf-8")
fh.setFormatter(logging.Formatter(fmt = "[%(levelname)s] %(asctime)s : %(message)s", datefmt = "%Y-%m-%d %H:%M:%S"))
logger.addHandler(fh)
	

def getCars(session: CommandSession):
	ID = None
	msg = session.get('message', prompt='选择哪个包上车？(ID或部分包名)')

	# if msg is the ID of cars:
	# 		-> Search cars with ID
	# else:
	# 		-> Search cars with string matching
	try:
		ID = eval(msg)
	except Exception:
		pass
	if ID:
		cars = station.getCars(None, ID)
	else:
		cars = station.getCars(msg)

	
	if len(cars) == 0:
		del session.state["message"]
		session.get('message', prompt='未找到{}所对应的包，请重新输入'.format(msg))
	elif len(cars) >= 2:
		del session.state["message"]
		session.get('message', prompt='{}所对应的包有{}个，包括：{}\n请重新输入'.format(msg, len(cars),
			"\n--------\n".join([""] + list(map(str, cars)))))
	
	return cars[0]



@on_command("发车")
async def launch(session: CommandSession):
	sender = session.ctx.sender

	# Get the description of the car
	description = session.get('description', prompt='包的标题是啥')

	# Get the price with right format
	price = session.get('price', prompt='包的价格是多少')
	try:
		price = eval(price)
	except Exception:
		del session.state["price"]
		price = session.get('price', prompt='{}不是合法的数字格式，请重试'.format(price))

	
	# Launch the actual car
	car = station.launch(description, price, (sender["user_id"], sender["nickname"]))

	# Log the message
	# logger.error("{} 发车".format(sender["nickname"]))

	# Respond with current status of car
	await session.send("发车成功！目前状态为\n{}\n{}".format(delim, str(car)))

@on_command("上车")
async def participate(session: CommandSession):
	sender = session.ctx.sender
	car = getCars(session)
	try:
		car.partipate(sender["user_id"], sender["nickname"])
	except Exception as e:
		await session.send("{}\n{}\n{}".format(e, delim, str(car)))
		return
	await session.send("上车成功！\n{}\n{}".format(delim, str(car)))
	
@on_command("锁车")
async def lockCar(session: CommandSession):
	car: Car = getCars(session)
	sender = session.ctx.sender

	if car.driver[0] != sender["user_id"]:
		await session.send("本车的发起人为 {}，你没有权限锁车\n".format(car.driver[1]))
		return
	
	if car.stop:
		await session.send("本车已经锁了\n")
		return

	car.stop()
	await session.send("锁车成功！")
	return

@on_command("看车")
async def printAllCar(session: CommandSession):
	result = station.printAllCar()
	await session.send(result)

@on_command("收钱")

@on_command("支付", aliases=["付好了","付了"])
async def pay(session: CommandSession):
	pass