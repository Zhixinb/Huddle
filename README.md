## Huddle Dev Set up

### Client

-   Install vue-cli [here](https://cli.vuejs.org/guide/installation.html)

-   Install Node/NPM [here](https://nodejs.org/en/)
-   Install dependencies

    > npm install

-   Serve with hot reload at localhost:8080
    > npm run dev

### Server

-   In /server, run the following to install all the required packages

    > python -m pip install -r requirements.txt

-   Running flask server at localhost:5000

> python app.py

### AWS Amplify (for Auth, etc.)

-   First get your aws_access_key_id and aws_secret_access_key via AWS Educate. Log into AWS Educate (seas email), go to AWS Account on the top right, get a starter account, click on the "Account Details" button, click show to show the keys, copy and set aside.
-   Set up AWS CLI: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-windows.html
-   Run the following to configure (choose 'us-east-1' for region)
    > aws configure
-   Next set up AWS Amplify with the following in the frontend folder:
    > npm install -g @aws-amplify/cli

> amplify init

-   When prompted what environment to use, choose N on existing env, rest all yes. Choose AWS Profile for authentication method (should be prompted to choose [default], if not then there is something wrong)

> amplify push

-   Wait for this to finish

-   Install the old over of amplify to fix an error with the latest

> npm install aws-amplify@^3.0.8

-   Now to set up the config on Cognito

-   To back to the page on AWS Educate where you get the keys, click the "AWS Console" button

-   In the search bar, search Cognito. Go to Manage User Pool > Message Customization (left-hand side) > verification type > choose link > save changes.

-   Again on the left-hand side, App Integration > Domain Name, choose a random domain prefix, check availability, save changes

-   Should now be able to build client, sign up and sign in

-   If developing, can hardcode default value of uid and make "/" route to "/home". Also you can sign up for multiple accounts with the same email if you append "+soemthing" (e.g. "bob@google.com, bob+1@google.com, bob+something@google.com" will all be "unique" emails, but you will receive verification emails in "bob@google.com")
