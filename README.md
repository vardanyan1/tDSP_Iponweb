# tDSP - Toy Demand-Side Platform
[![codecov](https://codecov.io/gh/vardanyan1/tDSP_Iponweb/branch/development/graph/badge.svg?token=JNV37UGX2P)](https://codecov.io/gh/vardanyan1/tDSP_Iponweb)
![GitHub CI](https://github.com/vardanyan1/tDSP_Iponweb/actions/workflows/test.yml/badge.svg)

This project aims to build a toy Demand-Side Platform (tDSP) for participating in Real-Time Bidding (RTB) auctions, competing with other DSPs for ad impressions. The tDSP will interact with a toy Supply-Side Platform (tSSP) and adhere to the specifications provided.
## Table of Contents

- [Overview](#Overview)
- [Installation](#Installation)
- [Usage](#Usage)
- [License](#license)

## Overview

The tDSP project is a dockerized application that consists of several components to provide a comprehensive environment for participating in Real-Time Bidding (RTB) auctions. The components of the project are defined in the docker-compose.yml file and include:

**Web**: A Django web application that serves as the core of the tDSP, handling the business logic and communication with the tSSP.

**Postgres**: A PostgreSQL database that stores the necessary data for the tDSP, such as ad campaigns and bidding information.

**Image Server Flask**: A Flask-based image server that stores and serves ad images for the tDSP.

**UI**: A User Interface built with a modern frontend framework (e.g., React) that allows users to interact with the tDSP.

**Prometheus**: A monitoring and alerting toolkit that collects and processes metrics from the tDSP components, ensuring optimal performance and reliability.

**Grafana**: A visualization platform that displays the metrics collected by Prometheus in customizable dashboards, providing insights into the tDSP's performance.

**Nginx**: A reverse proxy server that routes incoming requests to the appropriate services and handles SSL/TLS termination, load balancing, and other

## Installation

Before starting the installation process, ensure that you have Docker and Docker Compose installed on your machine. Follow these steps to set up the tDSP project:

**Clone the repository**: Clone the tDSP project repository from GitHub using the following command:

```
git clone https://github.com/vardanyan1/tDSP_Iponweb.git
```

**Navigate to the project directory**: Change your current working directory to the cloned tDSP project folder:
```
cd tDSP_Iponweb
```
**Create a .env.prod file**: Create a `.env.prod` file in the project directory and add the required environment variables. Use the provided `env.example` file as a template for the necessary variables. Be sure to replace the placeholders with the appropriate values for your setup.

**Build the Docker images**: Run the following command to build the Docker images for all the components defined in the docker-compose.yml file:
```
docker-compose -f docker-compose.prod.yaml build
```
**Start the tDSP services**: Run the following command to start all the tDSP services and their corresponding containers:
```
docker-compose -f docker-compose.prod.yaml up
```

Now, all the tDSP components should be running, and you can interact with the User Interface or access the backend services through their respective ports.

## Usage

The tDSP project provides a user-friendly interface and tools to manage and monitor the performance of your ad campaigns in the Real-Time Bidding (RTB) game.
You can access the user interface (UI) and Grafana dashboard for insights into your campaign performance and overall project statistics.

**Accessing the User Interface**

To access the tDSP user interface, open a web browser and navigate to http://localhost/ui. Here, you can perform various actions, including creating new campaigns and creatives, activating or deactivating campaigns, and setting the minimum bid for a specific campaign.

**Using Grafana Dashboard**

To access the Grafana dashboard and view real-time statistics about the game and the overall performance of the project, open a web browser and navigate to http://localhost:3060.
Use the credentials you have set in your `.env.prod` file to log in.

Once logged in, you can explore various pre-configured dashboards that display key performance indicators (KPIs) related to your ad campaigns and the tDSP system.
This data can help you make informed decisions about optimizing your bidding strategy and campaign performance.


## License

Include the license for your project, for example:

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
