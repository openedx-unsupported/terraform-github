Usage
=====

To run this terraform you'll need to set "GITHUB_TOKEN" variable to either a Github OAuth
token or a personal access token.

.. code-block::

    export GITHUB_TOKEN=...

.. code-block::
    :caption: If you're using pass to store secrets.

    source <(pass environment/github_pat)
