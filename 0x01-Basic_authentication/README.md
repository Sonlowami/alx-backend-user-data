0x01. Basic Authentication

A basic authentication strategy of authenticating users basically means a user
will provide their username and password, or whatever credentials they use with each request they make to the server.

The advantage is that it keeps REST APIs stateless.

In this project, we impliment a basic authentication for a simple flask application that does nothing but authenticating users.

All the API logic is in [api folder]('./api/v1') while models are defined in [models](./models)
