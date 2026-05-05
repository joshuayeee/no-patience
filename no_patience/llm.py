import os
from google import genai
from google.genai import types
from google.genai import errors
import psycopg2
from pathlib import Path
import time
import re

# DB connection
def get_db_connection():
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        raise ValueError("DATABASE_URL is not set")

    return psycopg2.connect(db_url)


# Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-3-flash-preview"

# Schema
SCHEMA = """
Table: AB133LicenseSurvey
- ID INT PRIMARY KEY
- LicenseID INT
- DateCompleted VARCHAR(12)

Table: AB133LicenseSurveyAnswer
- AB133LicenseSurvey_ID INT
- AB133SurveyQuestion_REF_Number INT
- AB133SurveyAnswerCategory_REF_ID INT
- AB133SurveyAnswer_REF_ID INT
- StringAnswer TEXT

Table: AB133SurveyAnswer_REF
- ID INT PRIMARY KEY
- SelectedAnswer VARCHAR(255)
- AB133SurveyQuestion_REF_Number INT,
- AB133SurveyAnswerCategory_REF_ID INT

Table: AB133SurveyAnswerCategory_REF
- ID INT PRIMARY KEY,
- Category VARCHAR(255)
- AnswerType VARCHAR(255)
- AB133SurveyQuestion_REF_Number INT

Table: AB133SurveyQuestion_REF
- Number INT PRIMARY KEY
- Title VARCHAR(255)
- Subtitle VARCHAR(255)

Table: AdministrativeActionTakenByOtherStateOrFederalGovernment
- LicenseID INT
- Jurisdiction VARCHAR(255)
- Description TEXT
- DateOfAction VARCHAR(12)

Table: AdministrativeCitationIssued
- LicenseID INT
- FineAmount VARCHAR(15)
- DateResolved VARCHAR(12)
- DateCitationIssued VARCHAR(12)
- Cause VARCHAR(255)

Table: AdministrativeDisciplinaryAction
- LicenseID INT
- CaseNumber VARCHAR(255),
- Description TEXT
- EffectiveDate VARCHAR(12)

Table: CourtOrder
- LicenseID INT
- DescriptionOfAction TEXT
- DateOfAction VARCHAR(12)
- PRIMARY KEY (LicenseID, DateOfAction)

Table: FelonyConviction
- LicenseID INT
- DescriptionOfAction TEXT
- EffectiveDateOfAction VARCHAR(12)
- Court VARCHAR(255)
- Docket VARCHAR(30)
- Sentence TEXT

Table: HospitalDisciplinaryAction
- LicenseID INT
- DescriptionOfAction TEXT
- HealthCareFacility VARCHAR(255)
- EffectiveDateOfAction VARCHAR(12)

Table: License
- LicenseID INT PRIMARY KEY
- LicenseType CHAR(1)
- LicenseNumber INT
- PrimaryStatusCode INT
- LastName VARCHAR(35)
- FirstName VARCHAR(35)
- MiddleName VARCHAR(35)
- NameSuffix VARCHAR(3)
- PreviousLastName VARCHAR(35)
- PreviousFirstName VARCHAR(35)
- PreviousMiddleName VARCHAR(35)
- PreviousNameSuffix VARCHAR(3)
- Sex CHAR(1)
- OriginalIssueDate VARCHAR(12)
- ExpirationDate VARCHAR(12)
- SchoolCode CHAR(5)
- GraduationDate VARCHAR(10)
- AddressOfRecordLine1 VARCHAR(50)
- AddressOfRecordLine2 VARCHAR(50)
- AddressOfRecordLine3 VARCHAR(50)
- AddressOfRecordCity VARCHAR(30)
- AddressOfRecordCountyCode INT
- AddressOfRecordState CHAR(2)
- AddressOfRecordCountry VARCHAR(56)
- AddressOfRecordZipCode VARCHAR(10)

Table: LicenseFeeExemptModifiers
- LicenseID INT PRIMARY KEY
- FeeExemptModifierCode VARCHAR(4)

Table: LicenseSecondaryStatusCodeModifiers
- LicenseID INT
- SecondaryStatusCodeModifier INT

Table: LicenseSurveyPracticeLocationResponse
- LicenseID INT
- SurveyID INT
- PatientCarePrimaryZipCode VARCHAR(10)
- PatientCarePrimaryCountyCode VARCHAR(10)
- PatientCareSecondaryZipCode VARCHAR(10)
- PatientCareSecondaryCountyCode VARCHAR(10)
- TelemedicinePrimaryZipCode VARCHAR(10)
- TelemedicinePrimaryCountyCode VARCHAR(10)
- TelemedicineSecondaryZipCode VARCHAR(10)
- TelemedicineSecondaryCountyCode VARCHAR(10)
- PRIMARY KEY (LicenseID, SurveyID)

Table: LicenseSurveyResponseCodes
- LicenseID INT
- SurveyID INT
- SurveyResponseCode VARCHAR(255)

Table: MalpracticeJudgment
- LicenseID INT
- DateOfAction VARCHAR(12)
- JudgmentAmount VARCHAR(15)
- Court VARCHAR(255)
- Docket VARCHAR(255)

Table: MisdemeanorConviction
- LicenseID INT,
- DescriptionOfAction TEXT
- EffectiveDate VARCHAR(12)
- Court VARCHAR(255)
- Docket VARCHAR(255)
- Sentence TEXT

Table: ProbationaryLicenseIssued
- LicenseID INT
- CaseNumber INT PRIMARY KEY
- Description TEXT
- EffectiveDate VARCHAR(12)

Table: ProbationSummary
- LicenseID INT PRIMARY KEY
- ProbationSummary TEXT

Table: PublicLetterOfReprimand
- LicenseID INT
- Description TEXT
- EffectiveDateOfAction VARCHAR(12)
- PRIMARY KEY (LicenseID, EffectiveDateOfAction)

Table: REF_FeeExemptModifier
- FeeExemptModifierCode VARCHAR(4) PRIMARY KEY
- ShortDescription VARCHAR(255)
- LongDescription TEXT

Table: REF_PrimaryStatusCode
- PrimaryStatusCode CHAR(2) PRIMARY KEY
- ShortDescription VARCHAR(255)
- LongDescription TEXT

Table: REF_SecondaryStatusCodeModifier
- SecondaryStatusModifierCode INT PRIMARY KEY
- ShortDescription TEXT
- LongDescription TEXT

Table: REF_SurveyCountyCode
- SurveyCountyCodeID INT PRIMARY KEY
- Name VARCHAR(255)

Table: REF_SurveyResponseCode
- SurveyResponseCode VARCHAR(255) PRIMARY KEY
- Description TEXT

Table: VoluntaryLimitation
- LicenseID INT
- EffectiveDate VARCHAR(12)
- Description TEXT
"""

# Extract SQL from response
def extract_sql(text):
    if not text:
        return None

    text = text.strip()

    if "CANNOT_ANSWER" in text:
        return None

    # Remove ```sql and ```
    text = text.replace("```sql", "").replace("```", "").strip()

    return text

# Remove excess from response
def clean_sql(sql):
    sql = sql.strip()

    # Remove anything before SELECT
    lower = sql.lower()
    if "select" in lower:
        sql = sql[lower.index("select"):]

    return sql

# Generate SQL
def generate_sql(user_question):
    prompt = f"""
You are a PostgreSQL query generator.

Rules:
- Only generate a valid SQL query
- Only use the tables below
- If unsure, return: CANNOT_ANSWER
- Any question about "physicians" in the below prompt will require checking entries in the License table
- If a WHERE CLAUSE is used, add an ILIKE operator
- Unless counting, please limit selection to only 5 entries per query

Schema:
{SCHEMA}

Question:
{user_question}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    try:
        print(response.text)
        return extract_sql(response.text)
    except:
        return None

# Validate SQL
def is_safe_sql(query):
    if not query:
        return False

    q = query.lower()

    forbidden = ["insert", "update", "delete", "drop", "alter", "truncate"]
    if any(word in q for word in forbidden):
        return False

    if not q.strip().startswith("select"):
        return False

    return True

# Execute SQL
def run_query(query):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(query)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        return columns, rows
    except:
        return None, None
    finally:
        cur.close()
        conn.close()

# Explain result
def explain_result(question, columns, rows):
    prompt = f"""
User question: {question}

SQL result:
Columns: {columns}
Rows: {rows}

Explain the result clearly and concisely.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    return response

def answer_question(user_question: str) -> str:
    try:
        sql_query = generate_sql(user_question)

        if not is_safe_sql(sql_query):
            return "Sorry, I couldn't generate a safe query."

        columns, rows = run_query(sql_query)

        explanation = explain_result(user_question, columns, rows)

        return explanation.text

    except Exception as e:
        return f"Error: {str(e)}"
    
def generate():
    print("Ask a question (type 'exit' to quit)\n")

    while True:
        user_question = input(">> ")

        if user_question.lower() == "exit":
            break

        response = answer_question(user_question)

        print("\nAnswer:")
        print(response)


if __name__ == "__main__":
    generate()