# Authoring Environments

Creating and maintaining images for **development** platforms is a
critical process, particularly when the images are designed to be immediately
consumable by developers.

This approach streamlines the development workflow by ensuring that
environments are standardized, consistent, and readily available for
deployment.

## Core Principles

### Single Creation, Multiple Consumption

An environment is typically created once, then pushed to the registry,
where it can be pulled and consumed countless times by any developer.

### Specialized Support for Database Services

**shepherd** offers enhanced support in:

- **State Management**: The environment's creator or maintainer can easily
  manipulate the state of the database, enabling them to tailor the
  environment to specific development needs.

- **Database Import**: Importing database dumps is straightforward,
  allowing for quick replication of data within the development environment.

## Creating a New Environment

Creating a new environment can be approached using various strategies,
depending on your specific requirements.
