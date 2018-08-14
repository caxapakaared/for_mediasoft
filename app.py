from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from config import Config
from datetime import datetime, time

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

class City(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable=False)

	def __repr__(self):
		return self.name

class Street(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=False, nullable=False) 
	city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
	city = db.relationship('City', backref=db.backref('streets', lazy=True))

	def __repr__(self):
		return self.name

class Shop(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=False, nullable=False)
	street_id = db.Column(db.Integer, db.ForeignKey('street.id'), nullable=False)
	street = db.relationship('Street', backref=db.backref('shops', lazy=True))
	city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
	city = db.relationship('City', backref=db.backref('shops', lazy=True))
	number = db.Column(db.String(20), unique=False, nullable=False)
	opening = db.Column(db.Time, nullable=False)
	closing = db.Column(db.Time, nullable=False)

	def __repr__(self):
		return self.name


def add_shop(shop):
	# данная функция вынесена отдельно, так как она используется в срипте наполнени БД

	def get_time(time_string):
		new_time = time_string.split(':')
		new_time = list(map(int, new_time))
		return time(new_time[0], new_time[1])

	city = City.query.filter_by(name=shop['city']).first()
	if not city:
		city = City(name=shop['city'])
		db.session.add(city)
	street = Street.query.filter_by(city=city).filter_by(name=shop['street']).first()
	if not street:
		street = Street(name=shop['street'], city=city)
		db.session.add(street)
	opening = get_time(shop['opening'])
	closing = get_time(shop['closing'])
	new_shop = Shop(name=shop['name'], street=street, city=city, number=shop['number'],
					opening=opening, closing=closing)
	return new_shop	


@app.route('/city/')
def city():
	city_list = []
	cities = City.query.all()
	for city in cities:
		city_list.append({'id' : city.id,
						  'name' : city.name})
	return jsonify(city_list)


@app.route('/city/<id>/street/')
def streets(id):
	street_list = []
	streets = Street.query.filter_by(city_id=id).all()
	if not streets:
		abort(400)
	for street in streets:
		street_list.append({'id' : street.id,
							'name' : street.name })
	return jsonify(street_list)

@app.route('/shop/', methods=['POST', 'GET'])
def shop():
	if request.method == 'GET':
		is_open = request.args.get('open')
		if is_open not in ('1', '0', None):
			abort(400)
		city_id = request.args.get('city')
		street_id =	request.args.get('street')
		now = datetime.now()
		now = time(now.hour, now.minute)
		shops = Shop.query

		if is_open == '1':
			shops = shops.filter(Shop.opening<=now, Shop.closing>=now)
		elif is_open == '0':
			shops = shops.filter(or_(Shop.opening>=now, Shop.closing<=now))
		if street_id:
			shops = shops.filter_by(street_id=street_id)
		elif city_id:
			shops = shops.filter_by(city_id=city_id)

		shops = shops.all()
		shop_list = []
		for shop in shops:
			shop_list.append({'name' : shop.name,
							  'city' : shop.city.name,
							  'street': shop.street.name,
							  'number': shop.number,})
		return jsonify(shop_list)
	
	else:
		shop = request.get_json()
		new_shop = add_shop(shop)
		db.session.add(new_shop)
		db.session.commit()
		r = {'id' : new_shop.id}
		return jsonify(r)

@app.errorhandler(Exception)
def all_exception_handler(error):
   return 'Error', 400


