# What's this

Python Google Cloud Datastore simple base object.


# Usage

Create your model object by making subclass of Base.
```python
from base import Base

class Contact(Base):
    @property
    def exclude_from_indexes(self):
        return ['name', 'email', 'message']
```


```python
# Create

contact = Contact(name='taro', email='taro@example.com', message='hello, world')
contact.put()

# Find
contact = Contact.query().fetch(1)

# Read
print(contact['name'])

# Update
contact['name'] = 'jiro'
contact.put()
```
