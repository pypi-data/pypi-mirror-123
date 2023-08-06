This image uses a base Docker container build by `base-postgresql-images` (where all builds of Postgres and required packages) are done.  Any changes to PG source builds goes in that package.

This package consumes those base images and installs the Compose management software on top of that.  

To add a new Postgres version, first add it to `base-postgresql-images`, wait for it to build, then add things to this package and build it.

## Running Image Tests

Each PostgreSQL version should include a `test` image with tests.

While developing locally, you can build the test image and run it by passing in a connection string to run the tests, like so:

    $ docker run -ti tests --connection-string="postgres://admin:<password>@somehost.net:32161/ibmclouddb"   # pragma: whitelist secret

You should get TAP output:

    ok 1 tests/test_select.py::test_select
    1..1
