# MEDMIND AI — Clinical Lesson Review & Safety Audit Checklist

> **EDUCATIONAL SIMULATION NOTICE**  
> MEDMIND AI is an educational simulation environment designed exclusively for medical and nursing students. All scenarios feature fictional patient cases. Lessons contain **NO real patient data**, **NO drug doses**, and **NO treatment instructions** for real clinical practice.

---

## 1. Clinical Reviewer Sign-off Checklist

Every lesson has been drafted under strict pedagogical guidelines and is flagged with `status: draft`, `reviewed_by: null`, and `reviewed_at: null`. Complete formal clinical review requires licensed haematologist / clinical educator verification below before `status` is transitioned to `published`.

| Lesson ID | Lesson Title | Reviewer Name | Review Date | Sign-off Status | Critical Feedback / Approval Notes |
|---|---|---|---|---|---|
| **LESSON-01** | Reading a Full Blood Count Systematically | _[ Blank ]_ | _[ Blank ]_ | `Draft - Pending Review` | _[ Blank ]_ |
| **LESSON-02** | Classifying Anaemia by Cell Size | _[ Blank ]_ | _[ Blank ]_ | `Draft - Pending Review` | _[ Blank ]_ |
| **LESSON-03** | Iron Studies and Ferritin Interpretation | _[ Blank ]_ | _[ Blank ]_ | `Draft - Pending Review` | _[ Blank ]_ |
| **LESSON-04** | The Microcytic Differential: Iron Deficiency, Thalassaemia, and Chronic Disease | _[ Blank ]_ | _[ Blank ]_ | `Draft - Pending Review` | _[ Blank ]_ |
| **LESSON-05** | Macrocytic Anaemia: Megaloblastic and Non-Megaloblastic Pathways | _[ Blank ]_ | _[ Blank ]_ | `Draft - Pending Review` | _[ Blank ]_ |
| **LESSON-06** | Choosing Investigations Wisely in Anaemia Workup | _[ Blank ]_ | _[ Blank ]_ | `Draft - Pending Review` | _[ Blank ]_ |
| **LESSON-07** | Diagnostic Reasoning and Cognitive Bias in Haematology | _[ Blank ]_ | _[ Blank ]_ | `Draft - Pending Review` | _[ Blank ]_ |
| **LESSON-08** | Must-Not-Miss Thinking and Finding the Cause in Anaemia | _[ Blank ]_ | _[ Blank ]_ | `Draft - Pending Review` | _[ Blank ]_ |

---

## 2. Reviewer Queries Raised (`TODO_REVIEWER` Registry)

The drafting assistant flagged the following specific questions in the `review_notes` field of each lesson YAML for clinical expert confirmation:

### LESSON-01: Reading a Full Blood Count Systematically
- `TODO_REVIEWER: Confirm whether local teaching hospital prefers reporting Hb in g/L or g/dL as primary standard.`
- `TODO_REVIEWER: Verify whether platelet indices (MPV) should be formally integrated into initial trainee reading checklist.`

### LESSON-02: Classifying Anaemia by Cell Size
- `TODO_REVIEWER: Verify standard teaching terminology for normocytic vs normochromic classifications.`
- `TODO_REVIEWER: Confirm whether reticulocyte production index formula should be introduced at this stage or deferred.`

### LESSON-03: Iron Studies and Ferritin Interpretation
- `TODO_REVIEWER: Validate local cut-off for ferritin in inflammatory states (e.g. < 50 ng/mL vs < 100 ng/mL).`
- `TODO_REVIEWER: Confirm availability of soluble transferrin receptor testing in regional laboratories.`

### LESSON-04: The Microcytic Differential: Iron Deficiency, Thalassaemia, and Chronic Disease
- `TODO_REVIEWER: Confirm whether Mentzer index (MCV/RBC < 13) should be presented solely as a heuristic screening tool or if another index (e.g. Green & King) is preferred.`
- `TODO_REVIEWER: Confirm laboratory protocol threshold for reflex haemoglobin electrophoresis in suspected thalassaemia minor.`

### LESSON-05: Macrocytic Anaemia: Megaloblastic and Non-Megaloblastic Pathways
- `TODO_REVIEWER: Validate guidance on checking methylmalonic acid vs total serum cobalamin in borderline B12 cases.`
- `TODO_REVIEWER: Confirm local policy regarding anti-intrinsic factor antibody testing in primary care.`

### LESSON-06: Choosing Investigations Wisely in Anaemia Workup
- `TODO_REVIEWER: Review cost-effectiveness ranking of initial haematology panels in regional healthcare network.`
- `TODO_REVIEWER: Confirm whether coeliac serology is recommended as routine first-line in all unexplained iron deficiency.`

### LESSON-07: Diagnostic Reasoning and Cognitive Bias in Haematology
- `TODO_REVIEWER: Verify suitability of cognitive forcing examples for undergraduate medical curriculum.`
- `TODO_REVIEWER: Review alignment with local clinical reasoning objective frameworks.`

### LESSON-08: Must-Not-Miss Thinking and Finding the Cause in Anaemia
- `TODO_REVIEWER: Verify age threshold (e.g. age >= 60 vs age >= 50) for fast-track colorectal referral in unexplained iron deficiency per local health service guidelines.`
- `TODO_REVIEWER: Confirm senior escalation trigger criteria for acute inpatient versus outpatient pathway.`

---

## 3. Reference Passages Audited

All facts in lessons are grounded in public, authoritative guidelines and peer-reviewed open literature:

| Reference ID | Title | Guideline / Authority Source | Public URL |
|---|---|---|---|
| **REF-FBC-001** | Systematic Review of Full Blood Count Parameters | British Society for Haematology | [b-s-h.org.uk](https://b-s-h.org.uk/guidelines/guidelines-cases/guidelines-for-the-laboratory-diagnosis-of-functional-iron-deficiency/) |
| **REF-FBC-002** | Red Cell Distribution Width and Anisocytosis | NCBI Bookshelf / StatPearls | [ncbi.nlm.nih.gov](https://www.ncbi.nlm.nih.gov/books/NBK545266/) |
| **REF-CELLSIZE-001** | Morphological Classification of Anaemias by Mean Cell Volume | NCBI Bookshelf / StatPearls | [ncbi.nlm.nih.gov](https://www.ncbi.nlm.nih.gov/books/NBK459254/) |
| **REF-CELLSIZE-002** | Normocytic Anaemia and Mixed Nutritional States | NCBI Bookshelf / StatPearls | [ncbi.nlm.nih.gov](https://www.ncbi.nlm.nih.gov/books/NBK560814/) |
| **REF-FERRITIN-002** | Ferritin Dynamics in Acute and Chronic Inflammation | World Health Organization (WHO) | [who.int](https://www.who.int/publications/i/item/9789240008526) |
| **REF-FERRITIN-003** | Transferrin Saturation and Iron Assessment in Complex States | British Society for Haematology | [b-s-h.org.uk](https://b-s-h.org.uk/guidelines/guidelines-cases/diagnosis-and-management-of-iron-deficiency/) |
| **REF-MICRODIFF-001** | Differentiating Iron Deficiency from Thalassaemia Trait | British Society for Haematology | [b-s-h.org.uk](https://b-s-h.org.uk/guidelines/guidelines-cases/investigation-of-haemoglobinopathies/) |
| **REF-MICRODIFF-002** | Anaemia of Chronic Disease and Iron Sequestration | NCBI Bookshelf / StatPearls | [ncbi.nlm.nih.gov](https://www.ncbi.nlm.nih.gov/books/NBK499888/) |
| **REF-MACRO-001** | Megaloblastic Haematopoiesis: B12 and Folate Deficiency | British Society for Haematology | [b-s-h.org.uk](https://b-s-h.org.uk/guidelines/guidelines-cases/guidelines-for-the-diagnosis-and-treatment-of-cobalamin-and-folate-disorders/) |
| **REF-MACRO-002** | Non-Megaloblastic Macrocytosis: Clinical Differential | NCBI Bookshelf / StatPearls | [ncbi.nlm.nih.gov](https://www.ncbi.nlm.nih.gov/books/NBK459295/) |
| **REF-TESTING-001** | High-Yield Diagnostic Testing Cascades in Anaemia | Choosing Wisely UK / AoMRC | [choosingwisely.co.uk](https://www.choosingwisely.co.uk/recommendations/) |
| **REF-TESTING-002** | Serial Evaluation and Avoiding Reflexive Low-Yield Testing | NICE Clinical Knowledge Summaries | [cks.nice.org.uk](https://cks.nice.org.uk/topics/anaemia-iron-deficiency/) |
| **REF-BIAS-001** | Cognitive Biases in Diagnostic Decision-Making | NCBI Bookshelf / StatPearls | [ncbi.nlm.nih.gov](https://www.ncbi.nlm.nih.gov/books/NBK557551/) |
| **REF-BIAS-002** | Calibration of Diagnostic Confidence and Evidence Weighting | Royal College of Physicians | [rcplondon.ac.uk](https://www.rcplondon.ac.uk/projects/outputs/improving-diagnostic-reasoning) |
| **REF-REDALERT-001** | Etiological Investigation of Iron Deficiency and Red-Flag Features | British Society of Gastroenterology | [bsg.org.uk](https://www.bsg.org.uk/clinical-resource/guidelines-for-the-management-of-iron-deficiency-anaemia/) |
| **REF-REDALERT-002** | Structured Escalation and Senior Communication in Haematological Care | General Medical Council (GMC) | [gmc-uk.org](https://www.gmc-uk.org/ethical-guidance/ethical-guidance-for-doctors/good-medical-practice) |

---

## 4. Prescribing Safety & Guardrails Verification

An automated safety test suite (`backend/tests/test_lessons.py::test_no_banned_prescribing_words`) was executed to confirm that:
- **Zero** instances of the string `dose` (including doses, dosage) appear in any lesson file.
- **Zero** instances of the string `mg` appear in any lesson file.
- **Zero** instances of the string `prescribe` (including prescribed, prescription) appear in any lesson file.
- All lessons reinforce diagnostic reasoning and escalation thresholds, strictly directing learners to `"consult local formulary"` or `"follow local institutional protocol"`.
