# Creating Global Card

This guide demonstrates how to create a **Global Virgil Card**. The main feature of Global Virgil Cards is that these Cards contain an identity, which must be confirmed by a user/device. For these cases, Virgil Security has a **Virgil Identity Service** responsible for user identities **validation**. Validating a user occurs after another service – **Virgil RA Service**  authorizes the creation of Global Virgil Cards.

After a Global Virgil Card was created, it's published at the Virgil Card Service, where an owner can find their Cards at any time.

**Warning**: You can not change a Global Virgil Card's content after its publishing.

Each Virgil Card contains a permanent digital signature that provides data integrity for the Virgil Card over its life cycle.

### Let's start to create a Global Virgil Card

Set up your project environment before you begin to create a Global Virgil Card, with the [getting started](/documentation/guides/configuration/client.md) guide.

The Global Virgil Card creation procedure is shown in the figure below.

![Card Intro](/documentation/img/Card_intro.png "Create Global Virgil Card")

In order to create a Global Virgil Card:

1. Developers need to initialize the **Virgil SDK**

```python
virgil = Virgil()
```

2. Once the SDK is ready we can proceed to the next step:


- Generate and save the Virgil Key (it's also necessary to enter the Virgil Key's name and password).
- Create a Global Virgil Card using their recently generated Virgil Key (they will need to enter some identifying information).


```python
# generate a new Virgil Key
alice_key = virgil.keys.generate()

# save the Virgil Key into the storage
alice_key.save("[KEY_NAME]", "[KEY_PASSWORD]")

# create Identity for global card
identity = virgil.identities.create_email("alice@virgilsecurity.com")

# initiate validation process
identity.check()

# confirm your identity
identity.confirm("[CONFIRMATION_CODE]")

# create a Global Virgil Card
alice_card = virgil.cards.create(identity, alice_key)
```

The Virgil Key will be saved into default device storage. Developers can also change the Virgil Key storage directory as needed, during Virgil SDK initialization.

Warning: Virgil doesn't keep a copy of your Virgil Key. If you lose a Virgil Key, there is no way to recover it.

3. Now, developers can initiate an identity verification process.
4. A User has to confirm a Virgil Card's identity using a **confirmation code** received by email.
5. Finally, developers must publish the User's Global Virgil Card on Virgil Services.

```python
virgil.cards.publish(alice_card)
```
