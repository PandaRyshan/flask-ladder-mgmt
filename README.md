# Ladder-Dashboard

This is a dashboard for ladder management. Includes user management, VPS management and notification push features.

---

## Usage for development

1. Prepare your .env file and fill it out

   ```shell
   cp .env.template .env
   ```

2. Start postgres and redis

   ```shell
   docker compose up -d
   ```

3. Install dependences

   ```shell
   pip install -e .[dev]
   ```

   If you met error when you install psycopg2, try to install dependences:

   * libpq-dev (Debian/Ubuntu)
   * postgresql-libs (Arch)
   * postgresql-server-devel and python311-devel (openSUSE)

4. Init db

   ```shell
   flask init-db
   ```

5. Run flask

   ```shell
   flask run
   ```

6. Run celery

   ```shell
   celery -A celery_app worker --loglevel=DEBUG
   ```

---

## TODO

* [x] User management
  * [ ] Reset password
* [ ] Ladder management
  * [ ] Ladder account management
  * [ ] Client download
* [ ] Notification
* [ ] Server auto upgrade
