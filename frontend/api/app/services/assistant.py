import logging
import json
import re
from typing import Dict, Any, List, Optional
from app.config import settings
from app.schemas.assistant import (
    AssistantChatRequest, AssistantChatResponse, AssistantCitation, RecommendedLessonItem,
    StarterPromptGroup, StarterPromptsResponse
)

logger = logging.getLogger("medmind.assistant")

ASSISTANT_SYSTEM_PROMPT = """You are MedMind AI Assistant, a specialized clinical reasoning and medical education tutor for students and healthcare trainees.
Your purpose is to coach learners on systematic haematology interpretation, diagnostic reasoning, laboratory evaluation, and evidence-based medicine.

CRITICAL GUARDRAILS:
1. EDUCATIONAL SIMULATION ONLY: Never provide clinical instructions, drug dosages, prescription advice, or direct management plans for real patients.
2. Emphasize that reference ranges vary between laboratories and individual institutional guidelines must always take precedence.
3. Reference grounding: Wherever possible, cite relevant reference IDs (e.g. REF-FBC-001, REF-IDA-001, REF-FERRITIN-001, REF-THAL-001, REF-MACRO-001, REF-REDALERT-001).
4. Socratic & Structured: Break down complex diagnostic dilemmas into clear, stepwise reasoning: morphology (MCV/RDW) -> iron/cofactor stores -> underlying pathophysiology -> must-not-miss red flags.
5. Case & Lesson alignment: Suggest relevant practice lessons (LESSON-01 through LESSON-08) to reinforce core competencies.
"""

KNOWLEDGE_BASE = [
    {
        "keywords": ["fbc", "full blood count", "cbc", "complete blood count", "systematic", "indices", "wbc", "platelet", "step"],
        "reply": (
            "### Systematic Full Blood Count (FBC) Interpretation\n\n"
            "When approaching an abnormal haemogram, follow a structured 5-step heuristic to avoid diagnostic shortcuts:\n\n"
            "1. **Confirm Anaemia**: Assess Haemoglobin (Hb) against local demographic reference ranges.\n"
            "2. **Morphological Classification via MCV**: Mean Corpuscular Volume classifies anaemia into microcytic (<80 fL), normocytic (80-100 fL), or macrocytic (>100 fL).\n"
            "3. **Evaluate Heterogeneity via RDW**: Red Cell Distribution Width reflects anisocytosis. An elevated RDW (>14.5%) indicates variable red cell size characteristic of nutritional deficiencies (iron, B12, folate).\n"
            "4. **Cross-Check Other Lineages**: Always review the White Blood Cell (WBC) and Platelet counts. Isolated anaemia suggests isolated erythroid pathology, whereas bi- or pancytopenia raises concern for bone marrow failure, megaloblastosis, or hypersplenism.\n"
            "5. **Examine the Peripheral Smear**: Smear morphology provides essential confirmation (e.g. pencil cells in iron deficiency, target cells in thalassaemia, hypersegmented neutrophils in megaloblastic states).\n\n"
            "> *Typical adult reference ranges vary by laboratory. Reference values must always be interpreted in the clinical context.*"
        ),
        "citations": [
            {"ref_id": "REF-FBC-001", "source_title": "Systematic Full Blood Count Interpretation", "relevance": "Outlines the 5-step heuristic for multi-lineage haematological evaluation."},
            {"ref_id": "REF-INDICES-001", "source_title": "Red Cell Indices in Diagnostic Haematology", "relevance": "Defines MCV morphological classification and RDW anisocytosis."}
        ],
        "suggested_questions": [
            "How does RDW help differentiate iron deficiency from thalassaemia trait?",
            "What should I do if both anaemia and thrombocytopenia are present?",
            "Why is checking the peripheral blood film so important?"
        ],
        "recommended_lessons": [
            {"id": "LESSON-01", "title": "Reading a Full Blood Count Systematically"},
            {"id": "LESSON-02", "title": "Classifying Anaemia by Cell Size"}
        ]
    },
    {
        "keywords": ["thalassaemia", "thalassemia", "mentzer", "microcytic differential", "target cell", "erythrocytosis"],
        "reply": (
            "### Differentiating Iron Deficiency from Beta-Thalassaemia Trait\n\n"
            "In patients with marked microcytosis (MCV < 80 fL), distinguishing iron deficiency from thalassaemia trait is a classic clinical problem:\n\n"
            "- **Beta-Thalassaemia Trait / Minor**:\n"
            "  - **MCV**: Disproportionately low relative to the mild degree of anaemia (often 58-68 fL with Hb 10-12 g/dL).\n"
            "  - **RBC Count**: Elevated (compensatory erythrocytosis, often > 5.5 x 10^12/L) to maintain adequate oxygen-carrying capacity.\n"
            "  - **RDW**: Typically normal (11.5-14.0%), reflecting uniform microcytes.\n"
            "  - **Ferritin**: Normal or elevated (body iron reserves are preserved).\n"
            "  - **Mentzer Index**: Heuristic ratio of `MCV / RBC`. A Mentzer index **< 13** strongly suggests thalassaemia trait.\n"
            "  - **Confirmation**: Haemoglobin electrophoresis (elevated HbA2 > 3.5%).\n\n"
            "- **Iron Deficiency Anaemia (IDA)**:\n"
            "  - **RBC Count**: Low or normal.\n"
            "  - **RDW**: Elevated (>14.5%, marked anisocytosis as new iron-deficient cells enter circulation).\n"
            "  - **Ferritin**: Depleted (< 15-30 ng/mL).\n"
            "  - **Mentzer Index**: Characteristically **> 13**.\n\n"
            "> *Caution: Never prescribe empiric iron therapy for microcytosis without confirming iron deficiency with a baseline ferritin. Iron in thalassaemia trait risks iatrogenic haemosiderosis.*"
        ),
        "citations": [
            {"ref_id": "REF-THAL-001", "source_title": "Haemoglobinopathies and Thalassaemia Trait", "relevance": "Delineates indices and electrophoresis criteria for thalassaemia minor."},
            {"ref_id": "REF-MICRODIFF-001", "source_title": "Microcytic Anaemia Differential Algorithms", "relevance": "Compares Mentzer index, RDW, and ferritin parameters."}
        ],
        "suggested_questions": [
            "Can a patient have both beta-thalassaemia trait and iron deficiency concurrently?",
            "What does a peripheral blood smear look like in thalassaemia minor?",
            "How is Mentzer index calculated and what is its sensitivity?"
        ],
        "recommended_lessons": [
            {"id": "LESSON-04", "title": "The Microcytic Differential: Iron Deficiency, Thalassaemia, and Chronic Disease"},
            {"id": "LESSON-03", "title": "Iron Studies and Ferritin Interpretation"}
        ]
    },
    {
        "keywords": ["ferritin", "iron studies", "inflammation", "acute phase", "hepcidin", "tibc", "transferrin"],
        "reply": (
            "### Ferritin and Iron Studies: Navigating Inflammatory Confounders\n\n"
            "Serum ferritin is the most specific non-invasive biomarker of reticuloendothelial storage reserves, but inflammation requires cautious interpretation:\n\n"
            "1. **Uncomplicated State (No Inflammation)**:\n"
            "   - Ferritin < 15-30 ng/mL is virtually 100% specific for depleted bone marrow iron stores.\n"
            "   - Transferrin Saturation (TSAT) is typically < 16-20%.\n\n"
            "2. **Inflammatory Confounding (Acute-Phase Response)**:\n"
            "   - Ferritin is an acute-phase reactant synthesized in response to pro-inflammatory cytokines (IL-6, TNF-alpha).\n"
            "   - In patients with autoimmune disease, chronic kidney disease, heart failure, or infection, ferritin can be 'falsely' normal or elevated (e.g. 100-400 ng/mL) despite coexisting cellular iron deficiency.\n"
            "   - In the presence of inflammation, an adjusted ferritin threshold of **< 100 ng/mL** often suggests true concurrent iron deficiency.\n\n"
            "3. **Hepcidin and Anaemia of Chronic Disease (ACD)**:\n"
            "   - Inflammatory IL-6 upregulates hepatic **hepcidin**, which degrades ferroportin and traps iron inside macrophages and hepatocytes.\n"
            "   - Laboratory picture: Low serum iron + Normal/High ferritin + Low Total Iron Binding Capacity (TIBC) + Low TSAT.\n\n"
            "> *Key Clinical Rule: Always check CRP or ESR alongside iron studies when evaluating complex hospitalised or multi-morbid patients.*"
        ),
        "citations": [
            {"ref_id": "REF-FERRITIN-001", "source_title": "Biomarkers of Iron Exhaustion: Serum Ferritin", "relevance": "Establishes baseline ferritin specificity in non-inflammatory states."},
            {"ref_id": "REF-FERRITIN-002", "source_title": "Ferritin as an Acute-Phase Reactant", "relevance": "Covers cytokine upregulation, hepcidin-ferroportin axis, and inflammatory cut-offs."}
        ],
        "suggested_questions": [
            "How do I differentiate Anaemia of Chronic Disease from combined ACD and iron deficiency?",
            "What is Transferrin Saturation and how is it calculated?",
            "Why is random serum iron an unreliable test on its own?"
        ],
        "recommended_lessons": [
            {"id": "LESSON-03", "title": "Iron Studies and Ferritin Interpretation"},
            {"id": "LESSON-06", "title": "Choosing Investigations Wisely in Anaemia Workup"}
        ]
    },
    {
        "keywords": ["macrocytic", "macrocytosis", "b12", "folate", "megaloblastic", "pernicious", "neuropathy", "paresthesia", "alcohol", "thyroid"],
        "reply": (
            "### Macrocytic Anaemia: Megaloblastic vs Non-Megaloblastic Pathways\n\n"
            "When MCV > 100 fL, the first diagnostic fork is determining whether the process is megaloblastic or non-megaloblastic:\n\n"
            "#### 1. Megaloblastic Anaemia (Impaired DNA Synthesis)\n"
            "- **Aetiologies**: Vitamin B12 (Cobalamin) deficiency, Folate deficiency, medications interfering with DNA synthesis (e.g. methotrexate, hydroxyurea).\n"
            "- **Peripheral Smear**: Hypersegmented neutrophils (>= 5 lobes in > 5% of cells, or any neutrophil with >= 6 lobes) and oval macrocytes (macro-ovalocytes).\n"
            "- **Clinical Signs**: Atrophic glossitis, lemon-tinted pallor. B12 deficiency specifically causes **sensory neuropathy**, subacute combined degeneration (dorsal column loss), and cognitive impairment.\n"
            "- **Underlying Cause Identification**: In B12 deficiency, always determine *why* the patient is deficient (e.g. strict veganism, pernicious anaemia with anti-intrinsic factor antibodies, Crohn's disease/ileal resection, gastric bypass).\n\n"
            "#### 2. Non-Megaloblastic Macrocytosis (Preserved DNA Synthesis)\n"
            "- **Aetiologies**: Chronic alcohol overuse, hepatic parenchymal disease, hypothyroidism, myelodysplastic syndrome, brisk reticulocytosis (young RBCs are larger, ~110-120 fL).\n"
            "- **Peripheral Smear**: Round macrocytes, target cells (liver disease), absence of hypersegmented neutrophils.\n\n"
            "> *Caution: Never treat presumed B12 deficiency with folate alone. Folate can partially correct the haematological cytopenia while allowing catastrophic, irreversible neurological degeneration to progress.*"
        ),
        "citations": [
            {"ref_id": "REF-B12-001", "source_title": "Cobalamin and Folate Deficiency in Megaloblastic Anaemia", "relevance": "Outlines megaloblastic haematopoiesis, neuropathy, and anti-IF testing."},
            {"ref_id": "REF-MACRO-001", "source_title": "Macrocytic Anaemia: Megaloblastic and Non-Megaloblastic Pathways", "relevance": "Differentiates marrow DNA defects from lipid membrane and reticulocyte causes."}
        ],
        "suggested_questions": [
            "What causes isolated folate deficiency without B12 deficiency?",
            "Why does alcohol cause macrocytosis even before liver cirrhosis develops?",
            "What is the significance of hypersegmented neutrophils on blood film?"
        ],
        "recommended_lessons": [
            {"id": "LESSON-05", "title": "Macrocytic Anaemia: Megaloblastic and Non-Megaloblastic Pathways"},
            {"id": "LESSON-02", "title": "Classifying Anaemia by Cell Size"}
        ]
    },
    {
        "keywords": ["red flag", "older adult", "endoscopy", "colonoscopy", "blood loss", "malignancy", "must-not-miss", "escalate", "escalation"],
        "reply": (
            "### Must-Not-Miss Thinking: Iron Deficiency in Adults and Older Patients\n\n"
            "In clinical reasoning, diagnosing iron deficiency is only the intermediate step—the paramount clinical question is: **What is causing the iron loss?**\n\n"
            "1. **The Golden Rule of Adult IDA**:\n"
            "   - In adult men of any age and in postmenopausal women, iron deficiency anaemia is **gastrointestinal blood loss until proven otherwise**.\n"
            "   - Dietary insufficiency alone is extraordinarily rare in adults eating an unrestricted diet; dietary causes should only be accepted after occult blood loss has been thoroughly excluded.\n\n"
            "2. **Red-Flag Clinical Features Requiring Urgent Escalation**:\n"
            "   - Age >= 50 (or >= 60 in some national pathways) with newly detected unexplained IDA.\n"
            "   - Unintentional weight loss, anorexia, or early satiety.\n"
            "   - Change in bowel habit (towards persistent looseness or frequency).\n"
            "   - Palpable abdominal or rectal mass, or positive fecal occult blood / FIT.\n\n"
            "3. **Mandatory Action**:\n"
            "   - Urgent referral for bidirectional gastrointestinal endoscopy (colonoscopy and gastroscopy / OGD).\n"
            "   - Starting iron pills and sending the patient away for routine review in 6 months without endoscopic investigation is a severe diagnostic cognitive trap (**premature closure**).\n\n"
            "> *Key Principle: A trainee's duty is not merely to replenish the haemoglobin, but to advocate for identifying the underlying bleeding source.*"
        ),
        "citations": [
            {"ref_id": "REF-REDALERT-001", "source_title": "Must-Not-Miss Red Flags in Unexplained Anaemia", "relevance": "Defines urgency criteria for endoscopy in adult iron deficiency."},
            {"ref_id": "REF-REDALERT-002", "source_title": "Clinical Escalation Protocols for Trainees", "relevance": "Guides effective communication when escalating suspected GI bleeding."}
        ],
        "suggested_questions": [
            "Why is iron deficiency in a 25-year-old female managed differently from a 70-year-old male?",
            "What should I do if a patient with IDA has a negative fecal occult blood test?",
            "What is premature closure and how can I avoid it in clinical practice?"
        ],
        "recommended_lessons": [
            {"id": "LESSON-08", "title": "Must-Not-Miss Thinking and Finding the Cause in Anaemia"},
            {"id": "LESSON-07", "title": "Diagnostic Reasoning and Cognitive Bias in Haematology"}
        ]
    },
    {
        "keywords": ["bias", "cognitive", "anchoring", "premature closure", "confirmation", "reasoning", "heuristics"],
        "reply": (
            "### Cognitive Bias and Diagnostic Traps in Medicine\n\n"
            "Up to 75% of diagnostic errors in medicine stem from cognitive bias and premature closure rather than lack of medical knowledge. Four key traps in haematology include:\n\n"
            "1. **Anchoring Bias**:\n"
            "   - Clinging onto an initial impression or handover note (e.g. 'Patient has fatigue from busy job') despite discordant objective laboratory data (e.g. severe microcytosis or high RDW).\n\n"
            "2. **Premature Closure**:\n"
            "   - Accepting a diagnosis before it has been fully verified (e.g. prescribing iron pills to an older adult with low Hb without checking ferritin or searching for GI blood loss).\n\n"
            "3. **Confirmation Bias**:\n"
            "   - Selectively seeking or emphasizing evidence that supports a favored hypothesis while ignoring conflicting findings (e.g. focusing on borderline low serum iron while ignoring normal ferritin and high RBC in thalassaemia trait).\n\n"
            "4. **Diagnostic Momentum**:\n"
            "   - Uncritically perpetuating a label affixed by a previous clinician without re-evaluating the primary evidence.\n\n"
            "**Mitigation Strategy: The 'Diagnostic Time-Out'**\n"
            "Before signing off a patient's chart, ask:\n"
            "- *'What else could this be?'*\n"
            "- *'Does any finding not fit my current explanation?'*\n"
            "- *'What is the worst-case must-not-miss alternative?'*"
        ),
        "citations": [
            {"ref_id": "REF-BIAS-001", "source_title": "Cognitive Biases in Diagnostic Decision-Making", "relevance": "Classifies anchoring, premature closure, and search satisficing."},
            {"ref_id": "REF-BIAS-002", "source_title": "Debiasing Strategies and Diagnostic Time-Outs", "relevance": "Presents structured debiasing checklists for clinical reasoning."}
        ],
        "suggested_questions": [
            "How does a diagnostic time-out work in emergency or acute ward rounds?",
            "What is the difference between systemic heuristics and cognitive biases?",
            "How can matching confidence to evidence prevent overconfidence error?"
        ],
        "recommended_lessons": [
            {"id": "LESSON-07", "title": "Diagnostic Reasoning and Cognitive Bias in Haematology"},
            {"id": "LESSON-08", "title": "Must-Not-Miss Thinking and Finding the Cause in Anaemia"}
        ]
    }
]

STARTER_PROMPTS = [
    StarterPromptGroup(
        category="Full Blood Count Basics",
        description="Core principles of systematic haemogram interpretation",
        prompts=[
            "How do I systematically read a full blood count step-by-step?",
            "What does an elevated RDW tell me that the MCV cannot?",
            "Why should I always check WBC and platelet counts in an anaemic patient?"
        ]
    ),
    StarterPromptGroup(
        category="Microcytic Differentials",
        description="Differentiating Iron Deficiency from Thalassaemia Trait and Chronic Disease",
        prompts=[
            "How do I distinguish iron deficiency from beta-thalassaemia trait?",
            "What is the Mentzer index and when should I use it as a screening heuristic?",
            "Why is prescribing empiric iron to a thalassaemia patient dangerous?"
        ]
    ),
    StarterPromptGroup(
        category="Ferritin & Inflammation",
        description="Understanding iron storage biomarkers and acute-phase confounders",
        prompts=[
            "Why can serum ferritin be normal or high even when a patient is iron deficient?",
            "How does hepcidin cause Anaemia of Chronic Disease?",
            "What role does Transferrin Saturation play in inflammatory states?"
        ]
    ),
    StarterPromptGroup(
        category="Macrocytosis & Megaloblastosis",
        description="Cobalamin, folate, and non-megaloblastic pathways",
        prompts=[
            "What are the hallmarks of a megaloblastic peripheral blood smear?",
            "Why must I never give folic acid alone in suspected B12 deficiency?",
            "What are the most common non-megaloblastic causes of high MCV?"
        ]
    ),
    StarterPromptGroup(
        category="Red Flags & Clinical Safety",
        description="Must-not-miss pathology, urgent endoscopy, and debiasing",
        prompts=[
            "Why is iron deficiency in an adult male or older adult considered GI bleeding until proven otherwise?",
            "What are the red flag symptoms in unexplained anaemia requiring senior escalation?",
            "What is premature closure and how do I avoid this diagnostic trap?"
        ]
    )
]

def query_fallback_assistant(message: str, context: Optional[Dict[str, Any]] = None) -> AssistantChatResponse:
    query = message.lower()
    
    # Calculate score for each knowledge entry based on keyword hits
    best_match = None
    highest_score = 0
    
    for entry in KNOWLEDGE_BASE:
        score = sum(1 for kw in entry["keywords"] if kw in query)
        if score > highest_score:
            highest_score = score
            best_match = entry

    if best_match and highest_score > 0:
        return AssistantChatResponse(
            reply=best_match["reply"],
            citations=[AssistantCitation(**c) for c in best_match["citations"]],
            suggested_questions=best_match["suggested_questions"],
            recommended_lessons=[RecommendedLessonItem(**l) for l in best_match["recommended_lessons"]],
            model="MedMind Clinical Knowledge Engine (Grounded Fallback)"
        )

    # General supportive default response
    default_reply = (
        "### Clinical Reasoning Guidance\n\n"
        f"Thank you for your question regarding: *\"{message}\"*\n\n"
        "In clinical haematology, our systematic framework begins by classifying anaemia according to the **Mean Corpuscular Volume (MCV)**:\n\n"
        "- **Microcytic (MCV < 80 fL)**: Think of impaired haemoglobin synthesis: Iron Deficiency (low ferritin, high RDW), Thalassaemia Trait (normal ferritin, normal RDW, high RBC count), or Anaemia of Chronic Disease (high ferritin, inflammatory disease).\n"
        "- **Normocytic (MCV 80-100 fL)**: Think of acute blood loss, haemolysis (check reticulocytes and bilirubin), chronic kidney disease, or early mixed nutritional deficiency.\n"
        "- **Macrocytic (MCV > 100 fL)**: Check blood smear for hypersegmented neutrophils. If megaloblastic, evaluate Vitamin B12 and folate; if non-megaloblastic, consider alcohol, liver disease, thyroid status, or medications.\n\n"
        "**Clinical Pearl**: Always correlate numerical values with the patient's age, dietary patterns, bleeding history, and physical examination before arriving at a diagnostic conclusion."
    )
    return AssistantChatResponse(
        reply=default_reply,
        citations=[
            AssistantCitation(
                ref_id="REF-INDICES-001",
                source_title="Red Cell Indices in Diagnostic Haematology",
                relevance="Core morphological framework for haematological evaluation."
            ),
            AssistantCitation(
                ref_id="REF-TESTING-001",
                source_title="Choosing Investigations Wisely in Haematology",
                relevance="Rational test ordering sequence and pre-test probability principles."
            )
        ],
        suggested_questions=[
            "How do I systematically read a full blood count step-by-step?",
            "How do I distinguish iron deficiency from beta-thalassaemia trait?",
            "Why can serum ferritin be normal or high even when a patient is iron deficient?",
            "What are the red flag symptoms in unexplained anaemia?"
        ],
        recommended_lessons=[
            RecommendedLessonItem(id="LESSON-01", title="Reading a Full Blood Count Systematically"),
            RecommendedLessonItem(id="LESSON-02", title="Classifying Anaemia by Cell Size")
        ],
        model="MedMind Clinical Knowledge Engine (Grounded Fallback)"
    )

def ask_assistant(request: AssistantChatRequest) -> AssistantChatResponse:
    # 1. If Anthropic Claude API key is configured and mode is live, call LLM
    if settings.get_tutor_mode() == "live" and settings.ANTHROPIC_API_KEY and settings.LLM_MODEL:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            
            # Format messages
            messages = []
            for msg in (request.history or [])[-6:]:
                messages.append({"role": msg.role, "content": msg.content})
            
            # Add current user message with context
            user_content = request.message
            if request.context:
                user_content = f"[Context: {json.dumps(request.context)}]\n\n{request.message}"
            messages.append({"role": "user", "content": user_content})

            response = client.messages.create(
                model=settings.LLM_MODEL,
                max_tokens=1000,
                system=ASSISTANT_SYSTEM_PROMPT,
                messages=messages,
                temperature=0.2
            )
            raw_text = response.content[0].text if response.content else ""
            
            # Parse citations from text or attach fallback references
            citations = []
            ref_matches = set(re.findall(r'REF-[A-Z0-9-]+', raw_text))
            for r_id in ref_matches:
                citations.append(AssistantCitation(ref_id=r_id, source_title=f"Clinical Evidence Chunk ({r_id})"))
            if not citations:
                citations.append(AssistantCitation(ref_id="REF-FBC-001", source_title="Systematic FBC Interpretation Guidelines"))

            return AssistantChatResponse(
                reply=raw_text,
                citations=citations[:3],
                suggested_questions=[
                    "What follow-up investigation would you recommend next?",
                    "How does this connect to our practice cases?",
                    "What cognitive biases should we beware of here?"
                ],
                recommended_lessons=[
                    RecommendedLessonItem(id="LESSON-01", title="Reading a Full Blood Count Systematically"),
                    RecommendedLessonItem(id="LESSON-07", title="Diagnostic Reasoning and Cognitive Bias in Haematology")
                ],
                model=f"Anthropic Claude ({settings.LLM_MODEL})"
            )
        except Exception as e:
            logger.warning("Anthropic live call failed, falling back gracefully: %s", e)

    # 2. Deterministic Grounded Knowledge Engine
    return query_fallback_assistant(request.message, request.context)

def get_starter_prompts() -> StarterPromptsResponse:
    return StarterPromptsResponse(groups=STARTER_PROMPTS)
