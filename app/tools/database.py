from app.tools import helpers

def create(db, model, **params):
    new_entry = model(**params)
    db.session.add(new_entry)
    db.session.commit()

def retrieve(model, **filters):
    record = model.query.filter_by(**filters).first()
    return record

def retrieve_from_join(db, model1, model2, username):
    db.session.query(
        model1, model2 
    ).join(
        model2
    ).filter(
        model1.username == username
    ).all()
    data = db.session.query(model2).join(model1).filter(model1.username == username).all()
    print(data)
    
    return data
