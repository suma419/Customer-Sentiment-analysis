# Customer-Sentiment-analysis
Built a real-time sentiment analysis pipeline using Kinesis, Lambda, Glue, and Comprehend to process social media data. Stored results in Amazon RDS and DynamoDB for structured and real-time querying. Visualized insights using Streamlit/Dash dashboards, with full monitoring via CloudWatch.


## Step 1: Data Ingestion using Amazon Kinesis

**Purpose:**  
To continuously receive incoming customer feedback (text/comments) from a source like a web form, app, or API and deliver it to AWS for processing in real time.

**How it works:**  
•	A Python script or frontend system sends JSON-formatted customer comments to a Kinesis Data Stream.  
•	Kinesis acts like a pipe that holds data temporarily and delivers it to consumers (like AWS Lambda).

**Why use Kinesis?**  
•	It handles high-throughput streaming.  
•	Supports multiple consumers (i.e., different Lambda functions or analytics systems).

**Output:**  
•	Raw data packets flow into the stream.  
•	Each record is ready to be picked up by a processing Lambda function.

---

## Step 2: Lambda Function 1 — Storing Raw Data in S3

**Triggered by:**  
The arrival of each record in the Kinesis stream.

**What it does:**  
•	Reads the data blob (Base64-encoded JSON) from Kinesis.  
•	Decodes the JSON.  
•	Saves the raw customer feedback into an Amazon S3 bucket in the input/ folder.

**Purpose:**  
•	To persist incoming feedback for durability and auditing.  
•	To serve as the trigger for downstream processing (e.g., sentiment analysis).

**Folder created in S3:**  
•	s3://your-bucket/input/abc123.json

**Format:**  
Each file contains one or more feedback entries in raw JSON.

---

## Step 3: Combined Lambda Function 2+ Sentiment Analysis + Store in DynamoDB

**Purpose:**  
To process each new file in /input/, run sentiment analysis, store results in DynamoDB, and optionally write a processed copy to S3.

**Triggered by:**  
An S3 ObjectCreated event in the /input/ folder.

---

### Step-by-Step Breakdown of What This Lambda Does:

1. **Fetch the Newly Uploaded File from S3**  
•	Reads the file uploaded by Lambda 1 from the input/ folder.  
•	Parses it as JSON (single record or a list).

2. **Analyze Sentiment using Amazon Comprehend**  
•	For each feedback:  
o	Extracts the text field.  
o	Sends the text to Amazon Comprehend.  
o	Receives:  
	Sentiment label (POSITIVE / NEGATIVE / NEUTRAL / MIXED)  
	Confidence scores for each label

3. **Write to DynamoDB (Table: SentimentResults)**  
•	For each result:  
o	Creates a new item in DynamoDB with:  
	id: Unique UUID  
	text: Original feedback  
	sentiment: Detected sentiment  
	scores: A map of confidence values for each category  
•	DynamoDB is used for:  
o	Fast lookup  
o	Querying sentiments by type  
o	Live dashboards / analytics queries

4. **Write Enriched Result Back to S3 /processed/**  
•	Creates a new .json file that includes:  
o	Original feedback  
o	Detected sentiment + scores  
•	Saved under:  
s3://your-bucket/processed/<same-filename>.json

**Output of this Lambda:**  
•	✅ Enriched file in /processed/  
•	✅ Record in DynamoDB  
•	⛔ No need for separate Lambda 3 anymore.

---

## Step 4: Streamlit Dashboard (Local or Web Visualization)

**Purpose:**  
To visualize and explore processed sentiment data for business users, analysts, or internal stakeholders.

**What happens:**  
•	The Streamlit app loads:  
o	Either from the enriched S3 JSON file, or  
o	Queries data directly from DynamoDB (if integrated)

**What it visualizes:**  
•	Data Table: showing text, sentiment, and scores  
•	Bar Chart: showing how many POSITIVE, NEGATIVE, etc.  
•	Line Graph: sentiment score trend over time  
•	Heatmap or timeline (advanced): patterns in feedback sentiment

**Why Streamlit?**  
•	Fast to build and run  
•	Beautiful and interactive charts (via Plotly or Matplotlib)  
•	Ideal for demos, stakeholders, or MVPs


## Summary Table

| Step | Service/Component         | Action/Trigger                         | Output/Next Step                |
|------|--------------------------|----------------------------------------|---------------------------------|
| 1    | Amazon Kinesis           | Receive JSON feedback                  | Stream to Lambda                |
| 2    | Lambda (Kinesis Trigger) | Store raw data in S3                   | S3 event for Lambda             |
| 3    | Lambda (S3 Trigger)      | Sentiment analysis, store in DynamoDB  | Enriched S3 file, DynamoDB item |
| 4    | Streamlit Dashboard      | Visualize sentiment data               | Interactive dashboard           |




![Image Alt](https://github.com/suma419/Customer-Sentiment-analysis/blob/e33eae7966eb0b5f043d4ff5d2573c7b176e7121/screenshort%20dashboard2.png)]




![Image Alt](https://github.com/suma419/Customer-Sentiment-analysis/blob/e33eae7966eb0b5f043d4ff5d2573c7b176e7121/screenshot%20dashboard1.png)]





![Image Alt](https://github.com/suma419/Customer-Sentiment-analysis/blob/4d25d05a59d0b9c127dbef4f4c722095d23154c1/folders.png)]





![Image Alt](https://github.com/suma419/Customer-Sentiment-analysis/blob/4d25d05a59d0b9c127dbef4f4c722095d23154c1/lamdaoutput2screenshot.png)]





![Image Alt](https://github.com/suma419/Customer-Sentiment-analysis/blob/4d25d05a59d0b9c127dbef4f4c722095d23154c1/sentimenttable_screenshot.png)]
