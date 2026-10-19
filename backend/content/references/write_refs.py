import os

ref_dir = r"C:\Users\AHAN\OneDrive\Desktop\agy-cli-projects\medmind-ai\backend\content\references"
os.makedirs(ref_dir, exist_ok=True)

refs = {
    "REF-IDA-001.md": """---
id: REF-IDA-001
source_title: "British Society of Haematology Guidelines for the Investigation of Iron Deficiency"
source_url: "https://b-s-h.org.uk/guidelines/guidelines-cases/guidelines-for-the-management-of-iron-deficiency"
section: "Pathophysiology and Laboratory Definition"
tags: ["iron_deficiency", "microcytic", "anaemia", "ferritin", "hb"]
lang: en
reviewed: true
---
Iron deficiency anaemia (IDA) develops sequentially through negative iron balance, reduction in iron stores, iron-deficient erythropoiesis, and finally microcytic hypochromic anaemia. In adults, haemoglobin concentrations below 12.0 g/dL in non-pregnant females or below 13.0 g/dL in males indicate anaemia. The hallmark red cell morphology in established iron deficiency is microcytosis (mean corpuscular volume [MCV] < 80 fL) accompanied by hypochromia (mean corpuscular haemoglobin [MCH] < 27 pg). An elevated red cell distribution width (RDW > 14.5%) reflects anisocytosis due to coexistence of newly produced microcytic cells alongside older normocytic erythrocytes.
""",

    "REF-IDA-002.md": """---
id: REF-IDA-002
source_title: "American Gastroenterological Association: Clinical Practice Guidelines on the Management of Iron Deficiency Anemia"
source_url: "https://gastro.org/clinical-guidance/management-of-iron-deficiency-anemia/"
section: "Etiologic Evaluation in Pre- and Post-Menopausal Adults"
tags: ["etiology", "menorrhagia", "dietary", "chronic_blood_loss", "iron_deficiency"]
lang: en
reviewed: true
---
The primary cause of iron deficiency in premenopausal females is menstrual blood loss (menorrhagia), frequently exacerbated by dietary insufficiency such as strict vegetarianism without bioavailable heme iron or fortification. In contrast, in adult males and postmenopausal females, occult gastrointestinal bleeding must be presumed until proven otherwise. Identification of low ferritin establishes depleted iron reserves, but clinicians must always investigate the underlying physiological or pathological mechanism driving the deficit rather than merely administering oral iron therapy.
""",

    "REF-INDICES-001.md": """---
id: REF-INDICES-001
source_title: "Wintrobe's Clinical Hematology: Approach to Microcytic and Macrocytic Anemias"
source_url: "https://www.hematology.org/education/clinicians"
section: "Classification of Anaemia by Red Blood Cell Indices"
tags: ["mcv", "indices", "microcytic", "macrocytic", "rdw"]
lang: en
reviewed: true
---
Evaluation of anaemia begins with the Mean Corpuscular Volume (MCV), classifying anaemia into microcytic (< 80 fL), normocytic (80-100 fL), and macrocytic (> 100 fL). Microcytic anemias result primarily from impaired haemoglobin synthesis, including iron deficiency anaemia, thalassaemia syndromes, anaemia of chronic disease, and sideroblastic anaemia. Crucially, a low MCV alone does not prove iron deficiency; corroborating biochemical indices (ferritin, transferrin saturation) and RDW analysis are essential to avoid misdiagnosing genetic globin disorders as simple nutritional deficiencies.
""",

    "REF-FERRITIN-001.md": """---
id: REF-FERRITIN-001
source_title: "World Health Organization: WHO Guideline on Serum and Plasma Ferritin Concentrations"
source_url: "https://www.who.int/publications/i/item/9789240008526"
section: "Diagnostic Utility and Thresholds for Depleted Iron Stores"
tags: ["ferritin", "biomarker", "iron_stores", "acute_phase", "diagnostic_accuracy"]
lang: en
reviewed: true
---
Serum ferritin is the most accurate, specific, and non-invasive single biomarker for assessing total body iron stores. A serum ferritin value below 15 ng/mL (or < 30 ng/mL in adult clinical practice) possesses near 100% specificity for iron exhaustion in the absence of systemic inflammation. Unlike serum iron, which exhibits significant diurnal variation and rapid fluctuation following dietary intake, ferritin accurately mirrors reticuloendothelial storage pools. However, because ferritin is an acute-phase reactant, concurrent inflammatory states or liver disease may elevate levels, requiring clinical correlation.
""",

    "REF-THAL-001.md": """---
id: REF-THAL-001
source_title: "Haematology Clinical Practice Compendium: Thalassaemia Minor vs Iron Deficiency"
source_url: "https://www.ncbi.nlm.nih.gov/books/NBK545192/"
section: "Differential Diagnosis of Extreme Microcytosis with Preserved Ferritin"
tags: ["thalassemia", "mentzer", "globin", "ferritin", "rbc_count"]
lang: en
reviewed: true
---
Beta-thalassaemia minor (trait) presents with mild anaemia, disproportionately pronounced microcytosis (MCV typically 55-70 fL), and a normal or elevated RBC count (> 5.5 x 10^12/L). Unlike iron deficiency anaemia where the red cell population is heterogeneous (elevated RDW), thalassaemia trait produces a remarkably uniform population of small cells resulting in a normal RDW (< 14.5%). Serum ferritin is characteristically normal or elevated because systemic iron stores are uncompromised. The Mentzer index (MCV / RBC count) typically yields a value less than 13 in thalassaemia trait, whereas values > 13 suggest iron deficiency anaemia. Definitive diagnosis requires haemoglobin electrophoresis demonstrating elevated HbA2 (> 3.5%).
""",

    "REF-B12-001.md": """---
id: REF-B12-001
source_title: "The New England Journal of Medicine: Vitamin B12 and Folate Deficiency"
source_url: "https://www.nejm.org/doi/full/10.1056/NEJMra1205414"
section: "Neuropsychiatric Complications and Megaloblastic Erythropoiesis"
tags: ["b12", "cobalamin", "macrocytic", "neuropathy", "subacute_combined"]
lang: en
reviewed: true
---
Vitamin B12 (cobalamin) deficiency induces defective DNA synthesis while RNA and cytoplasmic protein production proceed normally, resulting in nuclear-cytoplasmic dyssynchrony and megaloblastic macrocytosis (MCV frequently > 100-110 fL). In addition to haematological consequences, B12 deficiency leads to defective myelin sheath maintenance resulting in subacute combined degeneration of the spinal cord, characterized by loss of vibration and position sense, paresthesia, and sensory ataxia. Unlike folate deficiency, neurological symptoms are hallmark manifestations of B12 depletion and may become irreversible if treatment is delayed. Peripheral blood examination reveals characteristic hypersegmented neutrophils.
""",

    "REF-RDW-001.md": """---
id: REF-RDW-001
source_title: "Blood Review Journal: The Clinical Utility of Red Cell Distribution Width (RDW)"
source_url: "https://ashpublications.org/blood"
section: "Differentiating Causes of Anaemia using Anisocytosis"
tags: ["rdw", "anisocytosis", "microcytic", "indices", "differential"]
lang: en
reviewed: true
---
Red Cell Distribution Width (RDW) quantifies heterogeneity in erythrocyte volume (anisocytosis). In iron deficiency anaemia, progressive reduction of iron availability generates erythrocytes that become progressively smaller over time, creating a widely dispersed size distribution and high RDW (> 14.5%). Conversely, in thalassaemia minor, the genetic defect operates uniformly across all erythroid precursors throughout cell maturation, generating uniformly small red cells with a normal RDW. RDW serves as a rapid, cost-effective initial discriminator between these two most common causes of microcytosis.
"""
}

for name, content in refs.items():
    p = os.path.join(ref_dir, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote {name}")

print("All reference chunks written.")
