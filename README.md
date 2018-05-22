# MonkeyLearn API for Python

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


Before making requests to the API you need to create an instance of the MonkeyLearn client, using your [account API Key](https://app.monkeylearn.com/main/my-account/tab/api-keys/):

```python
from monkeylearn import MonkeyLearn

# Instantiate the client Using your API key
ml = MonkeyLearn('<YOUR API TOKEN HERE>')
```

### Requests

From the MonkeyLearn client instance you can call any endpoint (check the [available endpoints](#available-endpoints) below). For example you can [classify](#classify) a list of texts using the public [Sentiment analysis classifier](https://app.monkeylearn.com/main/classifiers/cl_oJNMkt2V/):


```python
response = ml.classifiers.classify(
    model_id='cl_Jx8qzYJh',
    data=[
        'Great hotel with excellent location',
        'This is the worst hotel ever.'
    ]
)

```

### Responses

The response object returned by every endpoint call is a `MonkeyLearnResponse` object. The `body` attribute has the parsed response from the API:

```python
print(response.body)
# =>  [
# =>      {
# =>          'text': 'Great hotel with excellent location',
# =>          'external_id': null,
# =>          'error': false,
# =>          'classifications': [
# =>              {
# =>                  'tag_name': 'Positive',
# =>                  'tag_id': 1994,
# =>                  'confidence': 0.922,
# =>              }
# =>          ]
# =>      },
# =>      {
# =>          'text': 'This is the worst hotel ever.',
# =>          'external_id': null,
# =>          'error': false,
# =>          'classifications': [
# =>              {
# =>                  'tag_name': 'Negative',
# =>                  'tag_id': 1941,
# =>                  'confidence': 0.911,
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

Endpoint calls may raise exceptions. Here is an example on how to handle them:

```python
from monkeylearn.exceptions import PlanQueryLimitError, MonkeyLearnException

try:
    response = ml.classifiers.classify('[MODEL_ID]', data=['My text'])
except PlanQueryLimitError as e:
    # No monthly queries left
    # e.response contains the MonkeyLearnResponse object
    print(e.error_code, e.detail)
except MonkeyLearnException:
    raise
```

Available exceptions:

| class                       | Description |
|-----------------------------|-------------|
| `MonkeyLearnException`      | Base class for every exception below.                                  |
| `RequestParamsError`        | An invalid parameter was send. Check the exception message or response object for more information. |
| `AuthenticationError`       | Authentication failed, usually because an invalid token was provided. For more information, check the exception message. More about [Authentication](https://monkeylearn.com/api/v3/#authentication). |
| `ForbiddenError`            | You don't have permissions to perform the action on the given resource. |
| `ModelLimitError`           | You have reached the custom model limit for your plan. |
| `ModelNotFound`             | The model does not exist, check the `model_id`. |
| `TagNotFound`               | The tag does not exist, check the `tag_id` parameter. |
| `PlanQueryLimitError`       | You have reached the monthly query limit for your plan. Consider upgrading your plan. More about [Plan query limits](https://monkeylearn.com/api/v3/#query-limits). |
| `PlanRateLimitError`        | You have sent too many requests in the last minute. Check the exception detail. More about [Plan rate limit](https://monkeylearn.com/api/v3/#plan-rate-limit). |
| `ConcurrencyRateLimitError` | You have sent too many requests in the last second. Check the exception detail. More about [Concurrency rate limit](https://monkeylearn.com/api/v3/#concurrecy-rate-limit). |
| `ModuleStateError`          | The state of the module is invalid. Check the exception detail.  |


### Auto-batching

[Classify](#classify) and [Extract](#extract) endpoints may require more than one request to the MonkeyLearn API in order to process every text in the `data` parameter. If the `auto_batch` parameter is `True` (which is the default value) you don't have to keep the `data` length below the max allowed value (200), you can just pass the full list and the library will handle the bactching making the necessary requests. If the `retry_if_throttled` parameter is `True` (which is the default value) it will also wait and retry if the API throttled a request.

Let's say you send a `data` parameter with 300 texts and `auto_batch` enabled. The list will be split internally and two requests will be sent to MonkeyLearn, the first one with the first 200 texts and the second one with the last 100. If all requests respond with an 200 status code the responses will be appended and you will get the 300 classifications as usual in the `MonkeyLearnResponse.body` attribute:

``` python
data = ['Text to classify'] * 300
response = ml.classifiers.classify('[MODEL_ID]', data)
assert len(response.body) == 300  # => True
```

Now let's say you only had 200 queries left when trying the previous example, the second internal request will fail since you don't have queries left after the first batch and a `PlanQueryLimitError` exception will be raised. The first 200 (successful) classifications will be in the exception object. However, if you don't manage this exception with an `except` clause, those first 200 classifications that did work will be lost. Here's how you should handle that case:

``` python
from monkeylearn.exceptions import PlanQueryLimitError

data = ['Text to classify'] * 300
batch_size = 200

try:
    response = ml.classifiers.classify('[MODEL_ID]', data, batch_size=batch_size)
except PlanQueryLimitError as e:
    partial_predictions = e.response.body  # The body of the successful responses
    non_2xx_raw_responses = r.response.failed_raw_responses  # List of requests responses objects
else:
    predictions = response.body
```

This is very convenient and usually should be enough. If you need more flexibility, you can manage batching and rate limits yourself.

``` python
import re
from time import sleep
from monkeylearn.exceptions import PlanQueryLimitError, ConcurrencyRateLimitError, PlanRateLimitError

data = ['Text to classify'] * 300
batch_size = 200
predictions = []

for i in range(0, len(data), batch_size):
    batch_data = data[i:i + batch_size]

    retry = True
    while retry:
        try:
            response = ml.classifiers.classify('[MODEL_ID]', batch_data, auto_batch=False,
                                               retry_if_throttled=False)
        except PlanRateLimitError:
            retry = True
            seconds = int(re.findall(r'available in (\d+) seconds', resoponse.body['detail'])[0])
            sleep(seconds)
        except ConcurrencyRateLimitError:
            retry = True
            sleep(2)
        except PlanQueryLimitError:
            raise
        else:
            retry = False

    predictions.extend(response.body)
```

This way you'll be able to control every request that's sent to the MonkeyLearn API.

Available endpoints
------------------------

These are all the endpoints of the API. For more information about each endpoint, check out the [API documentation](https://monkeylearn.com/api/v3/).

### Classifiers

#### [Classify](https://monkeylearn.com/api/v3/?shell#classify)


```python
def MonkeyLearn.classifiers.classify(model_id, data, production_model=False, batch_size=200,
                                     auto_batch=True, retry_if_throttled=True)
```

Parameters:

| Parameter          |Type               | Description                                               |
|--------------------|-------------------|-----------------------------------------------------------|
|*model_id*          |`str`              |Classifier ID. Always starts with `'cl'`, for example `'cl_oJNMkt2V'`. |
|*data*              |`list[str or dict]`|A list of up to 200 data elements to classify. Each element must be a *string* with the text or a *dict* with the required `text` key and the text as the value and an optional `external_id` key with a string that will be included in the response.  |
|*production_model*  |`bool`             |Indicates if the classifications are performed by the production model. Only use this parameter with *custom models* (not with the public ones). Note that you first need to deploy the production model from the UI model settings or using the [Classifier deploy endpoint](#deploy). |
|*batch_size*        |`int`              |Max amount of texts each request will send to MonkeyLearn. A number from 1 to 200. |
|*auto_batch*         |`bool`             |Split the `data` list into smaller valid lists, send each one in separate request to MonkeyLearn, and merge the responses together. |
|*retry_if_throttled* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits), sleep and retry the request. |

Example:

```python
data = ['First text', {'text': 'Second text', 'external_id': '2'}]
response = ml.classifiers.classify('[MODEL_ID]', data)
```

<br>

#### [Classifier detail](https://monkeylearn.com/api/v3/?shell#classifier-detail)


```python
def MonkeyLearn.classifiers.detail(model_id, retry_if_throttled=True)
```

Parameters:

| Parameter          |Type               | Description                                               |
|--------------------|-------------------|-----------------------------------------------------------|
|*model_id*          |`str`              |Classifier ID. Always starts with `'cl'`, for example `'cl_oJNMkt2V'`. |
|*retry_if_throttled* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits), sleep and retry the request. |

Example:

```python
response = ml.classifiers.detail('[MODEL_ID]')
```

<br>

#### [Create Classifier](https://monkeylearn.com/api/v3/?shell#create-classifier)


```python
def MonkeyLearn.classifiers.create(name, description='', algorithm='nb', language='en',
                                   max_features=10000, ngram_range=(1, 1), use_stemming=True,
                                   preprocess_numbers=True, preprocess_social_media=False,
                                   normalize_weights=True, stopwords=True, whitelist=None,
                                   retry_if_throttled=True)
```

Parameters:

Parameter | Type | Description
--------- | ------- | -----------
*name* | `str` | The name of the model.
*description* | `str` | The description of the model.
*algorithm* | `str` | The [algorithm](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-changing-the-algorithm) used when training the model. It can either be "nb" or "svm".
*language* | `str` | The [language](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-language) of the model. Full list of [supported languages](https://monkeylearn.com/api/v3/#classifier-detail).
*max_features* | `int` | The [maximum amount of features](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-max-features) used when training the model. Between 10 and 100000.
*ngram_range* | `tuple(int,int)` | Indicates which [N-gram range](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-n-gram-range) used when training the model. A list of two numbers between 1 and 3. The first one indicates the minimum and the second one the maximum N for the N-grams used.
*use_stemming* | `bool`| Indicates whether [stemming](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-stemming) is used when training the model.
*preprocess_numbers* | `bool` | Indicates whether [number preprocessing](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-preprocess-numbers) is done when training the model.
*preprocess_social_media* | `bool` | Indicates whether [preprocessing for social media](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-social-media-preprocessing-and-regular-expressions) is done when training the model.
*normalize_weights* | `bool` | Indicates whether [weights will be normalized](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-normalize-weights) when training the model.
*stopwords* | `bool or list` |  The list of [stopwords](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-filter-stopwords) used when training the model. Use false for no stopwords, true for the default stopwords, or a list of strings for custom stopwords.
*whitelist* | `list` | The [whitelist](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-whitelist) of words used when training the model.
*retry_if_throttled* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits), sleep and retry the request. |

Example:

```python
response = ml.classifiers.create(name='New classifier', stopwords=True)
```
<br>

#### [Edit Classifier](https://monkeylearn.com/api/v3/?shell#edit-classifier)


```python
def MonkeyLearn.classifiers.edit(model_id, name=None, description=None, algorithm=None,
                                 language=None, max_features=None, ngram_range=None,
                                 use_stemming=None, preprocess_numbers=None,
                                 preprocess_social_media=None, normalize_weights=None,
                                 stopwords=None, whitelist=None, retry_if_throttled=None)
```

Parameters:

Parameter | Type | Description
--------- | ------- | -----------
|*model_id*          |`str`              |Classifier ID. Always starts with `'cl'`, for example `'cl_oJNMkt2V'`. |
*name* | `str` | The name of the model.
*description* | `str` | The description of the model.
*algorithm* | `str` | The [algorithm](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-changing-the-algorithm) used when training the model. It can either be "nb" or "svm".
*language* | `str` | The [language](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-language) of the model. Full list of [supported languages](https://monkeylearn.com/api/v3/#classifier-detail).
*max_features* | `int` | The [maximum amount of features](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-max-features) used when training the model. Between 10 and 100000.
*ngram_range* | `tuple(int,int)` | Indicates which [N-gram range](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-n-gram-range) used when training the model. A list of two numbers between 1 and 3. The first one indicates the minimum and the second one the maximum N for the N-grams used.
*use_stemming* | `bool`| Indicates whether [stemming](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-stemming) is used when training the model.
*preprocess_numbers* | `bool` | Indicates whether [number preprocessing](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-preprocess-numbers) is done when training the model.
*preprocess_social_media* | `bool` | Indicates whether [preprocessing for social media](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-social-media-preprocessing-and-regular-expressions) is done when training the model.
*normalize_weights* | `bool` | Indicates whether [weights will be normalized](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-normalize-weights) when training the model.
*stopwords* | `bool or list` |  The list of [stopwords](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-filter-stopwords) used when training the model. Use false for no stopwords, true for the default stopwords, or a list of strings for custom stopwords.
*whitelist* | `list` | The [whitelist](http://help.monkeylearn.com/tips-and-tricks-for-custom-modules/parameters-whitelist) of words used when training the model.
*retry_if_throttled* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits), sleep and retry the request. |

Example:

```python
response = ml.classifiers.edit('[MODEL_ID]', description='The new description of the classifier')
```
<br>

#### [Delete classifier](https://monkeylearn.com/api/v3/?shell#delete-classifier)


```python
def MonkeyLearn.classifiers.delete(model_id, retry_if_throttled=True)
```

Parameters:

| Parameter          |Type               | Description                                               |
|--------------------|-------------------|-----------------------------------------------------------|
|*model_id*          |`str`              |Classifier ID. Always starts with `'cl'`, for example `'cl_oJNMkt2V'`. |
|*retry_if_throttled* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits), sleep and retry the request. |

Example:

```python
response = ml.classifiers.delete('[MODEL_ID]')
```

<br>

#### [List Classifiers](https://monkeylearn.com/api/v3/?shell#list-classifiers)


```python
def MonkeyLearn.classifiers.list(page=1, per_page=20, retry_if_throttled=True)
```

Parameters:

|Parameter          |Type               | Description |
|--------------------|-------------------|-------------|
|*page*              |`int`              |Specifies which page to get.|
|*per_page*          |`int`              |Specifies how many items to return per page. |
|*retry_if_throttled* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits), sleep and retry the request. |

Example:

```python
response = ml.classifiers.list(page=2)
```

<br>

#### [Deploy](https://monkeylearn.com/api/v3/?shell#deploy)


```python
def MonkeyLearn.classifiers.deploy(model_id, retry_if_throttled=True)
```

Parameters:

| Parameter          |Type               | Description                                               |
|--------------------|-------------------|-----------------------------------------------------------|
|*model_id*          |`str`              |Classifier ID. Always starts with `'cl'`, for example `'cl_oJNMkt2V'`. |
|*retry_if_throttled* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits), sleep and retry the request. |

Example:

```python
response = ml.classifiers.deploy('[MODEL_ID]')
```

<br>

#### [Tag detail](https://monkeylearn.com/api/v3/?shell#classify)


```python
def MonkeyLearn.classifiers.tags.detail(model_id, tag_id, retry_if_throttled=True)
```

Parameters:

| Parameter          |Type               | Description                                               |
|--------------------|-------------------|-----------------------------------------------------------|
|*model_id*          |`str`              |Classifier ID. Always starts with `'cl'`, for example `'cl_oJNMkt2V'`. |
|*tag_id*       |`int`              |Tag ID. |
|*retry_if_throttled* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits), sleep and retry the request. |

Example:

``` python
response = ml.classifiers.tags.detail('[MODEL_ID]', 25)
```

<br>

#### [Create tag](https://monkeylearn.com/api/v3/?shell#create-tag)


```python
def MonkeyLearn.classifiers.tags.create(model_id, name, parent_id=None, retry_if_throttled=True)
```

Parameters:

| Parameter          |Type               | Description                                               |
|--------------------|-------------------|-----------------------------------------------------------|
|*model_id*          |`str`              |Classifier ID. Always starts with `'cl'`, for example `'cl_oJNMkt2V'`. |
|*name*              |`str`              |The name of the new tag. |
|*parent_id*         |`int`              |**DEPRECATED** (only for v2 models). The ID of the parent tag. |
|*retry_if_throttled* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits), sleep and retry the request. |

Example:

```python
response = ml.classifiers.tags.create('[MODEL_ID]', 'Positive')
```

<br>

#### [Edit tag](https://monkeylearn.com/api/v3/?shell#edit-tag)


```python
def MonkeyLearn.classifiers.tags.edit(model_id, tag_id, name=None, parent_id=None,
                                      retry_if_throttled=True)
```

Parameters:

| Parameter          |Type               | Description                                               |
|--------------------|-------------------|-----------------------------------------------------------|
|*model_id*          |`str`              |Classifier ID. Always starts with `'cl'`, for example `'cl_oJNMkt2V'`. |
|*tag_id*       |`int`              |Tag ID. |
|*name*              |`str`              |The new name of the tag. |
|*retry_if_throttled* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits), sleep and retry the request. |

Example:

```python
response = ml.classifiers.tags.edit('[MODEL_ID]', 25, 'New name')
```

<br>

#### [Delete tag](https://monkeylearn.com/api/v3/?shell#delete-tag)


```python
def MonkeyLearn.classifiers.tags.delete(model_id, tag_id, move_data_to=None,
                                        retry_if_throttled=True)
```

Parameters:

| Parameter          |Type               | Description                                               |
|--------------------|-------------------|-----------------------------------------------------------|
|*model_id*          |`str`              |Classifier ID. Always starts with `'cl'`, for example `'cl_oJNMkt2V'`. |
|*tag_id*       |`int`              |Tag ID. |
|*move_data_to*      |`int`              |An optional tag ID. If provided, training data associated with the tag will be moved to the specified tag before deletion. |
|*retry_if_throttled* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits), sleep and retry the request. |

Example:

```python
response = ml.classifiers.tags.delete('[MODEL_ID]', 25)
```

<br>

#### [Upload training data](https://monkeylearn.com/api/v3/?shell#upload-data)


```python
def MonkeyLearn.classifiers.upload_data(model_id, data, retry_if_throttled=True)
```

Parameters:

| Parameter          |Type               | Description                                               |
|--------------------|-------------------|-----------------------------------------------------------|
|*model_id*          |`str`              |Classifier ID. Always starts with `'cl'`, for example `'cl_oJNMkt2V'`. |
|*data*              |`list[dict]`        |A list of dicts with the keys described below.
|*retry_if_throttled* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits), sleep and retry the request. |

`data` dict keys:

|Key             | Description |
|---------       | ----------- |
|text | A *string* of the text to upload.|
|tags | An optional *list* of tag ID integers. The text will be tagged with each of these tags.|
|marks | An optional *list* of *string*. Each one represents a mark that will be associated with the text. Marks will be created if needed.|

Example:

```python
response = ml.classifiers.upload_data(
    model_id='[MODEL_ID]',
    data=[{'text': 'text 1', 'tags': [15, 20]}]
)
```

<br>

### Extractors


#### [Extract](https://monkeylearn.com/api/v3/?shell#extract)


```python
def MonkeyLearn.extractors.extract(model_id, data, production_model=False, batch_size=200,
                                   retry_if_throttled=True, extra_args=None)
```

Parameters:

| Parameter          |Type               | Description                                               |
|--------------------|-------------------|-----------------------------------------------------------|
|*model_id*          |`str`              |Extractor ID. Always starts with `'ex'`, for example `'ex_oJNMkt2V'`. |
|*data*              |`list[str or dict]`|A list of up to 200 data elements to extract. Each element must be a *string* with the text or a *dict* with the required `text` key and the text as the value and an optional `external_id` key with a string that will be included in the response.  |
|*production_model*  |`bool`             |Indicates if the extractions are performed by the production model. Only use this parameter with *custom models* (not with the public ones). Note that you first need to deploy the production model from the UI model settings. |
|*batch_size*        |`int`              |Max amount of texts each request will send to MonkeyLearn. A number from 1 to 200. |
|*retry_if_throttled* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits), sleep and retry the request. |

Example:

```python
data = ['First text', {'text': 'Second text', 'external_id': '2'}]
response = ml.extractors.extract('[MODEL_ID]', data=data)
```

<br>

#### [Extractor detail](https://monkeylearn.com/api/v3/?shell#extractor-detail)


```python
def MonkeyLearn.extractors.detail(model_id, retry_if_throttled=True)
```

Parameters:

| Parameter          |Type               | Description                                               |
|--------------------|-------------------|-----------------------------------------------------------|
|*model_id*          |`str`              |Extractor ID. Always starts with `'ex'`, for example `'ex_oJNMkt2V'`. |
|*retry_if_throttled* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits), sleep and retry the request. |

Example:

```python
response = ml.extractors.detail('[MODEL_ID]')
```

<br>

#### [Extractor list](https://monkeylearn.com/api/v3/?shell#list-extractors)


```python
def MonkeyLearn.extractors.list(page=1, per_page=20, retry_if_throttled=True)
```

Parameters:

|Parameter           |Type               | Description |
|--------------------|-------------------|-------------|
|*page*              |`int`              |Specifies which page to get.|
|*per_page*          |`int`              |Specifies how many items to return per page. |
|*retry_if_throttled* |`bool`             |If a request is [throttled](https://monkeylearn.com/api/v3/#query-limits), sleep and retry the request. |

Example:

```python
response = ml.extractors.list(page=2)
```
