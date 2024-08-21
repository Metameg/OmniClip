
def create(db, model, **params):
    new_entry = model(**params)
    db.session.add(new_entry)
    db.session.commit()

def retrieve(model, *complex_filters, **kwargs):
    query = model.query.filter_by(**kwargs)
    if complex_filters:
        query = query.filter(*complex_filters)  # Handles more complex filters
    return query.first()

def retrieve_from_join(db, model1, model2, username):
    db.session.query(
        model1, model2 
    ).join(
        model2
    ).filter(
        model1.username == username
    ).all()
    data = db.session.query(model2).join(model1).filter(model1.username == username).all()
    
    return data

def remove(db, model, path):
    media_to_delete = retrieve(model, path=path)

    try: 
        db.session.delete(media_to_delete)
        db.session.commit()
    except:
        print("Error deleting media file.")

