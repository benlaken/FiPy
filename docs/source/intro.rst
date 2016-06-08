Introduction
============

Fispy is a personal finance projection system, built in Python and
designed to work with a web framework.

Users should be able to add (and update) assets to a portfolio.
From these assets, Fispy should calculate projections of personal finance.

At the moment, it features only simple functions. Assets should have a start
date (and if desired end date) associated with them, as the projection uses real
date times.

Types of assets currently supported (and some of their features):
* jobs
  * monthly salary property
* real estate
  * can be a property to rent
  * this type of asset can have debt and repayment properties
* stocks
  * can be a generic asset with a simple growth factor
  * or, can be a real stock,
  * will add options for monthly-growth randomly drawn from distributions based on historical data
