from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItems
app = Flask(__name__)


engine = create_engine('sqlite:///catelogitems.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Route for landing page, the main page
@app.route('/')
@app.route('/catelog')
def categoryShow():
    category = session.query(Category).all()
    return render_template('main.html', category=category)

# Route for catelog modification
@app.route('/catelog/new', methods=['GET','POST'])
def newCategory():
	"""Page to create a new category."""
	if request.method == 'POST':
		newCat = Category(name = request.form['name'])
		session.add(newCat)
		session.commit()
		return redirect(url_for('categoryShow'))
	else:
		return render_template('newcategory.html')


@app.route('/catelog/<int:category_id>/edit', methods=['GET','POST'])
def editCategory(category_id):
	editedCategory = session.query(Category).filter_by(id = category_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedCategory.name = request.form['name']
		session.add(editedCategory)
		session.commit()
		return redirect(url_for('categoryShow'))
	else:
		return render_template('editcategory.html', category_id = category_id, category = editedCategory)

@app.route('/catelog/<int:category_id>/delete', methods=['GET','POST'])
def deleteCategory(category_id):
	"""Page to delete a category. Task complete"""
	deletedCategory = session.query(Category).filter_by(id = category_id).one()
	if request.method == 'POST':
		session.delete(deletedCategory)
		session.commit()
		return redirect(url_for('categoryShow'))
	else:
		return render_template('deletecategory.html', category_id = category_id, category = deletedCategory)

# Route for Items modification
@app.route('/catelog/<int:category_id>')
def itemPage(category_id):
	category = session.query(Category).all()
	items = session.query(CategoryItems).filter_by(category_id = category_id).all()
	return render_template('itempage.html', category = category, category_id=category_id, items=items)

@app.route('/catelog/<int:category_id>/new', methods = ['GET','POST'])
def newItem(category_id):
	"""Page to add a new item to the specific category"""
	if request.method == 'POST':
		newItem = CategoryItems(name = request.form['name'], description = request.form['description'],category_id=category_id)
		session.add(newItem)
		session.commit()
		return redirect(url_for('itemPage', category_id=category_id))
	else:
		return render_template('newitem.html', category_id=category_id)


@app.route('/catelog/<int:category_id>/<int:item_id>/edit', methods=['GET','POST'])
def editItem(category_id, item_id):
	editedItem = session.query(CategoryItems).filter_by(id = item_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
			editedItem.description = request.form['description']
		session.add(editedItem)
		session.commit()
		return redirect(url_for('itemPage', category_id=category_id))
	else:
		return render_template('edititem.html', category_id = category_id, item_id = item_id, item = editedItem)

@app.route('/catelog/<int:category_id>/<int:item_id>/delete', methods=['GET','POST'])
def deleteItem(category_id, item_id):
	"""Page to delete a item."""
	deletedItem = session.query(CategoryItems).filter_by(id = item_id).one()
	if request.method == 'POST':
		session.delete(deletedItem)
		session.commit()
		return redirect(url_for('itemPage', category_id=category_id))
	else:
		return render_template('deleteitem.html', category_id = category_id, item_id = item_id, item = deletedItem)
	

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8888)