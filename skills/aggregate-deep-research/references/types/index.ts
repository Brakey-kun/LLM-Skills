// ============================================
// BEDROCK BUILDER ACADEMY - CORE TYPE DEFINITIONS
// Strictly typed for TypeScript, RAG compatibility, and GDPR compliance
// ============================================

/**
 * Proficiency levels in the curriculum
 * Maps to Skill Tree node tiers
 */
export type ProficiencyLevel = 'foundations' | 'toolstack' | 'entity-mechanics' | 'advanced-systems' | 'marketplace';

/**
 * Lesson difficulty rating for XP scaling
 */
export type Difficulty = 'easy' | 'medium' | 'hard' | 'expert';

/**
 * Node state in the Skill Tree
 */
export type NodeState = 'locked' | 'available' | 'in-progress' | 'completed' | 'mastered';

/**
 * Exercise types supported in the interactive curriculum
 */
export type ExerciseType = 
  | 'multiple-choice' 
  | 'drag-drop' 
  | 'code-editor' 
  | 'slider-input' 
  | 'json-builder' 
  | 'molang-parser';

/**
 * Achievement categories for gamification
 */
export type AchievementCategory = 
  | 'streak' 
  | 'xp-milestone' 
  | 'tool-mastery' 
  | 'curriculum-completion' 
  | 'marketplace-ready';

/**
 * User progress on a specific lesson node
 * GDPR-compliant: minimal PII, hashed identifiers only
 */
export interface LessonProgress {
  lessonId: string;
  unitId: string;
  state: NodeState;
  xpEarned: number;
  attempts: number;
  bestScore: number;
  completedAt: string | null; // ISO 8601 timestamp
  timeSpentMs: number;
  exerciseResults: ExerciseResult[];
}

/**
 * Result of a single exercise attempt
 */
export interface ExerciseResult {
  exerciseId: string;
  type: ExerciseType;
  score: number; // 0-100
  passed: boolean;
  submittedAt: string; // ISO 8601
  timeSpentMs: number;
  userAnswer: unknown; // Serialized answer for review
}

/**
 * Curriculum Unit - A collection of lessons
 */
export interface CurriculumUnit {
  id: string;
  proficiency: ProficiencyLevel;
  title: string;
  description: string;
  icon: string; // Lucide icon name
  order: number;
  prerequisites: string[]; // Unit IDs that must be completed first
  lessons: CurriculumLesson[];
  xpReward: number;
  estimatedHours: number;
}

/**
 * Individual Lesson within a Unit
 */
export interface CurriculumLesson {
  id: string;
  unitId: string;
  title: string;
  description: string;
  difficulty: Difficulty;
  order: number;
  prerequisites: string[]; // Lesson IDs
  exercises: Exercise[];
  xpReward: number;
  estimatedMinutes: number;
  tags: string[]; // For search/filtering: 'molang', 'typescript', 'blockbench', etc.
}

/**
 * Exercise definition for interactive lessons
 */
export interface Exercise {
  id: string;
  lessonId: string;
  type: ExerciseType;
  prompt: string;
  instructions: string;
  xpReward: number;
  
  // Type-specific configuration
  config: 
    | MultipleChoiceConfig
    | DragDropConfig
    | CodeEditorConfig
    | SliderConfig
    | JsonBuilderConfig
    | MolangParserConfig;
  
  // Validation
  validation: ValidationRule[];
  hints: string[];
  solutionExplanation: string;
}

/**
 * Exercise Type Configurations
 */
export interface MultipleChoiceConfig {
  options: { id: string; text: string; isCorrect: boolean }[];
  allowMultiple: boolean;
  shuffleOptions: boolean;
}

export interface DragDropConfig {
  zones: { id: string; label: string; acceptedTypes: string[] }[];
  items: { id: string; content: string; type: string; correctZone: string }[];
  snapToGrid: boolean;
}

export interface CodeEditorConfig {
  language: 'json' | 'typescript' | 'molang';
  starterCode: string;
  expectedOutput?: string;
  allowedImports?: string[];
  maxLines?: number;
  theme: 'vs-dark' | 'vs-light';
}

export interface SliderConfig {
  min: number;
  max: number;
  step: number;
  unit: string;
  targetValue: number;
  tolerance: number;
  showValue: boolean;
}

export interface JsonBuilderConfig {
  schema: JsonSchemaDefinition;
  requiredFields: string[];
  optionalFields: string[];
  exampleOutput: Record<string, unknown>;
}

export interface MolangParserConfig {
  expression: string;
  variables: Record<string, { min: number; max: number; default: number }>;
  expectedResult: number | boolean | string;
  contextDescription: string;
}

export interface JsonSchemaDefinition {
  type: 'object';
  properties: Record<string, JsonPropertyDefinition>;
  required: string[];
  additionalProperties: boolean;
}

export interface JsonPropertyDefinition {
  type: 'string' | 'number' | 'boolean' | 'object' | 'array';
  description: string;
  enum?: unknown[];
  items?: JsonPropertyDefinition;
  properties?: Record<string, JsonPropertyDefinition>;
  default?: unknown;
}

/**
 * Validation rules for exercise answers
 */
export interface ValidationRule {
  type: 'required' | 'schema' | 'custom' | 'regex' | 'range';
  field?: string;
  message: string;
  params?: Record<string, unknown>;
}

/**
 * User Profile - GDPR Article 25: Data Minimization
 * No email, name, or direct identifiers stored in progress DB
 * Auth handled separately via secure session tokens
 */
export interface UserProfile {
  userId: string; // Hashed/UUID v4 - no PII
  createdAt: string; // ISO 8601
  lastActiveAt: string; // ISO 8601
  totalXp: number;
  currentLevel: number;
  currentStreak: number;
  longestStreak: number;
  lastStreakDate: string | null; // ISO 8601 date only
  completedLessons: string[]; // Lesson IDs
  masteredLessons: string[]; // Lesson IDs with perfect scores
  achievements: UserAchievement[];
  preferences: UserPreferences;
  consentVersion: string; // Track consent for Law 09-08/GDPR
  dataRetentionExpiresAt: string | null; // Auto-delete timestamp
}

/**
 * User Achievement/Badge
 */
export interface UserAchievement {
  id: string;
  category: AchievementCategory;
  name: string;
  description: string;
  icon: string;
  earnedAt: string; // ISO 8601
  xpBonus: number;
  metadata?: Record<string, unknown>;
}

/**
 * User Preferences - Privacy-focused
 */
export interface UserPreferences {
  theme: 'dark' | 'light' | 'system';
  reducedMotion: boolean;
  soundEnabled: boolean;
  language: 'en' | 'fr' | 'ar'; // Primary languages for Morocco/intl
  dailyReminderTime: string | null; // HH:MM in user timezone
  analyticsOptIn: boolean; // Explicit consent for Law 09-08
}

/**
 * Skill Tree Node for Dashboard Visualization
 */
export interface SkillTreeNode {
  id: string;
  lessonId: string;
  unitId: string;
  position: { x: number; y: number };
  state: NodeState;
  connections: string[]; // Connected node IDs
  proficiency: ProficiencyLevel;
}

/**
 * Daily Challenge for Streak Maintenance
 */
export interface DailyChallenge {
  date: string; // ISO 8601 date
  lessonId: string;
  exerciseId: string;
  bonusXp: number;
  completed: boolean;
}

/**
 * Leaderboard Entry (Anonymized)
 */
export interface LeaderboardEntry {
  rank: number;
  userId: string; // Hashed
  totalXp: number;
  level: number;
  streak: number;
  // No display names, emails, or PII
}

/**
 * API Response Wrappers
 */
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: ApiError;
  timestamp: string;
}

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}

/**
 * Progress Sync Payload (for offline-first sync)
 */
export interface ProgressSyncPayload {
  userId: string;
  deviceId: string; // Hashed
  lastSyncAt: string;
  lessonProgress: LessonProgress[];
  profileUpdates: Partial<UserProfile>;
  checksum: string; // For conflict detection
}