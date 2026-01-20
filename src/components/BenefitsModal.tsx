import { useNavigate } from "react-router-dom";
import { ArrowRight, X } from "lucide-react";
import { plans, type Plan } from "@/data/plans";
import { useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface BenefitsModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  packageKey?: string | null;
}

export const BenefitsModal = ({ open, onOpenChange, packageKey }: BenefitsModalProps) => {
  const navigate = useNavigate();
  
  const currentPlan = useMemo(() => {
    if (!packageKey) return null;
    return plans.find(p => p.key === packageKey);
  }, [packageKey]);

  if (!currentPlan) return null;

  const handleBenefitClick = (benefitIndex: number) => {
    navigate(`/benefit/${packageKey}/${benefitIndex}`);
    onOpenChange(false);
  };

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          initial={{ opacity: 0, y: -10, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -10, scale: 0.95 }}
          transition={{ duration: 0.2, ease: "easeOut" }}
          className="fixed left-4 top-20 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50"
        >
          {/* Header */}
          <div className="px-4 py-3 border-b border-gray-100 flex items-center justify-between">
            <div>
              <h3 className="font-semibold text-gray-900">{currentPlan.name}</h3>
              <p className="text-xs text-gray-500">{currentPlan.subtitle}</p>
            </div>
            <button
              onClick={() => onOpenChange(false)}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Benefits List */}
          <div className="space-y-1 max-h-96 overflow-y-auto p-2">
            {currentPlan.features.map((feature, index) => (
              <motion.button
                key={index}
                whileHover={{ x: 4 }}
                transition={{ duration: 0.2 }}
                onClick={() => handleBenefitClick(index)}
                className="w-full text-left px-3 py-2 rounded-md hover:bg-blue-50 transition-colors group flex items-center justify-between"
              >
                <span className="text-sm text-gray-700 group-hover:text-blue-600 transition-colors">
                  {feature.text}
                </span>
                <ArrowRight className="w-4 h-4 text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity" />
              </motion.button>
            ))}
          </div>

          {/* Footer */}
          <div className="px-4 py-2 border-t border-gray-100 bg-gray-50 rounded-b-lg">
            <p className="text-xs text-gray-500 text-center">
              Click any benefit to learn more
            </p>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default BenefitsModal;
