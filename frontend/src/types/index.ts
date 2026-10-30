export type UserRole = 'student' | 'teacher' | 'admin';

export interface User {
  id: string;
  email: string;
  display_name: string;
  role: UserRole;
  preferred_lang: string;
  cohort_id?: string;
}

export interface CaseListItem {
  id: string;
  version: number;
  learning_objective: string;
  case_role: 'initial' | 'reassessment';
  title: string;
  disclaimer: string;
}

export interface LabItem {
  id: string;
  test: string;
  value: number | string;
  unit: string;
  ref: string;
  flag: 'low' | 'high' | 'normal';
}

export interface PatientInfo {
  name: string;
  age: number;
  sex: string;
}

export interface OptionItem {
  id: string;
  text: string;
}

export interface BranchChoice {
  id: string;
  label: string;
  next: string;
  flags?: string[];
}

export interface BranchNode {
  id: string;
  type: string;
  text?: string;
  reveal?: string;
  choices?: BranchChoice[];
}

export interface CaseView {
  id: string;
  version: number;
  learning_objective: string;
  case_role: 'initial' | 'reassessment';
  paired_case?: string;
  title: string;
  disclaimer: string;
  patient: PatientInfo;
  history: string;
  labs: LabItem[];
  question: string;
  options: OptionItem[];
  branching: {
    start: string;
    nodes: BranchNode[];
  };
  i18n?: {
    te?: {
      title?: string;
      patient?: { name?: string };
      question?: string;
    };
  };
}

export interface CriterionResult {
  id: string;
  description: string;
  met: boolean;
  points: number;
}

export interface Attempt {
  id: string;
  case_id: string;
  parent_attempt_id?: string | null;
  state: 'STARTED' | 'SUBMITTED' | 'FEEDBACK_READY' | 'LESSON_DONE' | 'COMPLETED';
  current_node: string;
  selected_answer?: string | null;
  reasoning_text?: string | null;
  selected_evidence: string[];
  confidence?: number | null;
  score?: number | null;
  max_score?: number | null;
  is_correct?: boolean | null;
  criteria_results?: CriterionResult[] | null;
  misconception_tags: string[];
  case_view: CaseView;
  current_node_data?: BranchNode | null;
  steps_history: { node_id: string; choice_id: string }[];
}

export interface Citation {
  ref_id: string;
  supports: string;
}

export interface FeedbackPayload {
  what_you_got_right: string[];
  what_needs_work: string[];
  why_it_matters: string;
  evidence_links: Citation[];
  reflection_prompt: string;
  next_step: string;
  uncertainty_note: string;
}

export interface FeedbackRecord {
  id: string;
  attempt_id: string;
  source: 'llm' | 'fallback';
  payload: FeedbackPayload;
  citations_valid: boolean;
  model?: string;
  latency_ms?: number;
}

export interface PracticeQuestion {
  id: string;
  question: string;
  options: { id: string; text: string; correct?: boolean }[];
  explanation: string;
}

export interface Lesson {
  id: string;
  title: string;
  content: {
    overview: string;
    key_principles: { title: string; explanation: string }[];
    clinical_pearl: string;
  };
  practice_questions: PracticeQuestion[];
}

export interface ObjectiveProgress {
  learning_objective: string;
  initial_score?: number | null;
  initial_max?: number | null;
  reassessment_score?: number | null;
  reassessment_max?: number | null;
  delta?: number | null;
  criteria_newly_met: string[];
  initial_attempt_id?: string | null;
  reassessment_attempt_id?: string | null;
}

export interface CalibrationPoint {
  confidence_bin: number;
  accuracy: number;
  count: number;
}

export interface MisconceptionItem {
  id: string;
  name: string;
  times_seen: number;
  last_seen_at?: string | null;
}

export interface LearnerProgress {
  user_id: string;
  display_name: string;
  objectives: ObjectiveProgress[];
  calibration: CalibrationPoint[];
  calibration_summary: {
    overconfident: number;
    underconfident: number;
    calibrated: number;
  };
  misconceptions: MisconceptionItem[];
}

export interface TeacherSummary {
  cohort_id: string;
  cohort_name: string;
  student_count: number;
  objective_averages: {
    learning_objective: string;
    avg_initial_score: number;
    avg_reassessment_score: number;
    delta: number;
    learner_count: number;
  }[];
  top_misconceptions: {
    name: string;
    students: number;
  }[];
  calibration_matrix: {
    confidence_bin: number;
    accuracy: number;
    total_attempts: number;
  }[];
}


export interface LessonListItem {
  id: string;
  title: string;
  objective_id?: string | null;
  status: string;
  estimated_minutes: number;
  difficulty: number;
  completed: boolean;
  best_score?: number | null;
  recommended: boolean;
  targets_misconceptions: string[];
}

export interface QuickCheckOption {
  id: string;
  text: string;
}

export interface QuickCheckQuestion {
  id: string;
  prompt: string;
  options: QuickCheckOption[];
  reference_id?: string;
}

export interface KeyPointItem {
  point: string;
  refs: string[];
}

export interface WorkedExampleItem {
  vignette: string;
  steps: string[];
}

export interface FurtherReadingItem {
  title: string;
  url?: string;
}

export interface ReferenceSummary {
  id: string;
  title: string;
  source_title: string;
  source_url?: string;
  text: string;
  key_facts: string[];
}

export interface QuestionResult {
  question_id: string;
  chosen: string;
  correct: string;
  is_correct: boolean;
  rationale: string;
  reference_id?: string;
}

export interface QuizResult {
  score: number;
  max_score: number;
  passed: boolean;
  best_score: number;
  attempts: number;
  results: Record<string, QuestionResult>;
}

export interface LessonDetail {
  id: string;
  title: string;
  objective_id?: string | null;
  status: string;
  reviewed_by?: string | null;
  reviewed_at?: string | null;
  estimated_minutes: number;
  difficulty: number;
  targets_misconceptions: string[];
  prerequisites: string[];
  learning_outcomes: string[];
  key_points: KeyPointItem[];
  worked_example?: WorkedExampleItem | null;
  common_pitfalls: string[];
  clinical_pearl?: string | null;
  quick_check: QuickCheckQuestion[];
  reference_ids: string[];
  further_reading: FurtherReadingItem[];
  references: Record<string, ReferenceSummary>;
  completed: boolean;
  best_score?: number | null;
  attempts: number;
  content?: {
    overview?: string;
    key_principles?: { title: string; explanation: string }[];
    clinical_pearl?: string;
  };
  practice_questions?: PracticeQuestion[];
}
