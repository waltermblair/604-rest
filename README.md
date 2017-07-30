Followed Cloud endpoints framework tutorial in assignment

Project ID: rest-175101

I worked in live environment for lack of time to set up local server and such - don't forget to redeploy when i make changes:
    -gcloud app deploy

Starting point from tutorial:
curl -H "Content-Type: application/json" -X POST -d '{"content":"hello world"}' https://rest-175101.appspot.com/_ah/api/echo/v1/echo

Next step - POST above but from file contents
cat posts/post1.json | curl -H "Content-Type: application/json" -X POST -d @- https://rest-175101.appspot.com/_ah/api/echo/v1/echo

Database
Next, I made a Cloud SQL database
I created a SQL instance and database named 604_db
 -Tutorial (https://cloud.google.com/sql/docs/mysql/quickstart)
 -gcloud sql connect rest-604 --user=root
 -create table 604_db.posts ( id INT NOT NULL, content VARCHAR(10000) NOT NULL, PRIMARY KEY(id) );
 -insert into 604_db.posts (id, content) VALUES (0, "test post 0 from inside mysql");
 -select * from 604_db.posts where id=0;

Enabled SQL API
I created a storage bucket 'rest-uploads', though I don’t think that was necessary here

Connecting Cloud SQL instance to Endpoints
    - (https://cloud.google.com/appengine/docs/standard/python/cloud-sql/)
    - app.yaml modifications:
         CLOUDSQL_CONNECTION_NAME: rest-175101:us-east1:rest-604  
         CLOUDSQL_USER: root  
         CLOUDSQL_PASSWORD: askme!  

HTTP

Testing REST operations from POSTMAN

    -Credentials
        Callback URL https://www.getpostman.com/oauth2/callback
        Token Name google cloud sql
        Auth URL https://accounts.google.com/o/oauth2/auth
        Access Token URL https://accounts.google.com/o/oauth2/token
        Client ID  XXXXXXXXXXXXXXXX
        Client Secret XXXXXXXXXXXXXXXX
        Scope https://www.googleapis.com/auth/sqlservice.admin
        
        Redirect URI https://accounts.google.com/o/oauth2/auth?client_id=XXXXXXXXXXXXX&redirect_uri=https://www.getpostman.com/oauth2/callback&response_type=code&scope=https://www.googleapis.com/auth/sqlservice.admin
        
        Having a hell of a time authenticating Postman - I don't receive the token...I tried removing Postman from my connect Google apps because I read that it won't resent the token if it's already connected. I did that ... both a past Postman app was connected from 659, but it also showed my recent attempt for this project connected. I removed both and tried requesting again, but now I don't see it as a connect app at all.
        
Developing online
    - Wrote a db_connect function that returns connection to Cloud SQL database
    - Call db_connect in endpoints code

    POST
    - First hard-coded an insert into the code and it worked.
    - Cat'ing the same file into the insert content works great
    - cat posts/post1.json | curl -H "Content-Type: application/json" -X POST -d @- https://rest-175101.appspot.com/_ah/api/echo/v1/echo
    
    GET
    - Get returns a string of all the blog id's and contents, and I'm starting to feel like I'm completely torturing the API here ;)
    - curl -X GET https://rest-175101.appspot.com/_ah/api/echo/v1/getPosts
    
    DELETE
    - hard-coded id
        curl -X DELETE https://rest-175101.appspot.com/_ah/api/echo/v1/deletePost
    - provided as arg
        curl -X DELETE -d '{"content":"2"}' https://rest-175101.appspot.com/_ah/api/echo/v1/deletePost
    
    PUT
    - cat posts/post1.json | curl -H "Content-Type: application/json" -X PUT -d @- https://rest-175101.appspot.com/_ah/api/echo/v1/replacePost
    

    
    






Using REST operations from my app

