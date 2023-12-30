## EFfective Serializer Django

### Serialize Objects
#### Serializing
`Serializer` Serialize an object into python's native datatypes

```python
serializer = CommentSerializer(comment)
json = JsonRenderer().render(serializer.data)
```
Convert python's native data to json string with `JsonRenderer`

#### Deserializing
`Serializer` cann also deserializing native datatypes into complex object (create, update) `after validated the data`
##### Validate data
```python
data = JsonParser().parse(stream)
serializer = CommentSerializer(data=data)

serializer.is_valid()
# True
serializer.validated_data
# validated_data
```
##### Saving Object
For saving object, serializer must implement `create()` or `update()` method
```python
serializer = CommentSerializer(data=data)
serializer.is_valid()
serializer.save() # Will create new Instance

serializer = CommentSerializer(comment, data=data)
serializer.is_valid()
serializer.save() # Will update Instance
```
##### Overriding `.save()`
In some case we want `.save()` do some task after validate the data. Such as sending mail.
```
class ContactFormSerializer(serializers.Serializer):
    email = serializer.EmailField()
    message = serializer.CharField()

    def save(self):
        email = self.validated_data['email']
        message = self.validated_data['message']
        send_mail(to=email, message=message)
```
#### Validation
after calling `is_valid()` `serializer.validated_data` and `save()` method are available.
If not valid, the `.errors` contains all the error fields of serializer.
```
# serializer.errors
# {'email': ['Enter a valid e-mail address.'], 'created': ['This field is required.']}
```
`non_field_errors` key may also be presented, customize key name by specify `NON_FIELD_ERRORS_KEY` in `REST_FRAMEWORK` setting.
##### Raise Exception
`serializers.is_valid(raise_exception=True)`. Using this flag cause it to raise `ValidationError` if validate fail and will be handled by default exception handler by DRF and return a `400 HTTP` response to client.

#### Serializer.data VS Serializer.validated_data
The different between `serializer.data` and `serializer.validated_data`


| serializer.data    | serializer.validated_data |
| ----------------   | --------------------------|
| `read_only` fields | `read_only` field         |
| use in `serializing` object  | use in `deserializing` data |
| available after serialized data from `instance` that return the python native data represent the instence | available after validating `data input` |
| contain `readable fields` that specified in serilizers | contain `writable` fields that specified in serializers |

#### Accessing internal instance and data
- `.instance` is available if initialize serializer with an object or queryset
-  `.internal_data` is available if initialize serializer with an argument `data=..` otherwise the prop `.internal_data` wont exist

#### Partial Update
```
serializer = Comment(comment, data={'content': 'Foo'}, parital=True)
```
#### Serialize support serialize multiple Object but (not multiple update)
#### Extra context
```
serializer = UserSerializer(user, context={'request': request})
```
`.context` can be access in any field logic
### Customizing Serializer
#### Overriding `to_representation()`
#### Overriding `to_internal_data()`