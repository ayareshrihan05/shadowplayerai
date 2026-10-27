import React from 'react';
import { Loader2 } from 'lucide-react';

interface LoadingSpinnerProps {
  message?: string;
  className?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  message = 'Loading tactical intelligence...',
  className = '',
}) => {
  return (
    <div className={`flex flex-col items-center justify-center p-12 text-center gap-3 ${className}`}>
      <Loader2 className="w-8 h-8 text-accent-green animate-spin" />
      <span className="text-sm text-text-secondary font-medium">{message}</span>
    </div>
  );
};
