import { LucideIcon } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { cn } from '@/lib/utils';

interface MetricCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  trend?: string;
  trendUp?: boolean;
  className?: string;
  valueClassName?: string;
}

export const MetricCard = ({
  title,
  value,
  icon: Icon,
  trend,
  trendUp,
  className,
  valueClassName
}: MetricCardProps) => {
  return (
    <Card className={cn("p-6 transition-smooth hover:shadow-lg", className)}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-muted-foreground">{title}</p>
          <div className="mt-2 flex items-baseline gap-2">
            <h3 className={cn("text-3xl font-bold font-heading", valueClassName)}>
              {value}
            </h3>
            {trend && (
              <span className={cn(
                "text-sm font-medium",
                trendUp ? "text-success" : "text-destructive"
              )}>
                {trend}
              </span>
            )}
          </div>
        </div>
        <div className={cn(
          "rounded-full p-3",
          trendUp ? "bg-success/10" : "bg-primary/10"
        )}>
          <Icon className={cn(
            "h-6 w-6",
            trendUp ? "text-success" : "text-primary"
          )} />
        </div>
      </div>
    </Card>
  );
};
