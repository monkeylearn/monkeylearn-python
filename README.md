# MonkeyLearn API for python

Official Python client for the [MonkeyLearn API](https://monkeylearn.com/api/). Build and run machine learning models for language processing from your Python apps.


Installation
---------------


You can use pip to install the library:

```bash
$ pip install monkeylearn
```

Alternatively you can just clone the repository and run the setup.py script:

```bash
$ python setup.py install
```


Usage
------


Before calling making requests to the API you need to create an instance of the MonkeyLearn client, using your account API Key:

```python
from monkeylearn import MonkeyLearn

# Instantiate the client Using your API key
ml = MonkeyLearn('<YOUR API TOKEN HERE>')
```

### Requests

From the MonkeyLearn client instance you can call any endpoint (checkout the [available endpoints](#available-endpoints) below). For example you can [classify](#classify) a list of texts (`data` parameter) using the public [Sentiment analysis classifier](https://app.monkeylearn.com/main/classifiers/cl_oJNMkt2V/):


```python
response = ml.classifiers.classify(
    model_id='cl_Jx8qzYJh,
    data=[
        'Great hotel with excellent location',
        'This is the worst hotel ever.',

    ]
)
```

### Responses

The response object returned by every endpoint call it's a `MonkeyLearnResponse` object. The `body` attribute has the parsed response from the API:

```python
print(response.body)
# =>  [
# =>      {
# =>          "text": "Hola amigo, como estás?",
# =>          "external_id": null,
# =>          "error": false,
# =>          "classifications": [
# =>              {
# =>                  "category_name": "Positive",
# =>                  "category_id": 1994,
# =>                  "confidence": 0.922,
# =>              }
# =>          ]
# =>      },
# =>      {
# =>          "text": "Hello my friend, how are you?",
# =>          "external_id": null,
# =>          "error": false,
# =>          "classifications": [
# =>              {
# =>                  "category_name": "Negative",
# =>                  "category_id": 1941,
# =>                  "confidence": 0.911,
# =>              }
# =>          ]
# =>      }
# =>  ]
```

You can also access other attributes in the response object to get information about the queries used or available:

```python
print(response.plan_queries_allowed)
# =>  300

print(response.plan_queries_remaining)
# =>  240

print(response.request_queries_used)
# =>  2
```

### Errors

Endpoint calls, may raise exceptions. Here's an example on how to handle them:

```python
from monkeylearn.exceptions import PlanQueryLimitError, MonkeyLearnException

try:
    response = ml.classifiers.classify('cl_XXXXXXXX', data=['My text'])
except PlanQueryLimitError as e:
    # No monthly queries left
    e.response  # The MonkeyLearnResponse object
    print(e.error_code, e.detail)
except MonkeyLearnException
    raise
```

Available exceptions:

| class                       | Description |
|-----------------------------|-------------|
| `MonkeyLearnException`      | Base class for every exception below                                  |
| `RequestParamsError`        | An invalid parameter was send. Checkout the exception message or response object for more information. |
| `AuthenticationError`       | Authentication failed, usually an invalid token was provided, check the exception message. More about [Authentication](https://monkeylearn.com/api/v3/#authentication). |
| `ForbiddenError`            | You don't have permissions to perform the action on the given resource. |
| `ModelLimitError`           | You have reached the custom model limit for your plan. |
| `ModelNotFound`             | The model does not exist, check the `model_id` |
| `CategoryNotFound`          | The classifier category does not exist, check the `category_id` parameter. |
| `PlanQueryLimitError`           | You have reached the monthly query limit for your plan. Consider upgrading your plan. More about [Plan query limits](https://monkeylearn.com/api/v3/#query-limits) |
| `PlanRateLimitError`        | You have sent too many requests in the last minute. Checkout the exception detail. More about [Plan rate limit](https://monkeylearn.com/api/v3/#plan-rate-limit). |
| `ConcurrencyRateLimitError` | You have sent too many requests in the last second. Checkout the exception detail. More about [Concurrency rate limit](https://monkeylearn.com/api/v3/#concurrecy-rate-limit). |


### Auto-batching

[Classify](#classify) and [Extract](#extract) enpoints may require more than one request to the MonkeyLearn API in order to process every text in the `data` parameter. If `auto_batch` is `True` (default) you don't have to keep the `data` length below the max allowed value (200), you can just pass the full list and the library will split the list and make the necessary requests. If `sleep_if_throttled` is `True` (default) it will also wait and retry if the API throttled a request.

Let's say you send a `data` parameter with 300 texts and `auto_batch` enabled. The list will be split internally and two requests will be sent to MonkeyLearn, the first one with the first 200 texts and the second one with the last 100. If all requests respond with an 200 status code the responses will be appended and you will get the 300 classifications as usual in the `MonkeyLearnResponse.body` attribute:

``` python
data = ['Text to classify'] * 300
response = ml.classifiers.classify('cl_oJNMkt2V', data)
assert len(response.body) == 300  # => True
```

Now let's say you only had 200 queries left when trying the previous example, the second internal request will fail since you don't have queries left after the first batch and a `PlanQueryLimitError` exception will be raised. If you don't manage this exception with an `except` clause the first 200 classifications that did worked are lost. Here's how you should handle that case:

``` python
from monkeylearn.exceptions import PlanQueryLimitError

data = ['Text to classify'] * 300
batch_size = 200

try:
    response = ml.classifiers.classify('cl_oJNMkt2V', data, batch_size=batch_size)
except PlanQueryLimitError as e:
    partial_response = e.response.body  # The body of the successful responses
    non_2xx_raw_responses = r.response.failed_raw_responses  # List of requests responses objects

predictions = response.body
```


This is very convenient and usually it's enough. If you need more flexibility you can manage batching and rate limits yourself.

``` python
from monkeylearn.exceptions import PlanQueryLimitError, ConcurrencyRateLimitError, PlanRateLimitError

data = ['Text to classify'] * 300
batch_size = 200
predictions = []

for i in range(0, len(data['data']), batch_size):
    batch_data = data[i:i + batch_size]

    retry = False
    while retry:
        try:
            response = ml.classifiers.classify('cl_oJNMkt2V', batch_data, auto_batch=False,
                                               sleep_if_throttled=False)
        except PlanRateLimitError:
            retry = True
            seconds = re.findall(r'available in (\d+) seconds', body['detail'])[0]
            sleep(seconds)
        except ConcurrencyRateLimitError:
            retry = True
            sleep(2)
        except PlanQueryLimitError:
            print('Out of queries')
            break
        else:
            retry = False

    predictions.extend(response.body)

```

This way you'll be able to control every request that's sent to the MonkeyLearn API.

Available endpoints
------------------------

### Classifiers

#### Classify


```python
def MonkeyLearn.classifiers.classify(model_id, data, production_model=None, batch_size=200,
                                     auto_batch=True, sleep_if_throttle=True)
```

Parameters:

| Parameter          |Type               | Description                                               |
|--------------------|-------------------|-----------------------------------------------------------|
|*model_id*          |`str`              |Classifier ID. Always start with *'cl'*, example *'cl_oJNMkt2V'*. |
|*data*              |`list[str or dict]`|A list of up to 200 data elements to classify. Each element must be a *string* with the text or a *dict* with the required `text` key and the text as the value and an optional `external_id` key with a string that will be included in the response.  |
|*production_model*  |`bool`             |Indicates if the classifications are performed by the production model. Only use this parameter on *custom models*. Note that you first need to deploy the production model from the UI model settings or using the [Classifier deploy endpoint](#deploy). |
|*batch_size*        |`int`              |Max amount of texts each request will send to MonkeyLearn. |
|*auto_batch*         |`bool`             |Split the `data` list into smaller valid lists and send each one in separate request to MonkeyLearn and merge the responses together. |
|*sleep_if_throttle* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits) sleep and retry the request. |

Example:

```python
response = ml.classifiers.classify('cl_oJNMkt2V', data)
```

<br>
#### Classifier detail


```python
def MonkeyLearn.classifiers.detail(model_id)
```

Parameters:

| Parameter          |Type               | Description                                               |
|--------------------|-------------------|-----------------------------------------------------------|
|*model_id*          |`str`              |Classifier ID. Always start with *'cl'*, example *'cl_oJNMkt2V'*. |
|*sleep_if_throttle* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits) sleep and retry the request. |

Example:

```python
response = ml.classifiers.detail('cl_oJNMkt2V')
```

<br>
#### Create Classifier


```python
def MonkeyLearn.classifiers.create(name, description='', algorithm='nb, language='en,
                                   max_features=10000, ngram_range=[1, 1], use_stemming=True,
                                   preprocess_numbers=True, preprocess_social_media=False,
                                   normalize_weights=True, stopwords=False, whitelist=None,
                                   sleep_if_throttled=True)
```

Parameters:

Parameter | Type | Description
--------- | ------- | -----------
name | `str` | The name of the model.
description | `str` | The description of the model.
algorithm | `str` | The [algorithm](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-changing-the-algorithm) used when training the model. It can either be "nb" or "svm".
language | `str` | The [language](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-language) of the model. Full list of [supported languages](https://monkeylearn.com/api/v3/#classifier-detail).
max_features | `int` | The [maximum amount of features](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-max-features) used when training the model. Between 10 and 100000.
ngram_range | `tuple[int,int]` | Indicates which [N-gram range](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-n-gram-range) used when training the model. A list of two numbers between 1 and 3. The first one indicates the minimum and the second one the maximum N for the N-grams used.
use_stemming | `bool`| Indicates whether [stemming](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-stemming) is used when training the model.
preprocess_numbers | `bool` | Indicates whether [number preprocessing](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-preprocess-numbers) is done when training the model.
preprocess_social_media | `bool` | Indicates whether [preprocessing for social media](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-social-media-preprocessing-and-regular-expressions) is done when training the model.
normalize_weights | `bool` | Indicates whether [weights will be normalized](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-normalize-weights) when training the model.
stopwords | `bool or list` |  The list of [stopwords](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-filter-stopwords) used when training the model. Use false for no stopwords, true for the default stopwords, or an array of strings for custom stopwords.
whitelist | `list` | The [whitelist](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-whitelist) of words used when training the model.
|*sleep_if_throttle* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits) sleep and retry the request. |

Example:

```python
response = ml.classifiers.create(name='Language detection', language='multi_language')
```

<br>
#### Delete classifier


```python
def MonkeyLearn.classifiers.delete(model_id, sleep_if_throttled=True)
```

Parameters:

| Parameter          |Type               | Description                                               |
|--------------------|-------------------|-----------------------------------------------------------|
|*model_id*          |`str`              |Classifier ID. Always start with *'cl'*, example *'cl_oJNMkt2V'*. |
|*sleep_if_throttle* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits) sleep and retry the request. |

Example:

```python
response = ml.classifiers.delete('cl_JkNtoMV2')
```

<br>
#### List Classifiers


```python
def MonkeyLearn.classifiers.list(page=1, per_page=20, sleep_if_throttled=True)
```

Parameters:

|Parameter          |Type               | Description |
|--------------------|-------------------|-------------|
|*page*              |`int`              |Specifies which page to get.|
|*per_page*          |`int`              |Specifies how many items to return per page. |
|*sleep_if_throttle* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits) sleep and retry the request. |

Example:

```python
response = ml.classifiers.list(page=2)
```

<br>
#### Deploy


```python
def MonkeyLearn.classifiers.deploy(model_id, sleep_if_throttled=True)
```

Parameters:

| Parameter          |Type               | Description                                               |
|--------------------|-------------------|-----------------------------------------------------------|
|*model_id*          |`str`              |Classifier ID. Always start with *'cl'*, example *'cl_oJNMkt2V'*. |
|*sleep_if_throttle* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits) sleep and retry the request. |

Example:

```python
response = ml.classifiers.deploy('cl_JkNtoMV2')
```

<br>
#### Category detail


```python
def MonkeyLearn.classifiers.categories.detail(model_id, category_id, sleep_if_throttled=True)
```

Parameters:

| Parameter          |Type               | Description                                               |
|--------------------|-------------------|-----------------------------------------------------------|
|*model_id*          |`str`              |Classifier ID. Always start with *'cl'*, example *'cl_oJNMkt2V'*. |
|*category_id*       |`int`              |Category ID. |
|*sleep_if_throttle* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits) sleep and retry the request. |

Example:

``` python
response = ml.classifiers.categories.detail('cl_JkNtoMV2', 25)
```

<br>
#### Create category


```python
def MonkeyLearn.classifiers.categories.create(model_id, name, parent_id=None, sleep_if_throttled=True)
```

Parameters:

| Parameter          |Type               | Description                                               |
|--------------------|-------------------|-----------------------------------------------------------|
|*model_id*          |`str`              |Classifier ID. Always start with *'cl'*, example *'cl_oJNMkt2V'*. |
|*name*              |`str`              |The name of the new category. |
|*parent_id*         |`int`              |**DEPRECATED**. The ID of the parent category. |
|*sleep_if_throttle* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits) sleep and retry the request. |

Example:

```python
response = ml.classifiers.categories.create('cl_XXXXXXXX, 'Positive')
```

<br>
#### Edit category


```python
def MonkeyLearn.classifiers.categories.edit(model_id, category_id, name=None, parent_id=None,
                                            sleep_if_throttled=True)
```

Parameters:

| Parameter          |Type               | Description                                               |
|--------------------|-------------------|-----------------------------------------------------------|
|*model_id*          |`str`              |Classifier ID. Always start with *'cl'*, example *'cl_oJNMkt2V'*. |
|*category_id*       |`int`              |Category ID. |
|*name*              |`str`              |The new name of the category. |
|*sleep_if_throttle* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits) sleep and retry the request. |

Example:

```python
response = ml.classifiers.categories.edit('cl_XXXXXXXX, 25, 'New name')
```

<br>
#### Delete category


```python
def MonkeyLearn.classifiers.categories.delete(model_id, category_id, move_data_to=None,
                                              sleep_if_throttled=True)
```

Parameters:

| Parameter          |Type               | Description                                               |
|--------------------|-------------------|-----------------------------------------------------------|
|*model_id*          |`str`              |Classifier ID. Always start with *'cl'*, example *'cl_oJNMkt2V'*. |
|*category_id*       |`int`              |Category ID. |
|*move_data_to*      |`int`              |An optional category ID. If provided, training data associated with the category will be moved to the specified category before deletion. |
|*sleep_if_throttle* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits) sleep and retry the request. |

Example:

```python
response = ml.classifiers.categories.delete('cl_XXXXXXXX, 25)
```

<br>
#### Upload training data


```python
def MonkeyLearn.classifiers.upload_data(model_id, data, sleep_if_throttled=True)
```

Parameters:

| Parameter          |Type               | Description                                               |
|--------------------|-------------------|-----------------------------------------------------------|
|*model_id*          |`str`              |Classifier ID. Always start with *'cl'*, example *'cl_oJNMkt2V'*. |
|*data*              |`list[dict]        |A list of dicts with the keys described below.
|*sleep_if_throttle* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits) sleep and retry the request. |

`data` dict keys:

|Key             | Description |
|---------       | ----------- |
|text | A *string* of the text to upload.|
|categories | An optional *list* of category ID integers. The text will be tagged with each of these categories.|
|marks | An optional *list* of *string*. Each one represents a mark that will be associated with the text. Marks will be created if needed.|

Example:

```python
response = ml.classifiers.upload_data(
    model_id='cl_XXXXXXXX',
    data=[{'text': 'text 1', 'categories': [15, 20]}]
)
```


<br>
### Extractors


#### Extract


```python
def MonkeyLearn.extractors.extract(model_id, data, production_model=False, batch_size=200,
                                   sleep_if_throttled=True, extra_args=None)
```

Parameters:

| Parameter          |Type               | Description                                               |
|--------------------|-------------------|-----------------------------------------------------------|
|*model_id*          |`str`              |Extractor ID. Always start with *'ex_'*, example *'ex_oJNMkt2V'*. |
|*data*              |`list[str or dict]`|A list of up to 200 data elements to extract. Each element must be a *string* with the text or a *dict* with the required `text` key and the text as the value and an optional `external_id` key with a string that will be included in the response.  |
|*production_model*  |`bool`             |Indicates if the extractions are performed by the production model. Only use this parameter on *custom models*. Note that you first need to deploy the production model from the UI model settings. |
|*batch_size*        |`int`              |Max amount of texts each request will send to MonkeyLearn. |
|*sleep_if_throttle* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits) sleep and retry the request. |

Example:

```python
response = ml.extractors.extract('ex_NokMJtV2',
                                 data=['First text', {'text': 'Second text', 'extranal_id': '2'}])
```

<br>
#### Extractor detail


```python
def MonkeyLearn.extractors.detail(model_id, sleep_if_throttled=True)
```

Parameters:

| Parameter          |Type               | Description                                               |
|--------------------|-------------------|-----------------------------------------------------------|
|*model_id*          |`str`              |Extractor ID. Always start with *'ex_'*, example *'ex_oJNMkt2V'*. |
|*sleep_if_throttle* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits) sleep and retry the request. |

Example:

```python
response = ml.extractors.detail('ex_NokMJtV2')
```


<br>
#### Extractor list


```python
def MonkeyLearn.extractors.list(page=1, per_page=20, sleep_if_throttled=True)
```

Parameters:

|Parameter           |Type               | Description |
|--------------------|-------------------|-------------|
|*page*              |`int`              |Specifies which page to get.|
|*per_page*          |`int`              |Specifies how many items to return per page. |
|*sleep_if_throttle* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits) sleep and retry the request. |

Example:

```python
response = ml.extractors.list(page=2)
```
