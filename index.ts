export * from './match';
export * from './player';
export * from './sequence';
export * from './counterfactual';
export * from './report';

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  meta: {
    generated_at: string;
    data_label: string;
  };
}

export type PersonalizationTier = 'casual' | 'analyst' | 'coach';
