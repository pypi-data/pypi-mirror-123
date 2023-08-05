# stdp.io client library

A library to interact with the stdp.io REST API and a framework to keep your local Akida models synced with your cloud stored models. You can train your models in the cloud and have them synced to your local devices.

## authenticating

Authenticate via username and password or via token. Specify the directory you want fetched models to be stored and synced.


```

from stdpio import stdpio

stdp = stdpio(username="username", password="password", model_dir="/tmp/")

```

or, if you already have a token

```

stdp = stdpio(token="example-token", model_dir="/tmp/")

```

to get a token:

```
stdp = stdpio(username="username", password="password")
token = stdp.get_token()
```


## fetching your Akida models


This will query the stdp.io API to bring back a list of your models. 


```

#get models
models = stdp.my_models()

# fetch all the model files & knowns
for model in models:

    # download the model file from stdp.io
    stdp.fetch_model_file(model)

    # print the labels and trained neurons for the model
    print(stdp.fetch_known(model))

```

You can also add search paramaters:


```
params = {"name__icontains": "mobilenet"}
stdp.my_models(**params)

```


## syncing your Akida models

When stdpio is initialised, it will begin a timer that will check models updated_at date. If you want to keep models synced with stdp.io, simply at it to the list of models to sync. The interval defaults to 1 second checks, this can be changed by passing in the keyword argument 'initerval'


```
stdp = stdpio(token="example-token", model_dir="/tmp/", interval=1)
stdp.sync_model("dbe69029-6ad0-4609-a06b-b0958e892f15")

```

and to stop syncing a model


```
stdp.unsync_model("dbe69029-6ad0-4609-a06b-b0958e892f15")
```



## running inference while syncing models

```
model_key = "ac738bf9-b492-42d7-b5c8-a3623db7a0ec"

stdp = stdpio(token="example-token", model_dir="/path/to/my/models")
stdp.sync_model(model_key)

inference = False

while True:

    akida_model = stdp.get_akida_model(model_key)
    if akida_model:
        inference = Model(filename=akida_model)

    if inference:
        image = load_img("thor.png")
        input_arr = tf.keras.preprocessing.image.img_to_array(image)
        input_arr = tf.image.resize_with_crop_or_pad(input_arr, 224, 224)
        input_arr = np.array([input_arr], dtype="uint8")
        predictions = inference.predict(input_arr, num_classes=10)

    time.sleep(1)

```
