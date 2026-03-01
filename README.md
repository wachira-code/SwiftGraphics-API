**Swift Graphics API**

This is a RESTful API builtwith django and django restframework for managing cyber solutions and providing basic cyber services including general printing, eulogy design and printing, business card design and printig,
photocopying services and other related cyber solutions.

**Table of Contents**

.Project Overview

.Project Structure

.Getting Started

.Environment Variables

.Models

.Authentication

.Endpoints

.Testing with Postman

.Deployment

**Project Overview**

Swift Graphics API is a business platform that enables customers to:

-Browse available services

-place orders for their desired services

-Add specific design details for business cards and eulogies

-Track order status

-Manage their profile and account

**Project Structure**

swift_graphics_api/
│
├── manage.py
├── Procfile
├── runtime.txt
├── requirements.txt
├── .env
├── .gitignore
│
├── swift_graphics_api/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── core/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── permissions.py

**Getting Started**

1. Clone the repo

2. create and activate virtual environment

3. install dependencies

4. set up environment variables: create .env file

5. run migrations

**Models**

1. Service- represents services offered by the business

2. Order- represents a cutomer's order or orders

3. BusinessCardDesign- stores design details for business card orders

4. EulogyDocument- stores details for eulogy printing orders
   
**Authentication**

This API uses Token-based Authentication

How it works

1. Register or login to receive token

2. Include the token in the Authorization header for all protected requests

