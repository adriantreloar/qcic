=============================
qcic
=============================

.. image:: https://badge.fury.io/py/qcic.png
    :target: http://badge.fury.io/py/qcic

.. image:: https://travis-ci.org/adriantreloar/qcic.png?branch=master
    :target: https://travis-ci.org/adriantreloar/qcic

.. image:: https://coveralls.io/repos/github/adriantreloar/qcic/badge.svg?branch=master 
    :target: https://coveralls.io/github/adriantreloar/qcic?branch=master 

.. image:: https://pypip.in/d/qcic/badge.png
    :target: https://pypi.python.org/pypi/qcic


Monitor remote processes in python with messages sent via 0MQ
=============================================================

In Development
--------------

qcic is in a pre-alpha state.

As soon as I have a minimum viable product it'll go on PyPl as an alpha version.


Problem Statement
-----------------

The motivation for this project is to ensure the guys who I work with are not constantly trying to monitor processes happening on their multiple clients' (i.e. people/company clients') servers.
Now we are not scheduling the jobs, so we can't simply use a scheduler.

The plan for this project is to make a background process that is expecting to receive zeromq (http://zeromq.org) messages from other processes.
If the messages are not received, then it can forward on notifications as other zeromq messages, or as email. I may connect it into an SMS sender.

The big issue with waiting for a nightly batch process to finish is that if the network goes down, or a server fails, we may never get to the part of a program that warns us there is an issue.
By having a separate monitoring program on a separate server waiting for notifications, we can raise the alarm when an expected notification _doesn't_ arrive.

So far so good, but who will watch the watchers? Creating pairs or even farms of remote monitors is part of the plan for this project - watchers can monitor each other, and take over notification duties when one of the watchers goes off-line.

What if the watcher was alive all along, and we've simply suffered a net split? Then notification messages will be sent twice. Support networks must be designed to handle this eventuality, along with the possibility that a cry for help is a false alarm.

Features
--------

* Load a set of schedules of expected messages from one or more JSON files
* Wait for the messages to arrive...and if the messages don't arrive.
* Create an email to escalate issues to humans

Technologies
------------

I've chosen the Python and 0MQ technologies because I have written projects with them before, and I'm sure I can knock up the basics pretty quickly.
I've made the decision that the monitor never replies to the monitored program, because some of our clients will barely allow the simple outbound socket to be opened from their systems, with the very bare protocol I'm planning. They certainy will not accept inbound traffic.

Licensing
---------

I've, made the project available as open-source and under a MPL v2 license because it is a useful thing I think a lot of people could join in with. If you ask people to join in you have to guarantee that their work won't be stolen and sold on - thus the MPL v2 license. At the same time, you can use all of the source files in a proprietary project without infecting your proprietary code with GPLness. 
There is no way a GPL or LGPL project of this type would even get off the ground.


Getting started. 
---------------

As soon as there is more to this project than this readme, I'll put some installation instructions in.

Overall Design
--------------

.. aafig::
    :aspect: 60
    :scale: 150
    :proportional:
    :textual:

    +--------------+         +-----------+          +----------------------------------------------+
    | Some Process +---zmq-->+ qcic      +--email-->+ AOK message                                  |
    +--------------+         +-----------+          +----------------------------------------------+

    +--------------+         +-----------+          +----------------------------------------------+
    | Some Process +         | qcic      +--email-->+ poor fool being woken up at 2 in the morning |
    +--------------+         +-----------+          +----------------------------------------------+

The design is like so - The watcher loads up some expected events, and starts a loop for checking if events have happened, and multiple loops which wait for incoming messages in various forms.

The checking loop sleeps for a variable amount of time - a long time if no activity is expected, a short time if lots of activity is expected.

The incoming message loops block until a message is received. If a received message is urgent it is handled immediately, otherwise it is placed on a queue of messages for the checking loop.

If the checking loop finds a message has not been received in the expected time, it will perform an associated action - usually notifying someone via email.

How I set this up
-----------------

To setup originally I ran:

    virtualenv -p python3 qcic
    pip install cookiecutter
    cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git


    pip install pytest-cov
    pip-install pyzmq
    easy_install -U sphinxcontrib-aafig

