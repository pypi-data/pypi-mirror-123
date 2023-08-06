# Adara Privacy SDK #

The Adara Privacy SDK allows you to tokenize Personally Identifiable Information (PII) within an isolated environment. The tokens produced using this SDK follow a set of simple standards that allow you interact with other token producers so that you can participate in meaningful data exchanges without revealing sensitive information about individual users.

ADARA wrote this SDK to offer out-of-the-box support for engagement with the ADARA Privacy Token API, but does not require this. Data partners can use the ADARA Privacy Token Server SDK without using the ADARA Privacy Token API.
> **NOTE:** Any tokenization data generated within this SDK is only transmitted to Adara explicitly as described below.

## Getting Started ##

### Download and Install ###

Download and install the SDK from PyPi (we strongly recommend installing in a virtual environment):
```bash
(venv) % pip install adara-privacy
```

### Setup your local configuration ###
Configure the ADARA Privacy Token Server SDK using a single JSON configuration file with the following format:
```json
{
  "client_id": "<optional: your client ID>",
  "client_secret": "<optional: your client secret>",
  "auth_uri": "https://auth.adara.com/oauth/token",
  "privacy": {
    "private_salt" : "<!!REQUIRED!!: your PRIVATE salt value>",
    "common_salts" : {
      "adara" : "7f0587e5843dff04240624af5f215fe57ba9d5841ae25c5a22b0d95900ceb3ed",
      "my_consortium" : "34ef58c071c6c125c06103bb8bd1ce239afd4046711676a8d999df0c6a0c0820",
      "my_other_consortium" : "3362e7e25a9b2616d954d71bc9fcac87fb6939b85f4cf04e8d926d0e995723bf"
    },
    "audience_uri": "https://api.adara.com",
    "pipeline_id": "<optional: your pipeline ID>"
  }
}
```

In the example above, the common salts for my_consortium and my_other_consortium are provided for illustrative purposes to represent that any consortiums of interest can be added by provided salt values in the "common_salts" node. There will be one token produced per identifier, per common salt, although this behavior can be overridden for specific identifiers at call time.

Set up your configuration file locally and point the environment variable `ADARA_SDK_CREDENTIALS` to your file location:

```bash
% export ADARA_SDK_CREDENTIALS=<path to your config>/my_config.txt
```
The file path, name and extension are unimportant as long as they point to a readable file location in your local enviroment.

## Code Quickstart ##

### Identities and Identifiers

The SDK is written to accept the PII you have access to for an individual and transform it into a privacy-safe set of tokens. An important point to remember is that tokens, by themselves, are intentionally pretty useless. They are useful only when maintained as a set of tokens pointing to an individual user. The classes within the SDK reflect this by using a set of **Identifiers** that belong to an **Identity**:
```python
from adara_privacy import Identity, Identifier

my_identity = Identity(
    # pass the identifier type as an arg (placement doesn't matter)
    Identifier('email', 'someone.special@somedomain.com'),
    # or use a named argument
    Identifier(state_id = "D1234567"),  
)
```

#### Supported identifier types
The ADARA Privacy SDK supports the following identifiers out of the box:

| Type Value         | Description                          | Keywords                             |
| ------------------ | ------------------------------------ | ------------------------------------ |
| cookie             | Persistent cookie identifier         | single: `cookie`                     |
| customer_id        | Internal customer ID                 | single: `customer_id`                |
| drivers_license    | State-issued driver's license number | single: `drivers_license`            |
| email              | Clear text email address             | single: `email`                      |
| hashed_email       | Hashed email address                 | single: `hashed_email`               |
| membership_id      | Membership / loyalty ID              | single: `membership_id`              |
| passport           | Passport number                      | single: `passport`                   |
| social_security    | Social security number               | single: `social_security`            |
| state_id           | Other state ID                       | single: `state_id`                   |
| streetname_zipcode | Street name and zip code             | composite: `street_name`, `zip_code` |

You can also extend the SDK with identifier types of your own.


### Tokens

Each `Identifier` can be turned into tokens. The tokens are generated using the **private salt** and one or more **common salts** defined in your local configuration. Using these salts and some standard hashing algorithms, the ADARA Privacy SDK turns the raw PII from the identifier into a **private token** and one or more **common tokens**. The type of identifier (example: email or driver license number) is also returned with the token, as well as an optional label.

You can see the tokens for an `Identity` by invoking the `to_tokens()` method:

```python
print(
    json.dumps(
        my_identity.to_tokens()
    )
)
```
For the first example above, this yields the following output (or something similar, based on your client salt):
```json
{
  "package_token": "1dec707d16232521608c722299d03e6a34f47b20d3bbacb2a0738384c06fd029",
  "tokens": [
    {
      "private": "15ba6cd3b7f2618e680180706ae65850093ee165d36fb743c4d64ec3a51bd823",
      "adara": "4447b2c72b9aa03977af4b9f085feaf001587b652f36a914363d8eb709bc20bf",
      "my_consortium": "b84057a0bf979e28d53b846c2f3148a1f58e07a282f1bd768ce73a0fce347aef",
      "my_other_consortium": "8077ddc77cf8735dd6143d929f9f04deceec33e53331fe8466ad63934e33be3e",
      "type": "email"
    },
    {
      "private": "8edeb62e51ff5e19bba160b2c00c1747578fc5f3ae0c2f10a1bafd1d3522fbf2",
      "adara": "141dd951d0a54dfb320bdea0f5c35c9b379726780670d3b8cd6dd0d5341bb106",
      "my_consortium": "b0a85ec62d29b137d403155301cdb613dcf7474d40345b9c141cd8d3b3a32dcd",
      "my_other_consortium": "923c5edbd61954b09f20044be534b7a14c3ebae717eb0c25eb81679df064d5fd",
      "type": "state_id"
    }
  ]
}
```

#### Private vs. Common Tokens ####

Here's a helpful way to consider the difference between **private tokens** and **common tokens**:

* **Private tokens** function as your own unique handle on an identifier. Because they are generated with your **private salt**, and only you should have access to your private salt, no one else is able to create the same tokens for a given identifier. If you use Adara's Privacy APIs, only you (verified through authentication) can use your private tokens to perform lookups. You can store private tokens as you see fit.
* **Common tokens** are shared amongst members of a consortium. Common tokens are generated with a **common salt**, and anyone with access to that salt (i.e., the members of a consortium) can generate the same common token. Common tokens are useful for matching against private tokens and are therefore used to build an identity graph. If you use Adara's Privacy APIs, common tokens **cannot** be used for lookups in any way, so there really isn't a point to storing common tokens yourself. The common tokens are submitted alongside private tokens so that the matching can occur internally.

#### Package Tokens ####

Tokens will be returned for each identifier and salt combination. For a given Identity instance, this can result in a large number of individual tokens, which is not necessarily convenient for storing alongside your data. To solve this issue, each tokenization result contains a **package token**. This is a private token derived from all the identifiers within an indentity. Like all tokens, it is deterministic, but if you add or remove idenitifers from an identity, the package token will change accordingly (the order in which you add identifiers is not important).

The package token is _at least as good as_ the best identifier token within the result. If you want to store a single token to reference the identity, use the package token.

#### Labels ####

If you are interested in capturing individual identifier tokens, you may find it helpful to **label** your identifiers. This is because a large number of identifiers in the result may get confusing to associate with specific identifiers, especially if you have more than one identifier of the same type.

To label an identifier, simply use the `label` option when invoking the call:

```python
my_identity = Identity(
        # labels help differentiate the tokens in the result
        Identifier('email', 'someone.special@somedomain.com', label="personal email"),
        Identifier('email', 'someone.special@someotherdomain.com', label="work email"),
)
```

and this would be the output:

```json
{
  "package_token": "e67529f593120f5b141b0920199ca6aabfea864c735ad6e3a1625227da735137",
  "tokens": [
    {
      "private": "15ba6cd3b7f2618e680180706ae65850093ee165d36fb743c4d64ec3a51bd823",
      "adara": "4447b2c72b9aa03977af4b9f085feaf001587b652f36a914363d8eb709bc20bf",
      "my_consortium": "b84057a0bf979e28d53b846c2f3148a1f58e07a282f1bd768ce73a0fce347aef",
      "my_other_consortium": "8077ddc77cf8735dd6143d929f9f04deceec33e53331fe8466ad63934e33be3e",
      "type": "email",
      "label": "personal email"
    },
    {
      "private": "b790e43743f7db5735e5b77034036bc040656b70dc969230a5ffeec182a10982",
      "adara": "e0732ffd3b6524bc204df41a479f8143ceb7675f03f4152bec4daf36fd920483",
      "my_consortium": "368405c8c20623bd234a5d242ae1b48806f9ee91513735dfc5c66671da7bc858",
      "my_other_consortium": "63ae761a793f944207c6a030c7b355ef9e407196786f071a3d4b0e038dc59d45",
      "type": "email",
      "label": "work email"
    }
  ]
}
```

Labels can be any string, so you can use something like a UUID to track tokens programmatically.

#### Cherry Picking Common Tokens ####
Your configuration file should contain all the salts you may want to use for token creation.  In some cases, however, you may only want to create common tokens for a subset of consortiums. This allows you to submit identity data to some identity graphs, while omitting it from others.

To limit token results for any identifier to only a subset of your defined common salts, use the `common_tokens` keyword argument in the Identifier instantiation:

```python
my_identity = Identity(
        # no "common_tokens" keyword, so all tokens will be generated
        Identifier('email', 'someone.special@somedomain.com', label="personal email"),
        
        # here, we omit "my_other_consortium"
        Identifier(email='someone.special@someotherdomain.com',
                   label="work email",
                   common_tokens=['adara', 'my_consortium']
                   ),
)
```
```json
{
  "package_token": "8736afea56e62d978360b8f304ea6f33c692203ba91649aaf1226eb0601ef353",
  "tokens": [
    {
      "private": "15ba6cd3b7f2618e680180706ae65850093ee165d36fb743c4d64ec3a51bd823",
      "adara": "4447b2c72b9aa03977af4b9f085feaf001587b652f36a914363d8eb709bc20bf",
      "my_consortium": "b84057a0bf979e28d53b846c2f3148a1f58e07a282f1bd768ce73a0fce347aef",
      "my_other_consortium": "8077ddc77cf8735dd6143d929f9f04deceec33e53331fe8466ad63934e33be3e",
      "type": "email",
      "label": "personal email"
    },
    {
      "private": "b790e43743f7db5735e5b77034036bc040656b70dc969230a5ffeec182a10982",
      "adara": "e0732ffd3b6524bc204df41a479f8143ceb7675f03f4152bec4daf36fd920483",
      "my_consortium": "368405c8c20623bd234a5d242ae1b48806f9ee91513735dfc5c66671da7bc858",
      "type": "email",
      "label": "work email"
    }
  ]
}
```

### Sending data to Adara ###
If you want to send your tokens into Adara's Privacy API, you can use the ```AdaraPrivacyApiStreamer``` class.
> You'll need to specify several of the "optional" settings in the configuration file for this, and you'll get these values from Adara's provisioning team.  They'll setup a configuration file for you with everything you need, such as client secrets, pipeline IDs, and API endpoints.

Here's some sample code that creates an `Identity` instance and send the tokenized result to Adara's Privacy API (note that tokenization is implicit):

```python
from adara_privacy import Identity, Identifier, AdaraPrivacyApiStreamer

# create instance of an API streamer
adara_api = AdaraPrivacyApiStreamer()

# create an identity instance
my_identity = Identity(
        # labels help differentiate the tokens in the result
        Identifier('email', 'someone.special@somedomain.com', label="personal email"),
        Identifier(email='someone.special@someotherdomain.com',
                   label="work email",
                   common_tokens=['adara', 'my_consortium']
                   ),
)

# push the identity tokens to ADARA
adara_api.save(my_identity)
```
