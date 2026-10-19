const BASE_URL = (import.meta as any).env?.VITE_API_URL || '/api';

// Fallback in-memory state for standalone static deployments (e.g. Vercel)
const mockState: Record<string, any> = {
  attempts: {},
};

export async function apiRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem('token');
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> || {}),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (response.ok) {
      return await response.json();
    }
  } catch (e) {
    // Backend offline or unreachable, fall through to client-side fallback
    console.warn(`API call ${endpoint} failed, falling back to local simulation mode.`);
  }

  // Fallback simulator for offline or static hosting on Vercel
  return mockSimulator(endpoint, options) as T;
}

function mockSimulator(endpoint: string, options: RequestInit = {}): any {
  const method = (options.method || 'GET').toUpperCase();
  const body = options.body ? JSON.parse(options.body as string) : {};

  if (endpoint === '/auth/login' || endpoint === '/auth/register') {
    const isTeacher = body.email && body.email.includes('sharma');
    return {
      access_token: 'mock-jwt-token-yukthi-2026',
      token_type: 'bearer',
      user: {
        id: isTeacher ? 'user-teacher-01' : 'user-student-01',
        email: body.email || 'student@medmind.ai',
        display_name: isTeacher ? 'Dr. Aarti Sharma, MD' : 'Alex Mercer (Student)',
        role: isTeacher ? 'teacher' : 'student',
        preferred_lang: 'en',
        cohort_id: 'cohort-med-2026-alpha',
      },
    };
  }

  if (endpoint === '/auth/me') {
    return {
      id: 'user-student-01',
      email: 'student@medmind.ai',
      display_name: 'Alex Mercer (Student)',
      role: 'student',
      preferred_lang: 'en',
      cohort_id: 'cohort-med-2026-alpha',
    };
  }

  if (endpoint === '/cases') {
    return [
      {
        id: 'CASE-FATIGUE-01',
        version: 1,
        learning_objective: 'LO-MICROCYTIC-01',
        case_role: 'initial',
        title: 'Persistent Fatigue in a Young Adult',
        disclaimer: 'Fictional case for education only. Not medical advice.',
      },
      {
        id: 'CASE-FATIGUE-02',
        version: 1,
        learning_objective: 'LO-MICROCYTIC-01',
        case_role: 'reassessment',
        title: 'Microcytic Indices with Preserved Iron Stores',
        disclaimer: 'Fictional case for education only. Not medical advice.',
      },
      {
        id: 'CASE-B12-01',
        version: 1,
        learning_objective: 'LO-MACROCYTIC-01',
        case_role: 'initial',
        title: 'Fatigue with Paresthesia and Macrocytic Indices',
        disclaimer: 'Fictional case for education only. Not medical advice.',
      },
    ];
  }

  if (endpoint === '/attempts' && method === 'POST') {
    const attemptId = 'att-' + Math.random().toString(36).substring(2, 9);
    const caseId = body.case_id || 'CASE-FATIGUE-01';

    const caseData =
      caseId === 'CASE-FATIGUE-02'
        ? {
            id: 'CASE-FATIGUE-02',
            version: 1,
            learning_objective: 'LO-MICROCYTIC-01',
            case_role: 'reassessment',
            title: 'Microcytic Indices with Preserved Iron Stores',
            disclaimer: 'Fictional case for education only. Not medical advice.',
            patient: { name: 'Jordan', age: 34, sex: 'male' },
            history:
              'Presents for a routine checkup with mild lifelong tiredness. Mediterranean ancestry with family history of mild anaemia. Normal diet, no bleeding.',
            labs: [
              { id: 'hb', test: 'Haemoglobin', value: 10.4, unit: 'g/dL', ref: '13.5-17.5', flag: 'low' },
              { id: 'mcv', test: 'Mean Corpuscular Volume (MCV)', value: 63, unit: 'fL', ref: '80-100', flag: 'low' },
              { id: 'rdw', test: 'Red Cell Distribution Width (RDW)', value: 12.6, unit: '%', ref: '11.5-14.5', flag: 'normal' },
              { id: 'ferritin', test: 'Serum Ferritin', value: 145, unit: 'ng/mL', ref: '20-250', flag: 'normal' },
              { id: 'rbc', test: 'Red Blood Cell Count (RBC)', value: 6.2, unit: 'x10^12/L', ref: '4.5-5.9', flag: 'high' },
            ],
            question: 'Which diagnosis best explains the disproportionately low MCV in the setting of normal ferritin and high RBC count?',
            options: [
              { id: 'A', text: 'Beta-thalassaemia trait / minor (Globin synthesis defect with microcytosis, normal ferritin, and normal RDW)' },
              { id: 'B', text: 'Refractory iron-deficiency anaemia requiring intravenous iron' },
              { id: 'C', text: 'Vitamin B12 or folate deficiency' },
              { id: 'D', text: 'Anaemia of chronic renal disease' },
            ],
            branching: {
              start: 'n_review',
              nodes: [
                {
                  id: 'n_review',
                  type: 'review_case',
                  text: 'You are evaluating Jordan\'s indices. Do you want to examine further diagnostic context?',
                  choices: [
                    { id: 'more_info', label: 'Review haemoglobin electrophoresis status', next: 'n_electrophoresis' },
                    { id: 'answer_now', label: 'Make diagnostic determination now', next: 'n_decide' },
                  ],
                },
                {
                  id: 'n_electrophoresis',
                  type: 'reveal',
                  reveal: 'Haemoglobin electrophoresis demonstrates HbA2 elevated at 5.2% (reference < 3.5%), confirming increased delta chain synthesis characteristic of beta-thalassaemia trait.',
                  choices: [{ id: 'continue', label: 'Proceed to conclusion', next: 'n_decide' }],
                },
                { id: 'n_decide', type: 'decision' },
              ],
            },
          }
        : {
            id: 'CASE-FATIGUE-01',
            version: 1,
            learning_objective: 'LO-MICROCYTIC-01',
            case_role: 'initial',
            title: 'Persistent Fatigue in a Young Adult',
            disclaimer: 'Fictional case for education only. Not medical advice.',
            patient: { name: 'Alex', age: 29, sex: 'female' },
            history:
              'Three months of progressive tiredness, breathlessness when climbing stairs, and noticeable pallor. Reports heavy menstrual periods over the past two years. Strict vegetarian diet.',
            labs: [
              { id: 'hb', test: 'Haemoglobin', value: 9.1, unit: 'g/dL', ref: '12.0-15.5', flag: 'low' },
              { id: 'mcv', test: 'Mean Corpuscular Volume (MCV)', value: 68, unit: 'fL', ref: '80-100', flag: 'low' },
              { id: 'rdw', test: 'Red Cell Distribution Width (RDW)', value: 17.5, unit: '%', ref: '11.5-14.5', flag: 'high' },
              { id: 'ferritin', test: 'Serum Ferritin', value: 8, unit: 'ng/mL', ref: '15-200', flag: 'low' },
              { id: 'wbc', test: 'White Blood Cell Count (WBC)', value: 6.8, unit: 'x10^9/L', ref: '4.0-11.0', flag: 'normal' },
            ],
            question: 'Which clinical interpretation best fits this patient\'s presentation and laboratory findings?',
            options: [
              { id: 'A', text: 'Iron-deficiency anaemia (Microcytic hypochromic anaemia secondary to chronic blood loss and low dietary intake)' },
              { id: 'B', text: 'Vitamin B12 deficiency anaemia (Megaloblastic macrocytic anaemia)' },
              { id: 'C', text: 'Anaemia of acute blood loss (Normocytic normochromic anaemia)' },
              { id: 'D', text: 'Physiological baseline variation (Benign low normal, no pathology)' },
            ],
            branching: {
              start: 'n_review',
              nodes: [
                {
                  id: 'n_review',
                  type: 'review_case',
                  text: 'You are reviewing Alex\'s chart. What diagnostic investigation would you like to review next?',
                  choices: [
                    { id: 'more_info', label: 'Request peripheral blood smear analysis', next: 'n_smear' },
                    { id: 'answer_now', label: 'Proceed immediately to diagnostic interpretation', next: 'n_decide' },
                  ],
                },
                {
                  id: 'n_smear',
                  type: 'reveal',
                  reveal: 'Peripheral blood smear shows marked microcytic, hypochromic red blood cells with anisopoikilocytosis and occasional pencil-shaped (cigar) cells.',
                  choices: [{ id: 'continue', label: 'Synthesize findings & enter decision', next: 'n_decide' }],
                },
                { id: 'n_decide', type: 'decision' },
              ],
            },
          };

    const attemptObj = {
      id: attemptId,
      case_id: caseId,
      state: 'STARTED',
      current_node: 'n_review',
      selected_evidence: [],
      case_view: caseData,
      current_node_data: caseData.branching.nodes[0],
      steps_history: [],
    };
    mockState.attempts[attemptId] = attemptObj;
    return {
      attempt_id: attemptId,
      case_id: caseId,
      state: 'STARTED',
      current_node: 'n_review',
      case_view: caseData,
    };
  }

  if (endpoint.startsWith('/attempts/') && endpoint.endsWith('/step')) {
    const attemptId = endpoint.split('/')[2];
    const att = mockState.attempts[attemptId];
    if (att) {
      if (body.choice_id === 'more_info') {
        att.current_node = att.case_id === 'CASE-FATIGUE-02' ? 'n_electrophoresis' : 'n_smear';
      } else {
        att.current_node = 'n_decide';
      }
      const node = att.case_view.branching.nodes.find((n: any) => n.id === att.current_node);
      att.current_node_data = node;
      return { current_node: att.current_node, flags: [], node_data: node };
    }
  }

  if (endpoint.startsWith('/attempts/') && endpoint.endsWith('/submit')) {
    const attemptId = endpoint.split('/')[2];
    const att = mockState.attempts[attemptId] || {};
    const isCorrect = body.selected_answer === 'A';
    att.score = isCorrect ? 10.0 : 4.0;
    att.max_score = 10.0;
    att.is_correct = isCorrect;
    att.state = 'SUBMITTED';
    att.selected_answer = body.selected_answer;
    att.selected_evidence = body.selected_evidence;
    att.reasoning_text = body.reasoning_text;
    att.confidence = body.confidence;
    att.criteria_results = [
      { id: 'C1', description: 'Chooses the best-fitting clinical interpretation', met: isCorrect, points: isCorrect ? 3 : 0 },
      { id: 'C2', description: 'Uses low MCV indicating microcytosis as primary supporting evidence', met: true, points: 2 },
      { id: 'C3', description: 'Identifies serum ferritin as marker of iron stores', met: true, points: 2 },
      { id: 'C4', description: 'Notes RDW index indicating red cell heterogeneity', met: true, points: 1 },
      { id: 'C5', description: 'Reasoning connects red cell morphology with underlying pathophysiology', met: isCorrect, points: isCorrect ? 2 : 0 },
    ];
    att.misconception_tags = isCorrect ? [] : ['MC-MACRO-MICRO-CONFUSED', 'MC-OVERCONFIDENT'];
    return {
      attempt_id: attemptId,
      state: 'SUBMITTED',
      score: att.score,
      max_score: 10.0,
      is_correct: isCorrect,
      criteria: att.criteria_results,
      misconceptions: att.misconception_tags,
      recommended_lesson_id: 'LESSON-MICROCYTIC-INDICES',
    };
  }

  if (endpoint.startsWith('/attempts/') && endpoint.endsWith('/feedback')) {
    const attemptId = endpoint.split('/')[2];
    const att = mockState.attempts[attemptId] || {};
    att.state = 'FEEDBACK_READY';
    const isThal = att.case_id === 'CASE-FATIGUE-02';
    return {
      id: 'fb-' + attemptId,
      attempt_id: attemptId,
      source: 'fallback',
      citations_valid: true,
      model: 'reviewed-guidelines',
      latency_ms: 120,
      payload: isThal
        ? {
            what_you_got_right: [
              'Correctly identified Beta-thalassaemia trait / minor as the explanation for microcytosis with normal ferritin.',
              'Recognised that normal ferritin (145 ng/mL) and normal RDW (12.6%) rule out simple iron deficiency.',
              'Synthesized the family history and Mediterranean ancestry with disproportionate microcytosis.',
            ],
            what_needs_work: [
              'Highlight the high RBC count (6.2 x 10^12/L) and low Mentzer index as classic confirmatory clues.',
            ],
            why_it_matters:
              'Prescribing oral iron to patients with thalassaemia trait is ineffective and potentially harmful due to secondary iron accumulation risks.',
            evidence_links: [
              {
                ref_id: 'REF-THAL-001',
                supports: 'Details the hallmarks of thalassaemia trait: extreme microcytosis, high RBC count, normal RDW, and preserved ferritin.',
              },
              {
                ref_id: 'REF-FERRITIN-001',
                supports: 'Confirms that normal ferritin indicates intact iron reserves.',
              },
            ],
            reflection_prompt:
              'Notice how comparing this case to the initial fatigue case highlights the crucial role of ferritin and RDW in differential diagnosis.',
            next_step: 'Examine your progress dashboard to review your mastery trajectory across the microcytic learning objective.',
            uncertainty_note: 'Haemoglobin electrophoresis (HbA2 quantification) remains the definitive confirmatory investigation.',
          }
        : {
            what_you_got_right: [
              'Accurately identified Iron-Deficiency Anaemia as the primary clinical diagnosis.',
              'Recognised the diagnostic significance of microcytosis (MCV 68 fL) and depleted iron stores (Ferritin 8 ng/mL).',
              'Correlated the patient\'s presentation with chronic menorrhagia and vegetarian diet.',
            ],
            what_needs_work: [
              'Ensure Red Cell Distribution Width (RDW) is explicitly cited to confirm marked anisocytosis.',
              'Note the clinical correlation between severe iron depletion and hypochromia on peripheral smear.',
            ],
            why_it_matters:
              'Microcytic anaemia with low ferritin is diagnostic of exhausted iron stores. In premenopausal women, menstrual blood loss combined with vegetarian diet is the leading cause. Differentiating this from thalassaemia trait requires evaluating ferritin and RDW.',
            evidence_links: [
              {
                ref_id: 'REF-IDA-001',
                supports: 'Confirms diagnostic criteria for microcytic hypochromic anaemia with low MCV and haemoglobin below normal thresholds.',
              },
              {
                ref_id: 'REF-FERRITIN-001',
                supports: 'Establishes serum ferritin below 15 ng/mL as the most specific biomarker for total body iron depletion.',
              },
              {
                ref_id: 'REF-RDW-001',
                supports: 'Explains elevated RDW as evidence of anisocytosis characteristic of progressive nutritional iron deficiency.',
              },
            ],
            reflection_prompt:
              'You demonstrated solid diagnostic reasoning. Reflect on how your confidence level aligns with your ability to cite all key quantitative findings (MCV, ferritin, and RDW).',
            next_step: 'Review the targeted module on Red Cell Indices and proceed to the reassessment case.',
            uncertainty_note: 'This educational case assumes no concurrent chronic inflammation; in inflammatory states, ferritin can be falsely elevated.',
          },
    };
  }

  if (endpoint.startsWith('/attempts/') && endpoint.endsWith('/lesson-complete')) {
    const attemptId = endpoint.split('/')[2];
    if (mockState.attempts[attemptId]) {
      mockState.attempts[attemptId].state = 'LESSON_DONE';
    }
    return { status: 'ok', state: 'LESSON_DONE' };
  }

  if (endpoint.startsWith('/attempts/') && endpoint.endsWith('/reassess')) {
    const newId = 'att-reassess-' + Math.random().toString(36).substring(2, 7);
    return mockSimulator('/attempts', {
      method: 'POST',
      body: JSON.stringify({ case_id: 'CASE-FATIGUE-02' }),
    });
  }

  if (endpoint.startsWith('/attempts/')) {
    const attemptId = endpoint.split('/')[2];
    if (mockState.attempts[attemptId]) {
      return mockState.attempts[attemptId];
    }
    // create default
    return mockSimulator('/attempts', { method: 'POST', body: JSON.stringify({ case_id: 'CASE-FATIGUE-01' }) });
  }

  if (endpoint.startsWith('/lessons/')) {
    return {
      id: 'LESSON-MICROCYTIC-INDICES',
      title: 'Mastering Red Cell Indices: MCV, RDW, and Microcytosis',
      content: {
        overview:
          'Red blood cell indices (MCV, MCH, and RDW) are the cornerstone of morphological classification in anaemia. Relying exclusively on haemoglobin concentration tells you THAT an anaemia exists, but the MCV and RDW tell you WHAT PATHOPHYSIOLOGY is responsible.',
        key_principles: [
          {
            title: '1. Mean Corpuscular Volume (MCV)',
            explanation: 'Values < 80 fL indicate microcytic anaemia. The most common causes are iron deficiency anaemia (IDA) and thalassaemia trait. Never diagnose anaemia type without noting MCV.',
          },
          {
            title: '2. Red Cell Distribution Width (RDW)',
            explanation: 'RDW measures the range of cell volumes (anisocytosis). Elevated RDW (> 14.5%) indicates high variation, typical of developing IDA. Normal RDW with low MCV points towards thalassaemia trait where cells are uniformly small.',
          },
        ],
        clinical_pearl: 'In any microcytic anaemia, your next reflexive step is checking Serum Ferritin and RDW before initiating therapy!',
      },
      practice_questions: [
        {
          id: 'PQ1',
          question: 'A 24-year-old patient has Hb 9.8 g/dL, MCV 66 fL, and RDW 18.2%. Which pathophysiological state is most strongly suggested by the elevated RDW?',
          options: [
            { id: 'A', text: 'Anisocytosis resulting from progressive iron exhaustion producing heterogeneous cell sizes', correct: true },
            { id: 'B', text: 'A genetic globin synthesis mutation producing uniformly sized small erythrocytes', correct: false },
            { id: 'C', text: 'Megaloblastic maturation defect with macro-ovalocytes', correct: false },
          ],
          explanation: 'High RDW reflects anisocytosis (unequal cell volumes), which is the hallmark of evolving nutritional iron deficiency.',
        },
      ],
    };
  }

  if (endpoint === '/progress/me') {
    return {
      user_id: 'user-student-01',
      display_name: 'Alex Mercer (Student)',
      objectives: [
        {
          learning_objective: 'LO-MICROCYTIC-01',
          initial_score: 5.0,
          initial_max: 10.0,
          reassessment_score: 9.0,
          reassessment_max: 10.0,
          delta: 4.0,
          criteria_newly_met: [
            'Identified normal ferritin as ruling out simple iron deficiency',
            'Recognised normal RDW characteristic of uniform microcytic cells in thalassaemia trait',
          ],
          initial_attempt_id: 'att-1',
          reassessment_attempt_id: 'att-2',
        },
      ],
      calibration: [
        { confidence_bin: 20, accuracy: 25.0, count: 2 },
        { confidence_bin: 40, accuracy: 50.0, count: 3 },
        { confidence_bin: 60, accuracy: 70.0, count: 4 },
        { confidence_bin: 80, accuracy: 85.0, count: 6 },
        { confidence_bin: 100, accuracy: 100.0, count: 2 },
      ],
      calibration_summary: { overconfident: 1, underconfident: 1, calibrated: 8 },
      misconceptions: [
        { id: 'MC-IGNORES-INDICES', name: 'Omission of Red Blood Cell Indices', times_seen: 2, last_seen_at: '2026-10-19T10:00:00Z' },
        { id: 'MC-FERRITIN-MISSED', name: 'Failure to Evaluate Body Iron Stores', times_seen: 1, last_seen_at: '2026-10-19T10:30:00Z' },
      ],
    };
  }

  if (endpoint.startsWith('/teacher/cohorts/')) {
    return {
      cohort_id: 'cohort-med-2026-alpha',
      cohort_name: 'Class 2026 - Clinical Medicine Cohort Alpha',
      student_count: 6,
      objective_averages: [
        { learning_objective: 'LO-MICROCYTIC-01', avg_initial_score: 48.0, avg_reassessment_score: 82.0, delta: 34.0, learner_count: 6 },
        { learning_objective: 'LO-MACROCYTIC-01', avg_initial_score: 55.0, avg_reassessment_score: 86.0, delta: 31.0, learner_count: 5 },
      ],
      top_misconceptions: [
        { name: 'Failure to Evaluate Body Iron Stores', students: 4 },
        { name: 'Omission of Red Blood Cell Indices', students: 3 },
        { name: 'Overlooking Anisocytosis Index (RDW)', students: 3 },
        { name: 'Confusion Between Microcytic and Macrocytic Anaemias', students: 2 },
        { name: 'High Diagnostic Confidence with Flawed Reasoning', students: 2 },
      ],
      calibration_matrix: [
        { confidence_bin: 20, accuracy: 33.3, total_attempts: 3 },
        { confidence_bin: 40, accuracy: 50.0, total_attempts: 4 },
        { confidence_bin: 60, accuracy: 66.7, total_attempts: 6 },
        { confidence_bin: 80, accuracy: 80.0, total_attempts: 10 },
        { confidence_bin: 100, accuracy: 75.0, total_attempts: 4 },
      ],
    };
  }

  return {};
}

export const api = {
  auth: {
    login: (credentials: { email: string; password: string }) =>
      apiRequest<{ access_token: string; user: any }>('/auth/login', {
        method: 'POST',
        body: JSON.stringify(credentials),
      }),
    register: (data: any) =>
      apiRequest<{ access_token: string; user: any }>('/auth/register', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    me: () => apiRequest<any>('/auth/me'),
  },
  cases: {
    list: () => apiRequest<any[]>('/cases'),
    get: (id: string) => apiRequest<any>(`/cases/${id}`),
  },
  attempts: {
    start: (caseId: string, lang = 'en', parentAttemptId?: string | null) =>
      apiRequest<any>('/attempts', {
        method: 'POST',
        body: JSON.stringify({
          case_id: caseId,
          lang,
          parent_attempt_id: parentAttemptId || null,
        }),
      }),
    get: (attemptId: string) => apiRequest<any>(`/attempts/${attemptId}`),
    step: (attemptId: string, nodeId: string, choiceId: string) =>
      apiRequest<any>(`/attempts/${attemptId}/step`, {
        method: 'POST',
        body: JSON.stringify({ node_id: nodeId, choice_id: choiceId }),
      }),
    submit: (attemptId: string, data: {
      selected_answer: string;
      reasoning_text: string;
      selected_evidence: string[];
      confidence: number;
    }) =>
      apiRequest<any>(`/attempts/${attemptId}/submit`, {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    feedback: (attemptId: string) =>
      apiRequest<any>(`/attempts/${attemptId}/feedback`, {
        method: 'POST',
      }),
    lessonComplete: (attemptId: string, answers: Record<string, string> = {}) =>
      apiRequest<any>(`/attempts/${attemptId}/lesson-complete`, {
        method: 'POST',
        body: JSON.stringify({ answers }),
      }),
    reassess: (attemptId: string) =>
      apiRequest<any>(`/attempts/${attemptId}/reassess`, {
        method: 'POST',
      }),
  },
  lessons: {
    get: (lessonId: string) => apiRequest<any>(`/lessons/${lessonId}`),
  },
  progress: {
    getMe: () => apiRequest<any>('/progress/me'),
  },
  teacher: {
    getSummary: (cohortId: string) => apiRequest<any>(`/teacher/cohorts/${cohortId}/summary`),
  },
};
