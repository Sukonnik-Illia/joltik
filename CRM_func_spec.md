# Functional requirements for CRM

## **CRM for a company providing digital marketing services:**
* Search Engine Optimization (SEO)
* Pay Per Click (PPC) Marketing
* Social Media Management (SMM)
* Display images and Video production

Reference [CRM video](https://www.youtube.com/watch?v=Ihu9rr1wRa0).

## **Customer Information Management**

#### The system shall store information including:
* Customers and potential customers info and contacts
* Contact person info for customers and potential customers
* Contact details (name, email, phone, address)
* Interaction history (dates, types of interactions, notes)
* Opportunities history (service types, dates, amounts)
* The system shall store information for customer accounts in Google Ads, Bing, Facebook, Instagram
#### The system shall allow viewing and editing the information above
#### Info should be easy to navigate and filter

## **Service Opportunities and Proposals Tracking**
#### The system shall track service opportunities, including:
* Opportunity description
* Customer associated with the opportunity
* Proposal details
* Status of the opportunity (e.g., new, in progress, closed)
#### The system shall allow updating the status of each opportunity.

## Ad Account Management
#### The system shall store information for customer accounts in Google Ads, Bing Ads, Facebook and Instagram including:
* Account ID
* Account credentials
* Account status
#### The system shall use this information for integration with respective platforms.

## Integration with Ad Platforms
#### API Integration with Google Ads and Bing Ads
* Create and configure ad campaigns
* Set campaign budgets and targeting options
* Retrieve performance metrics (clicks, impressions, conversions, cost)
* Store performance data in the database for reporting purposes

## Data Storage and Replication
#### Database Management
* All customer, opportunity, and ad campaign data shall be stored in a centralized database.
#### Data Entry via Google Sheets
* The system shall allow data entry through Google Sheets.
* The system shall replicate data from Google Sheets to the database daily or on request, ensuring data consistency and availability.

## Possible Use cases:
* See the interaction history of customer/contact person (filter in Excel)
* See sales history of a customer (filter in Excel)
* Create custom lists (example: companies/persons to reach with communication) based on filters you set (like CEO of logistic industry companies; companies not contacted for the last 90 days)
* Launch ad campaign
* Download ad campaign performance reports to Excel

## Advanced features:
* front-end interface
* multiple users and user rights restrictions
* add notes (to customers, contact persons and proposals)
* cross-user tasks records
* send e-mail
* invoices and payment tracking


