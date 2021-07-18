# General information
This is a recruitment task for python developer position. 

Application is available online at https://ngtask.herokuapp.com/


## Installation and usage
The easiest way to run this app is using Docker. Open terminal and go to the main directory of this project where you 
will find `Dockerfile` and `docker-compose.yml` files. Then simply run:

    docker-compose build --build-arg SECRET_KEY='<your-secrey-key-for-Django>'
    
Remember to put your own secret key value in place of `<your-secrey-key-for-Django>`. 

After successful build you can start app with:

    docker-compose up
    
Django app by default will start at port 8000.
