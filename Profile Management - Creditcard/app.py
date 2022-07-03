from email import message
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message
import os
from flask_login import LoginManager, UserMixin, login_manager, login_user, current_user

from sqlalchemy.orm import relationship

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'books.db')
app.config['JWT_SECRET_KEY'] = 'super-secret' #change IRL
app.config['SECRET_KEY'] = 'flask-secret' #change IRL

app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '5987602bdfeef8'
app.config['MAIL_PASSWORD'] = 'd4502ecb7ac807'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

ma = Marshmallow(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)
mail = Mail(app)
login_manager =LoginManager()
login_manager.init_app(app)

##--------------Database Code------------------------------------
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


@app.cli.command('db_seed')
def db_seed():
    book1 = Book(book_name='To Kill a Mockingbird',
                 book_genre='Fiction',
                 book_author='Harper Lee',
                 book_publisher='HarperCollins Publishers',
                 book_description='To Kill a Mockingbird is a 1961 novel by Harper Lee. Set in small-town Alabama, the novel is a bildungsroman, or coming-of-age story, and chronicles the childhood of Scout and Jem Finch as their father Atticus defends a Black man falsely accused of rape. ',
                 price=15.99,
                 year_published=1960,
                 copies_sold=40000000  # 40 million
                 )

    book2 = Book(book_name='1984',
                 book_genre='Dystopian',
                 book_author='George Orwell',
                 book_publisher='Secker & Warburg',
                 book_description="1984 is a dystopian novella by George Orwell published in 1949, which follows the life of Winston Smith, a low ranking member of 'the Party', who is frustrated by the omnipresent eyes of the party, and its ominous ruler Big Brother. 'Big Brother' controls every aspect of people's lives.",
                 price=14.79,
                 year_published=1949,
                 copies_sold=50000000  # 50 million
                 )

    book3 = Book(book_name='Da Vinci Code',
                 book_genre='Mystery',
                 book_author='Dan Brown',
                 book_publisher='Doubleday',
                 book_description="The Da Vinci Code follows 'symbologist' Robert Langdon and cryptologist Sophie Neveu after a murder in the Louvre Museum in Paris causes them to become involved in a battle between the Priory of Sion and Opus Dei over the possibility of Jesus Christ and Mary Magdalene having had a child together.",
                 price=12.99,
                 year_published=2003,
                 copies_sold=80000000  # 80 million
                 )
    book4 = Book(book_name='Ugly Love',
                 book_genre='Fiction',
                 book_author='Atria',
                 book_publisher='Atria',
                 book_description="A Supernatural Crime book",
                 price=12.99,
                 year_published=2014,
                 copies_sold=90000000  # 90 million
                 )
    book5 = Book(book_name='Dark Matter',
                 book_genre='Fiction',
                 book_author='Dan Brown',
                 book_publisher='Ballantine Books',
                 book_description="outlandish plot of this SF thriller from Crouch (the Wayward Pines trilogy). Jason Dessen, a quantum physicist, once had a brilliant research career ahead of him",
                 price=15.99,
                 year_published=2016,
                 copies_sold=60000000  # 60 million
                 )
    book6 = Book(book_name='I Know Your Secret',
                 book_genre='Mystery',
                 book_author='Daphne Benedis-Grab',
                 book_publisher='Scholastic Press',
                 book_description="TBD",
                 price=12.99,
                 year_published=2003,
                 copies_sold=30000000  # 30 million
                 )
    book7 = Book(book_name='The 48 Laws of Power',
                 book_genre='Bussiness',
                 book_author='Robert Greene',
                 book_publisher='Penguin Books',
                 book_description="A moral, cunning, ruthless, and instructive, this piercing work distills three thousand years of the history of power into forty-eight well-explicated laws.",
                 price=19.99,
                 year_published=2003,
                 copies_sold=180000000  # 180 million
                 )
    book8 = Book(book_name='Where the Crawdads Sing',
                 book_genre='Fiction',
                 book_author='Delia Owens',
                 book_publisher='Penguin Publishing Group',
                 book_description="a painfully beautiful first novel that is at once a murder mystery, a coming-of-age narrative and a celebration of nature.",
                 price=12.99,
                 year_published=2021,
                 copies_sold=120000000  # 120 million
                 )
    db.session.add(book1)
    db.session.add(book2)
    db.session.add(book3)
    db.session.add(book4)
    db.session.add(book5)
    db.session.add(book6)
    db.session.add(book7)
    db.session.add(book8)


    test_user = User(first_name='William',
                     last_name='Herschel',
                     email='test@test.com',
                     password='P@ssw0rd')



    db.session.add(test_user)
    db.session.commit()
    print('Database seeded!')

#--------------------------Routes-------------------------------
@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/super_simple')
def super_simple():
    return jsonify(message='Hello from the Planetary API.'), 200


@app.route('/not_found')
def not_found():
    return jsonify(message='That resource was not found'), 404


@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message="Sorry " + name + ", you are not old enough."), 401
    else:
        return jsonify(message="Welcome " + name + ", you are old enough!")


@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name: str, age: int):
    if age < 18:
        return jsonify(message="Sorry " + name + ", you are not old enough."), 401
    else:
        return jsonify(message="Welcome " + name + ", you are old enough!")


@app.route('/books')
def books():
    book_list = Book.query.all()
    result = book_schema.dump(book_list)
    return jsonify(result)


@app.route('/register', methods=['GET', 'POST'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='That email already exists.'), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="User created successfully."), 201




@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        login_user(test)

        return jsonify(message='Login succeeded!', access_token=access_token)
    else:
        return jsonify(message="Bad email or password"), 401

@app.route('/CreditCard', methods=['GET', 'POST'])
def make_creditcard():

    CC_num = request.form['CC_num']
    test2 = Creditcard.query.filter_by(CC_num=CC_num).first()
    if test2:
        return jsonify(message='That credit card already exists.'), 409
    else:
        test_id = current_user.id
        creditcard_cvv = request.form['creditcard_cvv']
        creditcard_exp = request.form['creditcard_ex']
        credit_card = Creditcard(CC_num=CC_num,
                                 creditcard_cvv=creditcard_cvv,
                                 creditcard_exp=creditcard_exp,
                                 foreign_key=test_id)
        db.session.add(credit_card)
        db.session.commit()
        return jsonify(message="Credit Card added successfully."), 201

@app.route('/retrieve_password/<string:email>', methods=['GET'])
def retrieve_password(email: str):
    user = User.query.filter_by(email=email).first()
    if user:
        msg = Message("Your planetary API password is" + user.password,
                        sender = "admin@planetary-api.com",
                        recipients=[email])
        mail.send(msg)
        return jsonify(message="Password sent to " + email)
    else:
        return jsonify(message="That email doesn't exist")

@app.route('/user_details/<int:id>', methods=["GET"])
def user_details(id: int):
    user = User.query.filter_by(id=id).first()
    if user:
        result = user_schema.dump(user)
        return jsonify(result)
    else:
        return jsonify(message="User does not exist"), 404

@app.route('/book_genre/<string:book_genre>', methods=['GET'])
def get_book_by_genre(book_genre: String):
    book = Book.query.filter_by(book_genre=book_genre).all()
    if book:
        result = books_schema.dump(book)
        return jsonify(result)
    else:
        return jsonify(message="Book Genre does not exist"), 404


@app.route('/book_by/<string:book_author>', methods=['GET'])#Sprint 4
def book_by(book_author: String):
    book = Book.query.filter_by(book_author=book_author).all()
    if book:
        result = books_schema.dump(book)
        return jsonify(result)
    else:
        return jsonify(message="Author does not exist"), 404

@app.route('/update_user', methods=['PUT'])#Sprint 4
def update_user():
    email = request.form['email']
    user = User.query.filter_by(email=email).first()
    if user:
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.password =request.form['password']
        db.session.commit()
        return jsonify("User information updated"),202
    else:
        return jsonify("Email not recognized."), 404

@app.route('/all_cards/<int:foreign_key>', methods=['GET'])#Sprint 4
def all_cards(foreign_key: int):
    card = Creditcard.query.filter_by(foreign_key=foreign_key).all()
    if card:
        user = User.query.filter_by(id=foreign_key).first()
        result_user = user_schema.dump(user)
    
        results = Creditcards_schema.dump(card)
        return jsonify(result_user, results)
    else:
        return jsonify(message="User does not exist"), 404


#--------------------------Database Models-------------------------------
# database models
class User(db.Model, UserMixin):#parent
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    #Relationship Management
    link_to_others = relationship("Creditcard", backref="USERS")






class Book(db.Model):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True)
    book_name = Column(String)
    book_genre = Column(String)
    book_author = Column(String)
    book_publisher = Column(String)
    book_description = Column(String)
    price = Column(Float)
    year_published = Column(Integer)
    copies_sold = Column(Integer)
    book_rating = Column(Float)

class Creditcard(db.Model): #child
    __tablename__ = 'creditcard'
    creditcard_id = Column(Integer, primary_key=True)
    CC_num = Column(Integer)
    creditcard_cvv = Column(Integer)
    creditcard_exp = Column(Integer)


    #Relationship Management
    foreign_key = Column(Integer, ForeignKey('users.id'))


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')


class BookSchema(ma.Schema):
    class Meta:
        fields = ('book_id', 'book_name', 'book_genre', 'book_author', 'book_publisher',
                  'book_description', 'price', 'year_published', 'copies_sold', 'book_rating')

class CreditcardSchema(ma.Schema):
    class Meta:
        fields = ('creditcard_id', 'CC_num', 'creditcard_cvv', 'creditcard_exp', 'foreign_key')



user_schema = UserSchema()
users_schema = UserSchema(many=True)

book_schema = BookSchema()
books_schema = BookSchema(many=True)

Creditcard_schema=CreditcardSchema()
Creditcards_schema=CreditcardSchema(many=True)

#-----------------Load User-------------------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.debug = True
    app.run()