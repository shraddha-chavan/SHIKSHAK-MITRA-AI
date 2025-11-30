import { AlertCircle, CheckCircle, XCircle } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { cn } from '@/lib/utils';

interface AlertItemProps {
  type: 'success' | 'warning' | 'critical';
  message: string;
  time: string;
}

export const AlertItem = ({ type, message, time }: AlertItemProps) => {
  const icons = {
    success: CheckCircle,
    warning: AlertCircle,
    critical: XCircle,
  };

  const Icon = icons[type];

  return (
    <Alert className={cn(
      "border-l-4",
      type === 'success' && "border-l-success bg-success/5",
      type === 'warning' && "border-l-warning bg-warning/5",
      type === 'critical' && "border-l-destructive bg-destructive/5"
    )}>
      <Icon className={cn(
        "h-4 w-4",
        type === 'success' && "text-success",
        type === 'warning' && "text-warning",
        type === 'critical' && "text-destructive"
      )} />
      <AlertDescription className="ml-2">
        <div className="flex items-center justify-between">
          <span className="text-sm">{message}</span>
          <span className="text-xs text-muted-foreground ml-4">{time}</span>
        </div>
      </AlertDescription>
    </Alert>
  );
};
