# Problem Statement: Automating Shipment Update Processing in Supply Chain
# Context:  
### In supply chain operations, logistics partners frequently send raw text updates about shipments. These updates often contain order IDs, shipment IDs, and delivery dates hidden in unstructured text. Manually parsing them slows down operations and introduces errors.
# Automation Goal:  
## Design a lightweight Flask-based microservice that:
### Accepts raw shipment update text via a POST request (tested with Postman).
### Uses regex to extract structured fields (order ID, shipment ID, delivery date).
### Validates the extracted data.
### Automatically forwards structured data to a central tracking system using requests.
### Follows a clean folder structure for maintainability.
