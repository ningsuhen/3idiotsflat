
[7m Application loaded using the "development" environment configuration
[0m
MEAN.JS application started on port 3000
[90mPOST /auth/signin [32m200 [90m77ms - 502b[0m
[90mPOST /auth/signup [32m200 [90m75ms - 463b[0m
[90mPOST /auth/signup [33m400 [90m63ms - 194b[0m
[90mPOST /auth/signin [32m200 [90m64ms - 502b[0m
[90mGET /auth/signout [36m302 [90m3ms - 35b[0m
[90mGET /users/usertest [32m200 [90m4ms - 463b[0m
[90mGET /users/me [32m200 [90m4ms - 502b[0m
[90mPATCH /users/me [32m200 [90m6ms - 539b[0m
[90mPOST /users/precreated2/contact-message [32m200 [90m942ms - 67b[0m
# TOC
   - [User Api Unit Tests: ](#user-api-unit-tests-)
     - [Method Signup: ](#user-api-unit-tests-method-signup-)
     - [Method Signin: ](#user-api-unit-tests-method-signin-)
     - [Method Signout: ](#user-api-unit-tests-method-signout-)
     - [Method Get Users](#user-api-unit-tests-method-get-users)
     - [Method Get User details](#user-api-unit-tests-method-get-user-details)
     - [Method Update User](#user-api-unit-tests-method-update-user)
     - [Method Contact User](#user-api-unit-tests-method-contact-user)
       - [Method Add Service](#user-api-unit-tests-method-contact-user-method-add-service)
       - [Method Get User Services](#user-api-unit-tests-method-contact-user-method-get-user-services)
       - [Method Update User Services](#user-api-unit-tests-method-contact-user-method-update-user-services)
       - [Method Delete Service](#user-api-unit-tests-method-contact-user-method-delete-service)
       - [Method Search User](#user-api-unit-tests-method-contact-user-method-search-user)
<a name=""></a>
 
<a name="user-api-unit-tests-"></a>
# User Api Unit Tests: 
<a name="user-api-unit-tests-method-signup-"></a>
## Method Signup: 
should create a user.

```js
var data;
data = {
  'username': testParams.username,
  'password': testParams.password,
  'firstName': testParams.firstName,
  'lastName': testParams.lastName,
  'email': testParams.email
};
return superTest(app).post("/auth/signup").send(data).expect(RestfulApiResponse).expect(jSendSuccess).end(function(err, res) {
  var userDetails;
  userDetails = res.body.data.user;
  expect(userDetails.username).to.eql(testParams.username);
  expect(userDetails.firstName).to.eql(testParams.firstName);
  expect(userDetails.lastName).to.eql(testParams.lastName);
  return done();
});
```

should not be able to create user with same username/email.

```js
var data;
data = {
  'username': preCreatedUserData.username,
  'password': preCreatedUserData.password,
  'firstName': preCreatedUserData.firstName,
  'lastName': preCreatedUserData.lastName,
  'email': preCreatedUserData.email
};
return superTest(app).post("/auth/signup").send(data).expect(RestfulApiResponse).expect(jSendFailure).end(function(err, res) {
  return done();
});
```

<a name="user-api-unit-tests-method-signin-"></a>
## Method Signin: 
should authenticate a user.

```js
return superTest(app).post('/auth/signin').send(preCreatedUserCredentials).expect(RestfulApiResponse).expect(jSendSuccess).end(function(err, res) {
  var body;
  sessionCookie = res.headers['set-cookie'][0];
  body = res.body;
  accountId = body._id;
  return done();
});
```

<a name="user-api-unit-tests-method-signout-"></a>
## Method Signout: 
should sign out a user.

```js
return superTest(app).get("/auth/signout").end(function(error, response) {
  expect(response.statusCode).to.eql(302);
  return done();
});
```

<a name="user-api-unit-tests-method-get-users"></a>
## Method Get Users
<a name="user-api-unit-tests-method-get-user-details"></a>
## Method Get User details
should return details of user.

```js
return superTest(app).get("/users/" + testParams.username).expect(RestfulApiResponse).expect(jSendSuccess).end(function(err, res) {
  var userDetails;
  userDetails = res.body.data.user;
  expect(userDetails.salt).to.be(void 0);
  expect(userDetails.password).to.be(void 0);
  return done();
});
```

should return details of logged in user.

```js
return superTest(app).get("/users/me").set('Cookie', preCreatedUserCookie).expect(RestfulApiResponse).expect(jSendSuccess).end(function(err, res) {
  var userDetails;
  userDetails = res.body.data.user;
  expect(userDetails.salt).to.be(void 0);
  expect(userDetails.password).to.be(void 0);
  expect(userDetails.username).to.eql(preCreatedUserData.username);
  expect(userDetails.firstName).to.eql(preCreatedUserData.firstName);
  expect(userDetails.lastName).to.eql(preCreatedUserData.lastName);
  expect(userDetails.displayName).to.eql(preCreatedUserData.displayName);
  return done();
});
```

<a name="user-api-unit-tests-method-update-user"></a>
## Method Update User
should update the details of the user.

```js
var updateUserData;
expect(preCreatedUser.description).to.eql(preCreatedUserData.description);
updateUserData = {
  description: "updated description"
};
return superTest(app).patch('/users/me').set('Cookie', preCreatedUserCookie).send(updateUserData).expect(RestfulApiResponse).expect(jSendSuccess).end(function(err, res) {
  var userDetails;
  userDetails = res.body.data.user;
  expect(userDetails.description).to.eql(updateUserData.description);
  User.findById(preCreatedUser._id, function(err, userDoc) {
    return expect(userDoc.description).to.eql(updateUserData.description);
  });
  return done();
});
```

<a name="user-api-unit-tests-method-contact-user"></a>
## Method Contact User
should send a contact email to the user exclusive.

```js
var data;
data = {
  'name': 'Neeraj Goel',
  'subject': 'Hi',
  'content': 'I would like to connect with you !!!'
};
return superTest(app).post("/users/" + preCreatedUser2Data.username + "/contact-message").set('Cookie', preCreatedUserCookie).send(data).end(function(err, res) {
  expectAPIResponse(res);
  expectJSendSuccess(res);
  return done();
});
```

<a name="user-api-unit-tests-method-contact-user-method-add-service"></a>
### Method Add Service
<a name="user-api-unit-tests-method-contact-user-method-get-user-services"></a>
### Method Get User Services
<a name="user-api-unit-tests-method-contact-user-method-update-user-services"></a>
### Method Update User Services
<a name="user-api-unit-tests-method-contact-user-method-delete-service"></a>
### Method Delete Service
<a name="user-api-unit-tests-method-contact-user-method-search-user"></a>
### Method Search User
