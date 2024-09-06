## Social Media Application Setup

Setup consists of multiple steps, which are as follows
1. Clone the repository
2. Spin container
    ```sh
    $ docker compose up --build
    ```
3. Enter into docker container shell 
    ```sh
    $ docker exec -it assignment_container bash
    ```

4. Now run following commands in container shell
    ```sh
    $ python manage.py makemigrations
    $ python manage.py migrate

    # below command will create an admin user
    $ python manage.py createsuperuser

    # below command will create multiple dummy users
    $ python manage.py loaduser --file user.json
    ```
5. We have following API endpoints available
    ```txt
    api/auth/create-user/
    api/auth/create-token/
    api/auth/create-access/
    api/auth/verify-access/
    api/auth/me/
    auth/list-user/
    api/auth/list-friends/
    api/auth/list-sent-requests/
    api/auth/list-receive-requests/
    api/auth/send-request/
    api/auth/accept-request/
    api/auth/reject-request/
    ```
6. For the reference we have __Postman__ collection, named __Assignment.postman_collection.json__, Import it to postman.