import { cn } from "@/lib/utils";
import { CheckCircle2, XCircle, Loader2, AlertCircle } from "lucide-react";

export type StatusType = "idle" | "loading" | "success" | "error";

interface StatusBadgeProps {
  status: StatusType;
  message?: string;
}

const statusConfig: Record<
  StatusType,
  { icon: React.ElementType; className: string }
> = {
  idle: {
    icon: AlertCircle,
    className: "text-white/30",
  },
  loading: {
    icon: Loader2,
    className: "text-cyan-400",
  },
  success: {
    icon: CheckCircle2,
    className: "text-green-400",
  },
  error: {
    icon: XCircle,
    className: "text-red-400",
  },
};

export default function StatusBadge({ status, message }: StatusBadgeProps) {
  const config = statusConfig[status];
  const Icon = config.icon;

  if (status === "idle" && !message) return null;

  return (
    <div className={cn("flex items-center gap-2 text-sm", config.className)}>
      <Icon
        className={cn(
          "w-4 h-4",
          status === "loading" && "animate-spin"
        )}
      />
      <span>{message || status}</span>
    </div>
  );
}