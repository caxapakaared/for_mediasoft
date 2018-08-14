from app import db
from app import add_shop


shops = [ { "name" : "Кожа из кожи",
			"city" : "Майна",
			"street" : "Гончарова",
			"number" : "7б", 
			"opening" : "8 : 20",
			"closing" : "19 : 00", },
 		{ "name" : "котята в рассрочку",
			"city" : "Ульяновск",
			"street" : "Ленина",
			"number" : "157", 
			"opening" : "8: 00",
			"closing" : "19: 53" },
		{ "name" : "телевизоры их камня",
			"city" : "Самара",
			"street" : "Советская",
			"number" : "78б", 
			"opening" : "8 : 00",
			"closing" : "19 : 00" }]

for shop in shops:
	new_shop = add_shop(shop)
	db.session.add(new_shop)

db.session.commit()
