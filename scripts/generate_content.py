import os
import re
import yaml
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_CONTENT = BASE_DIR / "backend" / "content"
API_CONTENT = BASE_DIR / "api" / "content"

REFERENCES = [
    {
        "id": "REF-FBC-001",
        "title": "Systematic Review of Full Blood Count Parameters",
        "source_title": "British Society for Haematology: Guidelines for the Laboratory Diagnosis of Functional Iron Deficiency",
        "source_url": "https://b-s-h.org.uk/guidelines/guidelines-cases/guidelines-for-the-laboratory-diagnosis-of-functional-iron-deficiency/",
        "retrieved_at": "2026-03-15",
        "licence_note": "Paraphrased summary of public guideline for educational use; no endorsement implied",
        "section": "Systematic Evaluation",
        "tags": ["fbc", "haematology", "indices", "systematic_review"],
        "lang": "en",
        "reviewed": False,
        "key_facts": [
            "A complete blood count should be interpreted in a structured sequence: haemoglobin, MCV, RDW, followed by white cells and platelets.",
            "Isolated evaluation of haemoglobin risks missing dual pathology or evolving haematological disorders.",
            "Typical adult reference ranges vary by laboratory and patient demographic factors."
        ],
        "body": """Systematic interpretation of the full blood count is fundamental to diagnostic haematology. Relying solely on haemoglobin concentration detects the presence of anaemia but provides zero insight into underlying etiology. A structured reading begins by confirming the degree of cytopenia through haemoglobin, followed immediately by erythrocyte indices: mean cell volume (MCV), mean cell haemoglobin (MCH), and red cell distribution width (RDW).

Evaluating the white blood cell count and platelet count is essential to differentiate isolated erythroid failure from multilineage involvement, such as aplastic processes, haematological malignancies, or splenic sequestration. In isolated iron depletion, reactive thrombocytosis is frequently observed due to shared megakaryocyte-erythroid progenitor stimulation. Conversely, combined cytopenias require prompt escalation. Typical adult reference ranges vary by laboratory and clinical demographic characteristics."""
    },
    {
        "id": "REF-FBC-002",
        "title": "Red Cell Distribution Width and Anisocytosis",
        "source_title": "NCBI Bookshelf / StatPearls: Red Cell Distribution Width",
        "source_url": "https://www.ncbi.nlm.nih.gov/books/NBK545266/",
        "retrieved_at": "2026-03-15",
        "licence_note": "Paraphrased summary of public guideline for educational use; no endorsement implied",
        "section": "Erythrocyte Indices",
        "tags": ["rdw", "anisocytosis", "fbc", "differential"],
        "lang": "en",
        "reviewed": False,
        "key_facts": [
            "RDW quantifies the variation in erythrocyte volume (anisocytosis).",
            "Elevated RDW is an early indicator of nutritional deficiency before MCV becomes frankly abnormal.",
            "Heterogeneous cell populations yield high RDW, whereas homogeneous microcytosis yields normal RDW."
        ],
        "body": """Red cell distribution width (RDW) is an automated mathematical coefficient measuring erythrocyte volume heterogeneity (anisocytosis). While MCV represents the average volume of millions of red cells, it obscures mixed or bimodal populations. For example, a patient with simultaneous iron deficiency (microcytic) and folate deficiency (macrocytic) can display a falsely reassuring normal MCV, while RDW is markedly elevated.

In early nutritional iron deficiency, newly synthesized microcytic, hypochromic cells circulate alongside preexisting normocytic erythrocytes, widening the distribution curve and elevating RDW before overt microcytic anaemia is established. Conversely, genetic disorders of globin synthesis, such as heterozygous thalassaemia trait, exhibit uniform microcytosis throughout erythropoiesis, typically yielding a normal RDW. Typical adult reference ranges vary by laboratory."""
    },
    {
        "id": "REF-CELLSIZE-001",
        "title": "Morphological Classification of Anaemias by Mean Cell Volume",
        "source_title": "NCBI Bookshelf / StatPearls: Microcytic Anemia",
        "source_url": "https://www.ncbi.nlm.nih.gov/books/NBK459254/",
        "retrieved_at": "2026-03-15",
        "licence_note": "Paraphrased summary of public guideline for educational use; no endorsement implied",
        "section": "Morphologic Classification",
        "tags": ["mcv", "microcytic", "macrocytic", "classification"],
        "lang": "en",
        "reviewed": False,
        "key_facts": [
            "Anaemia is morphologically categorized into microcytic, normocytic, and macrocytic patterns based on MCV.",
            "Microcytosis reflects diminished haemoglobin synthesis during erythroid maturation.",
            "Typical adult reference ranges vary by laboratory, typically spanning 80 to 100 fL."
        ],
        "body": """Mean cell volume (MCV) serves as the primary morphological branching point in the initial clinical evaluation of anaemia. Clinicians classify anaemia into three broad categories: microcytic, normocytic, and macrocytic. Typical adult reference ranges vary by laboratory, generally recognized between 80 and 100 fL.

Microcytosis indicates insufficient cytoplasmic haemoglobin production prior to nuclear extrusion, forcing erythroblasts to undergo extra divisions and producing small cells. Key etiologies include iron deficiency, thalassaemia syndromes, anaemia of chronic disease, and rare sideroblastic defects. Macrocytosis (MCV above normal limits) stems from either delayed DNA replication relative to cytoplasmic maturation (megaloblastic) or altered erythrocyte membrane lipid composition (non-megaloblastic). Cell size classification prevents non-targeted testing."""
    },
    {
        "id": "REF-CELLSIZE-002",
        "title": "Normocytic Anaemia and Mixed Nutritional States",
        "source_title": "NCBI Bookshelf / StatPearls: Normocytic Normochromic Anemia",
        "source_url": "https://www.ncbi.nlm.nih.gov/books/NBK560814/",
        "retrieved_at": "2026-03-15",
        "licence_note": "Paraphrased summary of public guideline for educational use; no endorsement implied",
        "section": "Normocytic States",
        "tags": ["normocytic", "haemolysis", "chronic_disease", "mixed_deficiency"],
        "lang": "en",
        "reviewed": False,
        "key_facts": [
            "Normocytic anaemia encompasses hypoproliferative states, acute blood loss, and early nutritional deficits.",
            "Reticulocyte count distinguishes bone marrow hypo-production from peripheral destruction or haemorrhage.",
            "Dual nutritional deficiencies can mathematically cancel each other out on MCV."
        ],
        "body": """Normocytic anaemia presents an extensive diagnostic challenge because erythrocyte dimensions remain within expected reference boundaries. The crucial immediate discriminator is the reticulocyte response. An elevated reticulocyte index indicates functional marrow response to acute haemorrhage or peripheral haemolysis. Conversely, a low or inappropriate reticulocyte response indicates hypoproliferation, common in renal failure, endocrine insufficiency, bone marrow infiltration, or anaemia of chronic disease.

Importantly, normocytic indices can conceal combined nutritional deficiencies. When iron deficiency coexists with vitamin B12 or folate deficiency, microcytic and macrocytic cell lines balance each other, generating a composite MCV within typical limits. Scrutinizing the blood film and RDW clarifies this pseudo-normal presentation. Typical adult reference ranges vary by laboratory."""
    },
    {
        "id": "REF-FERRITIN-002",
        "title": "Ferritin Dynamics in Acute and Chronic Inflammation",
        "source_title": "World Health Organization: WHO Guideline on Serum and Plasma Ferritin Concentrations",
        "source_url": "https://www.who.int/publications/i/item/9789240008526",
        "retrieved_at": "2026-03-15",
        "licence_note": "Paraphrased summary of public guideline for educational use; no endorsement implied",
        "section": "Inflammatory Dynamics",
        "tags": ["ferritin", "acute_phase", "inflammation", "iron_stores"],
        "lang": "en",
        "reviewed": False,
        "key_facts": [
            "Ferritin is an intracellular storage shell that leaks into plasma proportionally to reticuloendothelial reserves.",
            "Inflammatory cytokines stimulate hepatic ferritin production independently of iron stores.",
            "In inflammatory contexts, normal or elevated ferritin does not exclude concurrent iron deficiency."
        ],
        "body": """Serum ferritin is the most specific non-invasive laboratory marker of depleted iron reserves. In uncomplicated individuals without systemic inflammation, a subnormal ferritin level is diagnostic of exhausted iron stores. However, ferritin synthesis is heavily up-regulated by inflammatory cytokines including interleukin-6 and tumour necrosis factor during acute infection, systemic rheumatologic conditions, chronic kidney disease, hepatic inflammation, and neoplasia.

Consequently, in the setting of chronic inflammation, a patient with absolute iron exhaustion can exhibit a serum ferritin value well within or above the standard reference interval. In such complex cases, clinician interpretation must integrate inflammatory markers, transferrin saturation, and clinical context rather than accepting normal ferritin as proof of iron adequacy. Typical adult reference ranges vary by laboratory."""
    },
    {
        "id": "REF-FERRITIN-003",
        "title": "Transferrin Saturation and Iron Assessment in Complex States",
        "source_title": "British Society for Haematology: Diagnosis and Management of Iron Deficiency",
        "source_url": "https://b-s-h.org.uk/guidelines/guidelines-cases/diagnosis-and-management-of-iron-deficiency/",
        "retrieved_at": "2026-03-15",
        "licence_note": "Paraphrased summary of public guideline for educational use; no endorsement implied",
        "section": "Complex Iron Indices",
        "tags": ["transferrin", "tfsat", "ferritin", "iron_deficiency"],
        "lang": "en",
        "reviewed": False,
        "key_facts": [
            "Transferrin saturation (serum iron divided by total iron-binding capacity) reflects circulating iron available for erythropoiesis.",
            "Transferrin saturation below 20% indicates functional iron limitation even when ferritin is elevated by inflammation.",
            "Isolated serum iron without transferrin or ferritin is clinically unreliable due to diurnal fluctuations."
        ],
        "body": """When evaluating iron status in patients with coexisting inflammatory disorders, relying solely on ferritin is prone to misinterpretation. Measuring transferrin saturation (calculated as serum iron divided by total iron binding capacity, expressed as a percentage) provides critical diagnostic assistance. Transferrin saturation reflects the proportion of carrier protein currently saturated with iron and available to developing erythroblasts in the marrow.

A transferrin saturation below 20% strongly suggests iron-restricted erythropoiesis, even if serum ferritin appears normal or elevated due to an acute phase reaction. Unconjugated serum iron alone is vulnerable to extensive diurnal variation, recent food ingestion, and physiological stress; it should never be interpreted in isolation. Advanced markers such as soluble transferrin receptor can further clarify equivocal cases. Typical adult reference ranges vary by laboratory."""
    },
    {
        "id": "REF-MICRODIFF-001",
        "title": "Differentiating Iron Deficiency from Thalassaemia Trait",
        "source_title": "British Society for Haematology: Laboratory Investigation of Haemoglobinopathies",
        "source_url": "https://b-s-h.org.uk/guidelines/guidelines-cases/investigation-of-haemoglobinopathies/",
        "retrieved_at": "2026-03-15",
        "licence_note": "Paraphrased summary of public guideline for educational use; no endorsement implied",
        "section": "Microcytic Differential",
        "tags": ["thalassaemia", "iron_deficiency", "mentzer", "indices"],
        "lang": "en",
        "reviewed": False,
        "key_facts": [
            "Heterozygous thalassaemia trait produces marked microcytosis with relatively preserved or elevated red cell counts.",
            "Iron deficiency produces progressive microcytosis accompanied by anisocytosis and elevated RDW.",
            "Screening indices like the Mentzer ratio provide heuristics but require definitive laboratory confirmation."
        ],
        "body": """Differentiating iron deficiency anaemia from heterozygous beta-thalassaemia trait is a core haematological competency. Both conditions produce microcytic, hypochromic indices, yet their pathophysiological foundations diverge completely. Iron deficiency stems from substrate starvation: erythropoiesis is restricted, red cell count is subnormal, and cellular variation (RDW) is wide.

In contrast, heterozygous thalassaemia is a genetic condition of unbalanced globin chain synthesis with intact iron reserves. Marrow compensation maintains a normal or elevated red blood cell count despite tiny individual cell volumes (severe microcytosis disproportionate to mild anaemia), with uniform cell sizes and normal RDW. Mathematical indices like the Mentzer heuristic (MCV divided by red cell count) suggest thalassaemia when low and iron deficiency when high, but definitive confirmation requires haemoglobin variant analysis and ferritin testing. Typical adult reference ranges vary by laboratory."""
    },
    {
        "id": "REF-MICRODIFF-002",
        "title": "Anaemia of Chronic Disease and Iron Sequestration",
        "source_title": "NCBI Bookshelf / StatPearls: Anemia of Chronic Disease",
        "source_url": "https://www.ncbi.nlm.nih.gov/books/NBK499888/",
        "retrieved_at": "2026-03-15",
        "licence_note": "Paraphrased summary of public guideline for educational use; no endorsement implied",
        "section": "Chronic Disease Pathophysiology",
        "tags": ["hepcidin", "chronic_disease", "iron_sequestration", "microcytosis"],
        "lang": "en",
        "reviewed": False,
        "key_facts": [
            "Hepcidin upregulation locks iron inside macrophages and hepatocytes, starving circulating erythroid precursors.",
            "Indices are typically normocytic initially, progressing to mild microcytosis over months.",
            "Ferritin is normal or elevated, distinguishing it from uncomplicated iron deficiency."
        ],
        "body": """Anaemia of chronic disease (also designated anaemia of inflammation) occurs in chronic infections, autoimmune diseases, chronic kidney disease, and malignancies. The central pathogenic driver is cytokine-induced upregulation of hepcidin, the master systemic iron regulator. Hepcidin induces internalisation and degradation of ferroportin channels on enterocytes and macrophages, trapping iron within storage sites and preventing release into the circulation.

Although ample iron is sequestered in tissues, developing erythrocytes experience iron-restricted erythropoiesis. Peripheral blood findings commonly start as normocytic normochromic anaemia and can gradually shift to borderline microcytic hypochromic morphology. Crucially, serum ferritin is normal or elevated, and total iron-binding capacity is low or normal, reflecting macrophage iron retention rather than genuine systemic depletion. Typical adult reference ranges vary by laboratory."""
    },
    {
        "id": "REF-MACRO-001",
        "title": "Megaloblastic Haematopoiesis: B12 and Folate Deficiency",
        "source_title": "British Society for Haematology: Guidelines for the Diagnosis and Treatment of Cobalamin and Folate Disorders",
        "source_url": "https://b-s-h.org.uk/guidelines/guidelines-cases/guidelines-for-the-diagnosis-and-treatment-of-cobalamin-and-folate-disorders/",
        "retrieved_at": "2026-03-15",
        "licence_note": "Paraphrased summary of public guideline for educational use; no endorsement implied",
        "section": "Megaloblastic Anaemia",
        "tags": ["macrocytic", "megaloblastic", "b12", "folate"],
        "lang": "en",
        "reviewed": False,
        "key_facts": [
            "Megaloblastosis results from impaired thymidylate synthesis disrupting nuclear DNA replication.",
            "Peripheral blood smears demonstrate hypersegmented neutrophils (five or more lobes) alongside oval macrocytes.",
            "Vitamin B12 deficiency can induce irreversible neurological demyelination even without severe anaemia."
        ],
        "body": """Megaloblastic anaemia is characterized by dyssynchrony between nuclear and cytoplasmic maturation across haematopoietic lineages. Vitamin B12 (cobalamin) and folate function as essential cofactors in the single-carbon transfer pathways required for purine and thymidylate synthesis. When either nutrient is depleted, DNA synthesis stalls while RNA and cytoplasmic protein accumulation continue unimpeded, yielding oversized cells with open, immature nuclear chromatin.

On peripheral examination, the hallmark findings are oval macrocytes and hypersegmented polymorphonuclear neutrophils (defined as neutrophils exhibiting five or more nuclear lobes). Because cobalamin is also required for myelin maintenance through methylmalonyl-CoA mutase, deficiency can produce subacute combined degeneration of the spinal cord, paresthesias, and cognitive decline, which may precede or occur independently of severe haematological deficits. Typical adult reference ranges vary by laboratory."""
    },
    {
        "id": "REF-MACRO-002",
        "title": "Non-Megaloblastic Macrocytosis: Clinical Differential",
        "source_title": "NCBI Bookshelf / StatPearls: Macrocytic Anemia",
        "source_url": "https://www.ncbi.nlm.nih.gov/books/NBK459295/",
        "retrieved_at": "2026-03-15",
        "licence_note": "Paraphrased summary of public guideline for educational use; no endorsement implied",
        "section": "Non-Megaloblastic Causes",
        "tags": ["non_megaloblastic", "alcohol", "liver", "thyroid", "macrocytic"],
        "lang": "en",
        "reviewed": False,
        "key_facts": [
            "Non-megaloblastic macrocytosis occurs without nuclear-cytoplasmic maturation arrest or hypersegmented neutrophils.",
            "Frequent contributors include chronic alcohol intake, liver disease, hypothyroidism, and cytotoxic agents.",
            "Erythrocytes in non-megaloblastic macrocytosis are round rather than oval on the blood film."
        ],
        "body": """Not all elevated MCV values represent vitamin B12 or folate deficiency. Non-megaloblastic macrocytosis represents a distinct group of conditions where erythrocyte enlargement arises without defective DNA replication or abnormal nuclear maturation. On the blood film, erythrocytes appear round rather than oval, and neutrophil hypersegmentation is conspicuously absent.

Common secondary etiologies include chronic alcohol consumption, which exerts direct marrow toxicity and alters membrane lipid fluidity, resolving over weeks after cessation. Hepatic disease alters membrane cholesterol-phospholipid ratios, producing target cells and macrocytosis. Hypothyroidism reduces general metabolic turnover, often producing a mild round macrocytosis. Certain therapeutic agents, particularly antiretrovirals, hydroxycarbamide, and methotrexate, can also induce notable macrocytosis. Thorough clinical history is vital. Typical adult reference ranges vary by laboratory."""
    },
    {
        "id": "REF-TESTING-001",
        "title": "High-Yield Diagnostic Testing Cascades in Anaemia",
        "source_title": "Choosing Wisely UK / Academy of Medical Royal Colleges: Recommendations on Haematology Investigations",
        "source_url": "https://www.choosingwisely.co.uk/recommendations/",
        "retrieved_at": "2026-03-15",
        "licence_note": "Paraphrased summary of public guideline for educational use; no endorsement implied",
        "section": "Resource Stewardship",
        "tags": ["choosing_wisely", "diagnostic_stewardship", "investigations", "high_yield"],
        "lang": "en",
        "reviewed": False,
        "key_facts": [
            "Diagnostic investigation should follow a stepwise cascade guided by red cell indices.",
            "Ordering comprehensive panels simultaneously generates false positives and unneeded expenditures.",
            "Serum ferritin is the single highest-yield first-line test for microcytic presentations."
        ],
        "body": """Modern clinical guidelines advocate structured diagnostic cascades rather than indiscriminate laboratory ordering. When anaemia is identified, testing should be prioritized strictly by morphological phenotype. In microcytic anaemia, obtaining serum ferritin represents the initial high-yield investigation. Reflexively bundling haemoglobin electrophoresis, autoimmune panels, and abdominal imaging before ferritin is verified generates wasteful expenditure and potential diagnostic confusion.

Similarly, in macrocytic anaemia, initial blood film inspection alongside serum B12 and folate levels provides high diagnostic yield. Advanced testing—such as bone marrow aspiration or specialised haemoglobin analysis—should be reserved for cases where initial first-tier non-invasive investigations fail to reveal the diagnosis or when multilineage dysplasia is present. Typical adult reference ranges vary by laboratory."""
    },
    {
        "id": "REF-TESTING-002",
        "title": "Serial Evaluation and Avoiding Reflexive Low-Yield Testing",
        "source_title": "NICE Clinical Knowledge Summaries: Anaemia - Iron Deficiency",
        "source_url": "https://cks.nice.org.uk/topics/anaemia-iron-deficiency/",
        "retrieved_at": "2026-03-15",
        "licence_note": "Paraphrased summary of public guideline for educational use; no endorsement implied",
        "section": "Rational Workup",
        "tags": ["nice_cks", "serial_evaluation", "laboratory_stewardship"],
        "lang": "en",
        "reviewed": False,
        "key_facts": [
            "Clinical evaluation and targeted history direct the laboratory pathway.",
            "Uncalibrated panels risk incidental findings that distract from primary pathologies.",
            "Stepwise diagnostic sequences safeguard patient comfort and preserve resources."
        ],
        "body": """Clinical decision-making in haematological assessment benefits from sequential evaluation. Low-value testing frequently occurs when clinicians order broad panels in an attempt to shorten diagnostic latency, without considering pre-test probability. For example, testing serum iron without ferritin, or requesting extensive coagulopathies for simple microcytosis, adds cost with zero clinical benefit.

A rational diagnostic strategy establishes the morphological category, queries reversible nutritional deficiencies first, and interrogates clinical signs of blood loss, malabsorption, or systemic infection. By allowing each test result to inform subsequent orders, trainees minimize ambiguous borderline findings and protect patients from invasive downstream procedures. Typical adult reference ranges vary by laboratory."""
    },
    {
        "id": "REF-BIAS-001",
        "title": "Cognitive Biases in Diagnostic Decision-Making",
        "source_title": "NCBI Bookshelf / StatPearls: Cognitive Bias in Clinical Medicine",
        "source_url": "https://www.ncbi.nlm.nih.gov/books/NBK557551/",
        "retrieved_at": "2026-03-15",
        "licence_note": "Paraphrased summary of public guideline for educational use; no endorsement implied",
        "section": "Cognitive Biases",
        "tags": ["cognitive_bias", "anchoring", "premature_closure", "reasoning"],
        "lang": "en",
        "reviewed": False,
        "key_facts": [
            "Anchoring bias causes clinicians to over-rely on initial information while discounting subsequent contradictory data.",
            "Premature closure occurs when a clinician accepts a preliminary diagnosis before it has been properly verified.",
            "Cognitive forcing strategies help identify and mitigate heuristic diagnostic errors."
        ],
        "body": """Diagnostic errors in medicine are predominantly cognitive in origin, rooted in predictable heuristic traps rather than lack of factual knowledge. Anchoring bias occurs when a clinician locks onto an initial impression—such as assuming a tired young woman must have nutritional iron deficiency—and fails to adjust their diagnostic stance when subsequent laboratory findings (such as normal ferritin or profound basophilic stippling) conflict with that hypothesis.

Premature closure represents the failure to seek alternative explanations once an initial plausible diagnosis is identified, leading to missed dual pathology or underlying sinister causes. Employing cognitive forcing strategies, such as consciously asking 'What else could explain this laboratory pattern?' and 'What finding contradicts my leading hypothesis?', systematically improves diagnostic calibration and patient safety."""
    },
    {
        "id": "REF-BIAS-002",
        "title": "Calibration of Diagnostic Confidence and Evidence Weighting",
        "source_title": "Royal College of Physicians: Improving Diagnostic Reasoning in Clinical Practice",
        "source_url": "https://www.rcplondon.ac.uk/projects/outputs/improving-diagnostic-reasoning",
        "retrieved_at": "2026-03-15",
        "licence_note": "Paraphrased summary of public guideline for educational use; no endorsement implied",
        "section": "Confidence Calibration",
        "tags": ["calibration", "evidence_weighting", "metacognition", "safety"],
        "lang": "en",
        "reviewed": False,
        "key_facts": [
            "Overconfidence in diagnostic reasoning is strongly associated with high rates of preventable diagnostic error.",
            "Calibrated clinicians align their subjective certainty with objective evidential strength.",
            "Reflective pauses before finalising diagnoses facilitate identification of contradictory cues."
        ],
        "body": """Diagnostic calibration describes the degree of alignment between a clinician's subjective confidence in a diagnostic decision and its objective likelihood of accuracy. Studies across medical training consistently reveal poor calibration among novice learners, who frequently report 90% or greater diagnostic certainty on cases with incomplete, contradictory, or borderline evidence.

This mismatch breeds premature closure and prevents seeking senior guidance. Well-calibrated clinical reasoning requires weighting evidence according to diagnostic sensitivity and specificity, recognizing the limits of heuristic rules, and actively maintaining cognitive humility. Introducing deliberate reflective pauses before locking in clinical impressions enables trainees to spot incongruities between patient findings and suspected conditions."""
    },
    {
        "id": "REF-REDALERT-001",
        "title": "Etiological Investigation of Iron Deficiency and Red-Flag Features",
        "source_title": "British Society of Gastroenterology: Guidelines for the Management of Iron Deficiency Anaemia in Adults",
        "source_url": "https://www.bsg.org.uk/clinical-resource/guidelines-for-the-management-of-iron-deficiency-anaemia/",
        "retrieved_at": "2026-03-15",
        "licence_note": "Paraphrased summary of public guideline for educational use; no endorsement implied",
        "section": "Etiological Red Flags",
        "tags": ["iron_deficiency", "gastrointestinal", "red_flags", "underlying_cause"],
        "lang": "en",
        "reviewed": False,
        "key_facts": [
            "Iron deficiency is a clinical symptom requiring an underlying etiological diagnosis, not a final disease entity.",
            "In men and postmenopausal women, gastrointestinal blood loss must be suspected until proven otherwise.",
            "Red-flag features including altered bowel habit, rectal bleeding, or unintentional weight loss require urgent referral."
        ],
        "body": """Confirming iron deficiency through laboratory testing is only the initial step in patient care; identifying the underlying pathophysiological cause is essential. In adult men and postmenopausal women, dietary inadequacy alone is rarely the sole driver. Occult gastrointestinal bleeding from benign ulceration, inflammatory bowel disease, coeliac disease, or gastrointestinal malignancy represents the chief consideration.

Red-flag clinical features—including unintentional weight loss, visible rectal bleeding, persistent alteration in bowel habit, persistent dysphagia, or palpable abdominal masses—mandate prompt escalation and urgent referral for endoscopic investigation per national fast-track cancer pathways. Trainees must avoid labelling iron deficiency as a finished diagnosis without establishing why the deficit occurred. Typical adult reference ranges vary by laboratory."""
    },
    {
        "id": "REF-REDALERT-002",
        "title": "Structured Escalation and Senior Communication in Haematological Care",
        "source_title": "General Medical Council: Good Medical Practice and Raising Patient Safety Concerns",
        "source_url": "https://www.gmc-uk.org/ethical-guidance/ethical-guidance-for-doctors/good-medical-practice",
        "retrieved_at": "2026-03-15",
        "licence_note": "Paraphrased summary of public guideline for educational use; no endorsement implied",
        "section": "Escalation & Communication",
        "tags": ["escalation", "sbar", "patient_safety", "senior_consultation"],
        "lang": "en",
        "reviewed": False,
        "key_facts": [
            "Trainees must promptly escalate unexplained pancytopenia, rapid haemoglobin falls, or severe symptoms.",
            "Structured communication tools such as SBAR ensure concise, actionable transfer of critical clinical information.",
            "Timely escalation protects patient safety and enables rapid senior-level diagnostic intervention."
        ],
        "body": """Recognizing when patient findings exceed independent trainee scope is a foundational safety attribute. Critical haematological escalation triggers include profound symptomatic cytopenias, unexplained multilineage abnormalities (pancytopenia), suspected acute leukaemia or marrow infiltration, evidence of active acute internal bleeding, and atypical systemic symptoms accompanied by unexplained lymphadenopathy or organomegaly.

When communicating with senior medical staff, trainees should utilize validated structured frameworks such as SBAR (Situation, Background, Assessment, Recommendation). Clearly framing the patient's acute status, key objective laboratory values, diagnostic concerns, and specific requested senior action ensures efficient clinical decision-making and safeguards patient outcomes. Trainees should document escalation decisions meticulously."""
    }
]

LESSONS = [
    {
        "id": "LESSON-01",
        "title": "Reading a Full Blood Count Systematically",
        "objective_id": "LO-FBC-SYSTEMATIC",
        "status": "draft",
        "reviewed_by": None,
        "reviewed_at": None,
        "review_notes": [
            "TODO_REVIEWER: Confirm whether local teaching hospital prefers reporting Hb in g/L or g/dL as primary standard.",
            "TODO_REVIEWER: Verify whether platelet indices (MPV) should be formally integrated into initial trainee reading checklist."
        ],
        "estimated_minutes": 8,
        "difficulty": 1,
        "targets_misconceptions": ["MC-IGNORES-INDICES"],
        "prerequisites": [],
        "learning_outcomes": [
            "Identify all primary red cell indices including haemoglobin, mean cell volume, and red cell distribution width before arriving at a clinical conclusion.",
            "Recognize how white blood cell and platelet counts interact with red cell indices to identify multilineage processes.",
            "Formulate a structured sequence for reading haematology panels to prevent premature diagnostic assumptions."
        ],
        "key_points": [
            {
                "point": "Begin every full blood count review by noting haemoglobin to determine whether anaemia is present, but never stop there.",
                "refs": ["REF-FBC-001"]
            },
            {
                "point": "Evaluate mean cell volume to establish the morphological classification as microcytic, normocytic, or macrocytic.",
                "refs": ["REF-FBC-001"]
            },
            {
                "point": "Check red cell distribution width to identify anisocytosis, which highlights mixed populations or evolving deficiency.",
                "refs": ["REF-FBC-002"]
            },
            {
                "point": "Examine white blood cell and platelet counts to verify whether the pathology is isolated to erythrocytes or involves multiple cell lines.",
                "refs": ["REF-FBC-001"]
            },
            {
                "point": "Remember that typical adult ranges vary by laboratory and patient demographic factors.",
                "refs": ["REF-FBC-001"]
            }
        ],
        "worked_example": {
            "vignette": "A 24-year-old student attends clinic describing four weeks of generalized tiredness and breathlessness on exertion. Initial full blood count reveals a low haemoglobin level. Rather than immediately concluding iron deficiency based on tiredness alone, the attending resident reviews the entire panel step by step.",
            "steps": [
                "Step 1: Check haemoglobin to confirm the presence and severity of anaemia.",
                "Step 2: Examine MCV to classify the red cell size (found to be significantly low, confirming microcytosis).",
                "Step 3: Review RDW to determine if cell sizes are uniform or variable (elevated, indicating marked anisocytosis).",
                "Step 4: Check white cells and platelets (normal leukocytes, mildly elevated reactive platelets, suggesting an isolated erythroid response).",
                "Step 5: Synthesize findings into a complete picture before ordering targeted iron studies."
            ]
        },
        "common_pitfalls": [
            "Stopping after reading the haemoglobin value and guessing the underlying etiology without checking cell indices.",
            "Overlooking an elevated RDW in a patient whose MCV falls into the borderline normal range.",
            "Ignoring abnormal leukocyte or platelet counts that point to marrow infiltration rather than simple nutritional deficiency."
        ],
        "clinical_pearl": "A full blood count is a complete clinical puzzle; interpreting haemoglobin in isolation is like reading only the first sentence of a chapter.",
        "quick_check": [
            {
                "id": "Q1",
                "prompt": "A trainee receives a blood panel showing subnormal haemoglobin. Which sequence best illustrates a systematic diagnostic approach before concluding etiology?",
                "options": [
                    {"id": "A", "text": "Assess MCV and RDW, verify white cell and platelet counts, then review the blood film and targeted biomarkers."},
                    {"id": "B", "text": "Immediately arrange abdominal ultrasonography and request full cross-matching."},
                    {"id": "C", "text": "Focus solely on leukocyte numbers and ignore red cell indices if white cells are normal."},
                    {"id": "D", "text": "Assume nutritional deficiency immediately and skip checking other cell lineages."}
                ],
                "correct": "A",
                "rationale": "Option A follows the systematic sequence of reading indices, assessing multilineage integrity, and selecting targeted confirmatory tests. Option D commits premature closure, while Option B orders low-yield invasive imaging prematurely.",
                "reference_id": "REF-FBC-001"
            },
            {
                "id": "Q2",
                "prompt": "A patient presents with low haemoglobin, an MCV within typical limits, but a markedly elevated RDW. What is the most plausible explanation for this combination?",
                "options": [
                    {"id": "A", "text": "The patient has perfectly uniform erythrocytes with no variation in cell size."},
                    {"id": "B", "text": "A mixed population of microcytic and macrocytic cells is averaging out the MCV while widening the distribution curve."},
                    {"id": "C", "text": "The patient has pure beta-thalassaemia trait without any coexisting conditions."},
                    {"id": "D", "text": "Laboratory automation failure has inverted the platelet count and red cell volume."}
                ],
                "correct": "B",
                "rationale": "Option B correctly explains that concurrent nutritional deficiencies (e.g. iron plus B12) create dual cell populations that average out to a pseudo-normal MCV while widening RDW. Option A is contradicted by the elevated RDW, and Option C typically presents with a normal RDW.",
                "reference_id": "REF-FBC-002"
            },
            {
                "id": "Q3",
                "prompt": "When evaluating a patient with newly detected anaemia, why is checking platelet and white cell counts a vital initial step?",
                "options": [
                    {"id": "A", "text": "Platelet counts are required to calculate the exact mean corpuscular volume."},
                    {"id": "B", "text": "White blood cells directly synthesize haemoglobin during acute stress."},
                    {"id": "C", "text": "Multilineage cytopenias suggest marrow failure or infiltration, requiring urgent senior escalation rather than simple outpatient iron studies."},
                    {"id": "D", "text": "Platelet counts are completely unrelated to haematological assessment and can be omitted."}
                ],
                "correct": "C",
                "rationale": "Option C highlights patient safety: multilineage cytopenias indicate bone marrow processes or splenic pooling rather than simple isolated nutritional deficiency. Options A and B are biologically incorrect statements.",
                "reference_id": "REF-FBC-001"
            }
        ],
        "reference_ids": ["REF-FBC-001", "REF-FBC-002"],
        "further_reading": [
            {
                "title": "British Society for Haematology: Guidelines for the laboratory diagnosis of functional iron deficiency",
                "url": "https://b-s-h.org.uk/guidelines/guidelines-cases/guidelines-for-the-laboratory-diagnosis-of-functional-iron-deficiency/"
            },
            {
                "title": "StatPearls: Red Cell Distribution Width",
                "url": "https://www.ncbi.nlm.nih.gov/books/NBK545266/"
            }
        ]
    },
    {
        "id": "LESSON-02",
        "title": "Classifying Anaemia by Cell Size",
        "objective_id": "LO-CELL-SIZE-CLASSIFICATION",
        "status": "draft",
        "reviewed_by": None,
        "reviewed_at": None,
        "review_notes": [
            "TODO_REVIEWER: Verify standard teaching terminology for normocytic vs normochromic classifications.",
            "TODO_REVIEWER: Confirm whether reticulocyte production index formula should be introduced at this stage or deferred."
        ],
        "estimated_minutes": 7,
        "difficulty": 1,
        "targets_misconceptions": ["MC-MACRO-MICRO-CONFUSED"],
        "prerequisites": ["LESSON-01"],
        "learning_outcomes": [
            "Classify anaemias into microcytic, normocytic, and macrocytic categories based on mean cell volume.",
            "Differentiate the primary physiological mechanisms producing altered erythrocyte dimensions.",
            "Correlate cell size classifications with initial diagnostic possibilities before ordering advanced tests."
        ],
        "key_points": [
            {
                "point": "Mean cell volume divides anaemias into microcytic, normocytic, and macrocytic morphological groups.",
                "refs": ["REF-CELLSIZE-001"]
            },
            {
                "point": "Microcytosis indicates defective haemoglobin production, commonly seen in iron deficiency or globin defects.",
                "refs": ["REF-CELLSIZE-001"]
            },
            {
                "point": "Macrocytosis indicates impaired nuclear maturation or membrane alteration, seen in B12/folate deficiency or liver disease.",
                "refs": ["REF-CELLSIZE-001"]
            },
            {
                "point": "Normocytic anaemia demands assessing reticulocyte count to distinguish marrow failure from peripheral loss or haemolysis.",
                "refs": ["REF-CELLSIZE-002"]
            },
            {
                "point": "Typical adult ranges vary by laboratory, but MCV between 80 and 100 fL is the standard operational normocytic window.",
                "refs": ["REF-CELLSIZE-001"]
            }
        ],
        "worked_example": {
            "vignette": "A 52-year-old individual presents with progressive fatigue. Laboratory testing reveals haemoglobin below normal limits. The junior trainee notices an MCV of 71 fL and considers initiating vitamin B12 investigations. A senior colleague intervenes to review the morphological branch point.",
            "steps": [
                "Step 1: Check the MCV value (71 fL, which sits clearly below typical adult laboratory boundaries).",
                "Step 2: Classify the morphological presentation as microcytic anaemia.",
                "Step 3: Recognize that vitamin B12 deficiency produces macrocytosis (elevated MCV), making it an inappropriate initial path.",
                "Step 4: Align the workup to microcytic etiologies: iron deficiency, thalassaemia trait, or anaemia of chronic disease."
            ]
        },
        "common_pitfalls": [
            "Ordering vitamin B12 and folate tests for clear microcytic anaemia without clinical justification.",
            "Assuming all normocytic anaemias are benign without checking reticulocyte count or kidney function.",
            "Forgetting that mixed deficiencies can generate an apparently normal MCV while cell distribution is abnormal."
        ],
        "clinical_pearl": "Let the MCV narrow your differential compass before choosing the direction of your laboratory investigation.",
        "quick_check": [
            {
                "id": "Q1",
                "prompt": "A laboratory report shows a patient with marked anaemia and an MCV of 68 fL. Which diagnostic pathway is most appropriate to explore first?",
                "options": [
                    {"id": "A", "text": "Evaluate serum vitamin B12 and red cell folate concentration."},
                    {"id": "B", "text": "Schedule emergency bone marrow examination for suspected aplastic crisis."},
                    {"id": "C", "text": "Reassure the patient that cell size indicates complete nutritional adequacy."},
                    {"id": "D", "text": "Investigate microcytic etiologies including iron deficiency, thalassaemia trait, and chronic inflammation."}
                ],
                "correct": "D",
                "rationale": "Option D matches the microcytic presentation (MCV < 80 fL), pointing toward iron deficiency or thalassaemia. Option A is incorrect because B12 and folate deficiencies cause macrocytosis, making it an inappropriate initial focus.",
                "reference_id": "REF-CELLSIZE-001"
            },
            {
                "id": "Q2",
                "prompt": "Which mechanism explains why developing red blood cells become microcytic during states of substrate deficiency?",
                "options": [
                    {"id": "A", "text": "Impaired haemoglobin synthesis delays cytoplasmic density, prompting erythroblasts to undergo extra divisions."},
                    {"id": "B", "text": "Nuclear DNA synthesis ceases entirely while lipid membrane production accelerates."},
                    {"id": "C", "text": "Excess circulating iron physically compresses erythrocyte membranes within the spleen."},
                    {"id": "D", "text": "Erythroblasts skip cell divisions entirely, releasing undersized precursors into the blood."}
                ],
                "correct": "A",
                "rationale": "Option A correctly describes the cellular pathophysiology: lack of iron or globin leads to extra mitotic cycles before reaching critical haemoglobin density. Option D describes the opposite mechanism seen in megaloblastosis.",
                "reference_id": "REF-CELLSIZE-001"
            },
            {
                "id": "Q3",
                "prompt": "In an anaemic patient with a normal MCV (normocytic anaemia), which laboratory investigation provides the most immediate insight into bone marrow productivity?",
                "options": [
                    {"id": "A", "text": "Erythrocyte sedimentation rate (ESR)."},
                    {"id": "B", "text": "Reticulocyte count or reticulocyte production index."},
                    {"id": "C", "text": "Total serum cholesterol level."},
                    {"id": "D", "text": "Routine urine sediment microscopy."}
                ],
                "correct": "B",
                "rationale": "Option B directly quantifies marrow response, distinguishing hypo-productive states from ongoing destruction or acute blood loss. Options A, C, and D do not assess erythropoietic activity.",
                "reference_id": "REF-CELLSIZE-002"
            }
        ],
        "reference_ids": ["REF-CELLSIZE-001", "REF-CELLSIZE-002"],
        "further_reading": [
            {
                "title": "NCBI StatPearls: Microcytic Anemia",
                "url": "https://www.ncbi.nlm.nih.gov/books/NBK459254/"
            },
            {
                "title": "NCBI StatPearls: Normocytic Normochromic Anemia",
                "url": "https://www.ncbi.nlm.nih.gov/books/NBK560814/"
            }
        ]
    },
    {
        "id": "LESSON-03",
        "title": "Iron Studies and Ferritin Interpretation",
        "objective_id": "LO-FERRITIN-INTERPRETATION",
        "status": "draft",
        "reviewed_by": None,
        "reviewed_at": None,
        "review_notes": [
            "TODO_REVIEWER: Validate local cut-off for ferritin in inflammatory states (e.g. < 50 ng/mL vs < 100 ng/mL).",
            "TODO_REVIEWER: Confirm availability of soluble transferrin receptor testing in regional laboratories."
        ],
        "estimated_minutes": 9,
        "difficulty": 2,
        "targets_misconceptions": ["MC-FERRITIN-MISSED"],
        "prerequisites": ["LESSON-02"],
        "learning_outcomes": [
            "Interpret serum ferritin values as the primary indicator of total reticuloendothelial storage reserves.",
            "Analyze the confounding impact of systemic inflammation on acute-phase ferritin levels.",
            "Integrate transferrin saturation when ferritin interpretation is compromised by coexisting inflammation."
        ],
        "key_points": [
            {
                "point": "Serum ferritin is the most specific non-invasive laboratory marker of depleted iron storage reserves.",
                "refs": ["REF-FERRITIN-002"]
            },
            {
                "point": "A subnormal ferritin value is diagnostic of iron deficiency in non-inflammatory clinical settings.",
                "refs": ["REF-FERRITIN-002"]
            },
            {
                "point": "Ferritin functions as an acute-phase reactant; systemic inflammation falsely elevates circulating levels.",
                "refs": ["REF-FERRITIN-002"]
            },
            {
                "point": "Transferrin saturation below 20% identifies iron-restricted erythropoiesis when ferritin is elevated by inflammation.",
                "refs": ["REF-FERRITIN-003"]
            },
            {
                "point": "Isolated serum iron fluctuates widely with diurnal rhythm and meals; it should never be interpreted alone.",
                "refs": ["REF-FERRITIN-003"]
            }
        ],
        "worked_example": {
            "vignette": "A 64-year-old with active rheumatoid arthritis presents with worsening fatigue and microcytic anaemia. Serum ferritin returns at 110 ng/mL (within conventional laboratory reference boundaries). The trainee considers ruling out iron deficiency based on the ferritin number. The clinical educator reviews the confounding role of inflammatory cytokines.",
            "steps": [
                "Step 1: Note the coexisting inflammatory condition (rheumatoid arthritis with elevated CRP).",
                "Step 2: Recognize that inflammatory cytokines upregulate ferritin synthesis independently of iron reserves.",
                "Step 3: Review transferrin saturation (calculated at 11%, well below the 20% physiological threshold).",
                "Step 4: Conclude that true functional iron limitation exists despite the seemingly adequate ferritin reading."
            ]
        },
        "common_pitfalls": [
            "Ruling out iron deficiency solely because ferritin falls into the standard laboratory reference range during acute illness.",
            "Relying on random serum iron without calculating transferrin saturation or checking ferritin.",
            "Initiating iron therapy without establishing a baseline ferritin or identifying the underlying clinical cause."
        ],
        "clinical_pearl": "In an inflamed patient, a normal ferritin does not guarantee full iron stores; look to transferrin saturation to unmask functional deficiency.",
        "quick_check": [
            {
                "id": "Q1",
                "prompt": "Why is serum ferritin regarded as superior to random serum iron for evaluating body iron reserves?",
                "options": [
                    {"id": "A", "text": "Serum ferritin is exclusively produced by circulating red blood cells during haemolysis."},
                    {"id": "B", "text": "Random serum iron values never change during the day or following dietary intake."},
                    {"id": "C", "text": "Ferritin reflects total intracellular storage reserves, whereas serum iron fluctuates markedly with diurnal cycles and meals."},
                    {"id": "D", "text": "Serum ferritin directly measures oxygen delivery to peripheral tissues."}
                ],
                "correct": "C",
                "rationale": "Option C correctly identifies that ferritin reflects reticuloendothelial storage reserves, whereas serum iron exhibits substantial diurnal volatility. Option B is factually inverted.",
                "reference_id": "REF-FERRITIN-002"
            },
            {
                "id": "Q2",
                "prompt": "A patient with severe Crohn's colitis exhibits microcytic anaemia, a serum ferritin of 95 ng/mL, and an elevated C-reactive protein. What is the most appropriate next step in interpreting their iron status?",
                "options": [
                    {"id": "A", "text": "Completely exclude iron deficiency because ferritin is above the standard non-inflamed threshold."},
                    {"id": "B", "text": "Diagnose acute iron toxicity and prepare immediate chelation therapy."},
                    {"id": "C", "text": "Order routine bone marrow trephine biopsy as the mandatory second-line outpatient test."},
                    {"id": "D", "text": "Calculate transferrin saturation to evaluate whether functional iron-restricted erythropoiesis is present despite acute-phase elevation."}
                ],
                "correct": "D",
                "rationale": "Option D correctly addresses the acute-phase confounder: checking transferrin saturation identifies iron restriction when ferritin is elevated by active colitis. Option A falls into the common trap of ignoring inflammatory acute-phase response.",
                "reference_id": "REF-FERRITIN-003"
            },
            {
                "id": "Q3",
                "prompt": "In an otherwise healthy adult without infection or inflammatory disease, which laboratory finding is virtually pathognomonic for iron deficiency?",
                "options": [
                    {"id": "A", "text": "Serum ferritin below laboratory deficiency cut-off values."},
                    {"id": "B", "text": "Isolated mild elevation of white blood cell count."},
                    {"id": "C", "text": "Marginal elevation of mean corpuscular haemoglobin concentration."},
                    {"id": "D", "text": "Normal transferrin saturation accompanied by normal MCV."}
                ],
                "correct": "A",
                "rationale": "Option A is correct: low ferritin in the absence of inflammation is virtually 100% specific for depleted iron stores. Options B, C, and D do not demonstrate iron deficiency.",
                "reference_id": "REF-FERRITIN-002"
            }
        ],
        "reference_ids": ["REF-FERRITIN-002", "REF-FERRITIN-003"],
        "further_reading": [
            {
                "title": "WHO Guideline on use of ferritin concentrations to assess iron status",
                "url": "https://www.who.int/publications/i/item/9789240008526"
            },
            {
                "title": "British Society for Haematology: Diagnosis and management of iron deficiency",
                "url": "https://b-s-h.org.uk/guidelines/guidelines-cases/diagnosis-and-management-of-iron-deficiency/"
            }
        ]
    },
    {
        "id": "LESSON-04",
        "title": "The Microcytic Differential: Iron Deficiency, Thalassaemia, and Chronic Disease",
        "objective_id": "LO-MICROCYTIC-DIFFERENTIAL",
        "status": "draft",
        "reviewed_by": None,
        "reviewed_at": None,
        "review_notes": [
            "TODO_REVIEWER: Confirm whether Mentzer index (MCV/RBC < 13) should be presented solely as a heuristic screening tool or if another index (e.g. Green & King) is preferred.",
            "TODO_REVIEWER: Confirm laboratory protocol threshold for reflex haemoglobin electrophoresis in suspected thalassaemia minor."
        ],
        "estimated_minutes": 9,
        "difficulty": 2,
        "targets_misconceptions": ["MC-MICRO-DIFFERENTIAL"],
        "prerequisites": ["LESSON-02", "LESSON-03"],
        "learning_outcomes": [
            "Compare red cell distribution width patterns between iron deficiency and heterozygous thalassaemia trait.",
            "Evaluate red blood cell count and ferritin findings to distinguish reduced synthesis from defective globin chains.",
            "Recognize the role of anaemia of chronic disease in producing normal or low cell size with preserved iron stores."
        ],
        "key_points": [
            {
                "point": "The three primary causes of microcytic anaemia are iron deficiency, thalassaemia trait, and anaemia of chronic disease.",
                "refs": ["REF-MICRODIFF-001"]
            },
            {
                "point": "Heterozygous thalassaemia trait typically features severe microcytosis with an elevated or normal red blood cell count and normal RDW.",
                "refs": ["REF-MICRODIFF-001"]
            },
            {
                "point": "Iron deficiency features progressive microcytosis, subnormal red cell count, and an elevated RDW reflecting anisocytosis.",
                "refs": ["REF-MICRODIFF-001"]
            },
            {
                "point": "Mathematical screening formulas like the Mentzer heuristic (MCV/RBC) provide screening clues but require confirmatory testing.",
                "refs": ["REF-MICRODIFF-001"]
            },
            {
                "point": "Anaemia of chronic disease traps iron in storage cells, exhibiting normal or high ferritin with low transferrin saturation.",
                "refs": ["REF-MICRODIFF-002"]
            }
        ],
        "worked_example": {
            "vignette": "A 28-year-old of Mediterranean descent attends routine health screening. Blood tests show mild anaemia with an MCV of 64 fL and a red blood cell count of 6.2 x 10^12/L. The resident considers empirical iron therapy. The attending physician calculates the Mentzer heuristic (64 / 6.2 = 10.3) and reviews the red cell parameters.",
            "steps": [
                "Step 1: Observe that the MCV is markedly low out of proportion to the very mild anaemia.",
                "Step 2: Note the elevated red blood cell count (erythrocytosis), typical of thalassaemic marrow compensation.",
                "Step 3: Review RDW (normal, indicating uniform microcytic cells rather than variable nutritional deficiency).",
                "Step 4: Check serum ferritin (normal), ruling out simple iron deficiency and avoiding inappropriate iron supplementation.",
                "Step 5: Order haemoglobin variant analysis to confirm beta-thalassaemia trait."
            ]
        },
        "common_pitfalls": [
            "Assuming every patient with a low MCV has iron deficiency and administering prolonged iron therapy without testing ferritin.",
            "Missing thalassaemia trait because the mild anaemia was dismissed without noting the disproportionately low MCV.",
            "Treating screening ratios like Mentzer index as definitive diagnoses rather than heuristics requiring laboratory confirmation."
        ],
        "clinical_pearl": "Tiny cells with high red cell counts suggest thalassaemia trait; tiny cells with high RDW and low ferritin point to iron deficiency.",
        "quick_check": [
            {
                "id": "Q1",
                "prompt": "A patient presents with mild microcytic anaemia, an MCV of 62 fL, a high red cell count of 6.5 x 10^12/L, and a normal RDW. Which diagnosis is most strongly suggested by this constellation?",
                "options": [
                    {"id": "A", "text": "Acute gastrointestinal haemorrhage."},
                    {"id": "B", "text": "Heterozygous thalassaemia trait."},
                    {"id": "C", "text": "Advanced megaloblastic anaemia."},
                    {"id": "D", "text": "Severe uncomplicated iron deficiency anaemia."}
                ],
                "correct": "B",
                "rationale": "Option B is correct: thalassaemia trait produces uniform microcytosis (normal RDW) and a high red cell count. In iron deficiency (Option D), red cell count is typically low and RDW is elevated.",
                "reference_id": "REF-MICRODIFF-001"
            },
            {
                "id": "Q2",
                "prompt": "How does anaemia of chronic disease differ from uncomplicated iron deficiency in laboratory iron parameters?",
                "options": [
                    {"id": "A", "text": "Anaemia of chronic disease always exhibits a ferritin level below 10 ng/mL."},
                    {"id": "B", "text": "Total iron binding capacity is markedly elevated in anaemia of chronic disease."},
                    {"id": "C", "text": "Ferritin is preserved or elevated due to macrophage iron sequestration, with low to normal total iron-binding capacity."},
                    {"id": "D", "text": "Anaemia of chronic disease exhibits massive reticulocytosis and severe macrocytosis."}
                ],
                "correct": "C",
                "rationale": "Option C accurately reflects iron sequestration mediated by hepcidin in chronic inflammation: stores are retained (normal/high ferritin), but release is blocked. Option A describes true iron depletion.",
                "reference_id": "REF-MICRODIFF-002"
            },
            {
                "id": "Q3",
                "prompt": "What is the primary clinical hazard of empirically prescribing oral iron to a patient with heterozygous thalassaemia trait who has normal iron stores?",
                "options": [
                    {"id": "A", "text": "Immediate induction of severe megaloblastic crisis."},
                    {"id": "B", "text": "Conversion of beta-thalassaemia trait into acute aplastic anaemia."},
                    {"id": "C", "text": "Sudden catastrophic intravascular haemolysis of all circulating reticulocytes."},
                    {"id": "D", "text": "Ineffective therapy with risk of progressive iron overload and delay in accurate genetic counselling."}
                ],
                "correct": "D",
                "rationale": "Option D highlights patient safety: thalassaemia trait does not benefit from iron and unneeded therapy can produce secondary iron loading over time while missing genetic counselling opportunities.",
                "reference_id": "REF-MICRODIFF-001"
            }
        ],
        "reference_ids": ["REF-MICRODIFF-001", "REF-MICRODIFF-002"],
        "further_reading": [
            {
                "title": "British Society for Haematology: Laboratory investigation of haemoglobinopathies",
                "url": "https://b-s-h.org.uk/guidelines/guidelines-cases/investigation-of-haemoglobinopathies/"
            },
            {
                "title": "StatPearls: Anemia of Chronic Disease",
                "url": "https://www.ncbi.nlm.nih.gov/books/NBK499888/"
            }
        ]
    },
    {
        "id": "LESSON-05",
        "title": "Macrocytic Anaemia: Megaloblastic and Non-Megaloblastic Pathways",
        "objective_id": "LO-MACROCYTIC-ETIOLOGY",
        "status": "draft",
        "reviewed_by": None,
        "reviewed_at": None,
        "review_notes": [
            "TODO_REVIEWER: Validate guidance on checking methylmalonic acid vs total serum cobalamin in borderline B12 cases.",
            "TODO_REVIEWER: Confirm local policy regarding anti-intrinsic factor antibody testing in primary care."
        ],
        "estimated_minutes": 8,
        "difficulty": 2,
        "targets_misconceptions": ["MC-MACRO-CAUSE-MISSED"],
        "prerequisites": ["LESSON-02"],
        "learning_outcomes": [
            "Distinguish megaloblastic processes from non-megaloblastic causes of elevated erythrocyte volume.",
            "Identify secondary factors including alcohol exposure, thyroid hypofunction, liver disease, and specific therapeutics.",
            "Appraise the peripheral blood film for hypersegmented neutrophils and oval macrocytes to direct etiology."
        ],
        "key_points": [
            {
                "point": "Macrocytic anaemia is divided into megaloblastic (impaired DNA synthesis) and non-megaloblastic etiologies.",
                "refs": ["REF-MACRO-001"]
            },
            {
                "point": "Megaloblastic anaemia is characterized on blood film by oval macrocytes and hypersegmented polymorphonuclear leukocytes.",
                "refs": ["REF-MACRO-001"]
            },
            {
                "point": "Vitamin B12 deficiency can cause severe subacute combined degeneration of the cord without marked anaemia.",
                "refs": ["REF-MACRO-001"]
            },
            {
                "point": "Non-megaloblastic causes present with round macrocytes and include alcohol exposure, liver pathology, and hypothyroidism.",
                "refs": ["REF-MACRO-002"]
            },
            {
                "point": "Certain therapeutic classes (e.g. hydroxycarbamide, methotrexate, antiretrovirals) directly elevate MCV.",
                "refs": ["REF-MACRO-002"]
            }
        ],
        "worked_example": {
            "vignette": "A 58-year-old presenting with mild macrocytic anaemia (MCV 106 fL) mentions tingling in both feet and balance difficulties in the dark. The trainee notices normal liver enzymes and considers attributing the macrocytosis to alcohol intake without taking a neurological history. The attending emphasizes clinical examination.",
            "steps": [
                "Step 1: Identify macrocytosis (MCV 106 fL, above expected laboratory boundaries).",
                "Step 2: Recognize neurological complaints (paresthesias, loss of vibration sense and proprioception).",
                "Step 3: Review blood smear: hypersegmented neutrophils present, confirming megaloblastic process.",
                "Step 4: Check serum B12 and folate: cobalamin is profoundly depressed.",
                "Step 5: Prioritize cobalamin replacement per local protocol and investigate pernicious anaemia."
            ]
        },
        "common_pitfalls": [
            "Assuming all macrocytosis is due to alcohol without evaluating B12, folate, or medication exposures.",
            "Administering folate alone to a patient with undetected B12 deficiency, which can precipitate irreversible neurological damage.",
            "Overlooking subtle neurological deficits in elderly patients presenting with macrocytic indices."
        ],
        "clinical_pearl": "Never administer folate in megaloblastosis without first verifying cobalamin status, lest you worsen subacute combined degeneration.",
        "quick_check": [
            {
                "id": "Q1",
                "prompt": "Which peripheral blood smear feature is considered pathognomonic for a megaloblastic anaemia rather than non-megaloblastic macrocytosis?",
                "options": [
                    {"id": "A", "text": "Hypersegmented neutrophils exhibiting five or more nuclear lobes alongside oval macrocytes."},
                    {"id": "B", "text": "Target cells with completely round erythrocyte morphology."},
                    {"id": "C", "text": "Marked microcytosis with basophilic stippling."},
                    {"id": "D", "text": "Agglutinated clumps of platelets without red cell abnormalities."}
                ],
                "correct": "A",
                "rationale": "Option A describes the classical megaloblastic blood film reflecting disrupted nuclear replication. Target cells and round macrocytes (Option B) are characteristic of liver disease or alcohol effect (non-megaloblastic).",
                "reference_id": "REF-MACRO-001"
            },
            {
                "id": "Q2",
                "prompt": "Why is giving isolated folate therapy to a patient with unrecognized severe vitamin B12 deficiency clinically dangerous?",
                "options": [
                    {"id": "A", "text": "Folate accelerates gastrointestinal excretion of iron, causing acute hypovolaemia."},
                    {"id": "B", "text": "It can correct the haematological parameters while allowing devastating subacute combined degeneration of the spinal cord to progress."},
                    {"id": "C", "text": "It directly triggers acute renal tubular necrosis within twenty-four hours."},
                    {"id": "D", "text": "It neutralizes endogenous thyroid hormone, inducing myxoedema coma."}
                ],
                "correct": "B",
                "rationale": "Option B is a critical patient safety principle: folate can resolve megaloblastic erythropoiesis while leaving cobalamin-dependent myelination impaired, risking permanent paraplegia.",
                "reference_id": "REF-MACRO-001"
            },
            {
                "id": "Q3",
                "prompt": "In an anaemic patient with round macrocytes, no neutrophil hypersegmentation, normal B12 and folate levels, which underlying cause should be thoroughly explored?",
                "options": [
                    {"id": "A", "text": "Acute lead poisoning with mitochondrial enzyme blockage."},
                    {"id": "B", "text": "Isolated nutritional ascorbic acid deficiency."},
                    {"id": "C", "text": "Chronic alcohol consumption, chronic liver disease, or untreated hypothyroidism."},
                    {"id": "D", "text": "Alpha-thalassaemia trait with chain precipitation."}
                ],
                "correct": "C",
                "rationale": "Option C highlights the core non-megaloblastic differential: alcohol, liver disease, and hypothyroidism expand cell volume without megaloblastosis. Alpha-thalassaemia (Option D) produces microcytosis.",
                "reference_id": "REF-MACRO-002"
            }
        ],
        "reference_ids": ["REF-MACRO-001", "REF-MACRO-002"],
        "further_reading": [
            {
                "title": "British Society for Haematology: Guidelines for the diagnosis and treatment of cobalamin and folate disorders",
                "url": "https://b-s-h.org.uk/guidelines/guidelines-cases/guidelines-for-the-diagnosis-and-treatment-of-cobalamin-and-folate-disorders/"
            },
            {
                "title": "NCBI StatPearls: Macrocytic Anemia",
                "url": "https://www.ncbi.nlm.nih.gov/books/NBK459295/"
            }
        ]
    },
    {
        "id": "LESSON-06",
        "title": "Choosing Investigations Wisely in Anaemia Workup",
        "objective_id": "LO-RATIONAL-INVESTIGATION",
        "status": "draft",
        "reviewed_by": None,
        "reviewed_at": None,
        "review_notes": [
            "TODO_REVIEWER: Review cost-effectiveness ranking of initial haematology panels in regional healthcare network.",
            "TODO_REVIEWER: Confirm whether coeliac serology is recommended as routine first-line in all unexplained iron deficiency."
        ],
        "estimated_minutes": 7,
        "difficulty": 2,
        "targets_misconceptions": ["MC-WASTEFUL-TESTING"],
        "prerequisites": ["LESSON-01", "LESSON-02"],
        "learning_outcomes": [
            "Select high-yield initial investigations based on morphological classification of anaemia.",
            "Sequence secondary diagnostic testing logically to avoid redundant or low-yield laboratory requests.",
            "Defend resource-conscious diagnostic choices that reduce learner delay and healthcare waste."
        ],
        "key_points": [
            {
                "point": "Testing in anaemia should proceed in a logical stepwise cascade guided by initial red cell morphology.",
                "refs": ["REF-TESTING-001"]
            },
            {
                "point": "Ordering large indiscriminate panels increases false positive rates and causes diagnostic distraction.",
                "refs": ["REF-TESTING-001"]
            },
            {
                "point": "In microcytic anaemia, serum ferritin is the single highest-yield first-line investigation.",
                "refs": ["REF-TESTING-001"]
            },
            {
                "point": "Advanced investigations such as bone marrow trephine or specialised molecular testing are second-line steps.",
                "refs": ["REF-TESTING-002"]
            },
            {
                "point": "A careful history of blood loss, diet, alcohol, and medications narrows the diagnostic path without financial cost.",
                "refs": ["REF-TESTING-002"]
            }
        ],
        "worked_example": {
            "vignette": "A 34-year-old attends clinic with mild microcytic anaemia. The novice resident attempts to place electronic requests for bone marrow biopsy, abdominal CT, haemoglobin electrophoresis, full autoantibody screen, and heavy metal testing simultaneously. The supervising consultant reviews the requisition.",
            "steps": [
                "Step 1: Recognize that the clinical scenario is an uncomplicated, stable microcytic anaemia in a young adult.",
                "Step 2: Cancel unnecessary invasive and high-cost requests (bone marrow biopsy, CT scan, heavy metal screen).",
                "Step 3: Order high-yield first-line tests: serum ferritin and coeliac serology, alongside a dietary and menstrual history.",
                "Step 4: Reserve secondary tests (electrophoresis or endoscopic referrals) until ferritin and initial response are known."
            ]
        },
        "common_pitfalls": [
            "Ordering whole 'anaemia workup panels' that include low-yield or duplicate tests before checking basic cell indices.",
            "Requesting invasive bone marrow procedures before completing routine, non-invasive nutritional evaluations.",
            "Failing to take an accurate dietary, medication, and family history before ordering expensive genetic tests."
        ],
        "clinical_pearl": "Order tests sequentially based on pre-test probability; let the answer to the first question frame your second.",
        "quick_check": [
            {
                "id": "Q1",
                "prompt": "An otherwise well 22-year-old runner presents with mild microcytic anaemia. Which approach best exemplifies high-value, resource-conscious care?",
                "options": [
                    {"id": "A", "text": "Schedule urgent whole-body PET-CT scanning to rule out occult sarcoma."},
                    {"id": "B", "text": "Order routine marrow aspiration and immediate genetic sequencing of all globin genes."},
                    {"id": "C", "text": "Check serum iron alone every morning for seven consecutive days."},
                    {"id": "D", "text": "Obtain serum ferritin and a thorough dietary, exercise, and menstrual history before ordering advanced investigations."}
                ],
                "correct": "D",
                "rationale": "Option D represents rational diagnostic stewardship: identifying common nutritional or physiological iron depletion non-invasively first. Options A and B represent excessive, invasive over-investigation.",
                "reference_id": "REF-TESTING-001"
            },
            {
                "id": "Q2",
                "prompt": "What is a major clinical drawback of ordering indiscriminate multi-test panels for mild, uncomplicated anaemia?",
                "options": [
                    {"id": "A", "text": "Borderline false-positive results generate diagnostic confusion, patient anxiety, and unnecessary follow-up procedures."},
                    {"id": "B", "text": "Large laboratory panels actively suppress reticulocyte production in vivo."},
                    {"id": "C", "text": "Blood samples in multi-test requests always suffer severe in vitro haemolysis."},
                    {"id": "D", "text": "Automated analysers refuse to run full blood counts if additional tests are requested."}
                ],
                "correct": "A",
                "rationale": "Option A correctly describes the well-documented cognitive and financial harm of over-investigation: incidental false positives trigger cascades of invasive evaluations. Options B, C, and D are unfounded.",
                "reference_id": "REF-TESTING-002"
            },
            {
                "id": "Q3",
                "prompt": "In what clinical situation is a bone marrow biopsy considered a justified early step in the investigation of anaemia?",
                "options": [
                    {"id": "A", "text": "Mild microcytic anaemia responding well to iron supplementation."},
                    {"id": "B", "text": "Unexplained pancytopenia or presence of blast cells on the peripheral blood film."},
                    {"id": "C", "text": "A female student with heavy menses and low ferritin."},
                    {"id": "D", "text": "A patient with macrocytosis caused by known chronic alcohol intake and elevated GGT."}
                ],
                "correct": "B",
                "rationale": "Option B is correct: unexplained multilineage cytopenias or circulating immature blast cells indicate potential primary marrow failure or malignancy, justifying early marrow biopsy. Options A, C, and D are managed non-invasively.",
                "reference_id": "REF-TESTING-001"
            }
        ],
        "reference_ids": ["REF-TESTING-001", "REF-TESTING-002"],
        "further_reading": [
            {
                "title": "Choosing Wisely UK: Recommendations on Haematology Investigations",
                "url": "https://www.choosingwisely.co.uk/recommendations/"
            },
            {
                "title": "NICE CKS: Anaemia - iron deficiency",
                "url": "https://cks.nice.org.uk/topics/anaemia-iron-deficiency/"
            }
        ]
    },
    {
        "id": "LESSON-07",
        "title": "Diagnostic Reasoning and Cognitive Bias in Haematology",
        "objective_id": "LO-COGNITIVE-BIAS-REDUCTION",
        "status": "draft",
        "reviewed_by": None,
        "reviewed_at": None,
        "review_notes": [
            "TODO_REVIEWER: Verify suitability of cognitive forcing examples for undergraduate medical curriculum.",
            "TODO_REVIEWER: Review alignment with local clinical reasoning objective frameworks."
        ],
        "estimated_minutes": 8,
        "difficulty": 2,
        "targets_misconceptions": ["MC-OVERCONFIDENT", "MC-PREMATURE-CLOSURE"],
        "prerequisites": ["LESSON-01"],
        "learning_outcomes": [
            "Identify cognitive biases including anchoring, premature closure, and confirmation bias in diagnostic workups.",
            "Calibrate subjective diagnostic confidence against objective laboratory and clinical evidence.",
            "Apply cognitive forcing strategies to re-evaluate diagnostic assumptions before completing a case."
        ],
        "key_points": [
            {
                "point": "Diagnostic errors are frequently driven by cognitive heuristics rather than gaps in knowledge.",
                "refs": ["REF-BIAS-001"]
            },
            {
                "point": "Anchoring occurs when an initial finding fixates attention, blinding the clinician to contradictory evidence.",
                "refs": ["REF-BIAS-001"]
            },
            {
                "point": "Premature closure occurs when a clinician stops searching for alternative or dual etiologies too early.",
                "refs": ["REF-BIAS-001"]
            },
            {
                "point": "High reported diagnostic confidence in the setting of weak evidence leads to serious diagnostic failures.",
                "refs": ["REF-BIAS-002"]
            },
            {
                "point": "Cognitive forcing strategies such as diagnostic time-outs improve reasoning calibration.",
                "refs": ["REF-BIAS-002"]
            }
        ],
        "worked_example": {
            "vignette": "A trainee reviews a 70-year-old patient with mild fatigue. The automated chart triage notes 'iron deficiency history'. The trainee quickly enters a diagnosis of iron deficiency with 95% confidence, ignoring the laboratory report showing an MCV of 104 fL and a low platelet count. The supervising doctor initiates a cognitive debiasing walk-through.",
            "steps": [
                "Step 1: Identify anchoring on the chart triage note rather than current laboratory data.",
                "Step 2: Recognize premature closure: stopping at the first diagnosis without reviewing discordant indices.",
                "Step 3: Point out the objective evidence: macrocytosis and thrombocytopenia contradict simple iron deficiency.",
                "Step 4: Re-calibrate diagnostic confidence to reflect genuine diagnostic uncertainty.",
                "Step 5: Formulate a revised differential including myelodysplastic syndrome or combined pathology."
            ]
        },
        "common_pitfalls": [
            "Expressing 100% confidence in a diagnostic impression before laboratory confirmation is available.",
            "Dismissing laboratory findings that contradict your favourite leading hypothesis as 'laboratory error'.",
            "Failing to ask 'What else could this be?' when evaluating complex or non-responding patients."
        ],
        "clinical_pearl": "Match your diagnostic confidence to the weight of your evidence, not the speed of your hunch.",
        "quick_check": [
            {
                "id": "Q1",
                "prompt": "A clinician fixates on an initial triage note of 'probable dietary anaemia' and ignores a laboratory result showing thrombocytopenia and macrocytosis. What cognitive bias is primarily operating here?",
                "options": [
                    {"id": "A", "text": "Base-rate neglect."},
                    {"id": "B", "text": "Availability cascade."},
                    {"id": "C", "text": "Anchoring bias and premature closure."},
                    {"id": "D", "text": "Gambler's fallacy."}
                ],
                "correct": "C",
                "rationale": "Option C correctly describes anchoring on an early impression and prematurely closing the diagnostic search while ignoring discordant clinical findings. Options A, B, and D describe unrelated cognitive phenomena.",
                "reference_id": "REF-BIAS-001"
            },
            {
                "id": "Q2",
                "prompt": "What is the primary danger of poor diagnostic calibration (reporting high diagnostic confidence despite weak evidence) in clinical practice?",
                "options": [
                    {"id": "A", "text": "It leads to automated laboratory analyser shutdown."},
                    {"id": "B", "text": "It improves diagnostic speed with zero risk to patient safety."},
                    {"id": "C", "text": "It reduces the likelihood of malpractice litigation by projecting certainty."},
                    {"id": "D", "text": "It discourages seeking senior consultation, prevents re-evaluation of contradictory data, and delays correct diagnosis."}
                ],
                "correct": "D",
                "rationale": "Option D highlights how overconfidence blinds clinicians to alternative possibilities, stops critical reflection, and prevents timely senior escalation. Option B is demonstrably false.",
                "reference_id": "REF-BIAS-002"
            },
            {
                "id": "Q3",
                "prompt": "Which cognitive forcing strategy can a trainee apply during a complex haematology workup to mitigate premature closure?",
                "options": [
                    {"id": "A", "text": "Deliberately ask: 'What finding does NOT fit my leading diagnosis, and what must I not miss?' before finalising."},
                    {"id": "B", "text": "Always adopt the most rare and exotic diagnosis to ensure all conditions are considered."},
                    {"id": "C", "text": "Accept the first differential diagnosis generated by an electronic search engine without verification."},
                    {"id": "D", "text": "Never formulate any diagnostic hypothesis until all possible tests have returned."}
                ],
                "correct": "A",
                "rationale": "Option A is a recognized cognitive forcing technique that triggers metacognition and reveals contradictory evidence. Option B represents zebra-hunting, while Option C delegates clinical judgment unsafely.",
                "reference_id": "REF-BIAS-001"
            }
        ],
        "reference_ids": ["REF-BIAS-001", "REF-BIAS-002"],
        "further_reading": [
            {
                "title": "NCBI StatPearls: Cognitive Bias in Clinical Medicine",
                "url": "https://www.ncbi.nlm.nih.gov/books/NBK557551/"
            },
            {
                "title": "Royal College of Physicians: Improving diagnostic reasoning in clinical practice",
                "url": "https://www.rcplondon.ac.uk/projects/outputs/improving-diagnostic-reasoning"
            }
        ]
    },
    {
        "id": "LESSON-08",
        "title": "Must-Not-Miss Thinking and Finding the Cause in Anaemia",
        "objective_id": "LO-RED-FLAGS-ESCALATION",
        "status": "draft",
        "reviewed_by": None,
        "reviewed_at": None,
        "review_notes": [
            "TODO_REVIEWER: Verify age threshold (e.g. age >= 60 vs age >= 50) for fast-track colorectal referral in unexplained iron deficiency per local health service guidelines.",
            "TODO_REVIEWER: Confirm senior escalation trigger criteria for acute inpatient versus outpatient pathway."
        ],
        "estimated_minutes": 10,
        "difficulty": 3,
        "targets_misconceptions": ["MC-MISSED-DANGEROUS-ALTERNATIVE"],
        "prerequisites": ["LESSON-03", "LESSON-04"],
        "learning_outcomes": [
            "Investigate the underlying pathophysiological cause of confirmed iron deficiency rather than halting at the laboratory label.",
            "Identify red-flag clinical features that require urgent referral or senior escalation.",
            "Formulate structured escalation communications for senior medical staff when sinister etiologies are suspected."
        ],
        "key_points": [
            {
                "point": "Iron deficiency is a clinical sign of underlying pathology, never a complete standalone diagnosis.",
                "refs": ["REF-REDALERT-001"]
            },
            {
                "point": "In men and postmenopausal women, gastrointestinal blood loss is the leading concern until thoroughly evaluated.",
                "refs": ["REF-REDALERT-001"]
            },
            {
                "point": "Red flags such as unexplained weight loss, altered bowel habits, or dysphagia mandate urgent referral pathways.",
                "refs": ["REF-REDALERT-001"]
            },
            {
                "point": "Unexplained multilineage cytopenias or haemodynamic instability require immediate senior escalation.",
                "refs": ["REF-REDALERT-002"]
            },
            {
                "point": "Structured communication tools such as SBAR ensure clear, actionable information transfer to seniors.",
                "refs": ["REF-REDALERT-002"]
            }
        ],
        "worked_example": {
            "vignette": "A 66-year-old male presents with newly confirmed iron deficiency anaemia. The trainee plans to advise iron supplementation and discharge the patient to routine community follow-up. The attending physician halts the discharge to explore the underlying cause of iron loss.",
            "steps": [
                "Step 1: Recognize that dietary insufficiency is exceptionally rare in an adult male with iron deficiency.",
                "Step 2: Inquire about red-flag symptoms: the patient notes mild weight loss and loose bowel movements over the past two months.",
                "Step 3: Identify the must-not-miss possibility: occult gastrointestinal neoplasia.",
                "Step 4: Escalate to the senior gastroenterology team using a structured SBAR handoff.",
                "Step 5: Arrange urgent fast-track bidirectional endoscopy per national cancer guidelines."
            ]
        },
        "common_pitfalls": [
            "Treating iron deficiency with iron supplementation without investigating why iron was lost in the first place.",
            "Assuming iron deficiency in an adult male is due to poor dietary intake alone without gastrointestinal evaluation.",
            "Failing to escalate when a patient displays red flags such as unintentional weight loss or rectal bleeding."
        ],
        "clinical_pearl": "Never close the book on iron deficiency until you have discovered the page where blood is leaving the body.",
        "quick_check": [
            {
                "id": "Q1",
                "prompt": "A 62-year-old male is confirmed to have iron deficiency anaemia. What is the fundamental clinical principle governing his further evaluation?",
                "options": [
                    {"id": "A", "text": "Dietary modification is all that is required because men naturally consume insufficient iron."},
                    {"id": "B", "text": "Iron deficiency is a symptom, not a diagnosis; gastrointestinal blood loss must be investigated unless proven otherwise."},
                    {"id": "C", "text": "No further evaluation is needed once iron supplementation is started."},
                    {"id": "D", "text": "Haemoglobin electrophoresis is the only required investigation for older males."}
                ],
                "correct": "B",
                "rationale": "Option B states a core clinical safety axiom: adult males do not develop iron deficiency without an underlying cause, predominantly gastrointestinal bleeding. Option A ignores serious occult pathology.",
                "reference_id": "REF-REDALERT-001"
            },
            {
                "id": "Q2",
                "prompt": "Which combination of clinical features represents a red-flag scenario requiring urgent fast-track referral in a patient with anaemia?",
                "options": [
                    {"id": "A", "text": "Mild fatigue after running a marathon with normal bowel habit."},
                    {"id": "B", "text": "Lifelong mild microcytosis in an asymptomatic young adult with family history of thalassaemia."},
                    {"id": "C", "text": "New iron deficiency in a 65-year-old accompanied by unexplained weight loss and altered bowel habits."},
                    {"id": "D", "text": "A slightly low ferritin in a 19-year-old female with documented heavy menstrual bleeding."}
                ],
                "correct": "C",
                "rationale": "Option C presents classic red flags for lower gastrointestinal malignancy, requiring urgent fast-track endoscopic referral. Options A, B, and D do not represent urgent sinister alarms.",
                "reference_id": "REF-REDALERT-001"
            },
            {
                "id": "Q3",
                "prompt": "When communicating an urgent haematology escalation to a senior consultant, which element best completes the 'Recommendation' portion of an SBAR handoff?",
                "options": [
                    {"id": "A", "text": "Stating that you will wait three weeks to see if the blood count spontaneously normalises."},
                    {"id": "B", "text": "Reading the entire laboratory biochemistry printout from top to bottom."},
                    {"id": "C", "text": "Asking the senior to review the patient in clinic next month for routine follow-up."},
                    {"id": "D", "text": "Requesting immediate senior bedside review and agreement on an urgent endoscopic referral."}
                ],
                "correct": "D",
                "rationale": "Option D provides an explicit, actionable, time-critical request characteristic of high-quality SBAR communication. Options A and C fail to communicate urgency, and Option B clutters handoff.",
                "reference_id": "REF-REDALERT-002"
            }
        ],
        "reference_ids": ["REF-REDALERT-001", "REF-REDALERT-002"],
        "further_reading": [
            {
                "title": "British Society of Gastroenterology: Guidelines for the management of iron deficiency anaemia in adults",
                "url": "https://www.bsg.org.uk/clinical-resource/guidelines-for-the-management-of-iron-deficiency-anaemia/"
            },
            {
                "title": "General Medical Council: Good medical practice and raising patient safety concerns",
                "url": "https://www.gmc-uk.org/ethical-guidance/ethical-guidance-for-doctors/good-medical-practice"
            }
        ]
    }
]

def make_telugu_stub(lesson):
    stub = {
        "id": lesson["id"],
        "title": "TODO_TRANSLATE",
        "objective_id": lesson["objective_id"],
        "status": "draft",
        "reviewed_by": None,
        "reviewed_at": None,
        "reviewed_by_te": None,
        "review_notes": ["TODO_TRANSLATE"],
        "estimated_minutes": lesson["estimated_minutes"],
        "difficulty": lesson["difficulty"],
        "targets_misconceptions": lesson["targets_misconceptions"],
        "prerequisites": lesson["prerequisites"],
        "learning_outcomes": ["TODO_TRANSLATE" for _ in lesson["learning_outcomes"]],
        "key_points": [
            {"point": "TODO_TRANSLATE", "refs": kp["refs"]}
            for kp in lesson["key_points"]
        ],
        "worked_example": {
            "vignette": "TODO_TRANSLATE",
            "steps": ["TODO_TRANSLATE" for _ in lesson["worked_example"]["steps"]]
        },
        "common_pitfalls": ["TODO_TRANSLATE" for _ in lesson["common_pitfalls"]],
        "clinical_pearl": "TODO_TRANSLATE",
        "quick_check": [
            {
                "id": q["id"],
                "prompt": "TODO_TRANSLATE",
                "options": [
                    {"id": opt["id"], "text": "TODO_TRANSLATE"}
                    for opt in q["options"]
                ],
                "correct": q["correct"],
                "rationale": "TODO_TRANSLATE",
                "reference_id": q["reference_id"]
            }
            for q in lesson["quick_check"]
        ],
        "reference_ids": lesson["reference_ids"],
        "further_reading": [
            {"title": "TODO_TRANSLATE", "url": fr["url"]}
            for fr in lesson["further_reading"]
        ]
    }
    return stub

def main():
    print("Generating content files...")
    
    # Check banned words in references and lessons
    banned_pattern = re.compile(r'\b(dose|doses|dosage|mg|prescribe|prescribes|prescribed|prescriber|prescription)\b', re.IGNORECASE)
    
    # 1. References
    ref_dirs = [
        BACKEND_CONTENT / "references",
        API_CONTENT / "references"
    ]
    for d in ref_dirs:
        d.mkdir(parents=True, exist_ok=True)
        
    for ref in REFERENCES:
        frontmatter = {
            "id": ref["id"],
            "title": ref["title"],
            "source_title": ref["source_title"],
            "source_url": ref["source_url"],
            "retrieved_at": ref["retrieved_at"],
            "licence_note": ref["licence_note"],
            "section": ref["section"],
            "tags": ref["tags"],
            "lang": ref["lang"],
            "reviewed": ref["reviewed"],
            "key_facts": ref["key_facts"]
        }
        yaml_fm = yaml.dump(frontmatter, sort_keys=False, allow_unicode=True)
        content = f"---\n{yaml_fm}---\n\n{ref['body'].strip()}\n"
        
        # Check banned words
        matches = banned_pattern.findall(content)
        if matches:
            raise ValueError(f"Banned word found in {ref['id']}: {matches}")
            
        for d in ref_dirs:
            ref_path = d / f"{ref['id']}.md"
            with open(ref_path, "w", encoding="utf-8") as f:
                f.write(content)
        print(f"Created reference: {ref['id']}")
        
    # 2. Lessons
    lesson_dirs = [
        BACKEND_CONTENT / "lessons",
        API_CONTENT / "lessons"
    ]
    for d in lesson_dirs:
        d.mkdir(parents=True, exist_ok=True)
        
    te_dirs = [
        BACKEND_CONTENT / "translations" / "te",
        API_CONTENT / "translations" / "te"
    ]
    for d in te_dirs:
        d.mkdir(parents=True, exist_ok=True)
        
    answer_counts = {"A": 0, "B": 0, "C": 0, "D": 0}
    
    for lesson in LESSONS:
        yaml_content = yaml.dump(lesson, sort_keys=False, allow_unicode=True)
        
        # Check banned words
        matches = banned_pattern.findall(yaml_content)
        if matches:
            raise ValueError(f"Banned word found in {lesson['id']}: {matches}")
            
        # Count answers
        for q in lesson["quick_check"]:
            answer_counts[q["correct"]] += 1
            
        for d in lesson_dirs:
            l_path = d / f"{lesson['id']}.yaml"
            with open(l_path, "w", encoding="utf-8") as f:
                f.write(yaml_content)
                
        # Telugu stub
        te_stub = make_telugu_stub(lesson)
        te_yaml = yaml.dump(te_stub, sort_keys=False, allow_unicode=True)
        for d in te_dirs:
            te_path = d / f"{lesson['id']}.yaml"
            with open(te_path, "w", encoding="utf-8") as f:
                f.write(te_yaml)
                
        print(f"Created lesson & Telugu stub: {lesson['id']}")
        
    print("\nAnswer distribution across 24 questions:")
    for opt, count in sorted(answer_counts.items()):
        pct = (count / 24.0) * 100
        print(f"  {opt}: {count} ({pct:.1f}%)")
        assert pct <= 40.0, f"Option {opt} exceeds 40% ({pct:.1f}%)"
    print("Content generation completed successfully!")

if __name__ == "__main__":
    main()
